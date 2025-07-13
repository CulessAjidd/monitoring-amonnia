# Monitoring Amonia Dashboard

Step - step panduan isntalasi aplikasi flask

## ⚙️ Instalasi & Setup




```bash
git clone https://github.com/CulessAjidd/monitoring-amonnia.git
```
```bash
cd monitoring-amonnia
```

### 2. Buat virtual environtment
```bash
python -m venv venv
```

```bash
venv\Scripts\activate
```

### 3. Install library
```bash
pip install -r requirements.txt
```

### 4. Buat .env file
```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

### 5. Jalankan migrate database
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 6. Jalankan aplikasi
```bash
flask run
```

Buka http://localhost:5000
