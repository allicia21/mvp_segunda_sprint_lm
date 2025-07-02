from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id             = Column(Integer, primary_key=True)
    age            = Column("person_age", Integer)
    gender         = Column("person_gender", String)  # Alterado
    education      = Column("person_education", String)  # Alterado
    income         = Column("person_income", Integer)
    emp_exp        = Column("person_emp_exp", Integer)
    home_ownership = Column("person_home_ownership", String)  # Alterado
    amnt           = Column("loan_amnt", Float)
    intent         = Column("loan_intent", String)  # Alterado
    rate           = Column("loan_int_rate", Integer)
    percent        = Column("loan_percent_income", Integer)
    cred_length    = Column("cb_person_cred_hist_length", Integer)
    score          = Column("credit_score", Integer)
    previous       = Column("previous_loan_defaults_on_file", Integer)

    loan_status = Column("loan_status", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, age: int, gender: str, education: str, income: int, emp_exp: int,
                 home_ownership: str, amnt: float, intent: str, rate: int,
                 loan_status: Union[int, None], percent: int, cred_length: int, score: int, previous: int,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Cliente com as informações fornecidas.
        Se a data de inserção não for informada, será usada a data atual.
        """
        self.age = age
        self.gender = gender
        self.education = education
        self.income = income
        self.emp_exp = emp_exp
        self.home_ownership = home_ownership
        self.amnt = amnt
        self.intent = intent
        self.rate = rate
        self.percent = percent
        self.cred_length = cred_length
        self.score = score
        self.previous = previous
        self.loan_status = loan_status

        if data_insercao:
            self.data_insercao = data_insercao
