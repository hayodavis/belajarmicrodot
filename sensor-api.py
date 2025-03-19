import network
import time
import random
import uasyncio as asyncio
from microdot import Microdot, Response

# Konfigurasi Wi-Fi
SSID = 'BOE-'  # Ganti dengan nama Wi-Fi Anda
PASSWORD = ''  # Ganti dengan password Wi-Fi Anda

# Data global untuk menyimpan nilai sensor
data_sensor = {}
data_produksi_telur = {}

# Fungsi untuk menghubungkan ke Wi-Fi
def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Menghubungkan ke Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print("Terhubung ke Wi-Fi:", wlan.ifconfig())

# Jalankan koneksi Wi-Fi
connect_to_wifi()

# Inisialisasi Microdot
app = Microdot()
Response.default_content_type = 'application/json'

# Fungsi untuk memperbarui data produksi telur setiap hari
def update_produksi_telur():
    global data_produksi_telur
    jumlah_telur = random.randint(1, 10)  # Jumlah telur dalam biji
    berat_telur = round(jumlah_telur * random.uniform(0.05, 0.07), 2)  # Berat dalam KG
    
    # Mengambil tanggal saat ini
    t = time.localtime()
    tanggal = f"{t[0]}-{t[1]:02d}-{t[2]:02d}"  # Format YYYY-MM-DD
    
    data_produksi_telur = {
        "jumlah_telur": jumlah_telur,
        "berat_telur": f"{berat_telur} KG",
        "tanggal": tanggal
    }

# Fungsi untuk memperbarui data sensor setiap 2 detik
async def update_sensors():
    global data_sensor
    while True:
        data_sensor = {
            "suhu": {"kadar": f"{round(random.uniform(28, 35), 2)} C", "status": "Normal" if 28 <= random.uniform(28, 35) <= 32 else "Tinggi"},
            "kelembapan": {"kadar": f"{round(random.uniform(40, 80), 2)} %", "status": "Normal" if 50 <= random.uniform(40, 80) <= 70 else "Tidak Normal"},
            "amonia": {"kadar": f"{round(random.uniform(0, 10), 2)} ppm", "status": "Aman" if random.uniform(0, 10) < 5 else "Bahaya"},
            "oksigen": {"kadar": f"{round(random.uniform(18, 22), 2)} %", "status": "Normal" if 19 <= random.uniform(18, 22) <= 21 else "Tidak Normal"},
            "karbondioksida": {"kadar": f"{round(random.uniform(300, 1000), 2)} ppm", "status": "Normal" if random.uniform(300, 1000) < 600 else "Tinggi"},
            "karbonmonoksida": {"kadar": f"{round(random.uniform(0, 10), 2)} ppm", "status": "Aman" if random.uniform(0, 10) < 5 else "Bahaya"},
        }
        await asyncio.sleep(2)  # Perbarui setiap 2 detik

# Endpoint API
@app.get('/api/telur')
def telur_api(request):
    return data_produksi_telur

@app.get('/api/suhu')
def suhu_api(request):
    return data_sensor.get("suhu", {})

@app.get('/api/kelembapan')
def kelembapan_api(request):
    return data_sensor.get("kelembapan", {})

@app.get('/api/amonia')
def amonia_api(request):
    return data_sensor.get("amonia", {})

@app.get('/api/oksigen')
def oksigen_api(request):
    return data_sensor.get("oksigen", {})

@app.get('/api/karbondioksida')
def karbondioksida_api(request):
    return data_sensor.get("karbondioksida", {})

@app.get('/api/karbonmonoksida')
def karbonmonoksida_api(request):
    return data_sensor.get("karbonmonoksida", {})

# Fungsi utama untuk menjalankan pembaruan sensor dan server secara bersamaan
async def main():
    update_produksi_telur()  # Perbarui data produksi telur saat startup
    asyncio.create_task(update_sensors())  # Jalankan pembaruan sensor di background
    app.run(host="0.0.0.0", port=5000)

# Jalankan program
asyncio.run(main())
