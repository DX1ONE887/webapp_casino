bot.command('start', async (ctx) => {
    const user = users[ctx.from.id];
    const html = `
    <div class="container">
        <div class="balance">
            🏦 Ваш баланс: ${user.balance} ₽
        </div>
        
        <div class="game-section">
            <h2>🎰 Игровые автоматы</h2>
            <a href="/slot" class="btn btn-primary">Играть в слоты</a>
            <a href="/dice" class="btn btn-primary">Кости</a>
        </div>

        <div class="game-section">
            <h2>🎮 Другие игры</h2>
            <a href="/basket" class="btn btn-warning">Баскетбол</a>
            <a href="/football" class="btn btn-warning">Футбол</a>
        </div>

        <div class="game-section">
            <h2>⚙️ Управление</h2>
            <a href="/deposit" class="btn btn-primary">💰 Пополнить баланс</a>
            <a href="/withdraw" class="btn btn-danger">💸 Вывести средства</a>
            ${user.isAdmin ? '<a href="/admin" class="btn btn-warning">👑 Админ-панель</a>' : ''}
        </div>
    </div>
    `;
    await ctx.replyWithHTML(html);
});
