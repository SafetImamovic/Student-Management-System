from fastapi.testclient import TestClient
from main import app, prefix
from app.database.models.courses import Course

client = TestClient(app)


def test_create_course(create_course):
    assert create_course['name'] == "Test Course"

    assert create_course['description'] == "Test Description"


def test_get_count(create_course):
    response = client.get(prefix + "/courses/count/")

    assert response.status_code == 200


def test_get_by_id(create_course):
    course_id = create_course['course_id']

    response = client.get(prefix + f"/courses/{course_id}")

    assert response.status_code == 200

    course = response.json()

    assert course['course_id'] == course_id


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

    assert any(course['name'] == "Test Course" for course in courses)


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
