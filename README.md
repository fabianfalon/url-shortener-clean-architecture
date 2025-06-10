# URL Shortener with Clean Architecture and DDD

This project is a simple URL shortener application built using **FastAPI** and following the principles of **Clean Architecture** and **Domain-Driven Design (DDD)**. The aim of this project is to demonstrate how to structure a simple application while adhering to the principles of good design and DDD patterns.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Domain-Driven Design](#domain-driven-design)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- Shorten long URLs for easier sharing
- Retrieve original URLs from shortened links
- Clean and modular architecture following DDD principles
- Fast and efficient with FastAPI
- Unit tests to ensure reliability
- Domain events for side effects
- Value Objects for domain concepts

## Architecture

The application is structured using Clean Architecture principles and DDD patterns, which promote a clear separation of concerns and modularity. The main components are:

- **Delivery Layer**: Handles HTTP requests and responses using FastAPI.
- **Domain Layer**: Contains the core business models, value objects, and domain events.
- **Application Layer**: Implements use cases and orchestrates domain objects.
- **Infrastructure Layer**: Manages external dependencies such as databases and external APIs.

## Domain-Driven Design

### Aggregates
- **UrlAggregate**: Manages the lifecycle of URL entities and ensures consistency rules
  - Root Entity: Url
  - Value Objects: ShortCode, OriginalUrl

### Value Objects
- **ShortCode**: Represents the shortened URL code
- **OriginalUrl**: Represents the original URL with validation

### Domain Events
- **UrlShortenedEvent**: Triggered when a new URL is shortened
- **UrlAccessedEvent**: Triggered when a shortened URL is accessed

### Bounded Contexts
Currently, the application operates within a single bounded context: URL Management.

## Project Structure

```
src/
├── domain/           # Domain layer
│   ├── entities/     # Domain entities
│   ├── value_objects/# Value objects
│   └── events/       # Domain events
├── application/      # Application layer
│   ├── services/     # Use cases
│   └── interfaces/   # Ports
├── infrastructure/   # Infrastructure layer
│   ├── persistence/  # Database implementations
│   └── external/     # External service implementations
└── delivery/         # Delivery layer
    └── api/          # FastAPI endpoints
```

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:

    ```git clone https://github.com/fabianfalon/url-shortener-clean-architecture.git```

2. Create a virtual environment:

   ````python -m venv venv source venv/bin/activate````

3. Install the required dependencies:

   ````pip install -r requirements.txt```` or  ````pip install -r requirements-tests.txt````

4. To run the application, use the following command:

    ````uvicorn app.main:app --reload````

To set up with docker
1. ````docker-compose build````

2. ````docker-compose up````


## API Endpoints

- **POST /shorten**: Shortens a given URL.
- **GET /urls**: Get all urls.
- **GET /{shortened_id}**: Retrieves the original URL from a shortened ID.

### Example Requests

**Shorten a URL**

```http
POST /shorten
Content-Type: application/json

{
    "url": "https://example.com/some/long/url"
}
```
**Get short URLS**
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
**Retrieve Original URL**
```http
GET /abc123
Content-Type: application/json
```
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.