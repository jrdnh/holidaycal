from datetime import date
from dateutil.relativedelta import relativedelta, MO, TH, SU
from typing import Union, List, Optional, Callable

from holidaycal.easter import EasterDelta
from holidaycal.observance import sunday_to_monday, weekend_to_monday, sunday_to_tuesday


class AbstractHoliday:
    """
    Abstract holiday class that helps with type checking (e.g. `isinstance`).
    """

    def __init__(self, name: str, observance: Optional[Callable] = None):
        self.name = name
        self._observance = observance

    def dates(self, start_date, end_date, observed):
        raise NotImplementedError


class RecurringHoliday(AbstractHoliday):
    """
    Class for creating holidays based on recurrence rules.
    """

    def __init__(self, name: str, month: int = None, day: int = None,
                 offset: Union[relativedelta, List, EasterDelta, None] = None,
                 start_date: Optional[date] = None, end_date: Optional[date] = None,
                 observance: Optional[Callable] = None, skip: Optional[Callable] = None):
        """
        Args:
            name (str): Holiday name
            offset: List of or single dateutil.relativedelta.relativedelta
            start_date (int, optional): Year of first holiday
            end_date (int, optional): Year of last holiday
            observance: Function that takes a holiday date and returns the observed date
            skip: Function that takes a holiday and returns True if that holiday should be skipped, should reference
            holiday unadjusted for observance
        """
        super(RecurringHoliday, self).__init__(name=name, observance=observance)
        if offset is None and (month is None or day is None):
            raise ValueError('Must define either an offset rule or month/day definitions ')
        if offset is not None and (month is not None or day is not None):
            raise ValueError('Cannot have both an offset and month/day definitions')
        self.month = month
        self.day = day
        self.offset = offset
        self.start_date = start_date
        self.end_date = end_date
        self._skip = skip

    def dates(self, start_date, end_date, observed: bool = False):
        """Computes the holidays dates between start and end date, inclusive.

        Args:
            start_date (datetime-like): Starting date
            end_date (datetime-like): Ending date
            observed: Whether holidays should be adjusted to observed date, defaults to False

        Returns:
            list: List of `date`
        """
        if self.start_date is not None: start_date = max(self.start_date, start_date)
        if self.end_date is not None: end_date = min(self.end_date, end_date)

        reference_dates = self._reference_dates(start_date.year - 1, end_date.year + 1)

        if self._skip is not None:
            reference_dates = [dt for dt in reference_dates if self._skip(dt) is False]

        if self._observance is not None and observed:
            reference_dates = [self._observance(dt) for dt in reference_dates]

        return [dt for dt in reference_dates if start_date <= dt <= end_date]

    def _reference_dates(self, start_year, end_year):
        year_range = range(start_year, end_year + 1)

        if self.offset is not None:
            if isinstance(self.offset, list):
                hols = [date(yr, 1, 1) for yr in year_range]
                for offset in self.offset:
                    hols = [h + offset for h in hols]
                return hols
            else:
                return [date(yr, 1, 1) + self.offset for yr in year_range]
        else:
            return [date(yr, self.month, self.day) for yr in year_range]

    def __repr__(self):
        info = []
        if self.start_date is not None:
            info.append(f'start year={self.start_date.year}')
        if self.end_date is not None:
            info.append(f'end year={self.end_date.year}')
        if self.offset is not None:
            info.append(f'offset={self.offset}')
        else:
            info.append(f'month={self.month}, day={self.day}')
        if self._observance is not None:
            info.append(f'observance={self._observance.__name__}')
        if self._skip:
            info.append(f'skip={self._skip.__name__}')

        return f'RecurringHoliday: {self.name} ({", ".join(info)})'


class ListHoliday(AbstractHoliday):
    """
    Class for creating holidays based on a pre-defined list of dates.
    """

    def __init__(self, name: str, dates: List[date], observance: Optional[Callable] = None):
        """
        Args:
            name: Name of holiday
            dates: List of datetime-like holidays
        """
        super(ListHoliday, self).__init__(name=name, observance=observance)
        self._dates = dates

    def dates(self, start_date, end_date, observed: bool = False):
        """Computes the holidays dates between start and end date, inclusive.

        Args:
            start_date (datetime-like): Starting date
            end_date (datetime-like): Ending date
            observed: Whether holidays should be adjusted to observed date, defaults to False

        Returns:
            list: List of dates
        """
        if self._observance is None or not observed:
            ref_dates = self._dates
        else:
            ref_dates = [self._observance(dt) for dt in self._dates if start_date <= dt <= end_date]

        return [dt for dt in ref_dates if start_date <= dt <= end_date]

    def __repr__(self):
        info = []
        if self._dates:
            info.append(f'number of dates={len(self._dates)}')
        if self._observance is not None:
            info.append(f'observance={self._observance.__name__}')

        return f'ListHoliday: {self.name} ({", ".join(info)})'


# New York banking holidays
# https://www.nysenate.gov/legislation/laws/GCN/24
class NYBankHolidays:
    NewYearsDay = RecurringHoliday('New Year\'s Day', month=1, day=1, observance=sunday_to_monday)
    MLKDay = RecurringHoliday('Dr. Martin Luther King, Jr. Day', offset=relativedelta(month=1, weekday=MO(3)))
    # LincolnsBirthday = RecurringHoliday('Lincoln\'s Birthday', month=2, day=12, observance=sunday_to_monday)
    WashingtonsBirthday = RecurringHoliday('Washington\'s Birthday', offset=relativedelta(month=2, weekday=MO(3)))
    MemorialDay = RecurringHoliday('Memorial Day', offset=relativedelta(month=5, weekday=MO(-1)))
    # FlagDay = RecurringHoliday('Flag Day', offset=relativedelta(month=6, weekday=SU(2)))
    Juneteenth = RecurringHoliday('Juneteenth', month=6, day=19, observance=sunday_to_monday,
                                  start_date=date(2021, 6, 19))
    IndependenceDay = RecurringHoliday('Independence Day', month=7, day=4, observance=sunday_to_monday)
    LaborDay = RecurringHoliday('Labor Day', offset=relativedelta(month=9, weekday=MO(1)))
    ColumbusDay = RecurringHoliday('Columbus Day', offset=relativedelta(month=10, weekday=MO(2)))
    # https://www.nysenate.gov/legislation/laws/ELN/8-100
    # GeneralElection = RecurringHoliday('General Election Day', offset=[relativedelta(month=11, weekday=MO(1)),
    #                                                                    relativedelta(days=1)])
    VeteransDay = RecurringHoliday('Veterans Day', month=11, day=11, observance=sunday_to_monday)
    Thanksgiving = RecurringHoliday('Thanksgiving Day', offset=relativedelta(month=11, weekday=TH(4)))
    ChristmasDay = RecurringHoliday('Christmas Day', month=12, day=25, observance=sunday_to_monday)


# London banking holidays
# https://commonslibrary.parliament.uk/bank-holidays-how-are-they-created-and-changed/
# https://www.legislation.gov.uk/ukpga/1971/80
class LondonBankHolidays:
    """London bank (statutory) and public (common law and proclamation) holidays.

    Holidays may not be correct, in particular holidays prior to 1978. The Banking and Financial Dealings
    Act 1971 and updates in 1974 and 1978 added holidays and/or changed their observed dates.
    Additionally, ad hoc holidays may be added by royal proclamation.
    """

    NewYearsDay = RecurringHoliday('New Year\'s Day', month=1, day=1, observance=weekend_to_monday)
    GoodFriday = RecurringHoliday('Good Friday', offset=EasterDelta(days=-2))
    EasterMonday = RecurringHoliday('Easter Monday', offset=EasterDelta(days=1))
    EarlyMay = RecurringHoliday('Early May Holiday', offset=relativedelta(month=5, weekday=MO(2)),
                                start_date=date(1978, 1, 1))
    EarlyMayVEAnniversary = ListHoliday('Early May Holiday / VE Day Anniversary',
                                        [date(1995, 5, 8), date(2020, 5, 8)])
    SpringHoliday = RecurringHoliday('Spring Holiday', offset=relativedelta(month=5, weekday=MO(-1)))
    SummerHoliday = RecurringHoliday('Summer Holiday', offset=relativedelta(month=8, weekday=MO(-1)))
    Christmas = RecurringHoliday('Christmas', month=12, day=25, observance=sunday_to_tuesday)
    BoxingDay = RecurringHoliday('Boxing Day', month=12, day=26, observance=weekend_to_monday)
    Jubilees = ListHoliday('Jubilee', [date(1977, 2, 6), date(1992, 1,1), date(2002, 2, 6), date(2017, 2, 6)])
