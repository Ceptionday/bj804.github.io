# -*- coding: utf-8 -*-
import datetime, time
now_time = datetime.datetime.now()
str_time = now_time.strftime("%X")
tup_time = time.strptime(str_time, "%X")
hello_time_hour = tup_time.tm_hour