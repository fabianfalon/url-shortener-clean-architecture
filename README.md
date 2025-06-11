
# 🔗 URL Shortener with Clean Architecture & DDD

A ✨ **simple, elegant** URL shortener application built with **FastAPI**, following **Clean Architecture** and **Domain-Driven Design (DDD)** principles. This project demonstrates how to build a maintainable and scalable architecture while keeping things lightweight and developer-friendly.

---

## 📚 Table of Contents

- [🚀 Features](#-features)
- [🏗️ Architecture](#-architecture)
- [🧠 Domain-Driven Design](#domain-driven-design)
- [📁 Project Structure](#project-structure)
- [⚙️ Installation](#️-installation)
- [🌐 API Endpoints](#-api-endpoints)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

---

## 🚀 Features

- 🔗 Shorten long URLs for easier sharing.
- 📥 Retrieve original URLs from short codes.
- 🧱 Clean and modular architecture using DDD.
- ⚡ Built on **FastAPI** for speed and simplicity.
- ✅ Unit-tested for reliability.
- 🧩 Domain Events & Value Objects support.

---

## 🏗️ Architecture

The app follows **Clean Architecture**, dividing responsibilities across layers for separation of concerns:

- 🛣️ **Delivery Layer**: Handles HTTP requests with FastAPI.
- 🧠 **Domain Layer**: Business logic, entities, value objects, and domain events.
- ⚙️ **Application Layer**: Use cases and orchestrators.
- 🗄️ **Infrastructure Layer**: DB access and external APIs.

---

## 🧠 Domain-Driven Design

### 🧩 Aggregates
- `UrlAggregate`: Manages URL lifecycle.
  - 🔹 Root: `Url`
  - 🔹 Value Objects: `ShortCode`, `OriginalUrl`

### 🧪 Value Objects
- `ShortCode`: Shortened URL string
- `OriginalUrl`: Validated original URL

### 🛎️ Domain Events
- `UrlShortenedEvent`: Fired when a URL is shortened.
- `UrlAccessedEvent`: Triggered when a URL is accessed.

### 📦 Bounded Contexts
- URL Management (current context).

---

## 📁 Project Structure

```
src/
├── domain/           # Core business logic
│   ├── exceptions/
│   ├── value_objects.py
│   ├── url.py
│   ├── url_repository.py
│   └── events.py
├── application/      # Use cases & services
│   ├── create_short_url.py
│   ├── get_original_url.py
│   ├── get_url_stats.py
│   └── get_all_urls.py
├── infrastructure/   # DB and external service handling
│   ├── dto/
│   ├── storage/
│   ├── shortener/
│   └── events/
├── delivery/         # API layer with FastAPI
│   └── api/
│       ├── dependencies.py
│       └── routers.py
├── config.py        # Centralized configuration
└── main.py          # Main entry point
```

---

## ⚙️ Installation

### 🖥️ Local Setup

1. Clone the repository:

```bash
git clone https://github.com/fabianfalon/url-shortener-clean-architecture.git
cd url-shortener-clean-architecture
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
# or for dev and test support
pip install -r requirements-tests.txt
```

4. Run the app:

```bash
uvicorn app.main:app --reload
```

### 🐳 Docker Setup

```bash
docker-compose build
docker-compose up
```

---

## 🌐 API Endpoints

| Method | Endpoint              | Description               |
|--------|-----------------------|---------------------------|
| POST   | `/shorten`            | Shorten a long URL        |
| GET    | `/urls`               | List all shortened URLs   |
| GET    | `/{shortened_id}`     | Retrieve the original URL |
| GET    | `/{short_code}/stats` | Get URL statistics |
### 🔍 Example Requests

#### ➕ Shorten a URL

```http
POST /shorten
Content-Type: application/json

{
  "url": "https://example.com/some/long/url"
}
```

#### 📋 Get All Short URLs

```http
GET /urls
Content-Type: application/json

{
  "urls": [
    {
      "id": 1,
      "short_url": "abc123"
    }
  ]
}
```

#### 🔁 Retrieve Original URL

```http
GET /abc123
Content-Type: application/json
```

---

## 🤝 Contributing

Contributions are welcome! 🙌
Feel free to fork the repo and submit a pull request with improvements or bug fixes.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more details.