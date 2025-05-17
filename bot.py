import os
import json
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import LabeledPrice
from dotenv import load_dotenv
from games_logic import play_darts, init_mines, reveal_cell, roll_dice, spin_wheel

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_PROVIDER_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')
DATA_FILE = 'data/stats.json'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Загрузка/сохранение JSON
def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@dp.message(F.text == '/start')
async def cmd_start(msg: types.Message):
    kb = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('🎰 Открыть Казино', web_app=types.WebAppInfo(url=WEBAPP_URL)),
        types.InlineKeyboardButton('💳 Пополнить', callback_data='pay')
    )
    await msg.answer('Добро пожаловать в Казино!', reply_markup=kb)

@dp.callback_query(F.data == 'pay')
async def pay(query: types.CallbackQuery):
    prices = [LabeledPrice('Пополнение 100₽', 100*100)]
    await bot.send_invoice(query.from_user.id, 'Пополнение', '100₽ на баланс', 'payload', PAYMENTS_TOKEN, 'RUB', prices)

@dp.message(F.pre_checkout_query())
async def pre_checkout(q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

@dp.message(F.successful_payment)
async def success(msg: types.Message):
    data = load_data()
    data['payments'].append({'user': msg.from_user.id, 'amount': msg.successful_payment.total_amount, 'time': msg.date.timestamp()})
    save_data(data)
    await msg.answer('Платеж прошел успешно!')

@dp.message(F.web_app_data)
async def handle_game(msg: types.Message):
    params = json.loads(msg.web_app_data.data)
    game = params.get('game')
    if game == 'darts': res = play_darts(params['force'], params['angle'])
    elif game == 'mines':
        mines, counts = init_mines(params['size'], params['num_mines'])
        revealed = [[False]*params['size'] for _ in range(params['size'])]
        cells, ok = reveal_cell(mines, counts, revealed, params['i'], params['j'])
        res = {'cells': cells, 'ok': ok}
    elif game == 'dice': res = {'value': roll_dice()}
    elif game == 'wheel': res = spin_wheel(params['segments'])
    else: res = {'error': 'Unknown'}
    data = load_data()
    data['games'].append({'user': msg.from_user.id, 'game': game, 'result': res, 'time': msg.date.timestamp()})
    save_data(data)
    await msg.answer(f'Результат {game}: {res}')

if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))
