import subprocess
import sys


def run_rosemary_selenium():
    """Ejecuta pruebas Selenium con Rosemary."""
    print("Ejecutando pruebas Selenium con Rosemary...")
    result = subprocess.run(
        ["rosemary", "selenium"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        print("Pruebas Selenium fallaron.")
        sys.exit(1)


def run_rosemary_coverage():
    """Ejecuta pruebas con cobertura utilizando Rosemary."""
    print("Ejecutando pruebas de cobertura con Rosemary...")
    result = subprocess.run(
        ["rosemary", "coverage"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        print("Pruebas de cobertura fallaron.")
        sys.exit(1)


def run_rosemary_locust():
    """Ejecuta pruebas de rendimiento (Locust) con Rosemary."""
    print("Ejecutando pruebas de rendimiento con Rosemary...")
    result = subprocess.run(
        ["rosemary", "locust"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        print("Pruebas de rendimiento fallaron.")
        sys.exit(1)


def main():
    print("Iniciando pruebas automatizadas con Rosemary...")
    run_rosemary_selenium()
    run_rosemary_coverage()
    run_rosemary_locust()
    print("Todas las pruebas se ejecutaron con éxito.")


if __name__ == "__main__":
    main()
