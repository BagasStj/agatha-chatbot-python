from datetime import datetime, timedelta
import time

# String tanggal dan waktu awal
date_string = "04-09-2024 07:55"
date="04-09-2024 07:55"

# Parsing string ke objek datetime
dt_object = datetime.strptime(date_string, "%d-%m-%Y %H:%M")
date_obj = datetime.strptime(date, "%d-%m-%Y %H:%M")
schedule_time = date_obj - timedelta(minutes=10)
schedule_timestamp =  int(time.mktime(schedule_time.timetuple()))
       
print(f"Format Date - {schedule_timestamp}")

# Konversi ke Unix timestamp
unix_timestamp = int(time.mktime(dt_object.timetuple()))

print(unix_timestamp)