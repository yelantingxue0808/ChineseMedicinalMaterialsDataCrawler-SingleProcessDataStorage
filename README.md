# Chinese Medicinal Materials Data Crawler

A high\-efficiency crawler for scraping Chinese medicinal materials price data from [zyctd\.com](https://www.zyctd.com), implemented with **multi\-process**, **async coroutine** and **single\-process data storage** to balance performance and data consistency\.

## Project Overview

This project crawls medicinal materials price data \(including product name, specification, market, price, trend, etc\.\) from the [zyctd\.com](https://zyctd.com) price page\. It leverages multi\-process to parallelize URL processing, async coroutine \(asyncio \+ aiohttp\) for high\-speed HTTP requests, and a single process to save data to MySQL to avoid concurrent write conflicts\.

## Project Structure

```Plain Text
├── config/                  # Configuration files
│   ├── db_settings.py       # Database connection config (MySQL)
│   ├── https_settings.py    # HTTP request headers
│   ├── logging_settings.py  # Logging config (path/name)
│   └── settings.py          # URL/page split config
├── core/                    # Core business logic
│   ├── handler.py           # Async request/parsing + process task logic
│   └── service.py           # Multi-process orchestration
├── dao/                     # Data access layer
│   ├── database.py          # Singleton MySQL connection
│   └── save_data.py         # Single-process data storage
├── utils/                   # Utility functions
│   ├── logger.py            # Logging initialization
│   └── utils.py             # URL generation/split + SQL builder
├── main.py                  # Entry point of the project
└── log/                     # Log files (auto-generated)
    └── logger.log
```

## Key Features

- **Multi\-process Parallelism**: Split 122 pages of URLs into 4 chunks and process them in parallel with multiple processes\.

- **Async Coroutine Requests**: Use `asyncio` \+ `aiohttp` for non\-blocking HTTP requests to improve crawling efficiency\.

- **Single\-process Data Storage**: Use a dedicated process to read data from the multiprocessing queue and insert into MySQL \(avoids concurrent write issues\)\.

- **Comprehensive Logging**: Log request/parsing/storage details to both console and log file\.

- **Configurable Design**: Centralized configuration for URLs, database, logging, and HTTP headers \(easy to modify\)\.

- **Robust Error Handling**: Exception handling for data parsing and database operations \(with transaction rollback\)\.

## Environment Requirements

Install the required dependencies via pip:

```bash
pip install pymysql aiohttp lxml
```

## Configuration Instructions

### 1\. Database Configuration \(`config/db_settings.py`\)

Update MySQL connection info to match your local environment:

```python
DB_CONNECT_CONFIG = {
    'host': 'localhost',       # Your MySQL host
    'user': 'root',            # Your MySQL username
    'password': '123456',      # Your MySQL password
    'database': 'text3'        # Target database name (create first)
}
```

### 2\. Crawler Configuration \(`config/settings.py`\)

Adjust the page range/URL split size:

```python
URL = "https://www.zyctd.com/jiage/1-0-0-{}.html"  # Target URL template

class PageConfig:
    START = 0       # Start page (0-based)
    STOP = 122      # End page
    STEP = 35       # Chunk size for URL splitting (35 URLs per process)
```

### 3\. Logging Configuration \(`config/logging_settings.py`\)

Modify log file path/name if needed:

```python
LOGGER_NAME = "process_name"
LOGGER_PATH = './log'                  # Log directory
LOGGER_path_FILE = os.path.join(LOGGER_PATH, 'logger.log')  # Log file path
```

### 4\. HTTP Headers \(`config/https_settings.py`\)

Update User\-Agent to avoid anti\-crawling:

```python
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}
```

## How to Use

### 1\. Prepare MySQL Database

Create the target database and table first:

```sql
CREATE DATABASE IF NOT EXISTS text3 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE text3;

CREATE TABLE IF NOT EXISTS medical_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    品名 VARCHAR(255) NOT NULL,
    规格 VARCHAR(255),
    市场 VARCHAR(255),
    价格 VARCHAR(50),
    趋势 VARCHAR(50),
    周涨跌 VARCHAR(50),
    月涨跌 VARCHAR(50),
    年涨跌 VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### 2\. Run the Crawler

Execute the entry file:

```bash
python main.py
```

## Core Workflow

1. **URL Generation**: Generate all target URLs based on the page range in `settings.py`\.

2. **URL Splitting**: Split the URL list into chunks \(35 URLs/chunk\) for multi\-process processing\.

3. **Multi\-process \+ Coroutine Crawling**:

   - Each process runs async coroutines to send HTTP requests and parse HTML \(via lxml/XPath\)\.

   - Parsed data is put into a multiprocessing queue\.

4. **Single\-process Storage**:

   - A dedicated process reads data from the queue and inserts it into MySQL \(truncates old data first\)\.

   - Uses transaction commit/rollback to ensure data integrity\.

## Notes

- **Anti\-Crawling**: The `asyncio.sleep(0.5)` in `handler.py` controls request frequency \(adjust based on website anti\-crawl rules\)\.

- **Log Files**: All logs are stored in `./log/logger.log` \(auto\-created if the directory does not exist\)\.

- **Data Consistency**: Using a single process for data storage avoids concurrent write conflicts in MySQL\.

- **Error Handling**: Any parsing/database errors are logged \(check logs for troubleshooting\)\.

## License

This project is for learning and research purposes only\. Please comply with the website\&\#39;s robots\.txt and relevant laws/regulations when using it\.

A high\-efficiency crawler for scraping Chinese medicinal materials price data from [zyctd\.com](https://www.zyctd.com), implemented with **multi\-process**, **async coroutine** and **single\-process data storage** to balance performance and data consistency\.

## Project Overview

This project crawls medicinal materials price data \(including product name, specification, market, price, trend, etc\.\) from the [zyctd\.com](https://zyctd.com) price page\. It leverages multi\-process to parallelize URL processing, async coroutine \(asyncio \+ aiohttp\) for high\-speed HTTP requests, and a single process to save data to MySQL to avoid concurrent write conflicts\.

## Project Structure

```Plain Text
├── config/                  # Configuration files
│   ├── db_settings.py       # Database connection config (MySQL)
│   ├── https_settings.py    # HTTP request headers
│   ├── logging_settings.py  # Logging config (path/name)
│   └── settings.py          # URL/page split config
├── core/                    # Core business logic
│   ├── handler.py           # Async request/parsing + process task logic
│   └── service.py           # Multi-process orchestration
├── dao/                     # Data access layer
│   ├── database.py          # Singleton MySQL connection
│   └── save_data.py         # Single-process data storage
├── utils/                   # Utility functions
│   ├── logger.py            # Logging initialization
│   └── utils.py             # URL generation/split + SQL builder
├── main.py                  # Entry point of the project
└── log/                     # Log files (auto-generated)
    └── logger.log
```

## Key Features

- **Multi\-process Parallelism**: Split 122 pages of URLs into 4 chunks and process them in parallel with multiple processes\.

- **Async Coroutine Requests**: Use `asyncio` \+ `aiohttp` for non\-blocking HTTP requests to improve crawling efficiency\.

- **Single\-process Data Storage**: Use a dedicated process to read data from the multiprocessing queue and insert into MySQL \(avoids concurrent write issues\)\.

- **Comprehensive Logging**: Log request/parsing/storage details to both console and log file\.

- **Configurable Design**: Centralized configuration for URLs, database, logging, and HTTP headers \(easy to modify\)\.

- **Robust Error Handling**: Exception handling for data parsing and database operations \(with transaction rollback\)\.

## Environment Requirements

Install the required dependencies via pip:

```bash
pip install pymysql aiohttp lxml
```

## Configuration Instructions

### 1\. Database Configuration \(`config/db_settings.py`\)

Update MySQL connection info to match your local environment:

```python
DB_CONNECT_CONFIG = {
    'host': 'localhost',       # Your MySQL host
    'user': 'root',            # Your MySQL username
    'password': '123456',      # Your MySQL password
    'database': 'text3'        # Target database name (create first)
}
```

### 2\. Crawler Configuration \(`config/settings.py`\)

Adjust the page range/URL split size:

```python
URL = "https://www.zyctd.com/jiage/1-0-0-{}.html"  # Target URL template

class PageConfig:
    START = 0       # Start page (0-based)
    STOP = 122      # End page
    STEP = 35       # Chunk size for URL splitting (35 URLs per process)
```

### 3\. Logging Configuration \(`config/logging_settings.py`\)

Modify log file path/name if needed:

```python
LOGGER_NAME = "process_name"
LOGGER_PATH = './log'                  # Log directory
LOGGER_path_FILE = os.path.join(LOGGER_PATH, 'logger.log')  # Log file path
```

### 4\. HTTP Headers \(`config/https_settings.py`\)

Update User\-Agent to avoid anti\-crawling:

```python
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
}
```

## How to Use

### 1\. Prepare MySQL Database

Create the target database and table first:

```sql
CREATE DATABASE IF NOT EXISTS text3 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE text3;

CREATE TABLE IF NOT EXISTS medical_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    品名 VARCHAR(255) NOT NULL,
    规格 VARCHAR(255),
    市场 VARCHAR(255),
    价格 VARCHAR(50),
    趋势 VARCHAR(50),
    周涨跌 VARCHAR(50),
    月涨跌 VARCHAR(50),
    年涨跌 VARCHAR(50)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

### 2\. Run the Crawler

Execute the entry file:

```bash
python main.py
```

## Core Workflow

1. **URL Generation**: Generate all target URLs based on the page range in `settings.py`\.

2. **URL Splitting**: Split the URL list into chunks \(35 URLs/chunk\) for multi\-process processing\.

3. **Multi\-process \+ Coroutine Crawling**:

   - Each process runs async coroutines to send HTTP requests and parse HTML \(via lxml/XPath\)\.

   - Parsed data is put into a multiprocessing queue\.

4. **Single\-process Storage**:

   - A dedicated process reads data from the queue and inserts it into MySQL \(truncates old data first\)\.

   - Uses transaction commit/rollback to ensure data integrity\.

## Notes

- **Anti\-Crawling**: The `asyncio.sleep(0.5)` in `handler.py` controls request frequency \(adjust based on website anti\-crawl rules\)\.

- **Log Files**: All logs are stored in `./log/logger.log` \(auto\-created if the directory does not exist\)\.

- **Data Consistency**: Using a single process for data storage avoids concurrent write conflicts in MySQL\.

- **Error Handling**: Any parsing/database errors are logged \(check logs for troubleshooting\)\.

## License

This project is for learning and research purposes only\. Please comply with the website\&\#39;s robots\.txt and relevant laws/regulations when using it\.
