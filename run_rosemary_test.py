import subprocess
import sys

# Definir comandos como listas estáticas
ALLOWED_COMMANDS = {
    "selenium": ["rosemary", "selenium"],
    "coverage": ["rosemary", "coverage"],
    "locust": ["rosemary", "locust"],
}


def validate_command(command):
    """Valida que el comando esté dentro de los permitidos."""
    if not isinstance(command, list) or len(command) == 0:
        raise ValueError("El comando debe ser una lista no vacía.")
    if command not in ALLOWED_COMMANDS.values():
        raise ValueError(f"Comando no permitido: {command}")


def run_command(command):
    """Ejecuta un comando definido de forma segura y maneja errores."""
    try:
        validate_command(command)  # Validar el comando
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True  # Lanza excepción si el comando falla
        )
        print(result.stdout)
    except ValueError as ve:
        print(f"Error de validación: {ve}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando {command[0]}: {e.stderr.strip()}")
        sys.exit(e.returncode)
    except FileNotFoundError:
        print(f"Comando no encontrado: {command[0]}")
        sys.exit(1)


def run_rosemary_selenium():
    """Ejecuta pruebas Selenium con Rosemary."""
    print("Ejecutando pruebas Selenium con Rosemary...")
    run_command(ALLOWED_COMMANDS["selenium"])


def run_rosemary_coverage():
    """Ejecuta pruebas con cobertura utilizando Rosemary."""
    print("Ejecutando pruebas de cobertura con Rosemary...")
    run_command(ALLOWED_COMMANDS["coverage"])


def run_rosemary_locust():
    """Ejecuta pruebas de rendimiento (Locust) con Rosemary."""
    print("Ejecutando pruebas de rendimiento con Rosemary...")
    run_command(ALLOWED_COMMANDS["locust"])


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
