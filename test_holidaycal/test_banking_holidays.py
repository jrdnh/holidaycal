from datetime import date
import pytest

from holidaycal.calendar import LondonBankHolidayCalendar, NYBankHolidayCalendar


@pytest.fixture
def ny_bank_holidays():
    with open('test_holidaycal/historical_holidays/newyorkbankholidays.csv', 'r', encoding='utf-8-sig') as file:
        data = file.read().splitlines()
        return [date.fromisoformat(dt) for dt in data]


@pytest.fixture
def london_bank_holidays():
    with open('test_holidaycal/historical_holidays/londonbankholidays.csv', 'r', encoding='utf-8-sig') as file:
        data = file.read().splitlines()
        return [date.fromisoformat(dt) for dt in data]


def test_ny_bank_holidays(ny_bank_holidays):
    # test that observed weekday holidays match
    holidays = NYBankHolidayCalendar().holidays(date(2000, 1, 1), date(2021, 12, 31), observed=True)
    observed_holidays = [h for h in holidays if h.weekday() < 5]
    assert observed_holidays.sort() == ny_bank_holidays.sort()


def test_london_bank_holidays(london_bank_holidays):
    # test that observed weekday holidays match
    holidays = LondonBankHolidayCalendar().holidays(date(2000, 1, 1), date(2021, 12, 31), observed=True)
    observed_holidays = [h for h in holidays if h.weekday() < 5]
    assert observed_holidays.sort() == london_bank_holidays.sort()
