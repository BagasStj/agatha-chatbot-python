import psycopg2
import time
import requests
from dotenv import load_dotenv
import json
import os
from datetime import datetime, timedelta
import pytz

# Load the .env file
load_dotenv()

# Connection to database
connection = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    dbname=os.getenv('DB_NAME'),
)

# Variable to store the last value of the monitored column
last_value = None

def check_for_update():
    global last_value
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT nomor_antrean, nomor_hp, jadwal_konsultasi 
            FROM public.datanomorantrian 
            ORDER BY id DESC LIMIT 1
        ''')
        result = cursor.fetchone()

        if result and result[0] != last_value:
            last_value = result[0]
            print(f"get data from database {result[0], result[1], result[2]}")
            send_message(result[0], result[1], result[2])

def send_message(value, nomor_hp, jadwal_konsultasi):
    url = 'https://api.fonnte.com/send'
    token = os.getenv('FONNTE_TOKEN')
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
    }
    
    try:
        schedule_timestamp = convert_to_unix_timestamp(jadwal_konsultasi)
        print(f"Format Date - {schedule_timestamp}")
    except ValueError as e:
        print(f"Error: Invalid date format - {jadwal_konsultasi}. Error: {e}")
        schedule_timestamp = None
    
    formatted_date = jadwal_konsultasi.strftime("%d-%m-%Y %H:%M")
    payload = {
        'target': nomor_hp,
        'message': f'Jadwal Cek Rutin Dan Konsultasi Dokter Di Rumah Sakit Kami Adalah Pada Tanggal {formatted_date}, jangan lupa datang tepat waktu \n Maaf Anda tidak dapat membalas pesan ini',
        'schedule': schedule_timestamp
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

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

# Main loop
if __name__ == "__main__":
    try:
        while True:
            check_for_update()
            time.sleep(5)  # Cek setiap 5 detik
    except KeyboardInterrupt:
        print("Program dihentikan oleh pengguna")
    finally:
        connection.close()