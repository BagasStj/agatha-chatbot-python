from datetime import datetime, timedelta
import time

import pytz

# String tanggal dan waktu awal
date='04-09-2024 08:54'


def convert_to_unix_timestamp(date_string):
    # Set timezone to WIB (Western Indonesian Time)
    wib = pytz.timezone('Asia/Jakarta')
    
    # Parse the date string
    dt_object = datetime.strptime(date_string, "%d-%m-%Y %H:%M")
    
    # Localize the datetime object to WIB
    dt_object = wib.localize(dt_object)
    
    # Subtract 10 minutes
    dt_object -= timedelta(minutes=10)
    
    # Convert to Unix timestamp
    unix_timestamp = int(dt_object.timestamp())
    
    return unix_timestamp


# Parsing string ke objek datetime
dt_object = datetime.strptime(date, "%d-%m-%Y %H:%M")
date_obj = datetime.strptime(date, "%d-%m-%Y %H:%M")
schedule_time = date_obj - timedelta(minutes=10)
schedule_timestamp =  int(time.mktime(schedule_time.timetuple()))
       
print(f"Format Date - {schedule_timestamp}")
print(f"Format Date function - {convert_to_unix_timestamp(date)}")

# Konversi ke Unix timestamp
unix_timestamp = int(time.mktime(dt_object.timetuple()))

print(unix_timestamp)
