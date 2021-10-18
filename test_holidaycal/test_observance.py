from datetime import date

from holidaycal.observance import nearest_weekday, saturday_to_friday, sunday_to_monday, \
    weekend_to_friday, weekend_to_monday, sunday_to_tuesday


def test_nearest_weekday():
    assert nearest_weekday(date(2021, 9, 30)) == date(2021, 9, 30)  # Thursday
    assert nearest_weekday(date(2021, 10, 2)) == date(2021, 10, 1)  # Sat to Fri
    assert nearest_weekday(date(2021, 10, 3)) == date(2021, 10, 4)  # Sun to Mon


def test_saturday_to_friday():
    assert saturday_to_friday(date(2021, 9, 30)) == date(2021, 9, 30)  # Thursday
    assert saturday_to_friday(date(2021, 10, 2)) == date(2021, 10, 1)  # Sat to Fri
    assert saturday_to_friday(date(2021, 10, 3)) == date(2021, 10, 3)  # Sun


def test_sunday_to_monday():
    assert sunday_to_monday(date(2021, 9, 30)) == date(2021, 9, 30)  # Thursday
    assert sunday_to_monday(date(2021, 10, 2)) == date(2021, 10, 2)  # Sat
    assert sunday_to_monday(date(2021, 10, 3)) == date(2021, 10, 4)  # Sun to Mon


def test_weekend_to_monday():
    assert weekend_to_monday(date(2021, 9, 30)) == date(2021, 9, 30)  # Thursday
    assert weekend_to_monday(date(2021, 10, 2)) == date(2021, 10, 4)  # Sat to Mon
    assert weekend_to_monday(date(2021, 10, 3)) == date(2021, 10, 4)  # Sun to Mon


def test_weekend_to_friday():
    assert weekend_to_friday(date(2021, 9, 30)) == date(2021, 9, 30)  # Thursday
    assert weekend_to_friday(date(2021, 10, 2)) == date(2021, 10, 1)  # Sat to Fri
    assert weekend_to_friday(date(2021, 10, 3)) == date(2021, 10, 1)  # Sun to Fri


def test_sunday_to_tuesday():
    assert sunday_to_tuesday(date(2021, 9, 30)) == date(2021, 9, 30)  # Thursday
    assert sunday_to_tuesday(date(2021, 10, 2)) == date(2021, 10, 2)  # Sat
    assert sunday_to_tuesday(date(2021, 10, 3)) == date(2021, 10, 5)  # Sun to Tuesday
    assert sunday_to_tuesday(date(2021, 10, 4)) == date(2021, 10, 4)  # Monday
