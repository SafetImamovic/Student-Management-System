from fastapi.testclient import TestClient
from main import app, prefix
from app.database.models.courses import Course

client = TestClient(app)


def test_create_course(db_session):
    course_data = {
        "name": "Test Course 2",
        "description": "Test Description 2",
        "start_date": "2024-09-02",
        "end_date": "2024-09-02",
    }

    response = client.post(prefix + "/courses/", json=course_data)

    assert response.status_code == 201

    course = response.json()

    assert course['name'] == "Test Course 2"

    db_session.query(Course).filter(Course.course_id == course['course_id']).delete()

    db_session.commit()


def test_create_course_conflict(db_session):
    course_data = {
        "name": "Test Course 2",
        "description": "Test Description 2",
        "start_date": "2024-09-02",
        "end_date": "2024-09-02",
    }

    first_object = client.post(prefix + "/courses/", json=course_data)

    response = client.post(prefix + "/courses/", json=course_data)

    assert response.status_code == 409

    course = first_object.json()

    assert course['name'] == "Test Course 2"

    db_session.query(Course).filter(Course.course_id == course['course_id']).delete()

    db_session.commit()


def test_create_course_wrong_field_types():
    course_data = {
        "name": 1,
        "description": 2,
        "start_date": True,
        "end_date": False,
    }

    response = client.post(prefix + "/courses/", json=course_data)

    assert response.status_code == 422


def test_get_count(create_course):
    response = client.get(prefix + "/courses/count/")

    assert response.status_code == 200


def test_get_by_id(create_course):
    course_id = create_course['course_id']

    response = client.get(prefix + f"/courses/{course_id}")

    assert response.status_code == 200

    course = response.json()

    assert course['course_id'] == course_id


def test_get_by_id_not_found():
    response = client.get(prefix + f"/courses/0")

    assert response.status_code == 404


def test_get_by_name(create_course):
    course_name = create_course['name']

    response = client.get(prefix + f"/courses/name/{course_name}")

    assert response.status_code == 200

    course = response.json()

    assert course['name'] == course_name


def test_get_all(create_course):
    response = client.get(prefix + "/courses/", params={"skip": 0, "limit": 10})

    assert response.status_code == 200

    courses = response.json()

    assert isinstance(courses, list)


def test_deactivate_course(create_course):
    course_id = create_course['course_id']

    response = client.put(prefix + f"/courses/{course_id}")

    assert response.status_code == 200

    course = response.json()

    assert not course['is_active']


def test_activate_course(create_course):
    course_id = create_course['course_id']

    client.put(prefix + f"/courses/{course_id}")

    response = client.put(prefix + f"/courses/activate/{course_id}")

    assert response.status_code == 200

    course = response.json()

    assert course['is_active']
