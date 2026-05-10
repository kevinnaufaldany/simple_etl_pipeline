# 🛍️ Fashion Data Pipeline - ETL Project

> **A comprehensive data engineering project demonstrating Extract, Transform, and Load (ETL) operations on fashion product data**

## 📋 Project Overview

This is a submission project for Dicoding's "Fundamental Data Processing" course. It's a complete **ETL (Extract-Transform-Load) pipeline** that automatically scrapes fashion product data from a website, transforms it to ensure data consistency, and loads it into multiple storage systems (CSV, Google Sheets, and PostgreSQL).

### What This Project Demonstrates

As your first data engineering portfolio project, this demonstrates your ability to:
- ✅ **Web Scraping & Data Extraction** - Retrieve structured data from HTML using BeautifulSoup
- ✅ **Data Transformation** - Clean, validate, and convert data formats
- ✅ **Multi-destination Loading** - Export data to CSV, cloud storage (Google Sheets), and databases
- ✅ **Code Organization** - Professional structure with separation of concerns
- ✅ **Error Handling** - Robust exception handling and graceful fallbacks
- ✅ **Testing** - Unit tests with pytest for code reliability
- ✅ **Database Management** - PostgreSQL setup and data persistence

---

## 🏗️ Project Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FASHION DATA PIPELINE                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────┐
         │      EXTRACT (Web Scraping)      │
         │  • Fetch HTML from website       │
         │  • Parse product information     │
         │  • Multi-page pagination         │
         └──────────────────────────────────┘
                            │
                            ▼
         ┌──────────────────────────────────┐
         │    TRANSFORM (Data Processing)   │
         │  • Currency conversion           │
         │  • Type conversion               │
         │  • Column reordering             │
         └──────────────────────────────────┘
                            │
                ┌───────────┼───────────┐
                ▼           ▼           ▼
            ┌────────┐ ┌─────────┐ ┌──────────┐
            │  CSV   │ │ Sheets  │ │PostgreSQL│
            │ File   │ │ Cloud   │ │ Database │
            └────────┘ └─────────┘ └──────────┘
```

---

## 📁 Project Structure

```
web-submit/
├── main.py                    # Main orchestrator (Extract → Transform → Load)
├── setup_postgre.py           # PostgreSQL database initialization
├── pytest.ini                 # Pytest configuration
├── requirements.txt           # Python dependencies
├── client_secret.json         # Google Sheets credentials (optional)
├── fashion_data.csv           # Output CSV file
│
├── utils/                     # Core modules
│   ├── __init__.py
│   ├── extract.py            # Web scraping logic
│   ├── transform.py          # Data transformation logic
│   └── load.py               # Data export logic
│
└── tests/                     # Unit tests
    ├── __init__.py
    ├── test_extract.py       # Tests for extraction functions
    ├── test_transform.py     # Tests for transformation functions
    └── test_load.py          # Tests for loading functions
```

---

## 🔍 Module Breakdown

### 1. **Extract Module** (`utils/extract.py`)

**Purpose:** Fetches and parses fashion product data from the website

**Key Functions:**
- `fetching_content(url)` - Retrieves HTML content from a given URL with error handling
- `extract_fashion_data(card)` - Parses individual product information from HTML elements
- `scrape_fashion_data(base_url, start_page=1, delay=2)` - Orchestrates multi-page scraping

**Data Extracted Per Product:**
- `title` - Product name
- `price` - Price in USD (e.g., "$99.99")
- `rating` - Product rating (e.g., 4.5)
- `colors` - Number of available colors
- `size` - Available sizes
- `gender` - Target gender category
- `timestamp` - When the data was scraped

**Features:**
- Handles pagination automatically
- Includes delay between requests (2 seconds default) to be respectful to servers
- Regex-based parsing for flexible HTML structure handling
- Comprehensive error handling with informative messages

### 2. **Transform Module** (`utils/transform.py`)

**Purpose:** Cleans and standardizes the extracted data

**Transformations Applied:**

1. **Currency Conversion**
   - Strips `$` symbol from price strings
   - Converts to float type
   - Multiplies by exchange rate (default: 16,000 IDR/USD) to get price in Rupiah

2. **Data Type Conversion**
   - `rating` → float (decimal values)
   - `colors` → int64 (whole numbers)
   - Text fields → maintained as strings

3. **Column Organization**
   - Reorders columns to: `title`, `price`, `rating`, `colors`, `size`, `gender`, `timestamp`
   - Removes intermediate columns (price_in_dollars)

**Key Function:**
- `transform_data(data, exchange_rate)` - Applies all transformations in pipeline fashion

### 3. **Load Module** (`utils/load.py`)

**Purpose:** Exports processed data to multiple destinations

**Supported Outputs:**

#### a) **CSV Export** (`load_to_csv`)
- Simple local file storage
- Most portable format
- Easy to share and open in Excel

#### b) **Google Sheets** (`load_to_spreetsheet`)
- Cloud-based collaborative storage
- Requires Google OAuth credentials
- Automatically clears and updates sheet data
- Type conversion for compatibility

#### c) **PostgreSQL** (`store_to_postgre`)
- Relational database storage
- Suitable for large-scale data operations
- Enables SQL querying and analytics
- Uses SQLAlchemy for connection management

**Error Handling:**
- Graceful fallbacks if credentials are missing
- Detailed error messages for debugging
- Continues pipeline even if one destination fails

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- PostgreSQL (optional, for database storage)
- Google Account (optional, for Google Sheets integration)

### Installation

1. **Clone/Extract the project**
```bash
cd web-submit
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

### 📦 Dependencies

```
pandas>=1.3.0              # Data manipulation and analysis
requests>=2.26.0          # HTTP library for web requests
beautifulsoup4>=4.9.3     # HTML/XML parsing
sqlalchemy>=1.4.0         # Database ORM
psycopg2-binary>=2.9.0    # PostgreSQL adapter
gspread>=5.0.0            # Google Sheets API client
gspread-dataframe>=3.2.0  # Google Sheets DataFrame integration
google-auth-oauthlib>=0.4.6        # Google authentication
google-auth-httplib2>=0.1.0        # Google auth helpers
pytest>=7.0.0             # Testing framework
pytest-cov>=3.0.0         # Test coverage reporting
coverage>=6.0             # Coverage measurement
mock>=4.0.3               # Mocking for tests
```

---

## 🔧 Configuration & Setup

### Step 1: PostgreSQL Setup (One-time)

If you want to use PostgreSQL as a data destination:

```bash
python setup_postgre.py
```

**What this does:**
- Creates database: `db_fashion`
- Creates user: `developer` (password: `developer`)
- Grants all privileges to the developer user
- Handles idempotent operations (safe to run multiple times)

**Expected output:**
```
Setup database PostgreSQL untuk Fashion Scraper...
==============================================

Connected ke PostgreSQL sebagai postgres
Database 'db_fashion' sudah ada.
User 'developer' sudah ada, skip create.
```

### Step 2: Google Sheets Setup (Optional)

To enable Google Sheets integration:

1. Create a Google Cloud project
2. Enable Google Sheets API
3. Create a service account and download the JSON credentials
4. Save credentials as `client_secret.json` in the project root
5. Share the Google Sheet with the service account email

---

## ▶️ Running the Pipeline

### Execute the Full ETL Pipeline

```bash
python main.py
```

**Process Flow:**

1. **EXTRACT** - Scrapes all fashion products from the website
   - Displays: Raw data preview and row count
   
2. **TRANSFORM** - Cleans and standardizes the data
   - Currency conversion applied
   - Data types corrected
   - Columns reordered

3. **LOAD** - Exports to all configured destinations
   - Saves to CSV file
   - Uploads to Google Sheets (if credentials available)
   - Stores in PostgreSQL (if database is running)

**Example Output:**
```
EXTRACT: Melakukan web scraping...
DataFrame berhasil dibuat dengan shape: (150, 7)

Preview data (sebelum transformasi):
   title          price  rating  colors       size  gender   timestamp
0  Blue Jacket   $99.99     4.5      3    M, L, XL   Male   2024-01-15 10:30:00
...

TRANSFORM: Melakukan transformasi data...
DataFrame setelah transformasi dengan shape: (150, 7)

Preview data (setelah transformasi):
   title    price  rating  colors      size  gender
0  Blue Jacket  1599840  4.5      3   M, L, XL   Male
...

LOAD: Menyimpan data...
Data berhasil disimpan ke fashion_data.csv
Data berhasil disimpan ke Google Sheets: scraping
Data berhasil ditambahkan ke PostgreSQL!
```

---

## 🧪 Running Tests

This project includes comprehensive unit tests to ensure code reliability:

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=utils

# Run specific test file
pytest tests/test_extract.py -v

# Run with verbose output
pytest -v
```

**Test Coverage:**
- **test_extract.py** - Web scraping functionality and error handling
- **test_transform.py** - Data transformation and type conversion
- **test_load.py** - Export functionality (CSV, Google Sheets, PostgreSQL)

---

## 💡 Key Technical Insights

### 1. **Web Scraping Best Practices**
- Uses headers to mimic browser requests (avoid being blocked)
- Implements delay between requests (respectful to servers)
- Error handling for network issues
- Regex-based parsing for robust data extraction

### 2. **Data Quality**
- Type validation and conversion
- Currency standardization
- Timestamp tracking for data lineage
- Handles missing or malformed data gracefully

### 3. **Design Patterns**
- **Modular Architecture** - Separation of concerns (Extract/Transform/Load)
- **Pipeline Pattern** - Data flows through stages
- **Error Handling** - Try-catch with informative messages
- **Dependency Injection** - Configurable parameters (exchange rates, URLs)

### 4. **Testing Strategy**
- Unit tests for each module
- Mocking external dependencies (HTTP requests, Google Sheets, databases)
- Test fixtures for consistent test data
- Coverage reporting for code quality

---

## 📊 Data Output Example

**Before Transformation:**
```
title          price    rating  colors  size        gender     timestamp
Blue Jacket    $99.99   4.5     3       M, L, XL    Male       2024-01-15 10:30:00
Red Dress      $149.99  4.8     5       S, M, L     Female     2024-01-15 10:30:00
```

**After Transformation:**
```
title          price     rating  colors  size        gender     timestamp
Blue Jacket    1599840   4.5     3       M, L, XL    Male       2024-01-15 10:30:00
Red Dress      2399840   4.8     5       S, M, L     Female     2024-01-15 10:30:00
```

*Prices are now in Indonesian Rupiah (IDR) and data types are standardized*

---

## 🐛 Troubleshooting

### PostgreSQL Connection Error
**Problem:** `Connection refused` or database not found
**Solution:** Run `python setup_postgre.py` to initialize the database

### Google Sheets Authentication Failed
**Problem:** `FileNotFoundError: client_secret.json`
**Solution:** Follow the Google Sheets setup guide or skip this step (data will still be saved to CSV)

### HTTP Request Timeout
**Problem:** Website is slow or unreachable
**Solution:** Increase the `delay` parameter in `scrape_fashion_data()` or check internet connection

### Type Conversion Errors
**Problem:** `ValueError` during transformation
**Solution:** Check source data for invalid formats (non-numeric prices, etc.)

---

## 📈 Potential Extensions

This project can be extended with:
- 📅 **Scheduled Execution** - Run pipeline daily using APScheduler or cron
- 📊 **Data Analysis** - Add Jupyter notebooks for exploratory analysis
- 🔔 **Notifications** - Email alerts when scraping completes
- 📈 **Visualization** - Create dashboards using Tableau or Power BI
- 🔍 **Data Validation** - Add validation rules and data quality checks
- 🐳 **Containerization** - Docker for easy deployment
- ☁️ **Cloud Integration** - Deploy to AWS Lambda or Google Cloud Functions

---

## 📝 Files Reference

| File | Purpose |
|------|---------|
| `main.py` | Entry point - orchestrates the entire ETL pipeline |
| `utils/extract.py` | Web scraping and data fetching logic |
| `utils/transform.py` | Data cleaning and standardization |
| `utils/load.py` | Export to CSV, Google Sheets, PostgreSQL |
| `setup_postgre.py` | Initialize PostgreSQL database and user |
| `pytest.ini` | Pytest configuration |
| `requirements.txt` | Python package dependencies |
| `tests/` | Unit test suite |

---

## 🎓 Learning Outcomes

By working through this project, you'll understand:
- ✅ Web scraping techniques and HTML parsing
- ✅ Data pipeline architecture and orchestration
- ✅ ETL best practices
- ✅ Working with multiple data destinations
- ✅ SQL and relational database concepts
- ✅ API integration (Google Sheets)
- ✅ Unit testing and test-driven development
- ✅ Professional code organization

---

## 📄 License

This project is created as part of Dicoding's "Fundamental Data Processing" course.

---

## 👤 Author
kevinnaufaldany
Portfolio Project - Data Engineering Fundamentals
*First data engineering project demonstrating core ETL skills*

---

## 🤝 Support

For issues or questions:
1. Check the **Troubleshooting** section
2. Review test files for usage examples
3. Examine error messages carefully for clues

---

**Happy Data Engineering! 🚀**