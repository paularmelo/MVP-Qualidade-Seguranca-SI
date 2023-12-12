from model.avaliador import Avaliador
from model.carregador import Carregador
from model.modelo import Model

# To run: pytest -v test_modelos.py

# Instanciação das Classes
carregador = Carregador()
modelo = Model()
avaliador = Avaliador()

# Parâmetros
url_dados = "database/sleep_health_golden.csv"
colunas = [
    "person_ID",
    "gender",
    "age",
    "sleep_duration",
    "quality_sleep",
    "activity_level",
    "stress_level",
    "bmi_category",
    "blood_pressure",
    "heart_rate",
    "daily_steps",
    "disorder",
]

# Carga dos dados
dataset = carregador.carregar_dados(url_dados, colunas)

# Separando em dados de entrada e saída
X = dataset.iloc[:, 0:-1]
Y = dataset.iloc[:, -1]


# Método para testar o modelo do SVM a partir do arquivo correspondente
# O nome do método a ser testado necessita começar com "test_"
def test_modelo_svm():
    # Importando o modelo do SVM
    svm_path = "ml_model/sleep_health.pkl"
    modelo_svm = modelo.carrega_modelo(svm_path)

    # Obtendo as métricas do SVM
    acuracia_svm, recall_svm, precisao_svm, f1_svm = avaliador.avaliar(modelo_svm, X, Y)

    # Testando as métricas do SVM
    # Modifique as métricas de acordo com seus requisitos
    assert acuracia_svm >= 0.75
    assert recall_svm >= 0.5
    assert precisao_svm >= 0.5
    assert f1_svm >= 0.5
