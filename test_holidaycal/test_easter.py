from datetime import date
from dateutil.relativedelta import MO, relativedelta
import pytest

from holidaycal.easter import EasterDelta

# Fixtures
@pytest.fixture()
def start_date():
    return date(2021, 1, 1)


# Tests
@pytest.mark.parametrize(
    'easter_delta,expected',
    [
        (EasterDelta(), date(2021, 4, 4)),
        (EasterDelta(years=1), date(2022, 4, 4)),
        (EasterDelta(weeks=1), date(2021, 4, 11)),
        (EasterDelta(weekday=MO(-1)), date(2021, 3, 29)),
        (EasterDelta(month=11), date(2021, 11, 4))
    ]
)
def test_add(start_date, easter_delta, expected):
    assert easter_delta + start_date == start_date + easter_delta == expected
    # if other operand is not a date
    assert EasterDelta().__add__(2) == NotImplemented


@pytest.mark.parametrize(
    'easter_delta',
    [
        (EasterDelta()),
        (EasterDelta(years=1)),
        (EasterDelta(weeks=1)),
        (EasterDelta(weekday=MO(-1))),
        (EasterDelta(month=11))
    ]
)
def test_sub(start_date, easter_delta):
    with pytest.raises(TypeError):
        easter_delta - start_date


@pytest.mark.parametrize(
    'easter_delta',
    [
        (EasterDelta()),
        (EasterDelta(years=1)),
        (EasterDelta(weeks=1)),
        (EasterDelta(weekday=MO(-1))),
        (EasterDelta(month=11))
    ]
)
def test_rsub(start_date, easter_delta):
    with pytest.raises(TypeError):
        easter_delta - start_date
    # if other operand is not a date
    assert EasterDelta().__rsub__(2) == NotImplemented


def test_eq():
    assert EasterDelta(days=1) == EasterDelta(days=1)
    assert not EasterDelta(days=1) == EasterDelta(days=2)
    assert not EasterDelta(days=1) == relativedelta(days=1)


def test_ne():
    assert not EasterDelta(days=1) != EasterDelta(days=1)
    assert EasterDelta(days=1) != EasterDelta(days=2)


def test_create_from_dates():
    with pytest.raises(NotImplementedError):
        EasterDelta(dt1=date(2021, 1, 1), dt2=date(2022, 1, 1))


def test_repr():
    ed = EasterDelta(years=1, months=1, days=1,
                     year=2022, month=11, day=1)
    assert ed.__repr__() == 'EasterDelta(years=+1, months=+1, days=+1, year=2022, month=11, day=1)'


def test_hashable():
    assert hash(EasterDelta()) is not None
