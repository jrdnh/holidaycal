# holidaycal

*Holiday calendars for financial analysis.*

## Overview
`holidaycal` is a pure Python package for generating holidays and their observed dates. It is heavily inspired by the `pandas` holiday calendars, but it is faster and comes in a slim, single-purpose package. Additional features include an Easter offset, the ability to skip regularly scheduled holiday dates, and the concept of actual and observed dates. It has full test coverage. 

This package includes convenience calendars for New York and London banking holidays that are meant to reflect typical conventions loan documents. *While observed New York and London banking holidays beginning in 2000 are believed to be correct, there is no promise that they accurately reflect or will reflect actual banking holidays. See the license.*

## Usage

## Installation


`pip install holidaycal`

### Holidays

Holidays are the basic building block. 
* `RecurringHoliday` are either defined by a specific month and day or by a `dateutil.relativedelta.relativedelta` object which is added to the first day of the year.
* `ListHoliday` are defined by a list of specific dates.

Optionally, holidays can have an `observance` function which takes a holiday date and returns the date that it is observed. There are several built-in observance functions including `nearest_workday`, `sunday_to_monday` and `weekend_to_monday`.

Creating a holiday that occurs on the same date every year:
```python
>>> from datetime import date
>>> from holidaycal import RecurringHoliday, sunday_to_monday
>>> holiday = RecurringHoliday("New Year's Day", month=1, day=1, observance=sunday_to_monday)
>>> holiday.dates(start_date=date(2012, 1, 1), end_date=date(2017, 1, 1), observed=True)
[date(2012, 1, 2), date(2013, 1, 1), date(2014, 1, 1), date(2015, 1, 1), date(2016, 1, 1)]
```
Note that `observed=True` in the `dates` function, meaning that the method will return holidays between the start and end dates (inclusive), adjusted for their observance. In this case, any holidays that fall on a Sunday are pushed to their observed dates on the following Monday. January 1st fell on a Sunday in 2012 and 2017. If dates are adjusted for observance, the start and end dates apply to observed holidays. So, the observed holiday on 2017-01-02 is not returned even though the actual holiday on 2017-01-01 fell withing the requested time period.

Creating a holiday that occurs on a relative date:
```python
>>> from dateutil.relativedelta import MO, relativedelta
>>> holiday = RecurringHoliday("Third Monday in January (MLK Day)", offset=relativedelta(month=1, weekday=MO(3)))
>>> holiday.dates(start_date=date(2018, 1, 1), end_date=date(2021, 2, 1))
[datetime.date(2018, 1, 15), datetime.date(2019, 1, 21), datetime.date(2020, 1, 20), datetime.date(2021, 1, 18)]
```
The holiday above returns the third Monday in January which is Martin Luther King Jr. Day in the United States. 

The `EasterDelta` class is available to define holidays relative to Easter. It takes arguments similar to `relativedelta`.

### Calendars
Calendars are collections of holidays. Typically, calendars are created by defining a new `AbstractCalendar` subclass with a list of holiday `rules`.
```python
>>> from holidaycal import AbstractCalendar
>>> class MyCalendar(AbstractCalendar):
>>>     rules = [
>>>         RecurringHoliday("New Year's Day", month=1, day=1, observance=sunday_to_monday),
>>>         RecurringHoliday("MLK Day", offset=relativedelta(month=1, weekday=MO(3)))
>>>     ]
>>> MyCalendar().holidays(start_date=date(2018, 1, 1), end_date=date(2021, 1, 1), observed=True)
[datetime.date(2018, 1, 1), datetime.date(2018, 1, 15), datetime.date(2019, 1, 1), datetime.date(2019, 1, 21), datetime.date(2020, 1, 1), datetime.date(2020, 1, 20), datetime.date(2021, 1, 1)]
``` 
 
 The `.holidays` method returns the holiday dates in ascending order across rules, optionally with names and adjusted for observance.
 
 `LondonBankHolidayCalendar` and `NYBankHolidayCalendar` are built-in calendars for London and New York banking holidays, respectively. 
 