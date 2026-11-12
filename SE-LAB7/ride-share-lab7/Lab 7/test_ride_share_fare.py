
from hypothesis import given, strategies as st
import math

from ride_share_fare import parse_trip, fare_average, payable_fare


@given(st.one_of(st.text(), st.none()))
def test_parse_trip_no_crash(s):
    try:
        result = parse_trip(s)
        assert isinstance(result, tuple)
        assert len(result) == 2
        assert isinstance(result[0], str)
        assert isinstance(result[1], float)
        assert math.isfinite(result[1])
    except ValueError:
        pass


@given(st.one_of(st.text(), st.none()))
def test_fare_average_no_crash(s):
    try:
        result = fare_average(s)
        assert isinstance(result, int)
    except ValueError:
        pass


@given(st.one_of(st.text(), st.none()))
def test_payable_fare_no_crash(s):
    try:
        result = payable_fare(s)
        assert isinstance(result, float)
        assert math.isfinite(result)
        assert result >= 0
    except ValueError:
        pass
