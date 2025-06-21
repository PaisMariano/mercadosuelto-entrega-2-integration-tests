import requests

BASE_URL_PROD_CAT = "http://localhost:8080/api/v1"
BASE_URL_SEL_USR = "http://localhost:8081/api/v1"

def seller_data():
    return {
        "email": "testseller@example.com",
        "businessName": "test company",
        "companyName": "test company"
    }

def create_seller(data):
    response = requests.post(f"{BASE_URL_SEL_USR}/sellers", json=data)
    assert response.status_code == 201
    return response.json()["id"]

def create_product():
    seller_id = get_seller_id()
    payload = {"name": "Test Product", "price": 10.0, "description": "Test", "category": "Test", "sellerId": seller_id, "stock": 5}
    resp = requests.post(f"{BASE_URL_PROD_CAT}/products", json=payload)
    resp.raise_for_status()
    return resp.json()["id"]

def delete_seller(seller_id):
    response = requests.delete(f"{BASE_URL_SEL_USR}/sellers/{seller_id}")
    assert response.status_code == 204

def delete_product(product_id):
    requests.delete(f"{BASE_URL_PROD_CAT}/products/{product_id}")

def get_user_id():
    response = requests.get(f"{BASE_URL_SEL_USR}/users")
    response.raise_for_status()
    data = response.json()
    return data[0]["id"]  # Primer elemento del listado

def get_seller_id():
    response = requests.get(f"{BASE_URL_SEL_USR}/sellers")
    response.raise_for_status()
    data = response.json()
    return data[0]["id"]  # Primer elemento del listado


## TESTS PRODUCTS

def test_delete_all_products():
    response = requests.get(f"{BASE_URL_PROD_CAT}/products")
    response.raise_for_status()
    data = response.json()
    for product in data:
        product_id = product["id"]
        delete_resp = requests.delete(f"{BASE_URL_PROD_CAT}/products/{product_id}")
        delete_resp.raise_for_status()
        resp = requests.get(f"{BASE_URL_PROD_CAT}/products/{product_id}")
        assert resp.status_code == 404

def test_create_product():
    seller_id = create_seller(seller_data())
    payload = {"name": "Test N1", "price": 10.0, "description": "Test", "category": "Test", "sellerId": seller_id, "stock": 5}
    resp = requests.post(f"{BASE_URL_PROD_CAT}/products", json=payload)
    assert resp.status_code == 201
    prod_id = resp.json()["id"]
    delete_product(prod_id)

def test_get_all_products():
    resp = requests.get(f"{BASE_URL_PROD_CAT}/products")
    assert resp.status_code == 200

def test_create_and_delete_product():
    product_id = create_product()
    # Verifica que el producto fue creado
    resp = requests.get(f"{BASE_URL_PROD_CAT}/products/{product_id}")
    assert resp.status_code == 200
    # Limpieza
    delete_product(product_id)
    # Verifica que fue eliminado
    resp = requests.get(f"{BASE_URL_PROD_CAT}/products/{product_id}")
    assert resp.status_code == 404

## TEST SALE

def test_process_sale():
    product_id = create_product()
    user_id = get_user_id()
    payload = {
        "productId": product_id,
        "quantity": 1,
        "userId": user_id
    }
    resp = requests.post(f"{BASE_URL_PROD_CAT}/sales/process", json=payload)
    assert resp.status_code == 200
    # Limpieza
    delete_product(product_id)

## TEST USERS

def test_create_and_delete_user():
    # Crear usuario
    user_data = {
        "name": "Test",
        "lastName": "User",
        "email": "testuser@example.com",
        "password": "123456"
    }
    response = requests.post(f"{BASE_URL_SEL_USR}/users", json=user_data)
    assert response.status_code == 201
    user_id = response.json()["id"]

    # Obtener usuario
    get_response = requests.get(f"{BASE_URL_SEL_USR}/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == user_data["email"]

    # Borrar usuario (limpieza)
    del_response = requests.delete(f"{BASE_URL_SEL_USR}/users/{user_id}")
    assert del_response.status_code == 204

    # Verificar que ya no existe
    get_response = requests.get(f"{BASE_URL_SEL_USR}/users/{user_id}")
    assert get_response.status_code == 404

def test_get_all_users():
    response = requests.get(f"{BASE_URL_SEL_USR}/users")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

## TESTS SELLERS

def test_delete_all_sellers():
    response = requests.get(f"{BASE_URL_SEL_USR}/sellers")
    response.raise_for_status()
    data = response.json()
    for seller in data:
        seller_id = seller["id"]
        delete_resp = requests.delete(f"{BASE_URL_SEL_USR}/sellers/{seller_id}")
        delete_resp.raise_for_status()
        resp = requests.get(f"{BASE_URL_SEL_USR}/sellers/{seller_id}")
        assert resp.status_code == 404

def test_update_seller():
    seller_id = create_seller(seller_data())
    update_data = seller_data().copy()
    update_data["companyName"] = "NuevoNombre"
    resp = requests.put(f"{BASE_URL_SEL_USR}/sellers/{seller_id}", json=update_data)
    assert resp.status_code == 200
    assert resp.json()["businessName"] == "NuevoNombre"
    delete_seller(seller_id)

def test_get_all_sellers():
    seller_id = create_seller(seller_data())
    resp = requests.get(f"{BASE_URL_SEL_USR}/sellers")
    assert resp.status_code == 200
    assert any(s["id"] == seller_id for s in resp.json())
    delete_seller(seller_id)

def test_delete_seller_endpoint():
    seller_id = create_seller(seller_data())
    delete_seller(seller_id)
    get_resp = requests.get(f"{BASE_URL_SEL_USR}/sellers/{seller_id}")
    assert get_resp.status_code == 404

def test_create_and_get_seller():
    seller_id = create_seller(seller_data())
    get_resp = requests.get(f"{BASE_URL_SEL_USR}/sellers/{seller_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["email"] == seller_data()["email"]
    delete_seller(seller_id)