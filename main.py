import telebot
import requests
import json
from urllib import request
from collections import namedtuple

bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN_HERE')

@bot.message_handler(commands=['start'])
def start(message):
  send_mess = f"<b>Hello {message.from_user.first_name}!</b>\n"
  bot.send_message(message.chat.id, send_mess, parse_mode='html')


@bot.message_handler(commands=['help'])
def help(message):
  helpMessage = "Send me a Movie name and I will send you some info about it. I.e: Interstellar"
  bot.send_message(message.chat.id, helpMessage, parse_mode='html')

@bot.message_handler(content_types=['text'])
def mess(message):
  final_message = ""
  get_message_bot = message.text
  get_message_bot = get_message_bot.replace(' ', '_')
  try:
    resp = request.urlopen(f'http://www.omdbapi.com/?t={get_message_bot}&apikey={YOUR_OMDB_API_KEY_HERE}')
    
    data = resp.read().decode("UTF-8")

    movie = json.loads(data, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
    try:
      final_message = "Title: " + f"{movie.Title}" + f"\nYear: {movie.Year}" + f"\nRated: {movie.Rated}" + f"\nReleased: {movie.Released}" + f"\nGenre: {movie.Genre}" + f"\nRuntime: {movie.Runtime}" + f"\nDirector: {movie.Director}" + f"\nBox office: {movie.BoxOffice}" + f"\nAwards: {movie.Awards}" + f"\nPlot: {movie.Plot}"
    except Exception:
      final_message = "Title: " + f"{movie.Title}" + f"\nYear: {movie.Year}" + f"\nRated: {movie.Rated}" + f"\nReleased: {movie.Released}" + f"\nGenre: {movie.Genre}" + f"\nRuntime: {movie.Runtime}" + f"\nDirector: {movie.Director}" + f"\nAwards: {movie.Awards}" + f"\nPlot: {movie.Plot}"
    bot.send_photo(chat_id=message.chat.id, photo=f"{movie.Poster}")
    bot.send_message(message.chat.id, final_message, parse_mode='html')
    
  except Exception as e:
    print('Exception')
    bot.send_message(message.chat.id, "No Data Found", parse_mode='html')


bot.polling(none_stop=True)