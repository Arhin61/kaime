from uuid import UUID

from fastapi import APIRouter, Query, status

from app.dependencies import FinanceServiceDep
from app.schemas import (
    BillingRunRead,
    FeeStructureCreate,
    FeeStructureRead,
    FeeStructureUpdate,
    InvoiceCreate,
    InvoiceRead,
    InvoiceStatus,
    PaymentCreate,
    PaymentRead,
)

router = APIRouter(prefix="/dashboard/fees", tags=["Fees"])


# --- fee structures ------------------------------------------------------


@router.post(
    "/structures", response_model=FeeStructureRead, status_code=status.HTTP_201_CREATED
)
def create_fee_structure(payload: FeeStructureCreate, service: FinanceServiceDep):
    return service.create_fee_structure(payload)


@router.get("/structures", response_model=list[FeeStructureRead])
def list_fee_structures(service: FinanceServiceDep, term_id: int | None = None):
    return service.list_fee_structures(term_id=term_id)


@router.patch("/structures/{structure_id}", response_model=FeeStructureRead)
def update_fee_structure(
    structure_id: int, payload: FeeStructureUpdate, service: FinanceServiceDep
):
    return service.update_fee_structure(structure_id, payload)


@router.delete("/structures/{structure_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_fee_structure(structure_id: int, service: FinanceServiceDep):
    service.delete_fee_structure(structure_id)


@router.post("/structures/{structure_id}/bill", response_model=BillingRunRead)
def run_billing(structure_id: int, service: FinanceServiceDep):
    return service.run_billing(structure_id)


# --- invoices ------------------------------------------------------------


@router.post("/invoices", response_model=InvoiceRead, status_code=status.HTTP_201_CREATED)
def create_invoice(payload: InvoiceCreate, service: FinanceServiceDep):
    return service.create_invoice(payload)


@router.get("/invoices", response_model=list[InvoiceRead])
def list_invoices(
    service: FinanceServiceDep,
    student_id: UUID | None = None,
    term_id: int | None = None,
    invoice_status: InvoiceStatus | None = Query(default=None, alias="status"),
):
    return service.list_invoices(
        student_id=student_id, term_id=term_id, status=invoice_status
    )


@router.get("/invoices/{invoice_id}", response_model=InvoiceRead)
def get_invoice(invoice_id: UUID, service: FinanceServiceDep):
    return service.read_invoice(invoice_id)


@router.patch("/invoices/{invoice_id}/void", response_model=InvoiceRead)
def void_invoice(invoice_id: UUID, service: FinanceServiceDep):
    return service.void_invoice(invoice_id)


@router.delete("/invoices/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(invoice_id: UUID, service: FinanceServiceDep):
    service.delete_invoice(invoice_id)


# --- payments ------------------------------------------------------------


@router.post("/payments", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def record_payment(payload: PaymentCreate, service: FinanceServiceDep):
    return service.record_payment(payload)


@router.get("/invoices/{invoice_id}/payments", response_model=list[PaymentRead])
def list_payments(invoice_id: UUID, service: FinanceServiceDep):
    return service.list_payments(invoice_id)
