from microdot import Microdot, Response
import network
import utime
import urandom  # Menggunakan urandom untuk MicroPython

SSID = 'BOE-'
PASSWORD = ''

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        print("Menghubungkan ke jaringan...")
        utime.sleep(1)
    print("Terhubung dengan sukses!")
    print("Alamat IP:", wlan.ifconfig()[0])

def simulasi_telur_harian():
    return max(0, 8 + urandom.getrandbits(2))  # Hasil telur antara 8 - 11

app = Microdot()
Response.default_content_type = 'application/json'

@app.route('/')
def index(request):
    data = {
        'tanggal': '{}-{}-{}'.format(utime.localtime()[0], utime.localtime()[1], utime.localtime()[2]),
        'jumlah_telur': simulasi_telur_harian()
    }
    return data

def main():
    connect_to_wifi(SSID, PASSWORD)
    app.run(port=5000)

if __name__ == '__main__':
    main()
