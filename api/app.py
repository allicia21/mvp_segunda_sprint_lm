import os
from flask_openapi3 import OpenAPI, Info, Tag
from flask import jsonify, redirect, request, send_from_directory
from urllib.parse import unquote
from model.pipeline import Pipeline
from model.preprocessador import PreProcessador
from model.cliente import Cliente
from model._init_ import Session
from flask_cors import CORS
from schemas.cliente_schema import ClienteDeleteSchema, ClienteSchema, ClienteViewSchema, ListaClientesSchema, apresenta_clientes, apresenta_cliente
from schemas.erro_schema import ErrorSchema
import logging
import pandas as pd


logging.basicConfig(level=logging.INFO)

# Instanciando o objeto OpenAPI
info = Info(title="API AVALIAÇÃO DE APROVAÇÃO DE EMPRESTIMO", version="1.0.0")

app = OpenAPI(
    __name__, info=info, static_folder="../front", static_url_path="/front"
)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger",
)
cliente_tag = Tag(
    name="Clientes",
    description="Adição, visualização, remoção e predição de cliente para avaliação de aprovação" \
    " de empréstimo",
)


# Rota home - redireciona para o frontend
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para o index.html do frontend."""
    front_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "front"))
    return send_from_directory(front_path, "index.html")
    #return redirect('/openapi')

@app.get("/docs", tags=[home_tag])
def docs():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


logger = logging.getLogger(__name__)


@app.post(
    "/cliente",
    tags=[cliente_tag],
    responses={
        "200": ClienteViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)

def predict():
    try:
        data = request.get_json()
        form = ClienteSchema(**data)
    except Exception as e:
        return {"message": f"Erro na validação dos dados: {str(e)}"}, 400
    
    
    # Cria DataFrame com dados crus, com os nomes exatos das colunas originais do treino
    X_input = pd.DataFrame([{
        'person_age': form.person_age,
        'person_gender': form.person_gender,
        'person_education': form.person_education,
        'person_income': form.person_income,
        'person_emp_exp': form.person_emp_exp,
        'person_home_ownership': form.person_home_ownership,
        'loan_amnt': form.loan_amnt,
        'loan_intent': form.loan_intent,
        'loan_int_rate': form.loan_int_rate,
        'loan_percent_income': form.loan_percent_income,
        'cb_person_cred_hist_length': form.cb_person_cred_hist_length,
        'credit_score': form.credit_score,
        'previous_loan_defaults_on_file': form.previous_loan_defaults_on_file,
    }])

    pipeline = Pipeline()
    model_path = "./MachineLearning/pipelines/aprovacao_pipeline_rf.pkl"
    modelo = pipeline.carrega_pipeline(model_path)

    print(X_input.dtypes)
    print(X_input.head())

    categorical_cols = ['person_gender', 'person_education', 'person_home_ownership', 'loan_intent', 'previous_loan_defaults_on_file']

    for col in categorical_cols:
        X_input[col] = X_input[col].astype(str).str.title().str.strip()
        X_input[col] = X_input[col].replace({'Nan': 'Unknown'})

# Garantir que todas as colunas estão no formato certo
    X_input = X_input.fillna(0)

    loan_status = int(modelo.predict(X_input)[0])

    cliente = Cliente(
        age=form.person_age,
        gender=form.person_gender,
        education=form.person_education,
        income=form.person_income,
        emp_exp=form.person_emp_exp,
        home_ownership=form.person_home_ownership,
        amnt=form.loan_amnt,
        intent=form.loan_intent,
        rate=form.loan_int_rate,
        percent=form.loan_percent_income,
        cred_length=form.cb_person_cred_hist_length,
        score=form.credit_score,
        previous=form.previous_loan_defaults_on_file,
        loan_status=loan_status
    )

    try:
        session = Session()
        session.add(cliente)
        session.commit()

        logger.debug("Cliente adicionado com sucesso.")
        return apresenta_cliente(cliente), 200

    except Exception as e:
        logger.warning(f"Erro ao adicionar cliente: {e}")
        return {"message": "Não foi possível salvar novo item :/"}, 400
    

@app.get(
    "/clientes",
    tags=[cliente_tag],
    responses={"200": ListaClientesSchema, "404": ErrorSchema},
)
def get_clientes():
    """Lista todos os clientes cadastrados na base

    Returns:
        list: lista de clientes cadastrados na base
    """
    logger.debug("Coletando dados sobre todos os clientes")
    session = Session()
    clientes = session.query(Cliente).all()

    if not clientes:
        return {"clientes": []}, 200
    else:
        logger.debug(f"{len(clientes)} clientes encontrados")
        return apresenta_clientes(clientes), 200


# Rota de DELETE de cliente por ID
@app.delete('/cliente', tags=[cliente_tag],
            responses={'200': ClienteDeleteSchema, '404': ErrorSchema})
def del_cliente():
    data = request.get_json()
    cliente_id = data.get("id")

    print("Raw data:", request.data)

    print("ID recebido:", cliente_id)

    if cliente_id is None:
        return jsonify({"message": "ID inválido"}), 400

    with Session() as session:
        cliente = session.query(Cliente).get(cliente_id)
        print('Cliente encontrado:', cliente)

        if cliente:
            session.delete(cliente)
            session.commit()
            return jsonify({"message": "Cliente removido", "id": cliente_id}), 200

    return jsonify({"message": "Cliente não encontrado"}), 404
