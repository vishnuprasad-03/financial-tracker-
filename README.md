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
