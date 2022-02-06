from fastapi.testclient import TestClient
from yakshop.app import app
import json

client = TestClient(app)


def test_get_stock():
    dt_1 = 13
    dt_2 = 14

    res_1 = client.get(f"/yak-shop/stock/{dt_1}")
    assert res_1.status_code == 200
    assert type(res_1.json()) == dict
    assert res_1.json() == {"wool": 3, "milk": 1104.48}

    res_2 = client.get(f"/yak-shop/stock/{dt_2}")
    assert res_2.status_code == 200
    assert type(res_2.json()) == dict
    assert res_2.json() == {"wool": 4, "milk": 1188.81}


def test_get_herd():
    res = client.get("/yak-shop/herd/13")
    assert res.status_code == 200
    assert type(res.json()) == dict
    assert res.json()["herd"][0]["age"] == 4.13


def test_order_from_stock():
    data1 = {"customer": "string", "order": {"milk": 500, "wool": 2}}
    data2 = {"customer": "string", "order": {"milk": 500000, "wool": 2}}
    data3 = {"customer": "string", "order": {"milk": 500000, "wool": 2}}
    res_1 = client.post("/yak-shop/order/14", data=json.dumps(data1))
    res_2 = client.post("/yak-shop/order/14", data=json.dumps(data2))
    res_3 = client.post("/yak-shop/order/14", data=json.dumps(data3))

    assert res_1.json()["status_code"] == 201
    assert res_1.json()["milk"] == 500
    assert res_1.json()["wool"] == 2

    assert res_2.json()["status_code"] == 206
    assert res_2.json()["wool"] == 2

    assert res_3.status_code == 404
