from datetime import date
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta


class EasterDelta:
    """Class for Easter-based date offsets.

    `dateutil.relativedelta.relativedelta`-like object that applies the specified offset relative to Easter.
    Uses `relativedelta` and `dateutil.easter` to find Eastern for the applicable year.
    The Easter offset is applied prior to any other offsets. Adding to a datetime object does not preserve time.

    Accepts the same arguments as `relativedelta`, except for creating an instance from two dates.
    """

    def __init__(self, method=3, **kwargs):
        super(EasterDelta, self).__init__()
        if 'dt1' in kwargs.keys() or 'dt2' in kwargs.keys():
            raise NotImplementedError('Cannot create an EasterDelta object from two dates')
        self.relativedelta = relativedelta(**kwargs)
        self.method = method

    def __add__(self, other):
        if not isinstance(other, date):
            return NotImplemented
        ret = easter(other.year, method=self.method)

        return ret + self.relativedelta

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        # in case other object defines __rsub__
        return NotImplemented

    def __rsub__(self, other):
        return NotImplemented

    def __eq__(self, other):
        if not isinstance(other, EasterDelta):
            return NotImplemented
        return (self.relativedelta == other.relativedelta) and (self.method == other.method)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.method, self.relativedelta))

    def __repr__(self):
        l = []
        for attr in ["years", "months", "days", "leapdays",
                     "hours", "minutes", "seconds", "microseconds"]:
            value = getattr(self.relativedelta, attr)
            if value:
                l.append("{attr}={value:+g}".format(attr=attr, value=value))
        for attr in ["year", "month", "day", "weekday",
                     "hour", "minute", "second", "microsecond"]:
            value = getattr(self.relativedelta, attr)
            if value is not None:
                l.append("{attr}={value}".format(attr=attr, value=repr(value)))
        return "{classname}({attrs})".format(classname=self.__class__.__name__,
                                             attrs=", ".join(l))
