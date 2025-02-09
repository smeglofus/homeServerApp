# Použití oficiálního Python image
FROM python:3.11-slim

# Instalace PostgreSQL knihoven
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


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
