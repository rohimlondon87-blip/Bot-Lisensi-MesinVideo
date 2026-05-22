```python
import telebot
from telebot.types import BotCommand, InlineKeyboardMarkup, InlineKeyboardButton
import hashlib

# ==========================================
# KONFIGURASI BOT & KEAMANAN
# ==========================================
# Masukkan Token Bot Telegram Kamu
BOT_TOKEN = "8981166779:AAFb8Il6WNV_EIXhyNKj8ExDBxjunsjD9BA"
SECRET_SALT = "DjiW9@hXzP2*rKqLmN"

# ⚠️ ID TELEGRAM ADMIN (Untuk menerima laporan penjualan)
ADMIN_CHAT_ID = "5506138692" 

# KONTAK SUPPORT
NOMOR_WA = "6285280235833" 
PESAN_WA = "Halo Admin Mesin Video Pro, saya butuh bantuan."
URL_WA = f"https://wa.me/{NOMOR_WA}?text={PESAN_WA.replace(' ', '%20')}"

bot = telebot.TeleBot(BOT_TOKEN)

# ==========================================
# LOGIKA BALASAN UTAMA (/start)
# ==========================================
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    try:
        teks_sapaan = (
            "👋 Halo! Selamat datang di Layanan Aktivasi *Mesin Video Pro*.\n\n"
            "Silakan *Paste (Tempel)* ID Komputer (HWID) Anda ke obrolan ini, "
            "dan sistem akan membalas dengan Serial Key Anda secara otomatis."
        )
        
        # Tambahkan Tombol Support di pesan sapaan
        markup = InlineKeyboardMarkup()
        btn_support = InlineKeyboardButton(text="💬 Hubungi Support (WhatsApp)", url=URL_WA)
        markup.add(btn_support)

        bot.reply_to(message, teks_sapaan, parse_mode='Markdown', reply_markup=markup)
        print(f"✅ Membalas sapaan ke: {message.from_user.first_name}")
    except Exception as e:
        print(f"❌ Error sapaan: {e}")

# ==========================================
# LOGIKA MENU CUSTOMER SERVICE (/cs)
# ==========================================
@bot.message_handler(commands=['cs'])
def send_cs_info(message):
    try:
        teks_cs = (
            "☎️ *PUSAT BANTUAN MESIN VIDEO PRO*\n\n"
            "Mengalami kendala teknis atau ingin membeli lisensi tambahan?\n"
            "Silakan hubungi Customer Service kami secara langsung melalui WhatsApp."
        )
        
        markup = InlineKeyboardMarkup()
        btn_wa = InlineKeyboardButton(text="💬 Chat via WhatsApp", url=URL_WA)
        markup.add(btn_wa)
        
        bot.reply_to(message, teks_cs, parse_mode='Markdown', reply_markup=markup)
        print(f"✅ Membalas info CS ke: {message.from_user.first_name}")
    except Exception as e:
        print(f"❌ Error menu CS: {e}")

# ==========================================
# GENERATOR KUNCI LISENSI & LAPORAN ADMIN
# ==========================================
@bot.message_handler(func=lambda message: True)
def generate_and_reply(message):
    try:
        hwid_pembeli = message.text.strip()
        print(f"📥 Menerima HWID: {hwid_pembeli}")
        
        if len(hwid_pembeli) < 15:
            # Jika HWID salah, berikan juga tombol support
            markup_err = InlineKeyboardMarkup()
            markup_err.add(InlineKeyboardButton(text="Tanya Admin 💬", url=URL_WA))
            bot.reply_to(message, "⚠️ Format ID Komputer (HWID) tidak valid. Silakan copy dengan benar dari aplikasi.", reply_markup=markup_err)
            return

        # Generate Kunci
        raw = f"{SECRET_SALT}-{hwid_pembeli}"
        hashed = hashlib.sha256(raw.encode()).hexdigest()
        formatted_key = f"{hashed[0:4]}-{hashed[4:8]}-{hashed[8:12]}-{hashed[12:16]}".upper()

        pesan_balasan = (
            "✅ *KUNCI BERHASIL DIBUAT!*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💻 HWID: `{hwid_pembeli}`\n"
            f"🔑 SERIAL KEY: `{formatted_key}`\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💡 *Cara Penggunaan:*\n"
            "1. Klik pada Serial Key di atas untuk meng-copy.\n"
            "2. Buka aplikasi Mesin Video Pro.\n"
            "3. Paste di kolom Serial Key lalu klik Aktifkan.\n\n"
            "Terima kasih! 🚀"
        )
        
        # Tambahkan tombol Support di bawah Serial Key (Jaga-jaga jika pembeli bingung cara pakainya)
        markup_key = InlineKeyboardMarkup()
        markup_key.add(InlineKeyboardButton(text="☎️ Butuh Bantuan? Hubungi CS", url=URL_WA))

        # 1. Kirim Kunci ke Pembeli
        bot.reply_to(message, pesan_balasan, parse_mode='Markdown', reply_markup=markup_key)
        print(f"✅ Sukses mengirim kunci ke {message.from_user.first_name}")

        # 2. Kirim Laporan Rahasia ke Admin
        try:
            nama_user = message.from_user.first_name
            username = f"@{message.from_user.username}" if message.from_user.username else "Tidak ada username"
            user_id = message.from_user.id
            
            laporan_admin = (
                "📊 *LAPORAN LISENSI BARU TERJUAL*\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 *Pembeli:* {nama_user}\n"
                f"🏷️ *Username:* {username}\n"
                f"🆔 *User ID:* `{user_id}`\n"
                "━━━━━━━━━━━━━━━━━━━━\n"
                f"💻 *HWID:* `{hwid_pembeli}`\n"
                f"🔑 *Key Keluar:* `{formatted_key}`\n"
            )
            bot.send_message(ADMIN_CHAT_ID, laporan_admin, parse_mode='Markdown')
            print("✅ Laporan berhasil dikirim ke Admin.")
        except Exception as e_admin:
            print(f"❌ Gagal mengirim laporan ke Admin: {e_admin}")

    except Exception as e:
        print(f"❌ Error proses HWID: {e}")

# ==========================================
# EKSEKUSI PENGAMBILAN PESAN (POLLING)
# ==========================================
if __name__ == "__main__":
    print("🚀 Bot dijalankan oleh GitHub Actions...")
    bot.remove_webhook()
    
    # Daftarkan Menu ke Bot Telegram secara otomatis
    bot.set_my_commands([
        BotCommand("start", "Mulai layanan aktivasi"),
        BotCommand("cs", "Hubungi Customer Service (WhatsApp)")
    ])
    print("✅ Menu bot berhasil didaftarkan!")
    
    try:
        # Timeout 240 detik (4 menit)
        bot.polling(none_stop=True, timeout=240)
    except Exception as e:
        print(f"ℹ️ Polling cycle selesai/terputus: {e}")


```
