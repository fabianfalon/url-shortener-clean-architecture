# URL Shortener with Clean Architecture

This project is a simple URL shortener application built using **FastAPI** and following the principles of **Clean Architecture**. The aim of this project is to demonstrate how to structure a simple application while adhering to the principles of good design.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## Features

- Shorten long URLs for easier sharing
- Retrieve original URLs from shortened links
- Clean and modular architecture
- Fast and efficient with FastAPI
- Unit tests to ensure reliability

## Architecture

The application is structured using Clean Architecture principles, which promote a clear separation of concerns and modularity. The main components are:

- **Delivery Layer**: Handles HTTP requests and responses.
- **Domain Layer**: Defines the core business models and interfaces.
- **Application Layer**: Contains the business logic and application use cases.
- **Infrastructure Layer**: Manages external dependencies such as databases and external APIs.

This separation makes the codebase easier to maintain, test, and extend.

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
**Retrieve Original URL**
```http
GET /abc123
Content-Type: application/json
```
## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.