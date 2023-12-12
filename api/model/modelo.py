import numpy as np
import pickle
import joblib
from logger import logger


class Model:
    def carrega_modelo(path, scaler=None):
        """Dependendo se o final for .pkl ou .joblib, carregamos de uma forma ou de outra"""

        if path.endswith(".pkl"):
            model = pickle.load(open(path, "rb"))
        elif path.endswith(".joblib"):
            model = joblib.load(path)
        else:
            raise Exception("Formato de arquivo não suportado")

        if scaler is not None:
            model.scaler = scaler

        return model

    def preditor(model, form):
        """Realiza a predição de uma pessoa com base no modelo treinado"""
        X_input = np.array(
            [
                form.person_id,
                form.gender,
                form.age,
                form.sleep_duration,
                form.quality_sleep,
                form.activity_level,
                form.stress_level,
                form.bmi_category,
                form.blood_pressure,
                form.heart_rate,
                form.daily_steps,
            ]
        )

        # Faremos o reshape para que o modelo entenda que estamos passando
        X_input = X_input.reshape(1, -1)

        # Padronização nos dados de entrada usando o scaler utilizado em X_train
        X_input_scaled = model.scaler.transform(X_input)

        # Adicionando uma dimensão extra para corresponder ao formato esperado pelo modelo
        diagnosis = model.predict(X_input_scaled.reshape(1, -1))

        logger.info(f"================ diagnosis[0] ============ : '{diagnosis[0]}'")
        return int(diagnosis[0])

        # Faremos o reshape para que o modelo entenda que estamos passando

    # X_input = X_input.reshape(1, -1)

    # Padronização nos dados de entrada usando o scaler utilizado em X_train
    # X_input_scaled = model.scaler.transform(X_input)

    # Adicionando uma dimensão extra para corresponder ao formato esperado pelo modelo
    # diagnosis = model.predict(X_input_scaled.reshape(1, -1))

    # logger.info(f"================ diagnosis[0] ============ : '{diagnosis[0]}'")

    # return int(diagnosis[0])

    # Faremos o reshape para que o modelo entenda que estamos passando
    # logger.info(f" ============== X_input: '{X_input}'")
    # diagnosis = model.predict(X_input.reshape(1, -1))
    # return int(diagnosis[0])
