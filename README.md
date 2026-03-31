# Personal Finance API

A lightweight FastAPI-based backend for managing personal finances. It allows users to track incomes and expenses, set budgets, and receive alerts when budget limits are exceeded.

## Features
- **User Authentication**: Register and login users securely (using `passlib` and `bcrypt` for password hashing).
- **Transaction Management**: Record both income and expenses across various categories.
- **Budgeting & Alerts**: Set budget limits per category. If an expense causes a category to exceed its predefined limit, an automatic alert is generated.
- **Monthly Reports**: Retrieve summarized financial reports (total income, total expenses, net balance) filtered by month and year.

## Tech Stack
- **Framework**: FastAPI
- **Database**: SQLite & SQLAlchemy (ORM)
- **Validation**: Pydantic
- **Server**: Uvicorn

## Setup Instructions

1. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Seed the Database (Optional):**
   Run the seeding script to populate the SQLite database with default categories, a dummy user (`test_user@example.com`), and 60 random transactions for easy testing.
   ```bash
   python seed.py
   ```

4. **Run the Server:**
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once the server is running, FastAPI automatically generates interactive API documentation. You can view it by navigating to:
- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Key Endpoints
- `POST /register`, `POST /login` - Authentication
- `POST /transactions`, `GET /transactions` - Manage transactions
- `POST /budgets`, `GET /budgets` - Set and view category budgets
- `GET /reports/monthly` - Get monthly financial summaries (accepts `user_id`, `month`, and `year` query parameters)
- `GET /alerts` - View budget overflow alerts
