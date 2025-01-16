# Django Amazon Scraper

This project is a Django-based web application designed to scrape product information from Amazon. It utilizes Celery for asynchronous task processing, Selenium for browser automation, and Beautiful Soup for HTML parsing. This combination allows for efficient and reliable scraping of dynamic web content.

## Features

- **Amazon Product Scraping:** Extracts product details such as title, price, and availability.
- **Asynchronous Task Processing:** Employs Celery to manage scraping tasks in the background.
- **Scheduled Tasks:** Uses `django-celery-beat` to schedule periodic scraping operations.
- **Dynamic Content Handling:** Utilizes Selenium to interact with JavaScript-rendered content.
- **HTML Parsing:** Leverages Beautiful Soup to parse and extract data from HTML documents.
- **Result Storage:** Stores scraping results in the database for later retrieval and analysis.

## Prerequisites

Before setting up the project, ensure you have the following installed:

- **Python 3.8+**
- **Django**

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/django-amazon-scraper.git
   cd django-amazon-scraper
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Configure Environment Variables:**

   Create a `.env` file in the project root with the following content:

   ```env
   SECRET_KEY=your_secret_key
   DEBUG=True
   REDIS_URL=redis://127.0.0.1:6379/0
   ```

6. **Apply Migrations:**

   ```bash
   python manage.py migrate
   ```

7. **Create Superuser:**

   ```bash
   python manage.py createsuperuser
   ```

8. **Start Redis Server:**

   Ensure that the Redis server is running. If you have Docker installed, you can start Redis using:

   ```bash
   docker run --name redis-server -d -p 6379:6379 redis
   ```

9. **Start Celery Worker:**

   In a new terminal, activate the virtual environment and start the Celery worker:

   ```bash
   celery -A amazon_scraper worker --loglevel=info
   ```

10. **Start Django Development Server:**

    ```bash
    python manage.py runserver
    ```

## Usage


## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
