from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model import Base

# colunas = Pregnancies,Glucose,BloodPressure,SkinThickness,test,BMI,DiabetesPedigreeFunction,Age,Outcome
# Person ID,Gender,Age,Sleep Duration,Quality of Sleep,Physical Activity Level,Stress Level,BMI Category,Blood Pressure,Heart Rate,Daily Steps,Sleep Disorder


class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True)
    person_id = Column("ID Pessoa", Integer)
    gender = Column("Genero", String(1))
    age = Column("Idade", Integer)
    sleep_duration = Column("Duracao", Float)
    quality_sleep = Column("Qualidade", Integer)
    activity_level = Column("Atividade", Integer)
    stress_level = Column("Estresse", Integer)
    bmi_category = Column("IMC", Integer)
    blood_pressure = Column("Pressao", Float)
    heart_rate = Column("FrequenciaCardiaca", Integer)
    daily_steps = Column("Passos", Integer)
    outcome = Column("Disturbio", Integer, nullable=True)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(
        self,
        person_id: int,
        gender: str,
        age: int,
        sleep_duration: float,
        quality_sleep: int,
        activity_level: int,
        stress_level: int,
        bmi_category: int,
        blood_pressure: float,
        heart_rate: int,
        daily_steps: int,
        outcome: int,
        data_insercao: Union[DateTime, None] = None,
    ):
        """
        Cria uma Pessoa

        Arguments:
            person_id: identificador para cada indivíduo
            gender: Gênero: gênero da pessoa (Masculino/Feminino)
            age: idade
            sleep_duration: duração do sono (horas)
            quality_sleep: qualidade do Sono (escala: 1-10)
            stress_level: nivel de estresse (escala: 1-10)
            bmi_category: categoria de IMC: (Normal(1), Sobrepeso(2), Obeso(3)).
            blood_pressure: pressão arterial (sistólica/diastólica)
            heart_rate: frequência cardíaca (bpm)
            daily_steps: número de passos que a pessoa dá por dia.
            outcome: diagnóstico
            data_insercao: data de quando a pessoa foi inserida à base
        """
        self.person_id = person_id
        self.gender = gender
        self.age = age
        self.sleep_duration = sleep_duration
        self.quality_sleep = quality_sleep
        self.activity_level = activity_level
        self.stress_level = stress_level
        self.bmi_category = bmi_category
        self.blood_pressure = blood_pressure
        self.heart_rate = heart_rate
        self.daily_steps = daily_steps
        self.outcome = outcome

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
