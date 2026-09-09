from datetime import date
from decimal import Decimal
from uuid import uuid4

from fastapi import BackgroundTasks

from app.models import Invoice, Student
from app.schemas import PaymentCreate, PaymentMethod
from app.services.finance_service import FinanceService


class DummyNotification:
    sent = []

    def __init__(self, tasks):
        self.tasks = tasks

    async def send_email_with_template(self, subject, email, template_name):
        DummyNotification.sent.append(
            {
                "subject": subject,
                "to": email.email,
                "template_name": template_name,
                "body": email.body,
            }
        )


class DummySession:
    def add(self, entity):
        return None

    def commit(self):
        return None

    def refresh(self, entity):
        return None


class DummyRepository:
    def __init__(self, invoice, student):
        self.session = DummySession()
        self._invoice = invoice
        self._student = student

    def get_invoice(self, invoice_id):
        return self._invoice if self._invoice.id == invoice_id else None

    def get_student(self, student_id):
        return self._student if self._student.id == student_id else None

    def list_payments_for_invoices(self, invoice_ids):
        return []

    def save(self):
        return None

    def refresh(self, entity):
        return None


def test_record_payment_sends_student_confirmation_email(monkeypatch):
    student = Student(
        id=uuid4(),
        index_number="ST-1001",
        email="student@example.com",
        first_name="Ada",
        last_name="Lovelace",
        phone_number="123456789",
        program="Computer Science",
        level=100,
    )
    invoice = Invoice(
        id=uuid4(),
        student_id=student.id,
        term_id=1,
        description="Tuition fee",
        amount=Decimal("250.00"),
        due_date=date(2026, 8, 31),
        status="unpaid",
    )
    repository = DummyRepository(invoice=invoice, student=student)
    DummyNotification.sent = []
    monkeypatch.setattr(
        "app.services.finance_service.NotificationService",
        DummyNotification,
        raising=False,
    )

    service = FinanceService(repository=repository, tasks=BackgroundTasks())
    result = service.record_payment(
        PaymentCreate(
            invoice_id=invoice.id,
            amount=Decimal("250.00"),
            method=PaymentMethod.CASH,
            paid_on=date(2026, 8, 22),
        )
    )

    assert result.amount == Decimal("250.00")
    assert DummyNotification.sent[0]["to"] == [student.email]
    assert DummyNotification.sent[0]["template_name"] == "payment_receipt.html"
    assert DummyNotification.sent[0]["body"]["student_name"] == student.full_name
    assert DummyNotification.sent[0]["body"]["amount"] == Decimal("250.00")
