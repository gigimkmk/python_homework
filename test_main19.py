import pytest
from main19 import process_orders



def test_product_not_found():

    orders = [
        {"product": "banana", "quantity": 2}
    ]

    inventory = {
        "apple": 10
    }

    with pytest.raises(ValueError):
        process_orders(orders, inventory)



def test_not_enough_stock():

    orders = [
        {"product": "apple", "quantity": 20}
    ]

    inventory = {
        "apple": 10
    }

    with pytest.raises(ValueError):
        process_orders(orders, inventory)




def test_successful_order():

    orders = [
        {"product": "apple", "quantity": 3}
    ]

    inventory = {
        "apple": 10
    }

    result = process_orders(orders, inventory)

    assert result == orders
    assert inventory["apple"] == 7