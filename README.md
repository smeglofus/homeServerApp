# 🍶 HomeServerApp - Fermentator

## 📖 About the Project
HomeServerApp is a fermentation monitoring and control system. The core application, *Fermentator*, allows you to track and manage the fermentation process using IoT technology. 

An ESP32 microcontroller, equipped with a DHT11 sensor and a relay for heating control, collects temperature and humidity data. This data is sent to a Raspberry Pi server, which runs multiple Docker containers:

- **Nginx** (Reverse Proxy)
- **Django** (Backend API)
- **PostgreSQL** (Database)
- **PgAdmin** (Database Management)

Through the Django web application, you can:
- Monitor real-time temperature and humidity readings 📊
- View historical fermentation data
- Start new fermentation batches
- Adjust the heating system remotely via API

## ⚙️ Technologies Used
- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Frontend**: Django Templates (to be improved)
- **IoT**: ESP32, DHT11 Sensor, Relay Module
- **Infrastructure**: Raspberry Pi, Docker, Docker Compose, Nginx

## 🚀 Getting Started
### 1️⃣ Clone the Repository
```bash
 git clone https://github.com/yourusername/homeserverapp.git
 cd homeserverapp
```

### 2️⃣ Set up Environment Variables
Create a `.env` file and configure:
```env
SECRET_KEY=your-secret-key
DJANGO_ENV=local/docker
DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost
DATABASE_URL=postgres://user:password@db:5432/dbname

DB_NAME=dbname
DB_USER=user
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

### 3️⃣ Start the Application
```bash
docker-compose up --build
```

### 4️⃣ Access the Application
- **Web App**: `http://localhost:8000`
- **PgAdmin**: `http://localhost:5050`

## 📋 TODO
- [ ] Implement a more user-friendly frontend
- [ ] Add user authentication
- [ ] Export historical data for individual FermentBatches

## 📄 License
This project is licensed under the MIT License.

## 📸 Screenshots (Coming Soon)
Images of the physical fermentation box and UI will be added.

---

🇨🇿 Pro českou verzi si přečtěte `README_CS.md`.
