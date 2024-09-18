from datetime import datetime, timedelta
import time

import pytz

# String tanggal dan waktu awal
date = '2024-09-18 20:34:00.000'

def convert_to_unix_timestamp(jadwal_konsultasi):
    # Set timezone to WIB (Western Indonesian Time)
    wib = pytz.timezone('Asia/Jakarta')
    
    # If jadwal_konsultasi is a string, parse it
    if isinstance(jadwal_konsultasi, str):
        jadwal_konsultasi = datetime.strptime(jadwal_konsultasi, "%Y-%m-%d %H:%M:%S.%f")
    
    # Ensure jadwal_konsultasi is aware of its timezone
    if jadwal_konsultasi.tzinfo is None:
        jadwal_konsultasi = wib.localize(jadwal_konsultasi)
    else:
        jadwal_konsultasi = jadwal_konsultasi.astimezone(wib)
    
    # Subtract 10 minutes
    notification_time = jadwal_konsultasi - timedelta(minutes=10)
    
    # Convert to Unix timestamp
    unix_timestamp = int(notification_time.timestamp())
    
    return unix_timestamp

# Parsing string ke objek datetime
dt_object = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
schedule_time = dt_object - timedelta(minutes=10)
schedule_timestamp = int(time.mktime(schedule_time.timetuple()))

print(f"Format Date - {schedule_timestamp}")
print(f"Format Date function - {convert_to_unix_timestamp(date)}")

# Konversi ke Unix timestamp
unix_timestamp = int(time.mktime(dt_object.timetuple()))

print(unix_timestamp)
