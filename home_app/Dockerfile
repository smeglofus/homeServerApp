# Použití oficiálního Python image
FROM python:3.11-slim

# Nastavení pracovního adresáře v kontejneru
WORKDIR /app

# Zkopírujte soubory projektu do kontejneru
COPY . /app

# Nainstalujte závislosti
RUN pip install --no-cache-dir -r requirements.txt

# Exponujte port 8000
EXPOSE 8000

# Příkaz pro spuštění serveru
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "home_app.wsgi:application"]
