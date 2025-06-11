# Google Cloud PostgreSQL Database Setup

## Connection Configuration

1. **Edit the Database URL**: Open `backend/database/database.py` and update the `DATABASE_URL` variable with your Google Cloud PostgreSQL credentials:

```python
DATABASE_URL = "postgresql://username:password@/dbname?host=/cloudsql/project-id:region:instance-name"
```

Replace the following values:
- `username`: Your database username
- `password`: Your database password
- `dbname`: Your database name
- `project-id`: Your Google Cloud project ID
- `region`: The region where your database is hosted (e.g., us-central1)
- `instance-name`: Your Cloud SQL instance name

## Local Development

For local development, you'll need to use the Cloud SQL Proxy:

1. **Install the Cloud SQL Proxy**:
   - Follow the instructions at: https://cloud.google.com/sql/docs/postgres/connect-admin-proxy

2. **Start the Cloud SQL Proxy**:
   ```bash
   ./cloud-sql-proxy project-id:region:instance-name
   ```

3. **Update the Database URL** for local development:
   ```python
   DATABASE_URL = "postgresql://username:password@localhost:5432/dbname"
   ```

## Environment Variables

For better security, set your database credentials as environment variables:

1. **Create a .env file** in the backend directory:
   ```
   DATABASE_URL=postgresql://username:password@/dbname?host=/cloudsql/project-id:region:instance-name
   ```

2. **Install python-dotenv**:
   ```bash
   poetry add python-dotenv
   ```

3. **Update database.py** to use environment variables:
   ```python
   import os
   from dotenv import load_dotenv

   load_dotenv()

   DATABASE_URL = os.getenv("DATABASE_URL")
   ```

## Testing the Connection

You can test your database connection by running:

```bash
python backend/check_db_connection.py
```

## Initializing the Database

The database tables are automatically created when you start the application. If you need to manually initialize the database, run:

```bash
python -c "from database.init_db import init_db; init_db()"
```

## Database Migration

For more complex database migrations, consider using Alembic:

1. **Install Alembic**:
   ```bash
   poetry add alembic
   ```

2. **Initialize Alembic**:
   ```bash
   alembic init migrations
   ```

3. **Configure Alembic** by editing `alembic.ini` and `migrations/env.py`

4. **Create a migration**:
   ```bash
   alembic revision --autogenerate -m "Initial migration"
   ```

5. **Apply the migration**:
   ```bash
   alembic upgrade head
   ``` 