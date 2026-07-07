import calendar
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, timedelta, datetime
from functools import reduce

@dataclass
class HolidayStock:
    celebration: str
    day: int = None
    month: int = None
    day_delta: int = None
    move_to: calendar.Day = None

@dataclass
class Holiday:
    date: date
    celebration: str

EASTER_WEEK_HOLIDAYS: tuple[HolidayStock] = (
    HolidayStock(day_delta=-3, move_to=None, celebration="Jueves Santo"),
    HolidayStock(day_delta=-2, move_to=None, celebration="Viernes Santo"),
    HolidayStock(day_delta=40, move_to=calendar.MONDAY, celebration="Ascensión del Señor"),
    HolidayStock(day_delta=60, move_to=calendar.MONDAY, celebration="Corphus Christi"),
    HolidayStock(day_delta=67, move_to=calendar.MONDAY, celebration="Sagrado Corazón de Jesús")
)

HOLIDAYS: tuple[HolidayStock] = (
    HolidayStock(month=1, day=1, move_to=None, celebration="Año Nuevo"),
    HolidayStock(month=1, day=6, move_to=calendar.MONDAY, celebration="Día de los Reyes Magos"),
    HolidayStock(month=3, day=19, move_to=calendar.MONDAY, celebration="Día de San José"),
    HolidayStock(month=5, day=1, move_to=None, celebration="Día del Trabajo"),
    HolidayStock(month=6, day=29, move_to=calendar.MONDAY, celebration="San Pedro y San Pablo"),
    # http://www.secretariasenado.gov.co/senado/basedoc/ley_2578_2026.html
    HolidayStock(month=7, day=9, move_to=calendar.MONDAY, celebration="Señora del Rosario de Chiquinquirá"),
    HolidayStock(month=7, day=20, move_to=None, celebration="Día de la Independencia"),
    HolidayStock(month=8, day=7, move_to=None, celebration="Batalla de Boyacá"),
    HolidayStock(month=8, day=15, move_to=calendar.MONDAY, celebration="La Asunción de la Virgen"),
    HolidayStock(month=10, day=12, move_to=calendar.MONDAY, celebration="Día de la Raza"),
    HolidayStock(month=11, day=1, move_to=calendar.MONDAY, celebration="Todos los Santos"),
    HolidayStock(month=11, day=11, move_to=calendar.MONDAY, celebration="Independencia de Cartagena"),
    HolidayStock(month=12, day=8, move_to=None, celebration="Día de la Inmaculada Concepción"),
    HolidayStock(month=12, day=25, move_to=None, celebration="Día de Navidad")
)

def _next_weekday(d: date, weekday: int) -> date:
    """ https://stackoverflow.com/a/6558571 """
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + timedelta(days_ahead)

def _calc_easter(year: int) -> date:
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

def _holidays_by_month(year: int) -> dict[int, list[Holiday]]:
    result = defaultdict(list)
    for holiday in HOLIDAYS:
        holiday_date = date(year, holiday.month, holiday.day)
        if holiday.move_to is not None and holiday_date.weekday() != holiday.move_to.value:
            holiday_date = _next_weekday(holiday_date, holiday.move_to.value)

        key = holiday_date.month
        result[key].append(
            Holiday(date=holiday_date, celebration=holiday.celebration)
        )

        if len(result[key]) < 2:
            continue

        result[key].sort(key=lambda holiday: holiday.date)

    sunday_date = _calc_easter(year)
    for holiday in EASTER_WEEK_HOLIDAYS:
        holiday_date = sunday_date + timedelta(days=holiday.day_delta)
        if holiday.move_to is not None and holiday_date.weekday() != holiday.move_to:
            holiday_date = _next_weekday(holiday_date, holiday.move_to.value)

        key = holiday_date.month
        result[key].append(
            Holiday(date=holiday_date, celebration=holiday.celebration)
        )

        if len(result[key]) < 2:
            continue

        result[key].sort(key=lambda holiday: holiday.date)

    return dict(result)

def get_colombia_holidays_by_year(year: int) -> list[Holiday]:
    try:
        year = int(year)
    except ValueError:
        raise TypeError("El año debe ser un entero")

    if year < 1970 or year > 99999:
        raise ValueError("El año debe ser mayor a 1969 y menor a 100000")

    holiday_d = _holidays_by_month(year)
    keys = sorted(holiday_d.keys())
    return list(
        reduce(lambda result, k: result + holiday_d[k], keys, [])
    )

def is_holiday_date(d: datetime | date):
    if not isinstance(d, date):
        raise TypeError("Debe proporcionar un objeto tipo date")
    if isinstance(d, datetime):
        d = d.date()

    holiday_d = _holidays_by_month(d.year)
    if d.month not in holiday_d:
        return False

    return next((True for i in holiday_d[d.month] if i.date == d), False)
