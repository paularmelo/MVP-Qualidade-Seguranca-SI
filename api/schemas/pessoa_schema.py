from pydantic import BaseModel
from typing import Optional, List
from model.pessoa import Pessoa
import json
import numpy as np


class PessoaSchema(BaseModel):
    """Define como uma nova pessoa a ser inserido deve ser representado"""

    person_id: int = 1
    gender: str = "Masculino"
    age: int = 50
    sleep_duration: float = 6.1
    quality_sleep: int = 6
    activity_level: int = 42
    stress_level: int = 8
    bmi_category: int = 2.1
    blood_pressure: float = 126.83
    heart_rate: int = 77
    daily_steps: int = 4200


class PessoaViewSchema(BaseModel):
    """Define como uma pessoa será retornado"""

    id: int = 1
    person_id: int = 1
    gender: str = "Masculino"
    age: int = 50
    sleep_duration: float = 6.1
    quality_sleep: int = 6
    activity_level: int = 42
    stress_level: int = 8
    bmi_category: int = 2.1
    blood_pressure: float = 126.83
    heart_rate: int = 77
    daily_steps: int = 4200
    outcome: int = None


class PessoaBuscaSchema(BaseModel):
    """Define como deve ser a estrutura que representa a busca.
    Ela será feita com base no número da pessoa.
    """

    person_id: int = "1"


class ListaPessoasSchema(BaseModel):
    """Define como uma lista de pessoas será representada"""

    pessoas: List[PessoaSchema]


class PessoaDelSchema(BaseModel):
    """Define como uma pessoa para deleção será representada"""

    person_id: int = "1"


# Apresenta apenas os dados de uma pessoa
def apresenta_pessoa(pessoa: Pessoa):
    """Retorna uma representação da pessoa seguindo o schema definido em
    PessoaViewSchema.
    """
    return {
        "id": pessoa.id,
        "person_id": pessoa.person_id,
        "gender": pessoa.gender,
        "age": pessoa.age,
        "sleep_duration": pessoa.sleep_duration,
        "quality_sleep": pessoa.quality_sleep,
        "activity_level": pessoa.activity_level,
        "stress_level": pessoa.stress_level,
        "bmi_category": pessoa.bmi_category,
        "blood_pressure": pessoa.blood_pressure,
        "heart_rate": pessoa.heart_rate,
        "daily_steps": pessoa.daily_steps,
        "outcome": pessoa.outcome,
    }


# Apresenta uma lista de pessoas
def apresenta_pessoas(pessoas: List[Pessoa]):
    """Retorna uma representação da pessoa seguindo o schema definido em
    PessoaViewSchema.
    """
    result = []
    for pessoa in pessoas:
        result.append(
            {
                "id": pessoa.id,
                "person_id": pessoa.person_id,
                "gender": pessoa.gender,
                "age": pessoa.age,
                "sleep_duration": pessoa.sleep_duration,
                "quality_sleep": pessoa.quality_sleep,
                "activity_level": pessoa.activity_level,
                "stress_level": pessoa.stress_level,
                "bmi_category": pessoa.bmi_category,
                "blood_pressure": pessoa.blood_pressure,
                "heart_rate": pessoa.heart_rate,
                "daily_steps": pessoa.daily_steps,
                "outcome": pessoa.outcome,
            }
        )

    return {"pessoas": result}
