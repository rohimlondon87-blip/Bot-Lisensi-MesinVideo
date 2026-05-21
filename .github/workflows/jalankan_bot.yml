name: Auto Bot Telegram 24/7

on:
  schedule:
    # Menjalankan bot setiap 5 menit sekali tanpa henti
    - cron: '*/5 * * * *'
  workflow_dispatch: 
    # Tombol manual jika kamu ingin menyalakannya dari dashboard GitHub

jobs:
  run-bot:
    runs-on: ubuntu-latest
    
    # Batasi waktu eksekusi maksimal 5 menit agar tidak bentrok dengan siklus berikutnya
    timeout-minutes: 5

    steps:
    - name: Checkout Repository
      uses: actions/checkout@v3

    - name: Siapkan Python 3.10
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install Library pyTelegramBotAPI
      run: |
        python -m pip install --upgrade pip
        pip install pyTelegramBotAPI

    - name: Nyalakan Mesin Bot!
      run: |
        # Script akan berjalan dan mengambil semua antrean pesan
        python bot_keygen.py
