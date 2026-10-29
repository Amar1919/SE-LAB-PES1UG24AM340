
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


# Duty rate tests
def test_prohibited_weapons():
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("weapons", "US")


def test_prohibited_narcotics():
    with pytest.raises(ValueError, match="prohibited item"):
        duty_rate("narcotics", "US")


def test_electronics_fta():
    assert duty_rate("electronics", "FTA") == 0.10


def test_electronics_non_fta():
    assert duty_rate("electronics", "US") == 0.20


def test_clothing_fta():
    assert duty_rate("clothing", "FTA") == 0.05


def test_clothing_non_fta():
    assert duty_rate("clothing", "US") == 0.12


def test_books_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_other_category():
    assert duty_rate("furniture", "US") == 0.15


# Total duty tests
def test_negative_value():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("electronics", -100, "US", False)


def test_gift_under_limit():
    assert total_duty("electronics", 3000, "US", True) == 0


def test_gift_at_limit():
    assert total_duty("electronics", 5000, "US", True) == 0


def test_gift_above_limit():
    assert total_duty("electronics", 6000, "US", True) == 200


def test_non_gift_under_limit():
    assert total_duty("electronics", 500, "US", False) == 0


def test_non_gift_at_limit():
    assert total_duty("electronics", 1000, "US", False) == 0


def test_minimum_duty_boundary():
    assert total_duty("clothing", 1001, "FTA", False) == pytest.approx(50.05)


def test_normal_duty_calculation():
    assert total_duty("electronics", 2000, "US", False) == 400


def test_zero_duty_on_books():
    assert total_duty("books", 2000, "US", False) == 0


# Clearance channel tests
def test_clearance_prohibited_item():
    assert clearance_channel(500, "weapons", True) == "refuse"


def test_clearance_high_value():
    assert clearance_channel(100001, "electronics", True) == "inspect"


def test_clearance_high_value_without_documents():
    assert clearance_channel(25000, "electronics", False) == "inspect"


def test_clearance_high_value_with_documents():
    assert clearance_channel(25000, "electronics", True) == "green"


def test_clearance_low_value():
    assert clearance_channel(5000, "books", False) == "green"
