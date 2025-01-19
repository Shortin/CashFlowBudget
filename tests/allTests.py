import pytest
from fastapi.testclient import TestClient
from app.main import app  # Импортируйте ваш FastAPI объект приложения

client = TestClient(app)

# ------------------ Тесты для пользователей (Users) -------------------

# def test_create_user():
#     response = client.post("/users", json={"name": "John", "login": "john_doe", "password_hash": "hashed_password", "created_at": "2023-01-01T00:00:00"})
#     assert response.status_code == 200
#     assert response.json()["name"] == "John"
#     assert response.json()["login"] == "john_doe"

def test_get_user_by_id():
    response = client.get("/users/1")
    assert response.status_code == 200
#    assert response.json()["id"] == 1

def test_get_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_update_user():
#     response = client.put("/users/1", json={"name": "John Updated", "login": "john_doe_updated"})
#     assert response.status_code == 200
#     assert response.json()["name"] == "John Updated"

# def test_delete_user():
#     response = client.delete("/users/1")
#     assert response.status_code == 200
# #    assert response.json()["id"] == 1

# ------------------ Тесты для расходов (Expense) -------------------

# def test_create_expense():
#     response = client.post("/expenses", json={"amount": 100.0, "description": "Test Expense", "created_at": "2023-01-01T00:00:00"})
#     assert response.status_code == 200
#     assert response.json()["amount"] == 100.0
#     assert response.json()["description"] == "Test Expense"

def test_get_expense_by_id():
    response = client.get("/expenses/1")
    assert response.status_code == 200
#    assert response.json()["id"] == 1

def test_get_expenses():
    response = client.get("/expenses")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_update_expense():
#     response = client.put("/expenses/1", json={"amount": 150.0, "description": "Updated Expense"})
#     assert response.status_code == 200
#     assert response.json()["amount"] == 150.0
#     assert response.json()["description"] == "Updated Expense"
#
# def test_delete_expense():
#     response = client.delete("/expenses/1")
#     assert response.status_code == 200
# #    assert response.json()["id"] == 1

# ------------------ Тесты для доходов (Income) -------------------

# def test_create_income():
#     response = client.post("/incomes", json={"amount": 500.0, "description": "Test Income", "created_at": "2023-01-01T00:00:00", "user_name": "John"})
#     assert response.status_code == 200
#     assert response.json()["amount"] == 500.0
#     assert response.json()["user_name"] == "John"

def test_get_income_by_id():
    response = client.get("/incomes/1")
    assert response.status_code == 200
#    assert response.json()["id"] == 1

def test_get_incomes():
    response = client.get("/incomes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_update_income():
#     response = client.put("/incomes/1", json={"amount": 600.0, "description": "Updated Income", "user_name": "John Updated"})
#     assert response.status_code == 200
#     assert response.json()["amount"] == 600.0
#     assert response.json()["description"] == "Updated Income"
#     assert response.json()["user_name"] == "John Updated"
#
# def test_delete_income():
#     response = client.delete("/incomes/1")
#     assert response.status_code == 200
# #    assert response.json()["id"] == 1

# ------------------ Тесты для семей (Family) -------------------

# def test_create_family():
#     response = client.post("/families", json={"family_name": "Smith", "description": "The Smith Family", "created_at": "2023-01-01T00:00:00"})
#     assert response.status_code == 200
#     assert response.json()["family_name"] == "Smith"
#     assert response.json()["description"] == "The Smith Family"

def test_get_family_by_id():
    response = client.get("/families/1")
    assert response.status_code == 200
#    assert response.json()["id"] == 1

def test_get_families():
    response = client.get("/families")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_update_family():
#     response = client.put("/families/1", json={"family_name": "Johnson", "description": "The Johnson Family"})
#     assert response.status_code == 200
#     assert response.json()["family_name"] == "Johnson"
#     assert response.json()["description"] == "The Johnson Family"
#
# def test_delete_family():
#     response = client.delete("/families/1")
#     assert response.status_code == 200
# #    assert response.json()["id"] == 1

# ------------------ Тесты для ролей (Role) -------------------

# def test_create_role():
#     response = client.post("/roles", json={"name": "Admin"})
#     assert response.status_code == 200
#     assert response.json()["name"] == "Admin"

def test_get_role_by_id():
    response = client.get("/roles/1")
    assert response.status_code == 200
#    assert response.json()["id"] == 1

def test_get_roles():
    response = client.get("/roles")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# def test_update_role():
#     response = client.put("/roles/1", json={"name": "User"})
#     assert response.status_code == 200
#     assert response.json()["name"] == "User"
#
# def test_delete_role():
#     response = client.delete("/roles/1")
#     assert response.status_code == 200
# #    assert response.json()["id"] == 1
