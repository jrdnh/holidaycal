from datetime import date
from dateutil.relativedelta import relativedelta, MO
import pytest

from holidaycal.easter import EasterDelta
from holidaycal.holiday import AbstractHoliday, ListHoliday, RecurringHoliday
from holidaycal.observance import nearest_weekday


def test_abstract_holiday_dates():
    with pytest.raises(NotImplementedError):
        AbstractHoliday('holiday').dates(date(2021, 1, 1), date(2022, 1, 1), False)


def test_recurring_construction():
    with pytest.raises(ValueError):
        RecurringHoliday('Incomplete Holiday')
    with pytest.raises(ValueError):
        RecurringHoliday('Overdefined Holiday', month=1, day=1, offset=relativedelta(month=11, weekday=MO(2)))


def test_recurring_dates_absolute():

    def skip_years(dt):
        if dt.year in [2023, 2024, 2025, 2026, 2029, 2030, 2031, 2032, 2033]:
            return True
        return False

    holiday = RecurringHoliday('test', month=1, day=1, start_date=date(2022, 1, 1), end_date=date(2034, 1, 1),
                               observance=nearest_weekday, skip=skip_years)
    assert holiday.dates(date(2021, 1, 1), date(2035, 1, 1)) == \
           [date(2022, 1, 1), date(2027, 1, 1), date(2028, 1, 1), date(2034, 1, 1)]
    assert holiday.dates(date(2021, 1, 1), date(2034, 1, 1), observed=True) == \
           [date(2027, 1, 1), date(2027, 12, 31)]
    assert holiday.__repr__() == 'RecurringHoliday: test (start year=2022, end year=2034, month=1, day=1, ' \
                                 'observance=nearest_weekday, skip=skip_years)'


def test_recurring_dates_relative():

    def skip_years(dt):
        if dt.year in [2023, 2024, 2025, 2026, 2029, 2030, 2031, 2032, 2033]:
            return True
        return False

    holiday = RecurringHoliday('test', offset=relativedelta(month=1, day=1), start_date=date(2022, 1, 1),
                               end_date=date(2034, 1, 1), observance=nearest_weekday, skip=skip_years)
    assert holiday.dates(date(2021, 1, 1), date(2035, 1, 1)) == \
           [date(2022, 1, 1), date(2027, 1, 1), date(2028, 1, 1), date(2034, 1, 1)]
    assert holiday.dates(date(2021, 1, 1), date(2034, 1, 1), observed=True) == \
           [date(2027, 1, 1), date(2027, 12, 31)]
    assert holiday.__repr__() == 'RecurringHoliday: test (start year=2022, end year=2034, ' \
                                 'offset=relativedelta(month=1, day=1), observance=nearest_weekday, skip=skip_years)'


def test_recurring_dates_list():
    holiday = RecurringHoliday('test', offset=[relativedelta(month=11, weekday=MO(1)), relativedelta(days=1)],
                               start_date=date(2016, 11, 1), end_date=date(2021, 11, 2))
    assert holiday.dates(date(2015, 1, 1), date(2022, 1, 1)) == [
        date(2016, 11, 8), date(2017, 11, 7), date(2018, 11, 6), date(2019, 11, 5), date(2020, 11, 3), date(2021, 11, 2)
    ]
    assert holiday.dates(date(2015, 1, 1), date(2022, 1, 1), observed=True) == [
        date(2016, 11, 8), date(2017, 11, 7), date(2018, 11, 6), date(2019, 11, 5), date(2020, 11, 3), date(2021, 11, 2)
    ]
    assert holiday.__repr__() == 'RecurringHoliday: test (start year=2016, end year=2021, ' \
                                 'offset=[relativedelta(month=11, weekday=MO(+1)), relativedelta(days=+1)])'


def test_recurring_dates_easter():
    holiday = RecurringHoliday('test easter', offset=EasterDelta(days=1))
    assert holiday.dates(date(2016, 1, 1), date(2019, 12, 1)) == [date(2016, 3, 28), date(2017, 4, 17),
                                                                  date(2018, 4, 2), date(2019, 4, 22)]
    assert holiday.__repr__() == 'RecurringHoliday: test easter (offset=EasterDelta(days=+1))'


def test_list_holiday():
    holiday = ListHoliday('List holiday',
                          [date(2021, 1, 1), date(2021, 1, 2), date(2021, 1, 3)],
                          observance=nearest_weekday)
    assert holiday.dates(date(2021, 1, 1), date(2022, 1, 1)) == [date(2021, 1, 1), date(2021, 1, 2), date(2021, 1, 3)]
    assert holiday.dates(date(2021, 1, 1), date(2022, 1, 1), observed=True) == \
        [date(2021, 1, 1), date(2021, 1, 1), date(2021, 1, 4)]
    assert holiday.__repr__() == 'ListHoliday: List holiday (number of dates=3, observance=nearest_weekday)'
