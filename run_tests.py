import subprocess
import sys


def run_command(description, command):
    """Run a shell command and handle its output."""
    print(f"Running {description}...")
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        print(f"{description} failed.\n")
        return False
    return True


def run_pytest():
    """Run unit and integration tests with coverage."""
    return run_command(
        "pytest (unit and integration tests)",
        ["pytest", "--cov=app", "--cov-report=term", "--cov-report=html"],
    )


def run_selenium():
    """Run Selenium tests."""
    return run_command(
        "Selenium tests",
        ["pytest", "app/modules/**/tests/test_selenium.py"],
    )


def run_locust():
    """Run Locust for performance testing."""
    return run_command(
        "Locust tests",
        [
            "locust",
            "-f",
            "app/tests/locustfile.py",
            "--headless",
            "-u",
            "10",
            "-r",
            "2",
            "--run-time",
            "1m",
        ],
    )


def main():
    print("Starting automated tests...\n")

    # Run tests
    pytest_success = run_pytest()
    selenium_success = run_selenium()
    locust_success = run_locust()

    # Summarize results
    print("\n=== Test Summary ===")
    print(f"Pytest: {'PASSED' if pytest_success else 'FAILED'}")
    print(f"Selenium: {'PASSED' if selenium_success else 'FAILED'}")
    print(f"Locust: {'PASSED' if locust_success else 'FAILED'}")

    # Exit code based on overall success
    if not (pytest_success and selenium_success and locust_success):
        print("\nSome tests failed. Please check the logs above for details.")
        sys.exit(1)

    print("\nAll tests completed successfully.")


if __name__ == "__main__":
    main()
