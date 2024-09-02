from fastapi.testclient import TestClient
from main import app, prefix
from app.database.models.enrollments import Enrollment

client = TestClient(app)


def test_create_enrollment(db_session, create_user, create_course):
    enrollment_data = {
        "user_id": create_user['user_id'],
        "course_id": create_course['course_id'],
        "enrolled_date": "2024-09-02",
        "end_date": "2024-09-02",
        "associative_data": "Test Associative Data 2",
    }

    response = client.post(prefix + "/enrollments/", json=enrollment_data)

    assert response.status_code == 200

    enrollment = response.json()

    db_session.query(Enrollment).filter(
        Enrollment.user_id == enrollment['user_id'],
        Enrollment.course_id == enrollment['course_id']
    ).delete()

    db_session.commit()


def test_get_count(create_enrollment):
    response = client.get(prefix + "/enrollments/count/")

    assert response.status_code == 200

    assert response.json() > 0


def test_get_by_id(create_enrollment):
    user_id = create_enrollment['user_id']

    course_id = create_enrollment['course_id']

    response = client.get(prefix + f"/enrollments/{user_id}/{course_id}")

    assert response.status_code == 200

    enrollment = response.json()

    assert enrollment['user_id'] == user_id

    assert enrollment['course_id'] == course_id


def test_get_all(create_enrollment):
    response = client.get(prefix + "/enrollments/", params={"skip": 0, "limit": 10})

    assert response.status_code == 200

    enrollments = response.json()

    assert isinstance(enrollments, list)

    assert any(enrollment['user_id'] == create_enrollment['user_id'] and enrollment['course_id'] == create_enrollment[
        'course_id'] for enrollment in enrollments)


def test_delete_enrollment(create_enrollment):
    user_id = create_enrollment['user_id']

    course_id = create_enrollment['course_id']

    response = client.delete(prefix + f"/enrollments/{user_id}/{course_id}")

    assert response.status_code == 200

    deleted_enrollment = response.json()

    assert deleted_enrollment['user_id'] == user_id

    assert deleted_enrollment['course_id'] == course_id
