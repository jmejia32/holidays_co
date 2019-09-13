import calendar
from collections import namedtuple
from datetime import date, timedelta, datetime
_nt_holiday_stock = namedtuple("Holiday", ["day", "days_to_sum", "celebration"])

EASTER_WEEK_HOLIDAYS = [
    _nt_holiday_stock(day=-3, days_to_sum=None, celebration="Jueves Santo"),
    _nt_holiday_stock(day=-2, days_to_sum=None, celebration="Viernes Santo"),
    _nt_holiday_stock(day=39, days_to_sum=calendar.MONDAY, celebration="Ascensión del Señor"),
    _nt_holiday_stock(day=60, days_to_sum=calendar.MONDAY, celebration="Corphus Christi"),
    _nt_holiday_stock(day=68, days_to_sum=calendar.MONDAY, celebration="Sagrado Corazón de Jesús")
]

HOLIDAYS = [
    _nt_holiday_stock(day="01-01", days_to_sum=None, celebration="Año Nuevo"),
    _nt_holiday_stock(day="05-01", days_to_sum=None, celebration="Día del Trabajo"),
    _nt_holiday_stock(day="07-20", days_to_sum=None, celebration="Día de la Independencia"),
    _nt_holiday_stock(day="08-07", days_to_sum=None, celebration="Batalla de Boyacá"),
    _nt_holiday_stock(day="12-08", days_to_sum=None, celebration="Día de la Inmaculada Concepción"),
    _nt_holiday_stock(day="12-25", days_to_sum=None, celebration="Día de Navidad"),
    _nt_holiday_stock(day="01-06", days_to_sum=calendar.MONDAY, celebration="Día de los Reyes Magos"),
    _nt_holiday_stock(day="03-19", days_to_sum=calendar.MONDAY, celebration="Día de San José"),
    _nt_holiday_stock(day="06-29", days_to_sum=calendar.MONDAY, celebration="San Pedro y San Pablo"),
    _nt_holiday_stock(day="08-15", days_to_sum=calendar.MONDAY, celebration="La Asunción de la Virgen"),
    _nt_holiday_stock(day="10-12", days_to_sum=calendar.MONDAY, celebration="Día de la Raza"),
    _nt_holiday_stock(day="11-01", days_to_sum=calendar.MONDAY, celebration="Todos los Santos"),
    _nt_holiday_stock(day="11-11", days_to_sum=calendar.MONDAY, celebration="Independencia de Cartagena")
]

def next_weekday(d, weekday):
    """ https://stackoverflow.com/a/6558571 """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

def calc_easter(year):
    """ Returns Easter as a date object.

    upstream: http://code.activestate.com/recipes/576517-calculate-easter-western-given-a-year/

    :type year: integer

    :raises:
    :rtype: ValueError if year is not integer
    """
    year = int(year)
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return date(year, month, day)

def get_colombia_holidays_by_year(year):
    try:
        year = int(year)
    except ValueError:
        raise TypeError("El año debe ser un entero")

    if year < 1970 or year > 99999:
        raise ValueError("El año debe ser mayor a 1969 y menor a 100000")

    nt_holiday = namedtuple("Holiday", ["date", "celebration"])
    normal_holidays = []
    for holiday in HOLIDAYS:
        holiday_date = datetime.strptime("%s-%d" % (holiday.day, year), "%m-%d-%Y").date()
        if holiday.days_to_sum is not None and holiday_date.weekday() != holiday.days_to_sum:
            holiday_date = next_weekday(holiday_date, holiday.days_to_sum)
        normal_holidays.append(nt_holiday(date=holiday_date, celebration=holiday.celebration))

    sunday_date = calc_easter(year)
    easter_holidays = []
    for holiday in EASTER_WEEK_HOLIDAYS:
        holiday_date = sunday_date + timedelta(days=holiday.day)
        if holiday.days_to_sum is not None and holiday_date.weekday() != holiday.days_to_sum:
            holiday_date = next_weekday(holiday_date, holiday.days_to_sum)
        easter_holidays.append(nt_holiday(date=holiday_date, celebration=holiday.celebration))

    holiday_list = normal_holidays + easter_holidays
    holiday_list.sort(key=lambda holiday: holiday.date)
    return holiday_list

def is_holiday_date(d):
    if not isinstance(d, date):
        raise TypeError("Debe proporcionar un objeto tipo date")
    if isinstance(d, datetime):
        d = d.date()
    holiday_list = set([holiday.date for holiday in get_colombia_holidays_by_year(d.year)])
    return d in holiday_list
