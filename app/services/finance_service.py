import asyncio
from decimal import Decimal
from uuid import UUID

from fastapi import BackgroundTasks

from app.models import FeeStructure, Invoice, Payment, Student
from app.repositories.school_repository import SchoolRepository
from app.schemas import (
    BillingRunRead,
    FeeStructureCreate,
    FeeStructureRead,
    FeeStructureUpdate,
    InvoiceCreate,
    InvoiceRead,
    InvoiceStatus,
    PaymentCreate,
    PaymentMethod,
    PaymentRead,
    StudentBalanceRead,
    StudentStatus,
)
from app.services.exceptions import ResourceConflictError, ResourceNotFoundError
from app.services.user_notifications import EmailSchema, NotificationService

ZERO = Decimal("0.00")


class FinanceService:
    """Fee structures, student invoices and payments."""

    def __init__(
        self, repository: SchoolRepository, tasks: BackgroundTasks | None = None
    ):
        self.repository = repository
        self.tasks = tasks
        self.notification = (
            NotificationService(tasks=tasks) if tasks is not None else None
        )

    # --- fee structures ---------------------------------------------------

    def create_fee_structure(self, payload: FeeStructureCreate) -> FeeStructureRead:
        term = self.repository.get_term(payload.term_id)
        if term is None:
            raise ResourceNotFoundError(
                f"Term with id {payload.term_id} was not found."
            )
        structure = self.repository.add(FeeStructure.model_validate(payload))
        return self._to_structure_read(structure, term.name)

    def list_fee_structures(self, term_id: int | None = None) -> list[FeeStructureRead]:
        rows = self.repository.list_fee_structures(term_id=term_id)
        return [
            self._to_structure_read(structure, term.name) for structure, term in rows
        ]

    def get_fee_structure(self, structure_id: int) -> FeeStructure:
        structure = self.repository.get_fee_structure(structure_id)
        if structure is None:
            raise ResourceNotFoundError(
                f"Fee structure with id {structure_id} was not found."
            )
        return structure

    def update_fee_structure(
        self, structure_id: int, payload: FeeStructureUpdate
    ) -> FeeStructureRead:
        structure = self.get_fee_structure(structure_id)
        updates = payload.model_dump(exclude_none=True)
        for key, value in updates.items():
            setattr(structure, key, value)
        self.repository.save()
        self.repository.refresh(structure)
        term = self.repository.get_term(structure.term_id)
        return self._to_structure_read(structure, term.name if term else None)

    def delete_fee_structure(self, structure_id: int) -> None:
        structure = self.get_fee_structure(structure_id)
        if self.repository.list_invoices_for_structure(structure_id):
            raise ResourceConflictError(
                "Fee structure has issued invoices; void those invoices first."
            )
        self.repository.delete(structure)

    def run_billing(self, structure_id: int) -> BillingRunRead:
        """Issue an invoice to every active student the fee structure applies to."""
        structure = self.get_fee_structure(structure_id)
        students = self.repository.list_students(
            program=structure.program,
            level=structure.level,
            status=str(StudentStatus.ACTIVE),
        )

        created = 0
        skipped = 0
        for student in students:
            if self.repository.get_invoice_for_structure(student.id, structure_id):
                skipped += 1
                continue
            self.repository.session.add(
                Invoice(
                    student_id=student.id,
                    term_id=structure.term_id,
                    fee_structure_id=structure.id,
                    description=structure.name,
                    amount=structure.amount,
                    due_date=structure.due_date,
                )
            )
            created += 1
        self.repository.save()

        return BillingRunRead(
            fee_structure_id=structure_id,
            invoices_created=created,
            students_skipped=skipped,
        )

    # --- invoices ---------------------------------------------------------

    def create_invoice(self, payload: InvoiceCreate) -> InvoiceRead:
        student = self.repository.get_student(payload.student_id)
        if student is None:
            raise ResourceNotFoundError(
                f"Student with id {payload.student_id} was not found."
            )
        if self.repository.get_term(payload.term_id) is None:
            raise ResourceNotFoundError(
                f"Term with id {payload.term_id} was not found."
            )

        structure = None
        if payload.fee_structure_id is not None:
            structure = self.get_fee_structure(payload.fee_structure_id)
            if self.repository.get_invoice_for_structure(student.id, structure.id):
                raise ResourceConflictError(
                    f"{student.index_number} has already been invoiced for {structure.name}."
                )

        amount = (
            payload.amount
            if payload.amount is not None
            else (structure.amount if structure else None)
        )
        description = payload.description or (structure.name if structure else None)
        due_date = payload.due_date or (structure.due_date if structure else None)
        if amount is None or description is None or due_date is None:
            raise ResourceConflictError(
                "amount, description and due_date are required unless a fee structure is given."
            )

        invoice = self.repository.add(
            Invoice(
                student_id=student.id,
                term_id=payload.term_id,
                fee_structure_id=payload.fee_structure_id,
                description=description,
                amount=amount,
                due_date=due_date,
            )
        )
        return self._to_invoice_read(invoice, student, ZERO)

    def list_invoices(
        self,
        student_id: UUID | None = None,
        term_id: int | None = None,
        status: InvoiceStatus | None = None,
    ) -> list[InvoiceRead]:
        rows = self.repository.list_invoices(
            student_id=student_id,
            term_id=term_id,
            status=str(status) if status else None,
        )
        paid_by_invoice = self._paid_totals([invoice.id for invoice, _s in rows])
        return [
            self._to_invoice_read(
                invoice, student, paid_by_invoice.get(invoice.id, ZERO)
            )
            for invoice, student in rows
        ]

    def get_invoice(self, invoice_id: UUID) -> Invoice:
        invoice = self.repository.get_invoice(invoice_id)
        if invoice is None:
            raise ResourceNotFoundError(f"Invoice with id {invoice_id} was not found.")
        return invoice

    def read_invoice(self, invoice_id: UUID) -> InvoiceRead:
        invoice = self.get_invoice(invoice_id)
        student = self.repository.get_student(invoice.student_id)
        paid = self._paid_totals([invoice.id]).get(invoice.id, ZERO)
        return self._to_invoice_read(invoice, student, paid)

    def void_invoice(self, invoice_id: UUID) -> InvoiceRead:
        invoice = self.get_invoice(invoice_id)
        if self.repository.list_payments(invoice_id):
            raise ResourceConflictError(
                "Invoice has recorded payments and cannot be voided."
            )
        invoice.status = str(InvoiceStatus.VOID)
        self.repository.save()
        self.repository.refresh(invoice)
        student = self.repository.get_student(invoice.student_id)
        return self._to_invoice_read(invoice, student, ZERO)

    def delete_invoice(self, invoice_id: UUID) -> None:
        invoice = self.get_invoice(invoice_id)
        self.repository.delete_payments_for_invoice(invoice_id)
        self.repository.delete(invoice)

    # --- payments ---------------------------------------------------------

    def record_payment(self, payload: PaymentCreate) -> PaymentRead:
        invoice = self.get_invoice(payload.invoice_id)
        if invoice.status == InvoiceStatus.VOID:
            raise ResourceConflictError("Cannot pay a voided invoice.")

        paid = self._paid_totals([invoice.id]).get(invoice.id, ZERO)
        outstanding = invoice.amount - paid
        if payload.amount > outstanding:
            raise ResourceConflictError(
                f"Payment of {payload.amount} exceeds the outstanding balance of {outstanding}."
            )

        data = payload.model_dump(exclude_none=True)
        data["method"] = str(payload.method)
        payment = Payment.model_validate(data)
        self.repository.session.add(payment)

        invoice.status = str(self._status_for(invoice.amount, paid + payment.amount))
        self.repository.save()
        self.repository.refresh(payment)
        self._send_payment_confirmation(invoice, payment)

        return PaymentRead(
            id=payment.id,
            invoice_id=payment.invoice_id,
            amount=payment.amount,
            method=PaymentMethod(payment.method),
            reference=payment.reference,
            paid_on=payment.paid_on,
            recorded_at=payment.recorded_at,
        )

    def list_payments(self, invoice_id: UUID) -> list[PaymentRead]:
        self.get_invoice(invoice_id)
        return [
            PaymentRead(
                id=payment.id,
                invoice_id=payment.invoice_id,
                amount=payment.amount,
                method=PaymentMethod(payment.method),
                reference=payment.reference,
                paid_on=payment.paid_on,
                recorded_at=payment.recorded_at,
            )
            for payment in self.repository.list_payments(invoice_id)
        ]

    # --- balances ---------------------------------------------------------

    def student_balance(
        self, student_id: UUID, term_id: int | None = None
    ) -> StudentBalanceRead:
        student = self.repository.get_student(student_id)
        if student is None:
            raise ResourceNotFoundError(f"Student with id {student_id} was not found.")

        invoices = self.list_invoices(student_id=student_id, term_id=term_id)
        billable = [
            invoice for invoice in invoices if invoice.status != InvoiceStatus.VOID
        ]
        total_billed = sum((invoice.amount for invoice in billable), ZERO)
        total_paid = sum((invoice.amount_paid for invoice in billable), ZERO)

        return StudentBalanceRead(
            student_id=student.id,
            student_name=student.full_name,
            student_index_number=student.index_number,
            total_billed=total_billed,
            total_paid=total_paid,
            balance=total_billed - total_paid,
            invoices=invoices,
        )

    # --- helpers ----------------------------------------------------------

    def _paid_totals(self, invoice_ids: list[UUID]) -> dict[UUID, Decimal]:
        totals: dict[UUID, Decimal] = {}
        for payment in self.repository.list_payments_for_invoices(invoice_ids):
            totals[payment.invoice_id] = (
                totals.get(payment.invoice_id, ZERO) + payment.amount
            )
        return totals

    def _send_payment_confirmation(self, invoice: Invoice, payment: Payment) -> None:
        if self.tasks is None or self.notification is None:
            return

        student = self.repository.get_student(invoice.student_id)
        if student is None:
            return

        subject = "Fee payment confirmation"
        email = EmailSchema(
            email=[student.email],
            body={
                "student_name": student.full_name,
                "invoice_description": invoice.description,
                "amount": payment.amount,
                "payment_method": payment.method,
                "paid_on": payment.paid_on,
                "reference": payment.reference,
            },
        )

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            asyncio.run(
                self.notification.send_email_with_template(
                    subject=subject,
                    email=email,
                    template_name="payment_receipt.html",
                )
            )
            return

        self.tasks.add_task(
            self.notification.send_email_with_template,
            subject=subject,
            email=email,
            template_name="payment_receipt.html",
        )

    @staticmethod
    def _status_for(amount: Decimal, paid: Decimal) -> InvoiceStatus:
        if paid <= ZERO:
            return InvoiceStatus.UNPAID
        if paid >= amount:
            return InvoiceStatus.PAID
        return InvoiceStatus.PARTIAL

    @staticmethod
    def _to_structure_read(
        structure: FeeStructure, term_name: str | None
    ) -> FeeStructureRead:
        return FeeStructureRead(
            id=structure.id,
            term_id=structure.term_id,
            name=structure.name,
            description=structure.description,
            amount=structure.amount,
            program=structure.program,
            level=structure.level,
            due_date=structure.due_date,
            term_name=term_name,
        )

    @staticmethod
    def _to_invoice_read(
        invoice: Invoice, student: Student | None, paid: Decimal
    ) -> InvoiceRead:
        return InvoiceRead(
            id=invoice.id,
            student_id=invoice.student_id,
            term_id=invoice.term_id,
            fee_structure_id=invoice.fee_structure_id,
            description=invoice.description,
            amount=invoice.amount,
            issued_on=invoice.issued_on,
            due_date=invoice.due_date,
            status=InvoiceStatus(invoice.status),
            amount_paid=paid,
            balance=invoice.amount - paid,
            student_name=student.full_name if student else None,
            student_index_number=student.index_number if student else None,
        )
