import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice
from aiogram import F
import logging

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "8941772678:AAHuE6sJ-Y0jpib2DTir-eglISPCK_C_L4g"
ADMIN_IDS = [7089656336, 8707761326]

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def main_menu():
    kb = [
        [InlineKeyboardButton(text="🔥 Esila İfsx - 250 Yıldız", callback_data="pay_esila_250")],
        [InlineKeyboardButton(text="🔥 Gizem İfsx - 150 Yıldız", callback_data="pay_gizem_150")],
        [InlineKeyboardButton(text="🔥 Savega İfsx - 200 Yıldız", callback_data="pay_savega_200")],
        [InlineKeyboardButton(text="🔥 Türbanlı Zelal İfsx - 300 Yıldız", callback_data="pay_zelal_300")],
        [InlineKeyboardButton(text="🔥 Simge Barkanoğlu İfsx - 250 Yıldız", callback_data="pay_simge_250")],
        [InlineKeyboardButton(text="🔥 Zoktay Manifest İfsx - 100 Yıldız", callback_data="pay_zoktay_100")],
        [InlineKeyboardButton(text="🔥 Türk İfsx Arşivi - 120 Yıldız", callback_data="pay_turkifsa_120")],
        [InlineKeyboardButton(text="🔥 Türk Porn Arşivi - 150 Yıldız", callback_data="pay_turkporn_150")],
        [InlineKeyboardButton(text="🔥 Türbanlı İfsx - 180 Yıldız", callback_data="pay_turbanli_180")],
        [InlineKeyboardButton(text="🔥 Elit Kedi TikTok İfsx - 130 Yıldız", callback_data="pay_elitkedi_130")],
        [InlineKeyboardButton(text="🔥 Gizli Çekimler - 200 Yıldız", callback_data="pay_gizlicekim_200")],
        [InlineKeyboardButton(text="🔥 Ayak Arşivi - 100 Yıldız", callback_data="pay_ayak_100")],
        [InlineKeyboardButton(text="🔥 Rus Arşivi - 120 Yıldız", callback_data="pay_rus_120")],
        [InlineKeyboardButton(text="🔥 UwU Girl Arşivi - 100 Yıldız", callback_data="pay_uwu_100")],
        [InlineKeyboardButton(text="🔥 Tamirci Hasan İfsx - 250 Yıldız", callback_data="pay_tamirci_250")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

def admin_panel():
    kb = [
        [InlineKeyboardButton(text="📢 Duyuru Gönder", callback_data="duyuru")],
        [InlineKeyboardButton(text="👥 Aktif Kullanıcılar", callback_data="users")],
        [InlineKeyboardButton(text="🚫 Ban Listesi", callback_data="banlist")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "🎺 <b>GELİŞMİŞ İFŞX BOTU</b> 🎺\n\n"
        "Tüm premium içerikler Telegram Yıldızı ile satın alınabilir.\n\n"
        "Ödeme yaptıktan sonra yöneticilerimiz gerekli içeriği DM üzerinden gönderecektir.\n\n"
        "📢 Botumuzda ünlülerin ifşxlarını görmek istiyorsanız, satın alarak kesintisiz izleyebilirsiniz.\n\n"
        "📞 Destek için:\n"
        "@kiraflexx\n"
        "@NeonXyl",
        parse_mode='HTML',
        reply_markup=main_menu()
    )
@dp.message(Command("admin"))
async def admin_cmd(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ Yetkin yok.")
        return
    await message.answer("🛠 <b>S3xy Admin panel neonu gotten s1key1m ADFADSDFDS</b>", reply_markup=admin_panel())

# Admin Panel Butonları
@dp.callback_query(F.data == "duyuru")
async def duyuru(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer("Duyuru metnini yaz, herkese gönderilsin:")

@dp.message()
async def all_messages(message: types.Message):
    if message.from_user.id in ADMIN_IDS and len(message.text) > 3:
        # Duyuru gönder
        # (Şu an basit, istersen genişletirim)
        await message.answer("✅ Duyuru gönderildi (test mod).")

@dp.callback_query(F.data == "users")
async def users_list(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer("👥 Aktif kullanıcılar: (log sistemi eklenecek)")

@dp.callback_query(F.data == "banlist")
async def banlist(callback: types.CallbackQuery):
    if callback.from_user.id not in ADMIN_IDS: return
    await callback.message.answer("🚫 Banlı kimse yok (şu an).")

# Ödeme Sistemi
@dp.callback_query(F.data.startswith("pay_"))
async def handle_payment(callback: types.CallbackQuery):
    data = callback.data.split("_")
    name = " ".join(data[1:-1]).replace("_", " ")
    price = int(data[-1])

    prices = [LabeledPrice(label=f"{name} İfsx", amount=price)]

    await bot.send_invoice(
        chat_id=callback.from_user.id,
        title=f"{name} İfsx",
        description="Ödeme sonrası admin DM atacak.",
        payload=f"neonx_{name}_{price}",
        provider_token="",
        currency="XTR",
        prices=prices
    )

@dp.message(F.successful_payment)
async def successful_payment(message: types.Message):
    await message.answer("✅ Ödeme Başarılı! Adminler DM’den içeriği gönderecek.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
