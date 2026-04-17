from flask import Flask, jsonify, request


STUDENTS = {
    1001: {"name": "Ana", "grades": [4.5, 3.8, 4.2]},
    1002: {"name": "Luis", "grades": [2.8, 3.1, 2.9]},
    1003: {"name": "Marta", "grades": [5.0, 4.7, 4.9]},
}


def calculate_average(grades):
    if not grades:
        raise ValueError("La lista de notas no puede estar vacia")
    return round(sum(grades) / len(grades), 2)


def validate_grades(grades):
    if not isinstance(grades, list) or not grades:
        raise ValueError("Debes enviar una lista de notas")

    for grade in grades:
        if not isinstance(grade, (int, float)):
            raise ValueError("Todas las notas deben ser numericas")
        if grade < 0 or grade > 5:
            raise ValueError("Cada nota debe estar entre 0 y 5")


def student_summary(student_id):
    student = STUDENTS.get(student_id)
    if student is None:
        return None

    average = calculate_average(student["grades"])
    return {
        "id": student_id,
        "name": student["name"],
        "average": average,
        "passed": average >= 3.0,
    }


def create_app():
    app = Flask(__name__)

    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok", "service": "sistema-notas"})

    @app.get("/students/<int:student_id>/summary")
    def get_student_summary(student_id):
        summary = student_summary(student_id)
        if summary is None:
            return jsonify({"error": "Estudiante no encontrado"}), 404
        return jsonify(summary)

    @app.post("/grades/evaluate")
    def evaluate_grades():
        payload = request.get_json(silent=True) or {}
        grades = payload.get("grades")

        try:
            validate_grades(grades)
        except ValueError as error:
            return jsonify({"error": str(error)}), 400

        average = calculate_average(grades)
        return jsonify(
            {
                "average": average,
                "count": len(grades),
                "passed": average >= 3.0,
            }
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
