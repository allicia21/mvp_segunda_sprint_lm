from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from model.cliente import Cliente


class ClienteSchema(BaseModel):
    person_age: int
    person_gender: str  # Corrigido para string
    person_education: str  # Corrigido para string
    person_income: float
    person_emp_exp: float
    person_home_ownership: str  # Corrigido para string
    loan_amnt: float
    loan_intent: str  # Corrigido para string
    loan_int_rate: float
    loan_percent_income: float
    cb_person_cred_hist_length: int
    credit_score: int
    previous_loan_defaults_on_file: int


class ClienteViewSchema(ClienteSchema):
    id: int
    loan_status: Optional[int] = Field(None, example=1)
    data_insercao: Optional[datetime] = Field(None, example="2023-10-01T12:00:00Z")


class ClienteBuscaSchema(BaseModel):
    id: int


class ListaClientesSchema(BaseModel):
    clientes: List[ClienteViewSchema]


class ClienteDeleteSchema(BaseModel):
    id: int


def apresenta_cliente(cliente: Cliente) -> dict:
    return {
        "id": cliente.id,
        "person_age": cliente.age,
        "person_gender": cliente.gender,
        "person_education": cliente.education,
        "person_income": cliente.income,
        "person_emp_exp": cliente.emp_exp,
        "person_home_ownership": cliente.home_ownership,
        "loan_amnt": cliente.amnt,
        "loan_intent": cliente.intent,
        "loan_int_rate": cliente.rate,
        "loan_percent_income": cliente.percent,
        "cb_person_cred_hist_length": cliente.cred_length,
        "credit_score": cliente.score,
        "previous_loan_defaults_on_file": cliente.previous,
        "loan_status": cliente.loan_status,
        "data_insercao": cliente.data_insercao.isoformat() if cliente.data_insercao else None
    }


def apresenta_clientes(clientes: List[Cliente]) -> dict:
    result = []
    for c in clientes:
        result.append(apresenta_cliente(c))
    return {"clientes": result}
