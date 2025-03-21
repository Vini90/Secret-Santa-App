#  Secret Santa gift exchange application

A Python-based web API for managing Secret Santa gift exchanges using FastAPI 
and MongoDB.

---

##  Features

-  Feature 1 (Add/Delete users)
-  Feature 2 (Get Users list)
-  Feature 3 (Generate randomized assignments)
-  Feature 4 (Get exchange history)
-  Feature 5 (REST API with documentation)

---

## 📁 Project Structure

```bash
Secret-Santa-App/
├── main.py
├── .mongo.env
├── requirements.txt
├── README.md
```

---

## 📦 Requirements

- Python 3.8+
- pip
- MongoDB (local installation steps below)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash

```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate 
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.mongo.env` file or edit config files as needed:

```env
# Example for MongoDB
MONGO_URI="mongodb://localhost:27017"
DB_NAME="secretsanta"
```

---

## 🍃 Installing MongoDB Locally

### ▶️ On macOS (using Homebrew)

```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### ▶️ On Ubuntu / Debian

```bash
sudo apt update
sudo apt install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### ▶️ On Windows

1. Download MongoDB Community Edition from:
   https://www.mongodb.com/try/download/community
2. Install with default settings
3. Start MongoDB service:
   ```bash
   net start MongoDB
   ```

> ✅ To verify installation:
```bash
mongo  or
mongosh
```

---

## ▶️ Running the App

```bash
uvicorn main:app --reload
```

---

## 📄 API Documentation

The docs are available at:

- Swagger UI: `http://localhost:8000/docs`
   (Check all features on this page)

---

## 🧪 Running Tests

```bash
pytest test_app.py -s
```

---