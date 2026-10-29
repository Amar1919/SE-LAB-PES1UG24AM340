
import pytest
from customs_duty import duty_rate, total_duty, clearance_channel


def test_duty_rate_all_branches():
    with pytest.raises(ValueError):
        duty_rate("weapons", "US")

    with pytest.raises(ValueError):
        duty_rate("narcotics", "US")

    assert duty_rate("electronics", "FTA") == 0.10
    assert duty_rate("electronics", "US") == 0.20

    assert duty_rate("clothing", "FTA") == 0.05
    assert duty_rate("clothing", "US") == 0.12

    assert duty_rate("books", "US") == 0
    assert duty_rate("furniture", "US") == 0.15


def test_total_duty_all_branches():
    with pytest.raises(ValueError):
        total_duty("electronics", -1, "US", False)

    # Gift: value at or below 5000
    assert total_duty("electronics", 5000, "US", True) == 0

    # Gift: value above 5000, with minimum duty applied
    assert total_duty("clothing", 5100, "FTA", True) == 50

    # Non-gift: value at or below 1000
    assert total_duty("electronics", 1000, "US", False) == 0

    # Non-gift: value above 1000, minimum-duty condition false
    assert total_duty("electronics", 2000, "US", False) == 400

    # Zero duty makes the minimum-duty condition false
    assert total_duty("books", 2000, "US", False) == 0


def test_clearance_all_branches():
    # Prohibited category
    assert clearance_channel(500, "weapons", True) == "refuse"

    # Value above 100000
    assert clearance_channel(100001, "electronics", True) == "inspect"

    # Value at 100000 does not satisfy the first value condition
    assert clearance_channel(100000, "electronics", True) == "green"

    # Above 20000 without documents
    assert clearance_channel(25000, "electronics", False) == "inspect"

    # Above 20000 with documents
    assert clearance_channel(25000, "electronics", True) == "green"

    # Value at 20000
    assert clearance_channel(20000, "books", False) == "green"
