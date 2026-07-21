# Finance Tracker

A Finance Tracker application built using Python that started as a command-line application and has evolved into a Flask web application. The project includes transaction management, budget monitoring, reporting, SQLite database integration, Alembic migrations, and automated testing using pytest.

## Features Implemented

### Day 1 - Project Setup & CLI

* Project skeleton setup
* Virtual environment configuration
* Git and GitHub integration
* Command-line interface using argparse
* Income argument support
* Expense argument support
* Category argument support

### Day 2 - Object-Oriented Programming

* Category class implementation
* Transaction class implementation
* Input validation
* Type checking
* Docstrings
* Dunder methods:
  * **str**
  * **eq**
  * **lt**
* Assertion-based testing

### Day 3 - Advanced Functions 

* Custom decorators

  * @validate_amount
  * @timer
* Transaction amount validation using decorators
* Performance benchmarking using timer decorator
* Decorator testing
* Execution time measurement
* Generators
* itertools
* Functools
* lru_chace()
* Typehint PEP484
* Mypy


### Day 4

* Advanced Exception Handling
* Built a custom TransactionError hierarchy
* Created custom exceptions:
  * InvalidAmountError
  * InvalidCategoryError
  * InvalidTransactionTypeError
* Replaced generic exceptions with custom exceptions
* Implemented structured logging using Python's logging module
* Configured logging using logging.yaml
* Created centralized logger configuration (logger_config.py)
* Logged application errors to app.log
* Tested custom exception handling and logging successfully

### Day 5

* CSV File Handling
* csv.DictReader
* JSON Export
* pathlib.Path
* Bulk Transaction Import
* Malformed Row Handling
 
### Day 6

* Unit Testing with pytest
* Created 19 automated unit tests
* Tested models.py and io_manager.py
* Generated HTML coverage report
* Achieved 100% code coverage

### Day 7

* SQLAlchemy ORM
* SQLite Database Integration
* Created centralized database configuration (database.py)
* Created TransactionDB ORM model
* Created SQLite database (finance.db)
* Migrated transaction data from CSV to SQLite
* Verified database row count matches imported transactions
* Configured Alembic for database version control
* Generated and applied the initial Alembic migration

### Day 8

* SQLAlchemy Query API
* Report Generation
* Database Filtering using filter()
* Category-wise Aggregation using group_by()
* Aggregate calculations using func.sum()
* Sorted results using order_by()
* Retrieved top categories using limit()
* Implemented category_summary() in reports.py
* created test_reports.py for report validation
* Generated monthly spending summary (Top 3 spending categories)

#### Day 9

* Budget Feature
* Created `BudgetExceededError` for budget validation
* Implemented `check_budget()` in `budget.py`
* Compared category-wise spending against monthly budget limits
* Raised custom exception when a category exceeded its budget
* Displayed over-budget alerts in the terminal
* Created `BudgetDB` SQLAlchemy model
* Added `budgets` table to the database
* Regenerated Alembic initial migration to include both `transactions` and `budgets` tables
* Applied database migrations using Alembic
* Created `test_budget.py` to validate budget checking

### Day 10

* Flask Web Application Setup
* Implemented Flask Application Factory (`create_app()`)
* Created centralized application configuration (`config.py`)
* Integrated Flask with SQLite database
* Created `transactions` Blueprint
* Implemented `/transactions` route
* Connected Flask to SQLAlchemy for database access
* Retrieved transaction data from SQLite using SQLAlchemy ORM
* Created Jinja2 templates (`base.html` and `transactions.html`)
* Implemented template inheritance using `base.html`
* Rendered dynamic transaction data in an HTML table
* Enhanced the UI with responsive table styling, hover effects, and color-coded transaction types
* Successfully displayed all transactions from the database in the browser


### Day 11

* REST API Design
* Implemented RESTful API endpoints
* GET /api/transactions
* POST /api/transactions
* DELETE /api/transactions/<id>
* JSON responses using Flask jsonify
* HTTP Status Codes
  * 200 OK
  * 201 Created
  * 400 Bad Request
  * 404 Not Found
* API testing using Postman
* Error handling for invalid requests

### Day 12

* User Authentication using Flask-Login
* UserDB model implementation
* Password hashing using Werkzeug
* User Registration
* User Login
* User Logout
* Session Management
* Protected Routes using @login_required
* Redirect unauthenticated users to /login
* Remember-me cookie support
* Alembic migration for Users table
* Login and Register UI using Jinja2 templates

### Day 13

* HTML Forms (CRUD UI)
* Integrated Flask-WTF for form handling
* Created TransactionForm using WTForms
* Implemented form validation
  * Amount must be greater than zero
  * Category cannot be empty
  * Date is required
* Added CSRF protection using Flask-WTF
* Displayed validation error messages
* Implemented flash messages for successful transaction creation
* Redirected users after successful form submission (Post/Redirect/Get pattern)
* Designed responsive transaction form using HTML and CSS
* Added dashboard cards for:
  * Total Income
  * Total Expense
  * Balance
  * Total Transactions
* Styled the Finance Tracker dashboard with a clean, modern UI
* Added "View Transaction History" button with show/hide functionality
* Improved overall user experience with responsive layout and external CSS

### Day 14

* External API Integration
* Configured `requests.Session()` for efficient HTTP requests
* Implemented automatic retry mechanism using `HTTPAdapter`
* Integrated live Exchange Rate API
* Mapped API response to application data
* Implemented exchange rate caching using `functools.lru_cache`
* Converted total expense from INR to USD using live exchange rates
* Displayed USD equivalent on the Finance Tracker dashboard
* Added Live Exchange Rate badge showing current INR → USD conversion rate
* Enhanced dashboard with real-time currency conversion
* Successfully fetched and displayed live exchange rate data

### Day 15

* Charts and Data Visualization using Chart.js
* Integrated Chart.js via CDN
* Created Spending by Category doughnut chart
* Retrieved real expense data from SQLite using SQLAlchemy
* Grouped expense transactions by category using `func.sum()` and `group_by()`
* Displayed Top 6 spending categories and combined remaining categories as Other
* Created Monthly Spending Trend bar chart for the last 6 months
* Added `date` column to TransactionDB model
* Created and applied Alembic migration for transaction date
* Saved transaction date from WTForms to SQLite database
* Passed Python data from Flask to JavaScript using Jinja2 `tojson`
* Implemented responsive two-chart dashboard layout
* Charts automatically update using real database transaction data


## Day 16 – Dashboard UI Enhancement & Data Visualization

- Improved the Finance Tracker dashboard UI with a modern dark theme.
- Redesigned the header and navigation section.
- Added a hamburger menu for better navigation.
- Moved the following actions into the hamburger menu:
  - Add Transaction
  - View Transactions
  - Import CSV
  - Export CSV
  - Export PDF Report
  - Logout
- Added show/hide functionality for the Add Transaction form.
- Added show/hide functionality for Transaction History.
- Improved the dashboard card design and overall page layout.
- Added a doughnut chart to visualize spending by category.
- Displayed only the top spending categories in the chart.
- Added category percentages on hover.
- Added interactive highlighting for chart categories.
- Integrated the live INR-to-USD exchange rate into the dashboard header.


## Day 17 – Search, Filter & Pagination

- Implemented query string parameters for transaction filtering.
- Added dynamic SQLAlchemy filters.
- Added category-based transaction filtering.
- Added start-date and end-date range filtering.
- Created a filter UI inside the Transaction History section.
- Implemented pagination with a maximum of 10 transactions per page.
- Added Previous and Next page navigation.
- Preserved active filters while navigating between pages.
- Ensured the Transaction History section remains visible during pagination.
- Added anchor navigation to prevent returning to the top of the dashboard after changing pages.
- Added a live category search bar.
- Implemented automatic URL updates using JavaScript.
- Added debounce functionality to prevent unnecessary reloads while typing.
- Improved the filter UI to match the dark-themed dashboard.

### Day 18 – User Authentication & Security

- Implemented a secure user authentication system using Flask-Login.
- Added user registration with unique username validation.
-  Implemented secure password hashing using Werkzeug.
-  Added user login and logout functionality.
-  Protected dashboard and transaction routes using login authentication.
-  Implemented session management for authenticated users.
-  Added automatic redirection to the login page for unauthorized users.
-  Created a dedicated Users database table using SQLAlchemy.
-  Added user-friendly error messages for invalid login credentials.
-  Improved application security by preventing unauthorized access to protected pages.

### Day 19 – Database Integration, Reports & Performance
-  Migrated transaction storage from JSON files to a SQLite database using SQLAlchemy ORM.
- Implemented CRUD operations for transaction management.
- Added monthly budget management with category-wise budget limits.
- Implemented CSV import functionality for bulk transaction uploads.
- Added CSV export functionality for transaction data.
-  Implemented PDF report generation for transaction summaries.
- Added scheduled database backup functionality.
- Integrated API health check endpoint for application monitoring.
- Implemented rate limiting to protect the application from excessive requests.
- Improved application logging and exception handling for easier debugging.

### Day 20 – Dockerization & Deployment
- Containerized the Finance Tracker application using Docker.
- Created a production-ready Dockerfile for the Flask application.
- Configured Docker Compose for simplified application deployment.
- Integrated Gunicorn as the production WSGI server.
- Added a startup script (start.sh) to automate database initialization.
- Configured automatic database table creation during container startup.
- Organized project data by moving the SQLite database into a dedicated data/ directory.
- Configured Docker volumes for persistent database storage.
- Updated the application to use the new database location (data/finance.db).
- Fixed Docker networking and port configuration issues.
- Successfully deployed and verified the complete Finance Tracker application inside Docker.
