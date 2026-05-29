
from collections.abc import Iterable
from datetime import date
from enum import Enum
from typing import Union, Optional,Tuple

class DateFormat(str, Enum):
    DDMMYYYY = "%d/%m/%Y"  # 16/09/2025
    YYYYMMDD = "%Y-%m-%d"  # 2025-09-16
    MMDDYYYY = "%m/%d/%Y" # 09/16/2025
    DDMMYYYY_DASH = "%d-%m-%Y"  # 16-09-2025
    LONG = "%B %d, %Y"  # September 16, 2025
    SHORT_MONTH = "%d %b %Y"  # 16 Sep 2025

def _normalize_option_texts(option_texts: Optional[Union[str, Iterable]]) -> list[str]:
    if option_texts is None:
        return []
    if isinstance(option_texts, str):
        parts = [p.strip() for p in option_texts.split(",")] if "," in option_texts else [option_texts.strip()]
        return [p for p in parts if p]
    out = []
    for x in option_texts:
        s = ("" if x is None else str(x)).strip()
        if s:
            out.append(s)
    return out


def split_date(date_str: str, default_year: Optional[int] = None) -> Tuple[Optional[int], int, Optional[int]]:
    """
    Parse chuỗi ngày tháng linh hoạt:
    - dd/mm/yyyy (10/09/2025)
    - yyyy-mm-dd (2025-09-10)
    - September 2025 / Sep 2025
    - 10 September / Sep 10

    Trả về tuple: (day, month, year)
    Nếu không có year -> dùng default_year (hoặc year hiện tại)
    Nếu không có day -> trả về None
    """
    if default_year is None:
        default_year = datetime.today().year

    formats = [
        "%d/%m/%Y",  # 10/09/2025
        "%m/%d/%Y", # 09/10/2025
        "%Y-%m-%d",  # 2025-09-10
        "%B %Y",     # September 2025
        "%b %Y",     # Sep 2025
        "%d %B",     # 10 September
        "%b %d"      # Sep 10
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            year = dt.year if "%Y" in fmt else default_year
            day = dt.day if "%d" in fmt else None
            return day, dt.month, year
        except ValueError:
            continue

    raise ValueError(f"Unsupported date format: {date_str}")

def split_month_year(header_text: str) -> Tuple[int, int]:
    """
    Parse calendar header:
    - September 2025
    - Sep 2025
    """
    for fmt in ("%B %Y", "%b %Y"):
        try:
            dt = datetime.strptime(header_text.strip(), fmt)
            return dt.month, dt.year
        except ValueError:
            continue

    raise ValueError(f"Invalid month-year header: {header_text}")




from datetime import datetime

from typing import Union

def parse_date(date_str: str, fmt: Union[DateFormat, str]) -> datetime:
    if isinstance(fmt, DateFormat):
        return datetime.strptime(date_str.strip(), fmt.value)
    return datetime.strptime(date_str.strip(), fmt)

def format_date(date_object:datetime|date,out_format:str)->str:
    """
    Format date/datetime into string based on explicit format.
    :param date_object:
    :param out_format:
    :return:
    """
    if not isinstance(date_object, (date, datetime)):
        raise TypeError("format_date expects a datetime object")
    return date_object.strftime(out_format)

def convert_date(
    date_input: str | date | datetime,
    in_format: str,
    out_format: str
) -> str:
    """
    Convenience helper.
    NOT for date comparison logic.
    Use parse_date() for assertions.
    """
    if isinstance(date_input, (date, datetime)):
        return date_input.strftime(out_format)

    date_obj = parse_date(date_input, in_format)
    return format_date(date_obj, out_format)
