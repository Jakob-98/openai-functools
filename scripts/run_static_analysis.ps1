# run-black-and-flake8.ps1

# Ensure script stops on first error
$ErrorActionPreference = "Stop"

# Run black for automatic code formatting
Write-Output "Running Black for automatic code formatting..."
poetry run black .

# Run flake8 for linting
Write-Output "Running Flake8 for linting..."
poetry run flake8 .

# Run isort"
poetry run isort .

Write-Output "Static analysis completed successfully!"
