import pytest
from service_body_test import Order


@pytest.fixture
def sample_items():
    return [
        {'name': 'Laptop', 'price': 1000, 'quantity': 1},
        {'name': 'Mouse', 'price': 50, 'quantity': 2},
        {'name': 'Keyboard', 'price': 100, 'quantity': 1}
    ]

@pytest.fixture
def empty_order():
    return Order(id=999, items=[])

@pytest.fixture
def order(sample_items):
    return Order(id=1, items=sample_items)



def test_total_calculation(order):
    """Перевірка коректності підрахунку загальної суми."""
    
    assert order.total() == 1200

def test_total_empty(empty_order):
    """Перевірка total для порожнього списку (має бути 0)."""
    assert empty_order.total() == 0

def test_total_zero_quantity():
    """Перевірка, якщо кількість товару дорівнює 0."""
    items = [{'name': 'Air', 'price': 100, 'quantity': 0}]
    order = Order(2, items)
    assert order.total() == 0



def test_most_expensive_item(order):
    """Перевірка знаходження найдорожчого товару."""
    expensive = order.most_expensive()
    assert expensive['name'] == 'Laptop'
    assert expensive['price'] == 1000

def test_most_expensive_duplicate():
    """Перевірка, якщо є два товари з однаковою максимальною ціною."""
    items = [
        {'name': 'Item A', 'price': 500, 'quantity': 1},
        {'name': 'Item B', 'price': 500, 'quantity': 1}
    ]
    order = Order(3, items)

    assert order.most_expensive()['name'] == 'Item A'

def test_most_expensive_empty_raises_error(empty_order):
    """
    Критичний тест: max() на порожньому списку викликає ValueError.
    Ми очікуємо цю поведінку, оскільки клас не обробляє це окремо.
    """
    with pytest.raises(ValueError):
        empty_order.most_expensive()


def test_apply_discount_valid(order):
    """Перевірка застосування коректної знижки (10%)."""
   
    order.apply_discount(10)
    
    assert order.items[0]['price'] == 900
    assert order.items[1]['price'] == 45
    assert order.items[2]['price'] == 90
    
    
    assert order.total() == 1080

def test_apply_discount_zero_percent(order):
    """Знижка 0% не повинна змінювати ціни."""
    order.apply_discount(0)
    assert order.total() == 1200

def test_apply_discount_hundred_percent(order):
    """Знижка 100% повинна робити товари безкоштовними."""
    order.apply_discount(100)
    assert order.total() == 0
    for item in order.items:
        assert item['price'] == 0

@pytest.mark.parametrize("invalid_percent", [-1, 101, -0.01, 100.1])
def test_apply_discount_invalid_raises_error(order, invalid_percent):
    """Перевірка викиду помилки для невалідних відсотків (<0 або >100)."""
    with pytest.raises(ValueError, match="Invalid discount"):
        order.apply_discount(invalid_percent)



def test_repr_format(order):
    """Перевірка рядкового представлення об'єкта."""
   
    expected_str = "<Order 1: 3 items>"
    assert repr(order) == expected_str

def test_repr_empty(empty_order):
    """Перевірка repr для порожнього замовлення."""
    expected_str = "<Order 999: 0 items>"
    assert repr(empty_order) == expected_str