import os
import logging
import pickle
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# === Логирование ===
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === Токен и ID администратора ===
TOKEN = "7911189691:AAGdZfVSKRLLKAOfmZJJNIDN-cjogtGxtWM"  # ВСТАВЬ СВОЙ ТОКЕН
ADMIN_ID = 6660647501  # ВСТАВЬ СВОЙ CHAT_ID (без кавычек)

# === Загрузка или создание базы ===
if os.path.exists("orders.pkl"):
    with open("orders.pkl", "rb") as f:
        order_data = pickle.load(f)
else:
    order_data = {}

# === Меню ===
main_menu = ReplyKeyboardMarkup([
    [KeyboardButton("Заказать дизайн / монтаж")],
    [KeyboardButton("Портфолио работ")],
    [KeyboardButton("Связаться с менеджером")],
    [KeyboardButton("Дополнительно")]
], resize_keyboard=True)

services_menu = ReplyKeyboardMarkup([
    [KeyboardButton("Превью YouTube")],
    [KeyboardButton("Монтаж коротких видео (до 1 мин)")],
    [KeyboardButton("Монтаж длинных видео (до 10 мин)")],
    [KeyboardButton("Логотип или оформление профиля")],
    [KeyboardButton("Обработка фото / ретушь")],
    [KeyboardButton("Назад в меню")]
], resize_keyboard=True)

extra_menu = ReplyKeyboardMarkup([
    [KeyboardButton("Скидки / Акции")],
    [KeyboardButton("Оставить отзыв")],
    [KeyboardButton("Назад в меню")]
], resize_keyboard=True)

# === /start ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Здравствуйте! Я — бот NurMedia. Готов помочь с заказом превью, шапок, логотипов или видеомонтажа.",
        reply_markup=main_menu
    )

# === Обработка сообщений ===
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username or "Без ника"

    if text == "Заказать дизайн / монтаж":
        await update.message.reply_text("Выберите нужную услугу:", reply_markup=services_menu)

    elif text in [
        "Превью YouTube", "Монтаж коротких видео (до 1 мин)",
        "Монтаж длинных видео (до 10 мин)", "Логотип или оформление профиля",
        "Обработка фото / ретушь"
    ]:
        if user_id not in order_data:
            order_data[user_id] = {'orders': 0}
        order_data[user_id]['orders'] += 1
        orders = order_data[user_id]['orders']
        with open("orders.pkl", "wb") as f:
            pickle.dump(order_data, f)

        await update.message.reply_text("Спасибо! В течение 20 минут с вами свяжется наш менеджер.")
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Новая заявка: {text}\nОт: @{username} ({user_id})\nВсего заказов: {orders}"
        )

    elif text == "Портфолио работ":
        await update.message.reply_text("Примеры работ: https://www.instagram.com/invites/contact/?igsh=k5awcxh45q05&utm_content=y4w8ptt")

    elif text == "Связаться с менеджером":
        await update.message.reply_text("Ожидайте — с вами свяжется менеджер.")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"Запрос на связь от: @{username} ({user_id})")

    elif text == "Дополнительно":
        await update.message.reply_text("Дополнительные опции:", reply_markup=extra_menu)

    elif text == "Скидки / Акции":
        await update.message.reply_text(
            "Скидки и бонусы:\n"
            "- 15% на 1-й заказ\n"
            "- 5% за каждый 3 заказ (до 15%)\n"
            "- Отталкиваясь от заказа будут приятные бонусы"
        )

    elif text == "Оставить отзыв":
        await update.message.reply_text("https://montazh-i-oformlenie-jcylmrg.gamma.site/ Здесь можно оставить отзыв")

    elif text == "Назад в меню":
        await update.message.reply_text("Вы вернулись в главное меню.", reply_markup=main_menu)

    else:
        await update.message.reply_text("Пожалуйста, выберите действие из меню ниже.", reply_markup=main_menu)

# === Запуск ===
if __name__ == "__main__":
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Бот запущен и работает 24/7...")
    application.run_polling()
