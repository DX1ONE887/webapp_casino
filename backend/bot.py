import os
import json
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import LabeledPrice, WebAppInfo
from games_logic import play_darts, init_mines, reveal_cell, roll_dice, spin_wheel

# Загрузка переменных окружения из .env
load_dotenv()
BOT_TOKEN    = os.getenv('BOT_TOKEN')
PAYMENTS_TOKEN = os.getenv('PAYMENTS_PROVIDER_TOKEN')
WEBAPP_URL   = os.getenv('WEBAPP_URL')  # URL, где хостится ваш MiniApp
DATA_FILE    = 'data/stats.json'

# Логирование
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp  = Dispatcher()

# Утилиты для работы с JSON-файлом статистики
def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# /start — выдаём кнопку для открытия MiniApp и пополнения
@dp.message(F.text == '/start')
async def cmd_start(msg: types.Message):
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton(
            '🎰 Открыть Казино',
            web_app=WebAppInfo(url=WEBAPP_URL)
        ),
        types.InlineKeyboardButton(
            '💳 Пополнить баланс',
            callback_data='pay'
        )
    )
    await msg.answer(
        'Добро пожаловать в Казино! Нажмите кнопку ниже, чтобы начать:',
        reply_markup=kb
    )

# Кнопка «Пополнить»
@dp.callback_query(F.data == 'pay')
async def process_pay(query: types.CallbackQuery):
    prices = [LabeledPrice(label='Пополнение 100₽', amount=100 * 100)]
    await bot.send_invoice(
        chat_id=query.from_user.id,
        title='Пополнение баланса',
        description='Добавьте 100 рублей на баланс',
        payload='topup_100',
        provider_token=PAYMENTS_TOKEN,
        currency='RUB',
        prices=prices,
        start_parameter='topup'
    )
    await query.answer()

# Подтверждение pre-checkout
@dp.pre_checkout_query()
async def process_pre_checkout(q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(q.id, ok=True)

# Успешная оплата
@dp.message(F.successful_payment)
async def process_success_payment(msg: types.Message):
    data = load_data()
    payment = msg.successful_payment
    data['payments'].append({
        'user_id': msg.from_user.id,
        'amount': payment.total_amount,
        'currency': payment.currency,
        'time': msg.date.timestamp()
    })
    save_data(data)
    await msg.answer('✅ Платеж успешно обработан! Спасибо за пополнение.')

# Обработка данных из WebApp (игры и оплата)
@dp.message(F.web_app_data)
async def handle_webapp(msg: types.Message):
    payload = json.loads(msg.web_app_data.data)
    action = payload.get('action')
    result = None

    # Оплата из WebApp
    if action == 'pay':
        prices = [LabeledPrice(label='Пополнение 100₽', amount=100 * 100)]
        await bot.send_invoice(
            chat_id=msg.chat.id,
            title='Пополнение баланса',
            description='Добавьте 100 рублей на баланс',
            payload='topup_100',
            provider_token=PAYMENTS_TOKEN,
            currency='RUB',
            prices=prices,
            start_parameter='topup'
        )
        return

    # Игры
    if action == 'darts':
        force = float(payload.get('force', 0))
        angle = float(payload.get('angle', 0))
        result = play_darts(force, angle)

    elif action == 'mines':
        size      = int(payload.get('size', 5))
        num_mines = int(payload.get('num_mines', 5))
        i = int(payload.get('i', 0))
        j = int(payload.get('j', 0))
        mines, counts = init_mines(size, num_mines)
        revealed = [[False]*size for _ in range(size)]
        cells, ok = reveal_cell(mines, counts, revealed, i, j)
        result = {'cells': cells, 'ok': ok}

    elif action == 'dice':
        result = {'value': roll_dice()}

    elif action == 'wheel':
        segments = payload.get('segments', ['10','20','50','x2','0','100'])
        result = spin_wheel(segments)

    else:
        await msg.answer('❗️ Неизвестное действие.')
        return

    # Сохраняем результат игры
    data = load_data()
    data['games'].append({
        'user_id': msg.from_user.id,
        'action': action,
        'result': result,
        'time': msg.date.timestamp()
    })
    save_data(data)

    # Отвечаем пользователю
    await msg.answer(f'🎲 Результат игры «{action}»: {result}')

# Запуск поллинга
if __name__ == '__main__':
    import asyncio
    asyncio.run(dp.start_polling(bot))
