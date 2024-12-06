import subprocess
import sys
from shlex import quote

# Lista de comandos permitidos
ALLOWED_COMMANDS = {
    "selenium": ["rosemary", "selenium"],
    "coverage": ["rosemary", "coverage"],
    "locust": ["rosemary", "locust"]
}


def validate_command(command_key):
    """
    Valida que el comando solicitado esté en la lista de comandos permitidos.
    """
    if command_key not in ALLOWED_COMMANDS:
        raise ValueError(f"Comando no permitido: {command_key}")
    return ALLOWED_COMMANDS[command_key]


def sanitize_command(command):
    """
    Sanitiza los argumentos del comando para evitar inyecciones.
    """
    return [quote(arg) for arg in command]


def run_command(command_key):
    """
    Ejecuta un comando de forma segura después de validarlo y sanitizarlo.
    """
    try:
        # Validar y sanitizar el comando
        command = validate_command(command_key)
        sanitized_command = sanitize_command(command)

        # Ejecutar el comando
        result = subprocess.run(
            sanitized_command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True  # Genera una excepción si el comando falla
        )

        # Mostrar la salida del comando
        print(result.stdout)

    except ValueError as ve:
        print(f"Error de validación: {ve}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {command_key}: {e.stderr.strip()}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Comando no encontrado: {command_key}")
        sys.exit(1)


def run_rosemary_selenium():
    """Ejecuta pruebas Selenium con Rosemary."""
    print("Ejecutando pruebas Selenium con Rosemary...")
    run_command("selenium")


def run_rosemary_coverage():
    """Ejecuta pruebas de cobertura utilizando Rosemary."""
    print("Ejecutando pruebas de cobertura con Rosemary...")
    run_command("coverage")


def run_rosemary_locust():
    """Ejecuta pruebas de rendimiento (Locust) con Rosemary."""
    print("Ejecutando pruebas de rendimiento con Rosemary...")
    run_command("locust")


def main():
    print("Iniciando pruebas automatizadas con Rosemary...")
    try:
        run_rosemary_selenium()
        run_rosemary_coverage()
        run_rosemary_locust()
        print("Todas las pruebas se ejecutaron con éxito.")
    except Exception as e:
        print(f"Error durante la ejecución de pruebas: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
