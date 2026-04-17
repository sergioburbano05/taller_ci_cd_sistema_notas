# Taller CI/CD con GitHub Actions

Este repositorio de ejemplo implementa una API simple para el sistema de notas de la Universitaria y sirve como base para practicar CI/CD con GitHub.

## Endpoints incluidos

- GET /health
- GET /students/<student_id>/summary
- POST /grades/evaluate

## Requisitos

- Python 3.12
- Git
- Cuenta en GitHub
- Docker Desktop para la parte de CD

## Ejecucion local

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements-dev.txt
python -m pytest
python app.py
```

## Lint y cobertura

```bash
python -m ruff check .
python -m pytest --cov=app --cov-report=term-missing --cov-fail-under=70
```

Todas las dependencias necesarias para ejecutar el taller por consola estan cubiertas en los archivos requirements:

- requirements.txt: dependencias de ejecucion.
- requirements-dev.txt: dependencias de pruebas, cobertura y lint.

## Construccion Docker

```bash
docker build -t sistema-notas:local .
docker run -p 5000:5000 sistema-notas:local
```

## Badge de workflow

Reemplaza TU_USUARIO y TU_REPOSITORIO en el siguiente enlace:

```md
![CI](https://github.com/TU_USUARIO/TU_REPOSITORIO/actions/workflows/ci.yml/badge.svg)
```

## Flujo sugerido para la clase

1. Crear el repositorio en GitHub y subir este contenido.
2. Ejecutar pruebas en local.
3. Hacer push y revisar la pestana Actions.
4. Crear una rama feature y abrir un Pull Request.
5. Introducir un fallo intencional y analizar el resultado del pipeline.
