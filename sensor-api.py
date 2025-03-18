import network
import time
import random
import utime  # Gantilah time.strftime dengan cara manual
from microdot import Microdot, Response

# Konfigurasi Wi-Fi
SSID = 'BOE'  # Ganti dengan nama Wi-Fi Anda
PASSWORD = ''  # Ganti dengan password Wi-Fi Anda

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

# Fungsi untuk mendapatkan data produksi telur
def get_produksi_telur():
    jumlah_telur = random.randint(1, 10)  # Jumlah telur dalam biji
    berat_telur = round(jumlah_telur * random.uniform(0.05, 0.07), 2)  # Berat dalam KG

    # Mengambil tanggal saat ini
    t = utime.localtime()
    tanggal = f"{t[0]}-{t[1]:02d}-{t[2]:02d}"  # Format YYYY-MM-DD

    return {
        "jumlah_telur": jumlah_telur,  # Tetap bilangan bulat
        "berat_telur": f"{berat_telur} KG",  # Berat dalam KG
        "tanggal": tanggal
    }

# Fungsi untuk mendapatkan data suhu
def get_suhu():
    suhu = round(random.uniform(28, 35), 2)
    status = "Normal" if 28 <= suhu <= 32 else "Tinggi"
    return {"kadar": f"{suhu} C", "status": status}

# Fungsi untuk mendapatkan data kelembapan
def get_kelembapan():
    kelembapan = round(random.uniform(40, 80), 2)
    status = "Normal" if 50 <= kelembapan <= 70 else "Tidak Normal"
    return {"kadar": f"{kelembapan} %", "status": status}

# Fungsi untuk mendapatkan data amonia
def get_amonia():
    amonia = round(random.uniform(0, 10), 2)
    status = "Aman" if amonia < 5 else "Bahaya"
    return {"kadar": f"{amonia} ppm", "status": status}

# Fungsi untuk mendapatkan data oksigen
def get_oksigen():
    oksigen = round(random.uniform(18, 22), 2)
    status = "Normal" if 19 <= oksigen <= 21 else "Tidak Normal"
    return {"kadar": f"{oksigen} %", "status": status}

# Fungsi untuk mendapatkan data karbondioksida
def get_karbondioksida():
    karbondioksida = round(random.uniform(300, 1000), 2)
    status = "Normal" if karbondioksida < 600 else "Tinggi"
    return {"kadar": f"{karbondioksida} ppm", "status": status}

# Fungsi untuk mendapatkan data karbonmonoksida
def get_karbonmonoksida():
    karbonmonoksida = round(random.uniform(0, 10), 2)
    status = "Aman" if karbonmonoksida < 5 else "Bahaya"
    return {"kadar": f"{karbonmonoksida} ppm", "status": status}

# Endpoint API
@app.get('/api/telur')
def telur_api(request):
    return get_produksi_telur()

@app.get('/api/suhu')
def suhu_api(request):
    return get_suhu()

@app.get('/api/kelembapan')
def kelembapan_api(request):
    return get_kelembapan()

@app.get('/api/amonia')
def amonia_api(request):
    return get_amonia()

@app.get('/api/oksigen')
def oksigen_api(request):
    return get_oksigen()

@app.get('/api/karbondioksida')
def karbondioksida_api(request):
    return get_karbondioksida()

@app.get('/api/karbonmonoksida')
def karbonmonoksida_api(request):
    return get_karbonmonoksida()

# Jalankan server
app.run(host="0.0.0.0", port=5000)
