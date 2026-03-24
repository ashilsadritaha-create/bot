import requests
import time
import random
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ────────────────────────────────────────────────
# BOT AYARLARI
# ────────────────────────────────────────────────
BOT_TOKEN = "8763202675:AAG66L0cb8Yr4HfznEig3e76A3I6uFUT4I8"
REQUIRED_CHANNEL = "@elkaide1988"
API_URL = "https://basedemezler.com/api/query"

# Cookie (Siteye girip F12 ile yenileyebilirsin)
COOKIE_STRING = (
    "cf_clearance=5wfULDQaMMy24eNvOHVmdkd0ogyTfhdZfuGKvS5M6Io;"
    "next-auth.callback-url=http%3A%2F%2Flocalhost;"
    "next-auth.csrf-token=99d2149477e7ff66ee904de7dfea12152d6163209469be2a466569b4a7b5fc7b%7Ccd7ed96b08556bb80c22edd5a3c2f7ba206f09cc9e52a07bba3a95b2dc7c1b04;"
    "next-auth.session-token=eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..ymo9LORUpBKJ7Exo.z1bzaLXKe8LbU4pQZ58H4zk51u2bpiUO1hjApMgXSVfyXtXsdeNXWlfWuiqwC-3a-rT3dIw8odQvX_2fPWkHt4nQD9A6hQJU3J37wmo4Njduc1rViILoVp4dR6AC9gqPFJwBuTlS_hFefBZokKTsCjqEpKBLrOqjlzf7F_EXmlBnhG9AtBpkomHorqp1iZR8XBBcluRd_YyMdeoltCBTfzhoKw.KyCPp2M6I43Rjo_L8dqq6w"
)

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Origin": "https://basedemezler.lol",
    "Referer": "https://basedemezler.lol/",
    "Cookie": COOKIE_STRING
}

bot = telebot.TeleBot(BOT_TOKEN)
user_state = {}   # Kullanıcının hangi sorguyu beklediğini tutar

# ────────────────────────────────────────────────
# KANAL KONTROLÜ
# ────────────────────────────────────────────────
def check_channel_membership(user_id):
    try:
        member = bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ['member', 'administrator', 'creator', 'restricted']
    except:
        return False

# ────────────────────────────────────────────────
# API SORGUSU
# ────────────────────────────────────────────────
def api_sorgula(payload):
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=35)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Hatası: {response.status_code}"}
    except Exception as e:
        return {"error": f"Bağlantı hatası: {str(e)}"}

# ────────────────────────────────────────────────
# LÜKS ve MODERN TXT FORMATI
# ────────────────────────────────────────────────
def format_lux_result(data, sorgu_tipi):
    result = f"╔════════════════════════════════════════════╗\n"
    result += f"          ELKAİDE SORGULAMA SİSTEMİ           \n"
    result += f"╚════════════════════════════════════════════╝\n\n"
    result += f"🔍 Sorgu Türü : {sorgu_tipi.upper()}\n"
    result += f"⏰ Tarih      : {time.strftime('%d.%m.%Y %H:%M:%S')}\n"
    result += f"🔧 Yapımcı    : @kiraflexx\n\n"
    result += "╔════════════════════════════════════════════╗\n"
    result += "               SORGULAMA SONUÇLARI             \n"
    result += "╚════════════════════════════════════════════╝\n\n"

    if isinstance(data, dict) and "data" in data:
        data = data["data"]

    if isinstance(data, list) and data:
        for idx, item in enumerate(data, 1):
            result += f"📌 Kayıt {idx}\n"
            result += "────────────────────────────────────────────\n"
            for key, value in item.items():
                emoji = {
                    "ad": "👤", "soyad": "👥", "tc": "🆔", "gsm": "📱",
                    "adres": "🏠", "anne": "👩", "baba": "👨",
                    "il": "📍", "ilce": "🏙️", "tapu": "🏡"
                }.get(key.lower(), "📌")
                result += f"{emoji} {key.capitalize()}: {value}\n"
            result += "────────────────────────────────────────────\n\n"
    elif isinstance(data, dict):
        for key, value in data.items():
            emoji = {
                "ad": "👤", "soyad": "👥", "tc": "🆔", "gsm": "📱",
                "adres": "🏠", "anne": "👩", "baba": "👨",
                "il": "📍", "ilce": "🏙️", "tapu": "🏡"
            }.get(key.lower(), "📌")
            result += f"{emoji} {key.capitalize()}: {value}\n"
    else:
        result += f"Sonuç: {data}\n"

    result += "\n🔥 Elkaide Sorgu Botu - Profesyonel Sorgu Hizmeti 🔥\n"
    result += "Yapımcı: @kiraflexx\n"
    return result

# ────────────────────────────────────────────────
# START KOMUTU
# ────────────────────────────────────────────────
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.first_name

    if check_channel_membership(user_id):
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("👤 Ad Soyad", callback_data="query_adsoyad"),
            InlineKeyboardButton("🆔 TC Bilgi", callback_data="query_tcbilgi")
        )
        markup.add(
            InlineKeyboardButton("📱 GSM Sorgu", callback_data="query_gsm"),
            InlineKeyboardButton("📱 TC → GSM", callback_data="query_tcgsm")
        )
        markup.add(
            InlineKeyboardButton("📞 GSM → TC", callback_data="query_gsmtc"),
            InlineKeyboardButton("🏠 Adres Sorgu", callback_data="query_adres")
        )
        markup.add(
            InlineKeyboardButton("🏡 Tapu Sorgu", callback_data="query_tapu")
        )

        hos_geldin = f"""
🌟 **Hoş Geldin {username}!** 🌟

**Elkaide Sorgu Botu**'na hoş geldiniz.

Profesyonel sorgu hizmetimizden yararlanabilirsiniz.

Aşağıdaki butonlardan sorgunuzu seçin.
        """
        bot.send_message(message.chat.id, hos_geldin, parse_mode="Markdown", reply_markup=markup)
    else:
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("📌 Kanala Katıl", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}"))
        markup.add(InlineKeyboardButton("✅ Onayla", callback_data="onayla"))

        bot.send_message(
            message.chat.id,
            f"Merhaba {username}!\n\nBotu kullanmak için @{REQUIRED_CHANNEL[1:]} kanalına katılmanız gerekmektedir.\n\nKatıldıktan sonra 'Onayla' butonuna basın.",
            reply_markup=markup
        )

# ────────────────────────────────────────────────
# CALLBACK HANDLER
# ────────────────────────────────────────────────
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "onayla":
        if check_channel_membership(call.from_user.id):
            bot.answer_callback_query(call.id, "✅ Onaylandı! Bot aktif.", show_alert=True)
            start(call.message)
        else:
            bot.answer_callback_query(call.id, "❌ Henüz kanala katılmadınız!", show_alert=True)
        return

    if call.data.startswith("query_"):
        cmd = call.data.split("_")[1]
        user_state[call.from_user.id] = cmd

        usages = {
            "adsoyad": "👤 Ad Soyad sorgusu için:\nÖrnek: `Mustafa Yılmaz`",
            "tcbilgi": "🆔 TC sorgusu için:\nÖrnek: `27727166918`",
            "gsm": "📱 GSM sorgusu için:\nÖrnek: `5551234567`",
            "tcgsm": "📱 TC → GSM için:\nÖrnek: `27727166918`",
            "gsmtc": "📞 GSM → TC için:\nÖrnek: `5551234567`",
            "adres": "🏠 Adres sorgusu için:\nÖrnek: `27727166918`",
            "tapu": "🏡 Tapu sorgusu için:\nÖrnek: `27727166918`"
        }

        bot.send_message(call.message.chat.id, usages.get(cmd, "Bilgiyi gönderin."))

# ────────────────────────────────────────────────
# SORGU İŞLEME
# ────────────────────────────────────────────────
@bot.message_handler(func=lambda m: m.chat.type == 'private' and m.from_user.id in user_state)
def handle_sorgu(message):
    user_id = message.from_user.id
    if user_id not in user_state:
        return

    cmd = user_state.pop(user_id)
    query_text = message.text.strip()

    payload = {"type": cmd}

    if cmd == "adsoyad":
        parts = query_text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Lütfen Ad ve Soyad girin (örnek: Mustafa Yılmaz)")
            return
        payload["ad"] = " ".join(parts[:-1])
        payload["soyad"] = parts[-1]
    elif cmd in ["tcbilgi", "tcgsm", "adres", "tapu"]:
        payload["tc"] = query_text
    elif cmd in ["gsm", "gsmtc"]:
        payload["gsm"] = query_text

    bot.reply_to(message, "🔄 Sorgu yapılıyor, lütfen bekleyin...")

    sonuc = api_sorgula(payload)

    if "error" in sonuc:
        bot.reply_to(message, f"❌ Hata oluştu: {sonuc['error']}")
        return

    formatted_text = format_lux_result(sonuc, cmd)
    dosya_adi = f"Elkaide_{cmd.upper()}_{int(time.time())}.txt"

    with open(dosya_adi, "w", encoding="utf-8") as f:
        f.write(formatted_text)

    with open(dosya_adi, "rb") as f:
        bot.send_document(
            message.chat.id,
            f,
            caption=f"✅ {cmd.upper()} sorgusu tamamlandı.\nYapımcı: @kiraflexx",
            reply_to_message_id=message.message_id
        )

    time.sleep(random.uniform(15, 35))

print("🚀 Elkaide Sorgu Botu başarıyla başlatıldı...")
bot.infinity_polling()