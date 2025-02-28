# HomeServerApp - Fermentator

## 📌 O projektu
HomeServerApp je systém pro řízení a sledování fermentace v domácím fermentačním boxu. 
Hlavní částí je aplikace **Fermentator**, která sbírá a vizualizuje data ze senzoru a umožňuje řídit teplotu v boxu.

## ⚙️ Jak to funguje
Fermentační box obsahuje **ESP32** s čidlem **DHT11**, které měří teplotu a vlhkost. ESP32 ovládá relé, které spíná topné těleso. 
Data jsou odesílána na **Raspberry Pi**, kde běží několik **Docker kontejnerů**:
- **Nginx** (reverzní proxy)
- **Django** (backend a API pro řízení fermentace)
- **PostgreSQL** (databáze)
- **PgAdmin** (webové rozhraní pro správu databáze)

Na **frontendové straně** lze sledovat:
- Aktuální teplotu a vlhkost v boxu
- Graf s průběhem fermentace
- Správu fermentačních várek (*FermentBatch*)
- Možnost vzdáleně řídit teplotu

## 🚀 Instalace
### 1️⃣ Klonování repozitáře
```sh
git clone https://github.com/uzivatel/HomeServerApp.git
cd HomeServerApp
```

### 2️⃣ Konfigurace prostředí
Vytvořte soubor `.env` a nastavte proměnné (například **SECRET_KEY**, databázové přístupy apod.).

### 3️⃣ Spuštění v Dockeru
```sh
DJANGO_ENV=docker docker-compose up --build
```

## 🛠 Technologie
- **Python** (Django)
- **JavaScript** (Graf teplot a vlhkosti)
- **PostgreSQL** (databáze)
- **Docker** (kontejnerizace)
- **ESP32** (senzorová část)
- **Raspberry Pi** (server)

## 📋 TODO
- [ ] Implementovat vhodnější frontend
- [ ] Přidat uživatelskou autentizaci
- [ ] Export historických dat do jednotlivých FermentBatchů

## 📜 Licence
Tento projekt je licencován pod licencí **MIT**.

## 📷 Screenshoty a fotky
Připravuji fotky fermentačního boxu a screenshoty aplikace.

---
📌 *Projekt je stále v rané fázi vývoje. Máte nápady na vylepšení? Neváhejte přispět!* 😊
