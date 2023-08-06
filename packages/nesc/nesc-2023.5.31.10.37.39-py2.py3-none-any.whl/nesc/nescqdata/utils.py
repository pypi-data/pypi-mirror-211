import calendar
import datetime
import re
from . import selfException


def check_year_month(year_month):
    """
    校验年月YYYYmm
    :param year_month: -->str
    :return: None
    """
    reg = re.compile('^(19|20)\d{2}(0[1-9]|1[0-2])$')
    if not reg.match(year_month):
        raise selfException.FormatError(f"Illegal year month {year_month}")


def check_date(date):
    """
    校验日期格式YYYYmmdd
    :param date: str
    :return: None
    """
    reg = re.compile('^((((19|20)\d{2})(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(((19|20)\d{2})(0[13578]|1[02])31)|'
                     '(((19|20)\d{2})02(0[1-9]|1\d|2[0-8]))|((((19|20)([13579][26]|[2468][048]|0[48]))|'
                     '(2000))0229))$')
    if not reg.match(date):
        raise selfException.FormatError(f"Illegal date {date}")


def check_time(time):
    """
    校验时间的格式YYYYmmdd HHMMSS
    :param time: str
    :return: None
    """
    reg = re.compile('^((((19|20)\d{2})(0[13-9]|1[012])(0[1-9]|[12]\d|30))|(((19|20)\d{2})(0[13578]|1[02])31)|'
                     '(((19|20)\d{2})02(0[1-9]|1\d|2[0-8]))|((((19|20)([13579][26]|[2468][048]|0[48]))|'
                     '(2000))0229))\s' + '(([0-1][0-9])|(2[0-3]))([0-5][0-9])([0-5][0-9])$')
    if not reg.match(time):
        raise selfException.FormatError(f"Illegal time {time}")


def valid_month(year_month, today=None):
    """
    校验时间比当前时间小
    :param year_month:
    :param today:
    :return:
    """
    if today is None:
        today = datetime.datetime.now()
    year = today.year
    month = today.month
    if year < int(year_month[:4]):
        raise selfException.FutureTimeError(f"Future year {year_month[:4]}")
    if year == int(year_month[:4]) and month < int(year_month[4:]):
        raise selfException.FutureTimeError(f"Future month {int(year_month[4:6])}")
    return True


def valid_date(date):
    """
    校验日期，不允许比当前时间大
    :param date: str 形如YYYYmmdd
    :return:
    """
    date = datetime.datetime.strptime(date, '%Y%m%d').date()
    today = datetime.date.today()
    if date > today:
        raise selfException.FutureTimeError(f"Future date {date}")
    return True


def valid_time(start_time, end_time):
    """
    校验时间 start_time比end_time小，且end_time比当前时间小
    :param start_time: 开始时间 --> str 形如YYYYmmdd HHMMSS
    :param end_time: 结束时间 --> str 形如YYYYmmdd HHMMSS
    :return: None
    """
    start_time = datetime.datetime.strptime(start_time, '%Y%m%d %H%M%S')
    end_time = datetime.datetime.strptime(end_time, '%Y%m%d %H%M%S')
    if end_time < start_time:
        raise selfException.InvalidTypeError("End time must be later than start time.")
    if end_time > datetime.datetime.now():
        raise selfException.InvalidTypeError(f"Future end time {end_time}")


def get_year_month_and_day(time):
    """
    :param time: like YYYYmmdd HHMMSS
    :return: tuple(year_month, day, time)
    """
    return time[:6], time[:8], time[9:15]


def get_date_iter(start_date, end_date):
    """
    获取指定时间段内的日期
    :param start_date: 起始时间 --> str YYYYmmdd
    :param end_date: 结束时间 --> str YYYYmmdd
    :return: iter
    """
    dt = datetime.datetime.strptime(start_date, '%Y%m%d')
    date = start_date[:]
    yield date
    while date < end_date:
        dt = dt + datetime.timedelta(days=1)
        date = dt.strftime("%Y%m%d")
        yield date


def get_month_iter(start_month, end_month):
    """
    获取时间段内的月份
    :param start_month: 开始月份 --> str YYYYmm
    :param end_month: 结束月份 --> str YYYYmm
    :return: iter
    """
    dt = datetime.datetime.strptime(start_month, '%Y%m')
    month = start_month[:]
    yield month
    while month < end_month:
        dt = dt + datetime.timedelta(days=calendar.monthrange(dt.year, dt.month)[1])
        month = dt.strftime("%Y%m")
        yield month


def get_hdfs_file_path(dfs, file_path):
    """
    获取带协议头的hdfs路径
    :param dfs: hdfs连接
    :param file_path: 目录路径
    :return: 文件路径列表，若为空则返回[]
    """
    hdfs_file_path = dfs.ls(file_path)
    if not hdfs_file_path:
        return []
    else:
        if "hdfs://" in hdfs_file_path[0]:
            return hdfs_file_path
        else:
            return [dfs.info(path)["path"] for path in hdfs_file_path]


if __name__ == '__main__':
    # valid_month("202202")
    # print(check_year_month("202102"))
    # print(valid_date("20220105"))
    # print(valid_month("202202"))
    # print(check_time("20280301 093000000"))
    # print(valid_time(start_time="20220103 093000000", end_time="20220104 154200000"))
    # print(get_year_month_and_day("20220103 093000000"))
    # for i in get_date_iter("20211213", "20220104"):
    #     print(i)
    for i in get_month_iter("202012", "202202"):
        print(i)
