import pytest
from app import app  # importe seu app Flask

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_clientes(client):
    response = client.get('/clientes')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data['clientes'], list)

def test_deletar_cliente(client):
    # Primeiro, adicione um cliente para garantir que haja algo para deletar
    response = client.post('/cliente', json={
        "person_age": 30,
        "person_gender": "F",
        "person_education": "Bachelor",
        "person_income": 50000,
        "person_emp_exp": 5,
        "person_home_ownership": "Own",
        "loan_amnt": 10000,
        "loan_intent": "Personal",
        "loan_int_rate": 5.0,
        "loan_percent_income": 20.0,
        "cb_person_cred_hist_length": 24,
        "credit_score": 700,
        "previous_loan_defaults_on_file": 0,
        "loan_status": 1
    })
    assert response.status_code == 200

def test_client_prediction(client):
    response = client.post('/cliente', json={
        "person_age": 30,
        "person_gender": "F",
        "person_education": "Bachelor",
        "person_income": 50000,
        "person_emp_exp": 5,
        "person_home_ownership": "Own",
        "loan_amnt": 10000,
        "loan_intent": "Personal",
        "loan_int_rate": 5.0,
        "loan_percent_income": 20.0,
        "cb_person_cred_hist_length": 24,
        "credit_score": 700,
        "previous_loan_defaults_on_file": 0
    })
    assert response.status_code == 200