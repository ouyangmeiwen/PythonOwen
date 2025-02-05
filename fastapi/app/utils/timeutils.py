from datetime import datetime, timedelta
import pytz
class TimeUtils:
    @staticmethod
    def get_current_time():
        """获取当前时间（处理时区）"""
        # 获取 UTC 时间
        utc_now = datetime.now(pytz.utc)
        # 将 UTC 时间转换为本地时区
        local_now = utc_now.astimezone(pytz.timezone("Asia/Shanghai"))
        return local_now

    @staticmethod
    def format_time(dt, fmt="%Y-%m-%d %H:%M:%S"):
        """格式化时间"""
        return dt.strftime(fmt)

    @staticmethod
    def add_days(dt, days):
        """在给定的时间上增加天数"""
        return dt + timedelta(days=days)

    @staticmethod
    def time_difference(start_time, end_time):
        """计算时间差"""
        return (end_time - start_time).total_seconds()

    @staticmethod
    def subtract_days(dt, days):
        """在给定的时间上减少天数"""
        return dt - timedelta(days=days)

    @staticmethod
    def parse_time(time_str, fmt="%Y-%m-%d %H:%M:%S"):
        """将字符串解析为时间"""
        return datetime.strptime(time_str, fmt)

    @staticmethod
    def is_past(dt):
        """判断时间是否在当前时间之前"""
        return dt < datetime.now()

    @staticmethod
    def get_day_of_week(dt):
        """获取时间的星期几"""
        return dt.strftime("%A")  # 返回星期几的名称，如"Monday"

    @staticmethod
    def get_start_of_day(dt):
        """获取当天的起始时间（00:00:00）"""
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_end_of_day(dt):
        """获取当天的结束时间（23:59:59）"""
        return dt.replace(hour=23, minute=59, second=59, microsecond=999999)

    @staticmethod
    def get_time_in_seconds(dt):
        """将时间转换为从午夜开始的秒数"""
        return (dt - datetime.combine(dt.date(), datetime.min.time())).total_seconds()


if __name__ == "__main__":
    # 当前时间
    current_time = TimeUtils.get_current_time()
    print("当前时间:", current_time)

    # 格式化时间
    formatted_time = TimeUtils.format_time(current_time, "%Y-%m-%d")
    print("格式化时间:", formatted_time)

    # 增加天数
    new_date = TimeUtils.add_days(current_time, 5)
    print("增加5天:", new_date)

    # 计算时间差
    start_time = datetime(2025, 1, 1, 12, 0)
    end_time = datetime(2025, 1, 1, 14, 30)
    diff = TimeUtils.time_difference(start_time, end_time)
    print("时间差（秒）:", diff)

    # 减少天数
    earlier_date = TimeUtils.subtract_days(current_time, 3)
    print("减少3天:", earlier_date)

    # 解析时间字符串
    time_str = "2025-01-01 15:30:00"
    parsed_time = TimeUtils.parse_time(time_str)
    print("解析时间:", parsed_time)

    # 判断时间是否是过去
    is_past = TimeUtils.is_past(datetime(2024, 1, 1))
    print("是否是过去时间:", is_past)

    # 获取星期几
    day_of_week = TimeUtils.get_day_of_week(current_time)
    print("星期几:", day_of_week)

    # 获取当天起始时间
    start_of_day = TimeUtils.get_start_of_day(current_time)
    print("当天起始时间:", start_of_day)

    # 获取当天结束时间
    end_of_day = TimeUtils.get_end_of_day(current_time)
    print("当天结束时间:", end_of_day)

    # 获取时间的秒数
    time_in_seconds = TimeUtils.get_time_in_seconds(current_time)
    print("从午夜开始的秒数:", time_in_seconds)
