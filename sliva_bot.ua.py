import telebot
import speech_recognition as sr
from pydub import AudioSegment
import os
import requests

# 🔐 ВСТАВЬ СЮДА СВОЙ TELEGRAM ТОКЕН и API КЛЮЧ OpenRouter
TELEGRAM_TOKEN = "6159099464:AAH5ktsljXFMTfikGU7TofuOITv-o0sdvO0"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

# 📌 Триггеры, по которым бот поймёт, что надо сгенерировать изображение
IMAGE_TRIGGER_PHRASES = [
    "сгенерируй картинку", "создай изображение", "сделай арт", 
    "создай арт", "картинку", "batu", "generate", "image", "art"
]

# Проверка, содержит ли сообщение триггер на генерацию изображения
def contains_image_trigger(text):
    return any(trigger in text.lower() for trigger in IMAGE_TRIGGER_PHRASES)

# Заглушка: вместо генерации картинки (позже подключим реальное API)
def generate_image(prompt):
    return "https://via.placeholder.com/512x512.png?text=Генерация..."

# 🎙 Обработка голосовых сообщений
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    try:
        file_info = bot.get_file(message.voice.file_id)
        file = bot.download_file(file_info.file_path)

        with open("voice.ogg", 'wb') as f:
            f.write(file)

        sound = AudioSegment.from_ogg("voice.ogg")
        sound.export("voice.wav", format="wav")

        recognizer = sr.Recognizer()
        with sr.AudioFile("voice.wav") as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='uk-UA')

        bot.reply_to(message, f"Ти сказав: {text}")

        if contains_image_trigger(text):
            bot.send_message(message.chat.id, "🎨 Генерую зображення...")
            image_url = generate_image(text)
            bot.send_photo(message.chat.id, image_url)

    except Exception as e:
        bot.reply_to(message, f"Помилка: {e}")

# 💬 Обработка обычных текстовых сообщений
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    text = message.text

    if contains_image_trigger(text):
        bot.send_message(message.chat.id, "🖼 Генерую картинку по твоему описанию...")
        image_url = generate_image(text)
        bot.send_photo(message.chat.id, image_url)
    else:
        bot.send_message(message.chat.id, "Надішли мені голосове або напиши запит ✨")

print("✅ Бот запущен!")
bot.polling()
