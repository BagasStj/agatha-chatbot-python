import psycopg2
import time
import requests
from dotenv import load_dotenv
import json
import os
from datetime import datetime, timedelta

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
        cursor.execute('SELECT no_antrian, nomor_hp, date FROM public."SampleDataNomorAntrian" ORDER BY id DESC LIMIT 1')
        result = cursor.fetchone()

        # Cek apakah ada perubahan pada kolom yang dipantau
        if result and result[0] != last_value:
            last_value = result[0]
            send_message(result[0], result[1], result[2])

def send_message(value, nomor_hp, date):
    url = 'https://api.fonnte.com/send'
    token = os.getenv('FONNTE_TOKEN')  # Get token from environment variable
    
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json',
    }
    
    # Convert date string to Unix timestamp and subtract 10 minutes
    try:
        date_obj = datetime.strptime(date, "%d-%m-%Y %H:%M")
        schedule_time = date_obj - timedelta(minutes=10)
        schedule_timestamp = int(schedule_time.timestamp())
        print(f"Format Date - {schedule_timestamp}")
    except ValueError:
        print(f"Error: Invalid date format - {date}")
        schedule_timestamp = None
    
    payload = {
        'target': nomor_hp,  # Menggunakan nomor_hp dari database
        'message': f'Jadwal Cek Rutin Dan Konsultasi Dokter Di Rumah Sakit Kami Adalah Pada Tanggal {date} , jangan lupa datang tepat waktu',
        'schedule': schedule_timestamp  # Menggunakan Unix timestamp
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

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