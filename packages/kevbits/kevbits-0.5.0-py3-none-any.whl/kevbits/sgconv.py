"""
Float to sexagesimal number conversion routines.
"""

from typing import Optional, Any
import re
import math


ftosg_format_rx = re.compile(r"([+\- ]?)(0?)(\d*)/(\D?)(\d*)/(\d*)")


class SgconvError(Exception):
    pass


def sgtof(s: str) -> float:
    """
    sgtof(string) --> float
    Sexagesimal to float number conversion routine.
    E.g. "-10:20:30:40.567" --> -10.341854476851852
    """
    s = s.strip().replace(":", " ")
    t = [float(p) for p in s.split()]
    result = 0.0
    for x in reversed(t):
        result = abs(x) + result / 60.0
    if s[0] == "-":
        result = -result
    return result


def ftosg_parse_format(fmt: Optional[str] = None) -> dict[str, int | str]:
    """
    format_spec ::=  [sign][0][width]/[separator][groups]/[precision]
    sign        ::=  "+" | "-" | " "
    width       ::=  integer
    separator   ::=  character
    groups     ::=  integer
    precision   ::=  integer

    The sign option can be one of the following:
    '+'	indicates that a sign should be used for both positive as well as negative numbers.
    '-'	indicates that a sign should be used only for negative numbers (this is the default behavior).
    ' '	indicates that a leading space should be used on positive numbers, and a minus sign on negative numbers.

    width is a decimal integer defining the minimum number of the digits in the 1st sexagesimal group (not
    including sign). If not specified, then the field width will be determined by the content. Preceding the
    width field by a zero ('0') character enables sign-aware zero-padding.

    separator is a character which is inserted between sexagesimal groups (defaults to colon sign ':').

    groups is a decimal integer defining the number of sexagesimal groups (defaults to 3)

    precision is a decimal number indicating how many digits should be displayed after the decimal point for the
    last sexagesimal group (defaults to 2).

    Examples:
    '+02/:3/1'  -->  '+01:23:45.6'
    '+2/ 3/2'   -->  ' +1 23 45.60'
    ' 2/2/0'    -->  '  1:24'
    '2/2/0'     -->  ' 1:24'
    """
    if fmt in (None, ""):
        fmt = "//"

    try:
        m = ftosg_format_rx.match(fmt)
        assert m is not None
        sign, fillchar, width, separator, groups, precision = m.groups()
    except Exception as exc:
        raise SgconvError(f'ftosg: bad format string: "{fmt}"') from exc

    if sign == "":
        sign = "-"
    if fillchar == "":
        fillchar = " "
    if width == "":
        width = "0"
    if separator == "":
        separator = ":"
    if groups == "":
        groups = "3"
    if precision == "":
        precision = "2"
    return {
        "sign": sign,
        "fillchar": fillchar,
        "width": int(width),
        "separator": separator,
        "groups": int(groups),
        "precision": int(precision),
    }


def ftosg_from_opts(
    value: float,
    groups: int = 3,
    sign: str | bool = "-",
    width: int = 0,
    precision: int = 2,
    separator: str = ":",
    fillchar: str = " ",
) -> str:
    """
    ftosg(float) --> string
    Float to sexagesimal number conversion routine.
    E.g. -10.341854476851852 --> "-10:20:30:40.567"

    2018-09: Change sign option valid values (was True/False):
    '+'	indicates that a sign should be used for both positive as well as negative numbers.
    '-'	indicates that a sign should be used only for negative numbers (this is the default behavior).
    ' '	indicates that a leading space should be used on positive numbers, and a minus sign on negative numbers.

    2018-09: Add fillchar option to pad 1st group to the required width.
    """
    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-locals

    # convert sign option from old-style True/False
    if sign is True:
        sign = "+"
    if sign is False:
        sign = "-"

    minus = value < 0
    value = abs(value)

    precision = max(precision, 0)
    precision = min(precision, 10)

    frac, intp = math.modf(value)
    t = [intp]
    for i in range(groups - 1):
        frac, d = math.modf(frac * 60.0)
        t.append(d)

    # processing rounding...
    fracmul = math.pow(10, precision)  # 1, 10, 100, ...
    frac = math.floor(frac * fracmul + 0.5)
    if frac >= fracmul:
        frac = 0.0
        t[-1] += 1.0
    for i in range(len(t) - 1, 0, -1):
        if t[i] >= 60.0:
            t[i] = 0.0
            t[i - 1] += 1.0

    if minus:
        signstr = "-"
    else:
        signstr = sign if sign in ("+", " ") else ""

    numstr = str(int(t[0]))
    fillstr = fillchar * (width - len(numstr))

    if fillchar == "0":
        result = signstr + fillstr + numstr
    else:
        result = fillstr + signstr + numstr

    for i in range(1, len(t)):
        result += separator + f"{int(t[i]):02d}"

    if precision:
        result += f".{int(frac):0{precision}d}"
    return result


def ftosg(value: float, fmt: Optional[str] = None, **options: Any) -> str:
    """
    ftosg(float, string) --> string
    Float to sexagesimal number conversion routine.
    See ftosg_parse_format() for format string description.
    E.g. ftosg(1.396, '+02/:3/1') --> '+01:23:45.6'
    """
    if fmt is not None:
        assert not options
        options = ftosg_parse_format(fmt)
    return ftosg_from_opts(value, **options)


rx_sg6 = re.compile(r"^([-+]?)(\d\d)(\d\d)(\d\d)((?:\.\d*)?)$")


def sg6_prettify(s: str) -> str:
    """
    Considering input string as a sexagesimal number in the form
    [sign]DDMMSS[.SSS] (the sign and fractional part are optional)
    convert it to the string with delimiters (colons): [sign]DD:MM:SS[.SSS]
    Example: '-284321.3' --> '-28:43:21.3'
    """
    m = rx_sg6.match(s)
    if m is None:
        raise SgconvError(f"sg6_prettify: bad input: {s}")
    return "{}{}:{}:{}{}".format(*m.groups())  # pylint: disable=consider-using-f-string
