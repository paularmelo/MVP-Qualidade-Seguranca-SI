from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
import joblib

from sqlalchemy.exc import IntegrityError

from model import Session, Pessoa, Model
from logger import logger
from schemas import *
from flask_cors import CORS


# Instanciando o objeto OpenAPI
info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo tags para agrupamento das rotas
home_tag = Tag(
    name="Documentação",
    description="Seleção de documentação: Swagger, Redoc ou RapiDoc",
)
pessoa_tag = Tag(
    name="Pessoa",
    description="Adição, visualização, remoção e predição de pessoa com um distúrbio do sono",
)


# Rota home
@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


# Rota de listagem de pacientes
@app.get(
    "/pessoas",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "404": ErrorSchema},
)
def get_pessoas():
    """Lista todos as pessoas cadastrados na base
    Retorna uma lista de pessoas cadastrados na base.

    Args:
        person_id (int): número da pessoa

    Returns:
        list: lista de pessoas cadastradas na base
    """
    session = Session()

    # Buscando todos os pacientes
    pessoas = session.query(Pessoa).all()

    if not pessoas:
        logger.warning("Não há pessoas cadastradas na base :/")
        return {"message": "Não há pessoas cadastradas na base :/"}, 404
    else:
        logger.debug(f"%d pessoas econtradas" % len(pessoas))
        return apresenta_pessoas(pessoas), 200


# Rota de adição de pessoa
@app.post(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "400": ErrorSchema, "409": ErrorSchema},
)
def predict(form: PessoaSchema):
    """Adiciona uma nova pessoa à base de dados
    Retorna uma representação das pessoas e presença ou ausência de um distúrbio do sono

    Args:
        person_id (int): identificador para cada indivíduo
        gender (str): Gênero: gênero da pessoa (Masculino/Feminino)
        age (int): idade
        sleep_duration (float): duração do sono (horas)
        quality_sleep (int): qualidade do Sono (escala: 1-10)
        stress_level (int): nivel de estresse (escala: 1-10)
        bmi_category (int): categoria de IMC: (Normal(1), Sobrepeso(2), Obeso(3)).
        blood_pressure (float): pressão arterial (sistólica/diastólica)
        heart_rate (int): frequência cardíaca (bpm)
        daily_steps (int): número de passos que a pessoa dá por dia.

    Returns:
        dict: representação de pessoa e diagnóstico associado
    """

    # Carregando modelo
    ml_path = "ml_model/sleep_health.joblib"
    scaler = joblib.load("ml_model/scaler.joblib")
    modelo = Model.carrega_modelo(ml_path, scaler)

    pessoa = Pessoa(
        person_id=form.person_id,
        gender=form.gender,
        age=form.age,
        sleep_duration=form.sleep_duration,
        quality_sleep=form.quality_sleep,
        activity_level=form.activity_level,
        stress_level=form.stress_level,
        bmi_category=form.bmi_category,
        blood_pressure=form.blood_pressure,
        heart_rate=form.heart_rate,
        daily_steps=form.daily_steps,
        outcome=Model.preditor(modelo, form),
    )
    logger.info(f"Adicionando pessoa de número: '{pessoa.person_id}'")

    try:
        # Criando conexão com a base
        session = Session()

        # Checando se paciente já existe na base
        if session.query(Pessoa).filter(Pessoa.person_id == form.person_id).first():
            error_msg = "Pessoa já existente na base :/"
            logger.warning(
                f"Erro ao adicionar pessoa '{pessoa.person_id}', {error_msg}"
            )
            return {"message": error_msg}, 409

        # Adicionando pessoa
        session.add(pessoa)
        # Efetivando o comando de adição
        session.commit()
        # Concluindo a transação
        logger.debug(f"Adicionado pessoa de número: '{pessoa.person_id}'")
        return apresenta_pessoa(pessoa), 200

    # Caso ocorra algum erro na adição
    except Exception as e:
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pessoa '{pessoa.person_id}', {error_msg}")
        return {"message": error_msg}, 400


# Métodos baseados em nome
# Rota de busca de paciente por nome
@app.get(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "404": ErrorSchema},
)
def get_pessoa(query: PessoaBuscaSchema):
    """Faz a busca por um paciente cadastrado na base a partir do nome

    Args:
        person_id (int): número de identificacao da pessoa

    Returns:
        dict: representação do pessoa e diagnóstico associado
    """

    pessoa_id = query.person_id
    logger.debug(f"Coletando dados sobre produto #{pessoa_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pessoa = session.query(Pessoa).filter(Pessoa.person_id == pessoa_id).first()

    if not pessoa:
        # se o paciente não foi encontrado
        error_msg = f"Pessoa {pessoa_id} não encontrado na base :/"
        logger.warning(f"Erro ao buscar pessoa '{pessoa_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pessoa encontrada: '{pessoa_person_id}'")
        # retorna a representação do paciente
        return apresenta_pessoa(pessoa), 200


# Rota de remoção de paciente por nome
@app.delete(
    "/pessoa",
    tags=[pessoa_tag],
    responses={"200": PessoaViewSchema, "404": ErrorSchema},
)
def delete_pessoa(query: PessoaBuscaSchema):
    """Remove um pessoa cadastrada na base a partir do número de identificacao

    Args:
        person_id (int): número de identificacao da pessoa

    Returns:
        msg: Mensagem de sucesso ou erro
    """
    logger.info("Deletando dados sobre pessoa")
    pessoa_id = query.person_id
    logger.info(f"Deletando dados sobre pessoa #{pessoa_id}")

    # Criando conexão com a base
    session = Session()

    # Buscando pessoa
    pessoa = session.query(Pessoa).filter(Pessoa.person_id == pessoa_id).first()

    if not pessoa:
        error_msg = "Pessoa não encontrada na base :/"
        logger.warning(f"Erro ao deletar pessoa '{pessoa_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(pessoa)
        session.commit()
        logger.debug(f"Deletado pessoa #{pessoa_id}")
        return {"message": f"Pessoa {pessoa_id} removido com sucesso!"}, 200
