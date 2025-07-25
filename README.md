# Splitred 💸
**Splitred** is a simple web app to split expenses between friends in a fair and transparent way. You can create groups, track shared expenses, and automatically calculate who owes what to whom.

## ✨ Features

Managing group expenses during trips or events can be messy. SplitRed makes it easier by providing a clean interface and reliable backend logic to handle group balances. Splitred allows you to:

 - Create and manage groups of people
 - Add expenses indicating payer and participants
 - Automatically compute who owes what
 - View per-group debt summary
 - Responsive UI, mobile-friendly

---

## 🛠️ Tech Stack

### Frontend
- [Vite](https://vitejs.dev/)
- [React](https://reactjs.org/)
- [TypeScript](https://www.typescriptlang.org/)

### Backend
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)
- [Flask-Limiter](https://flask-limiter.readthedocs.io/)

---

## Backend

### Clone the repository
```
git clone https://github.com/your-username/splitred-backend.git
cd splitred-backend
```

### Create a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Create a .env file
```
touch .env
echo "DATABASE_URL=sqlite:///./splitred.db
FRONTEND_URL=http://localhost:5173" > .env
```

### Run Backend Server
```
flask run --host=0.0.0.0 --port=5000
```

### If you encounter with problems finding folders of the app, maybe running this you fix it:
```
export PYTHONPATH=$(pwd)
```

---

## Frontend

### Install dependencies
```
cd frontend
npm install
```

### Create a .env file
```
touch .env
echo "VITE_BACKEND_URL=http://localhost:5000" > .env
```

### Run Frontend Server
```
npm run dev
```
