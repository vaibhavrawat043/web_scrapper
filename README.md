# FastAPI Web Scraper

This project is a web scraper built using FastAPI, Selenium, BeautifulSoup, and Redis. The scraper fetches product details from a given website, caches the results, and stores the data in a local JSON file.

## Features

- Scrapes product details including title, price, and image URL.
- Supports pagination.
- Caches results using Redis to avoid redundant updates.
- Stores the scraped data in a local JSON file.
- Notifies the user about the scraping results.

## Requirements

- Python 3.7+
- Redis server
- Chrome browser
- ChromeDriver

## Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Download ChromeDriver**:
    - Download ChromeDriver from [ChromeDriver Download](https://sites.google.com/a/chromium.org/chromedriver/downloads)
    - Extract the `chromedriver` executable to the `app/` directory.

5. **Ensure ChromeDriver has execute permissions**:
    ```sh
    chmod +x app/chromedriver
    ```

6. **Start Redis server**:
    ```sh
    redis-server
    ```

## Configuration

- Update the `config.py` file with your base URL and static token:
    ```python
    BASE_URL = "https://dentalstall.com/shop/"
    STATIC_TOKEN = "your-static-token"
    ```

## Running the Application

1. **Run the FastAPI application**:
    ```sh
    uvicorn app.main:app --reload
    ```

2. **Access the API**:
    - Open your browser and go to: `http://127.0.0.1:8000/docs` to see the API documentation and test the endpoints.

## API Endpoints

- **POST /scrape**
    - **Description**: Scrapes the website and returns the number of products updated.
    - **Request Body**:
        ```json
        {
            "pages": 5,
            "proxy": null
        }
        ```
    - **Headers**: 
        ```json
        {
            "x-token": "your-static-token"
        }
        ```
    - **Response**:
        ```json
        {
            "message": "Scraped X products"
        }
        ```

- **GET /test-header**
    - **Description**: Verifies the static token in the header.
    - **Headers**: 
        ```json
        {
            "x-token": "your-static-token"
        }
        ```
    - **Response**:
        ```json
        {
            "message": "Header is valid"
        }
        ```


