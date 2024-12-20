from locust import HttpUser, TaskSet, task
from core.environment.host import get_host_for_locust_testing
import os
import secrets

SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_bytes())


def extract_token_from_email(response):
    """
    Extraer el token del correo electrónico.
    """
    response_text = response.text
    if "Follow this link to reset your password" in response_text:
        return response_text.split("=")[1]
    return None  # Retornar explícitamente None si no se encuentra el token


class ForgotPasswordBehavior(TaskSet):
    """
    Comportamiento de prueba para cargar la página de recuperación de contraseña.
    """
    def on_start(self):
        self.index()

    @task
    def index(self):
        response = self.client.get("/forgotPassword/forgot")

        if response.status_code != 200:
            print(f"Forgotpassword index failed: {response.status_code}")
        else:
            print("Forgotpassword index success")


class ResetPasswordBehavior(TaskSet):
    def on_start(self):
        # Login al inicio de las pruebas
        response = self.client.post("/login", data={"email": "user@example.com", "password": "test1234"})
        if response.status_code != 200:
            print("Login failed!")
        else:
            print("Login success!")
        token = extract_token_from_email(response)  # Extraer el token del correo

        if not token:
            print("No token received!")
            return

        # Ahora puedes realizar la solicitud para cambiar la contraseña con el token
        new_password = {"password": "NewPassword123!"}
        response = self.client.post(f"/forgotPassword/password/{token}", data=new_password)
        if response.status_code == 200 and "Password successfully changed!" in response.text:
            print("Password reset success!")
        else:
            print(f"Password reset failed: {response.status_code}")

    @task
    def resetPassword(self):
        """
        Prueba de reseteo de contraseña.
        """
        token = extract_token_from_email(self.client.get("/email_mock"))
        if token:
            new_password = {"password": "NewPassword123!"}

            # Simular la solicitud POST para cambiar la contraseña
            with self.client.post(f"/forgotPassword/password/{token}",
                                  data=new_password, catch_response=True)as response:
                if response.status_code == 200 and "Password successfully changed!" in response.text:
                    response.success()
                    print("Reset password success!")
                else:
                    response.failure(f"Reset password failed: {response.status_code}")

    def on_stop(self):
        """
        Logout al finalizar las pruebas.
        """
        self.client.get("/logout")


class PasswordUser(HttpUser):
    tasks = [ForgotPasswordBehavior, ResetPasswordBehavior]
    min_wait = 5000
    max_wait = 9000
    host = get_host_for_locust_testing()
