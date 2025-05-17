import os, json
from flask import Flask, render_template, request, redirect, url_for, abort
from dotenv import load_dotenv

load_dotenv()
ADMIN_TOKEN = os.getenv('ADMIN_TOKEN', 'secret123')
DATA_FILE = 'data/stats.json'

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    token = request.args.get('token')
    if token != ADMIN_TOKEN:
        abort(403)
    data = load_data()
    if request.method == 'POST':
        if request.form.get('action') == 'clear':
            data = {'games': [], 'payments': []}
            save_data(data)
        return redirect(url_for('admin') + f'?token={token}')
    return render_template('admin.html', data=data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
