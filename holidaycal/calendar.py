from typing import List, Optional

from holidaycal.holiday import AbstractHoliday, LondonBankHolidays, NYBankHolidays


class AbstractCalendar:
    """
    Abstract object to create a calendar with a list of holiday rules.
    """

    rules: List[AbstractHoliday] = []

    def __init__(self, name: Optional[str] = None,
                 rules: Optional[List[AbstractHoliday]] = None):
        """Base calendar object.

        Initializes a calendar with holidays. Normally the class defines the list of holiday rules.

        Args:
            name: Name of the calendar, defaults to class name
            rules: Holiday or list of Holiday objects
        """
        super().__init__()
        if name is None:
            name = type(self).__name__
        self.name = name
        if rules is not None:
            self.rules = rules

    def holidays(self, start_date, end_date, names=False, observed=False):
        """Returns the holidays between start_date and end_date.

        Returns the holidays between start_date and end_date, inclusive, optionally with holiday names.
        If observed is True, adjusts holidays to observed weekday dates.
        Args:
            start_date (datetime-like): Starting date
            end_date (datetime-like): Ending date
            names (bool): If True, return
            observed (bool): Observed holidays, default True

        Returns:
            list: List of dates or (date, holiday name)
        """
        if len(self.rules) == 0:
            raise ValueError('Calendar must have holiday rules.')

        holidays = [(r.name, h) for r in self.rules for h in r.dates(start_date, end_date, observed)]
        holidays.sort(key=lambda h: h[1])

        if names is False:
            holidays = [h[1] for h in holidays]

        return holidays

    def holiday_names(self):
        """Returns the names of the holiday rules in the calendar."""
        return [h.name for h in self.rules]

    def __repr__(self):
        num_rules = len(self.rules) if self.rules else 0
        return f'Calendar: {self.name} ({num_rules} holiday rules)'


class NYBankHolidayCalendar(AbstractCalendar):

    rules = [
        NYBankHolidays.NewYearsDay,
        NYBankHolidays.MLKDay,
        # NYBankHolidays.LincolnsBirthday,
        NYBankHolidays.WashingtonsBirthday,
        NYBankHolidays.MemorialDay,
        # NYBankHolidays. FlagDay,
        NYBankHolidays.Juneteenth,
        NYBankHolidays.IndependenceDay,
        NYBankHolidays.LaborDay,
        NYBankHolidays.ColumbusDay,
        # NYBankHolidays.GeneralElection,
        NYBankHolidays.VeteransDay,
        NYBankHolidays.Thanksgiving,
        NYBankHolidays.ChristmasDay
    ]


class LondonBankHolidayCalendar(AbstractCalendar):

    rules = [
        LondonBankHolidays.NewYearsDay,
        LondonBankHolidays.GoodFriday,
        LondonBankHolidays.EasterMonday,
        LondonBankHolidays.EarlyMay,
        LondonBankHolidays.EarlyMayVEAnniversary,
        LondonBankHolidays.SpringHoliday,
        LondonBankHolidays.SummerHoliday,
        LondonBankHolidays.Christmas,
        LondonBankHolidays.BoxingDay,
        LondonBankHolidays.Jubilees
    ]
