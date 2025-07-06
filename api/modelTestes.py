import pytest
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

# Caminho do modelo
MODEL_PATH = './MachineLearning/pipelines/aprovacao_pipeline_rf.pkl'

# URL do dataset original
DATASET_URL = "https://raw.githubusercontent.com/allicia21/mvp_segunda_sprint_lm/refs/heads/master/avaliacaoEmprestismos.csv"

# Thresholds de desempenho esperados
ACCURACY_THRESHOLD = 0.85
PRECISION_THRESHOLD = 0.85
RECALL_THRESHOLD = 0.80
F1_THRESHOLD = 0.82


@pytest.fixture
def dados_teste():
    """Carrega dados e retorna conjunto de teste formatado"""
    df = pd.read_csv(DATASET_URL, nrows=5000)
    X = df.drop(columns=['loan_status'])
    y = df['loan_status'].astype(int)
    return train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)


def test_modelo_predicao(dados_teste):
    """Testa se o modelo atinge os critérios de desempenho"""
    X_train, X_test, y_train, y_test = dados_teste

    # Carrega pipeline
    modelo = joblib.load(MODEL_PATH)

    # Faz predições
    y_pred = modelo.predict(X_test)

    # Avalia métricas
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"Accuracy: {acc:.4f}, Precision: {prec:.4f}, Recall: {rec:.4f}, F1-score: {f1:.4f}")

    # Asserções
    assert acc >= ACCURACY_THRESHOLD, f"Accuracy abaixo do esperado: {acc:.4f}"
    assert prec >= PRECISION_THRESHOLD, f"Precision abaixo do esperado: {prec:.4f}"
    assert rec >= RECALL_THRESHOLD, f"Recall abaixo do esperado: {rec:.4f}"
    assert f1 >= F1_THRESHOLD, f"F1-score abaixo do esperado: {f1:.4f}"

def test_modelo_rf(dados_teste):
    """Testa se o modelo Random Forest atinge os critérios de desempenho"""
    X_train, X_test, y_train, y_test = dados_teste

    # Carrega pipeline Random Forest
    rf_model_path = './MachineLearning/models/rf_best_model.pkl'
    modelo_rf = joblib.load(rf_model_path)

    # Faz predições
    y_pred_rf = modelo_rf.predict(X_test)

    # Avalia métricas
    acc_rf = accuracy_score(y_test, y_pred_rf)
    prec_rf = precision_score(y_test, y_pred_rf, zero_division=0)
    rec_rf = recall_score(y_test, y_pred_rf, zero_division=0)
    f1_rf = f1_score(y_test, y_pred_rf, zero_division=0)

    print(f"RF - Accuracy: {acc_rf:.4f}, Precision: {prec_rf:.4f}, Recall: {rec_rf:.4f}, F1-score: {f1_rf:.4f}")

    # Asserções
    assert acc_rf >= ACCURACY_THRESHOLD, f"RF Accuracy abaixo do esperado: {acc_rf:.4f}"
    assert prec_rf >= PRECISION_THRESHOLD, f"RF Precision abaixo do esperado: {prec_rf:.4f}"
    assert rec_rf >= RECALL_THRESHOLD, f"RF Recall abaixo do esperado: {rec_rf:.4f}"
    assert f1_rf >= F1_THRESHOLD, f"RF F1-score abaixo do esperado: {f1_rf:.4f}"

