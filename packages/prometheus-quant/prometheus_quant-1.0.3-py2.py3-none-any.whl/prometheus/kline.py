from datetime import datetime, timedelta


class generator:
    """k线生成器"""

    def __init__(self, call_back_function=None):
        """初始化方法"""

        # 记录计算参数
        self.__call_back_function = call_back_function               # 新的一根k线创建之后的回调函数

        # 计算的各个容器
        self.__kline_cache = dict()                                  # K线的缓存容器{标的，K线数据}     

    def update_tick(self, tick: dict):
        """添加一更新的K线"""

        # 解析行情
        date = tick.get("Date", None)
        time = tick.get("Time", None)
        millisecond = tick.get("Millisecond", 0) * 1000
        instrument_id = tick.get("InstrumentID", None)

        last = tick.get("Last", None)
        volume = tick.get("Volume", None)
        amount = tick.get("Amount", None)

        # 如果解析失败，退出
        if last is None or date is None or time is None or instrument_id is None:
            return

        # 将时间转换为datetime，方便计算
        current_datetime = datetime.strptime(
            f"{date} {time}.{millisecond}", "%Y%m%d %H:%M:%S.%f"
        )

        # 需要计算的kline时间
        kline_datetime = datetime(
            current_datetime.year,
            current_datetime.month,
            current_datetime.day,
            current_datetime.hour,
            current_datetime.minute,
            0, 0
        ) + timedelta(minutes=1)

        # 如果触发事件没有设置过，利用第一帧配置
        if instrument_id not in self.__kline_cache:
            self.__kline_cache[instrument_id] = {
                "InstrumentID": instrument_id,
                "DateTime": kline_datetime,
                "Date": date,
                "Time": time,
                "OpenPrice": last,
                "HighPrice": last,
                "LowPrice": last,
                "ClosePrice": last,
                "Volume": volume,
                "Amount": amount,
            }
            return

        # 如果k线的计算时间发生改变，触发回调，将K线推送出去
        if kline_datetime != self.__kline_cache[instrument_id]["DateTime"]:
            # 触发回调推送K线
            if self.__call_back_function is not None:
                self.__call_back_function(self.__kline_cache[instrument_id])

            # 重新填充缓存数据
            self.__kline_cache[instrument_id] = {
                "InstrumentID": instrument_id,
                "DateTime": kline_datetime,
                "Date": date,
                "Time": time,
                "OpenPrice": last,
                "HighPrice": last,
                "LowPrice": last,
                "ClosePrice": last,
                "Volume": volume,
                "Amount": amount,
            }
            return

        # 上述情况都不符合，进行计算
        self.__kline_cache[instrument_id]["HighPrice"] = max(last, self.__kline_cache[instrument_id]["HighPrice"])
        self.__kline_cache[instrument_id]["LowPrice"] = min(last, self.__kline_cache[instrument_id]["LowPrice"])
        self.__kline_cache[instrument_id]["ClosePrice"] = last
        self.__kline_cache[instrument_id]["Volume"] = volume
        self.__kline_cache[instrument_id]["Amount"] = amount
