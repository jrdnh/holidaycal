from datetime import date
import pytest

from holidaycal.calendar import AbstractCalendar
from holidaycal.holiday import ListHoliday, RecurringHoliday
from holidaycal.observance import nearest_weekday


@pytest.fixture
def empty_calendar():
    return AbstractCalendar()


@pytest.fixture
def calendar_from_init():
    holiday = RecurringHoliday('New Holiday', month=1, day=8, observance=nearest_weekday)
    return AbstractCalendar('Calendar from init', rules=[holiday])


@pytest.fixture
def calendar_from_class():

    class CalendarFromClass(AbstractCalendar):
        rules = [
            RecurringHoliday('New Holiday', month=1, day=8, observance=nearest_weekday),
            ListHoliday('List Holiday', [date(2021, 1, 15), date(2021, 2, 14)], observance=nearest_weekday)
        ]

    return CalendarFromClass


def test_calendar_repr(empty_calendar, calendar_from_init, calendar_from_class):
    assert empty_calendar.__repr__() == 'Calendar: AbstractCalendar (0 holiday rules)'
    assert calendar_from_init.__repr__() == 'Calendar: Calendar from init (1 holiday rules)'
    assert calendar_from_class().__repr__() == 'Calendar: CalendarFromClass (2 holiday rules)'


def test_holiday_names(empty_calendar, calendar_from_init, calendar_from_class):
    assert empty_calendar.holiday_names() == []
    assert calendar_from_init.holiday_names() == ['New Holiday']
    assert calendar_from_class().holiday_names() == ['New Holiday', 'List Holiday']


def test_holidays(empty_calendar, calendar_from_init, calendar_from_class):
    with pytest.raises(ValueError):
        assert empty_calendar.holidays(date(2021, 1, 1), date(2024, 1, 1))
    assert calendar_from_init.holidays(date(2021, 1, 1), date(2024, 1, 1)) == [
        date(2021, 1, 8), date(2022, 1, 8), date(2023, 1, 8)
    ]
    assert calendar_from_class().holidays(date(2021, 1, 1), date(2024, 1, 1)) == [
        date(2021, 1, 8), date(2021, 1, 15), date(2021, 2, 14), date(2022, 1, 8), date(2023, 1, 8)
    ]


def test_holidays_with_names(empty_calendar, calendar_from_init, calendar_from_class):
    with pytest.raises(ValueError):
        assert empty_calendar.holidays(date(2021, 1, 1), date(2024, 1, 1), names=True)
    assert calendar_from_init.holidays(date(2021, 1, 1), date(2024, 1, 1), names=True) == [
        ('New Holiday', date(2021, 1, 8)), ('New Holiday', date(2022, 1, 8)), ('New Holiday', date(2023, 1, 8))
    ]
    assert calendar_from_class().holidays(date(2021, 1, 1), date(2024, 1, 1), True) == [
        ('New Holiday', date(2021, 1, 8)), ('List Holiday', date(2021, 1, 15)), ('List Holiday', date(2021, 2, 14)),
        ('New Holiday', date(2022, 1, 8)), ('New Holiday', date(2023, 1, 8))
    ]


def test_holidays_observed(empty_calendar, calendar_from_init, calendar_from_class):
    with pytest.raises(ValueError):
        assert empty_calendar.holidays(date(2021, 1, 1), date(2024, 1, 1), observed=True)
    assert calendar_from_init.holidays(date(2021, 1, 1), date(2024, 1, 1), observed=True) == [
        date(2021, 1, 8), date(2022, 1, 7), date(2023, 1, 9)
    ]
    assert calendar_from_class().holidays(date(2021, 1, 1), date(2024, 1, 1), observed=True) == [
        date(2021, 1, 8), date(2021, 1, 15), date(2021, 2, 15), date(2022, 1, 7), date(2023, 1, 9)
    ]
