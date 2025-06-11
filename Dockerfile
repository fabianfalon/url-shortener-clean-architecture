FROM python:3.12.7-alpine

WORKDIR /app

# Instalar dependencias del sistema necesarias
RUN apk add --no-cache gcc musl-dev linux-headers

# Copiar requirements primero para aprovechar la caché de Docker
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000

# Ejecuta la aplicación FastAPI cuando se inicie el contenedor
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]