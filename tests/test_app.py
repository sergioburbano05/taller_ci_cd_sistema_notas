import pytest

from app import create_app, student_summary, validate_grades


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_health_returns_200(client):
    response = client.get("/health")

    assert response.status_code == 200


def test_health_returns_service_name(client):
    response = client.get("/health")

    assert response.get_json() == {"status": "ok", "service": "sistema-notas"}


def test_student_summary_returns_existing_student(client):
    response = client.get("/students/1001/summary")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["name"] == "Ana"


def test_student_summary_calculates_average_correctly():
    summary = student_summary(1001)

    assert summary["average"] == 4.17


def test_student_summary_marks_student_as_passed():
    summary = student_summary(1003)

    assert summary["passed"] is True


def test_student_summary_returns_none_for_unknown_student():
    assert student_summary(9999) is None


def test_evaluate_grades_returns_average_and_count(client):
    response = client.post("/grades/evaluate", json={"grades": [3.0, 4.0, 5.0]})

    assert response.status_code == 200
    assert response.get_json() == {"average": 4.0, "count": 3, "passed": True}


def test_evaluate_grades_marks_failed_average(client):
    response = client.post("/grades/evaluate", json={"grades": [2.0, 2.5, 3.0]})

    assert response.get_json()["passed"] is False


def test_validate_grades_rejects_empty_list():
    with pytest.raises(ValueError, match="Debes enviar una lista de notas"):
        validate_grades([])


def test_validate_grades_rejects_grade_out_of_range():
    with pytest.raises(ValueError, match="Cada nota debe estar entre 0 y 5"):
        validate_grades([4.0, 6.0])
