# TalentTrek

<p align="center">
  <img src="https://placehold.co/300x80?text=TalentTrek+Logo" alt="TalentTrek Logo" height="80"/>
</p>

⛰️ A multi-source job scraping platform for collecting and saving job postings. TalentTrek scrapes jobs from multiple sources, allows users to save scraped jobs as reports, and provides a simple interface for job search and data collection.

---

## Features

✅ Scrape jobs from static and JavaScript-heavy pages (BeautifulSoup, Selenium, Scrapy)  
✅ Clean and deduplicate scraped data  
✅ Save scraped jobs as reports for future reference  
✅ User authentication and report management  
✅ User can select from predefined sources (e.g., LinkedIn, python.org, WeWorkRemotely) and provide a keyword to search across multiple sources simultaneously  
✅ Docker support for reproducible runs  
✅ Modular architecture with unit, integration, and fixture tests

---

## Quick Start

### Production Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd TalentTrek
   ```

2. **Set up environment variables:**
   ```bash
   cd server
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Start with Docker Compose:**
   ```bash
   make setup
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

### Development Setup (Recommended)

For faster development with auto-reload:

1. **Start development environment:**
   ```bash
   # Windows
   env/dev.bat
   
   # Linux/Mac
   ./env/dev.sh
   
   # Or use Makefile
   make dev
   ```

2. **Access the development application:**
   - Frontend: http://localhost:5173 (with hot reload)
   - Backend API: http://localhost:8000 (with auto-reload)
   - API Documentation: http://localhost:8000/docs

3. **Development commands:**
   ```bash
   make dev          # Start development environment
   make dev-up       # Start in background
   make dev-down     # Stop development environment
   make dev-logs     # View logs
   make dev-restart  # Restart services
   ```

**💡 Benefits of Development Mode:**
- **Auto-reload**: Changes to code automatically restart services
- **Hot reload**: Frontend updates instantly without page refresh
- **Volume mounting**: Code changes are immediately reflected
- **Faster iteration**: No need to rebuild containers for code changes

---

## Source Selection & Keyword-Based Scraping (NEW)

TalentTrek now supports a flexible, user-driven scraping workflow:

- **Predefined sources** (with selectors and search URL templates) are configured in `config/sources.yaml`.
- **User selects sources** and enters a **keyword** via the frontend UI.
- The backend dynamically builds search URLs and scrapes jobs from the selected sources using the keyword.
- Results are displayed instantly in the dashboard.

### Example Workflow

1. **User opens the dashboard** and sees a list of available sources (LinkedIn, python.org, WeWorkRemotely, etc.).
2. **User enters a keyword** (e.g., `python developer`).
3. **User selects one or more sources** to search in.
4. **User clicks "Scrape Jobs"**. The backend scrapes all selected sources using the keyword and returns the results.
5. **Results are shown in a table** with job title, company, location, source, and link.
6. **User can click "Save Report"** to save all scraped jobs as a report for future reference.

### API Endpoints

- `GET /api/sources` — List all available sources (id, name, type)
- `POST /api/scrape/jobs` — Scrape jobs from selected sources with a keyword
  - Request body: `{ "keyword": "python developer", "sources": ["linkedin", "python_org"] }`
  - Response: `{ "jobs": [ ... ] }`

### Configuration Example (`config/sources.yaml`)

```yaml
sources:
  - id: linkedin
    name: LinkedIn
    type: dynamic
    search_url: "https://www.linkedin.com/jobs/search/?keywords={keyword}"
    selectors:
      job_selector: ".job-card-container"
      title: ".job-card-list__title"
      company: ".job-card-container__company-name"
      location: ".job-card-container__metadata-item"
      date_posted: ".job-card-container__listed-time"
    scroll_count: 5
  - id: python_org
    name: Python.org
    type: static
    search_url: "https://www.python.org/jobs/?q={keyword}"
    selectors:
      job_selector: "ol.list-recent-jobs > li"
      title: "h2.listing-company a"
      company: "span.listing-company-name"
      location: "span.listing-location"
      date_posted: "span.listing-posted time"
  - id: weworkremotely
    name: WeWorkRemotely
    type: static
    search_url: "https://weworkremotely.com/remote-jobs/search?term={keyword}"
    selectors:
      job_selector: "section.jobs li.feature"
      title: "span.title"
      company: "span.company"
      location: "span.region"
      date_posted: "time"
```

---

## Project Structure

```
TalentTrek/
├── env/                    # Environment and deployment files
│   ├── dev.sh             # Development startup script (Linux/macOS)
│   ├── dev.bat            # Development startup script (Windows)
│   ├── prod.sh            # Production startup script (Linux/macOS)
│   ├── prod.bat           # Production startup script (Windows)
│   ├── docker-compose.yml # Production Docker Compose
│   ├── docker-compose.dev.yml # Development Docker Compose
│   └── README.md          # Environment documentation
├── app/
│   ├── Dockerfile
│   ├── eslint.config.js
│   ├── index.html
│   ├── nginx.conf
│   ├── package-lock.json
│   ├── package.json
│   ├── public/
│   │   └── vite.svg
│   ├── src/
│   │   ├── App.jsx
│   │   ├── assets/
│   │   │   └── react.svg
│   │   ├── components/
│   │   │   ├── LoginForm.jsx
│   │   │   ├── RegisterForm.jsx
│   │   │   └── UserReports.jsx
│   │   ├── contexts/
│   │   │   └── AuthContext.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   └── vite.config.js
├── docker-compose.yml
├── Makefile
├── README.md
├── server/
│   ├── config/
│   │   ├── scrapers.yaml
│   │   ├── settings.yaml
│   │   └── sources.yaml
│   ├── data_output/
│   │   ├── jobs.db
│   │   └── raw/
│   ├── Dockerfile
│   ├── src/
│   │   ├── supabase/
│   │   │   ├── init_supabase_db.py
│   ├── main.py
│   ├── requirements.txt
│   └── src/
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── reports.py
│       │   ├── statistics.py
│       │   └── trends.py
│       ├── api/
│       │   ├── __init__.py
│       │   └── v1/
│       │       ├── __init__.py
│       │       ├── actions.py
│       │       ├── auth.py
│       │       ├── supabase_auth.py
│       │       └── urls.py
│       ├── data/
│       │   ├── __init__.py
│       │   ├── database.py
│       │   ├── models.py
│       │   └── processors.py
│       ├── scrapers/
│       │   ├── __init__.py
│       │   ├── base_scraper.py
│       │   ├── selenium_scraper.py
│       │   ├── static_scraper.py
│       │   └── scrapy_crawler/
│       │       ├── __init__.py
│       │       ├── items.py
│       │       ├── jobs_spider.py
│       │       ├── pipelines.py
│       │       └── settings.py
│       ├── schemas/
│       │   ├── __init__.py
│       │   └── auth.py
│       ├── utils/
│       │   ├── __init__.py
│       │   ├── auth.py
│       │   ├── config.py
│       │   ├── helpers.py
│       │   ├── logger.py
│       │   ├── supabase.py
│       │   └── supabase_auth.py
│       └── tests/
│           └── unit/
│               ├── __init__.py
│               ├── test_auth.py
│               └── test_supabase_auth.py
```

### Key Directories
- `app/` — Frontend (React, Vite, Material-UI)
- `server/` — Backend (FastAPI, Python, Docker)
  - `src/` — Main backend source code
  - `config/` — Scraper/source configuration files
  - `data_output/` — All output data, reports, and processed files
  - `templates/` — HTML templates for reports
  - `tests/` — Unit, integration, and fixture tests

### Notable Files
- `docker-compose.yml` — Orchestrates frontend and backend containers
- `Makefile` — Common commands for building, running, and testing
- `README.md` — Project documentation

---

## Architecture Diagram

```mermaid
<diagram>
```

---

## Quickstart

### 1️⃣ Build and Start All Services (Recommended)

```bash
make build   # Build both backend and frontend Docker images
make up      # Start both backend and frontend (Docker Compose)
```

- The backend will be available at http://localhost:8000
- The frontend dashboard will be available at http://localhost:5173 (or as configured)

### 2️⃣ Supabase Setup (Optional)

If you want to use Supabase PostgreSQL instead of SQLite:

1. **Create a Supabase project** at https://supabase.com
2. **Get your project credentials** from Settings > API
3. **Create a `.env` file** in the `server/` directory with your Supabase credentials
4. **Initialize the database:**
   ```bash
   make docker-backend-init-supabase
   ```
5. **Start the application:**
   ```bash
   make up
   ```

### 3️⃣ Stop or Restart Services

```bash
make down      # Stop all services
make restart   # Restart all services
make rebuild   # Rebuild all services
make re        # Rebuild and restart all services
```

### 4️⃣ Local Development (without Docker)

- Start the backend locally (requires Python environment):
  ```bash
  make local-backend
  ```
- Start the frontend locally (requires Node.js environment):
  ```bash
  make local-frontend
  ```

### 5️⃣ Backend Pipeline Tasks (via Docker)

- Initialize the database:
  ```bash
  make docker-backend-init
  ```
- Scrape jobs:
  ```bash
  make docker-backend-scrape
  ```
- Analyze data:
  ```bash
  make docker-backend-analyze
  ```
- Generate report:
  ```bash
  make docker-backend-report
  ```
- Run backend tests:
  ```bash
  make docker-backend-test
  ```

### 6️⃣ Logs

```bash
make docker-logs   # Show logs for all Docker Compose services
```

---

## Makefile Commands (Highly Recommended)

- `setup` — Build and start both server and frontend (Docker)
- `up` — Start both server and frontend together (Docker)
- `build` — Build both server and frontend together (Docker)
- `down` — Stop both server and frontend together (Docker)
- `restart` — Restart both server and frontend together (Docker)
- `rebuild` — Rebuild both server and frontend together (Docker) and start
- `re` — Rebuild and restart both server and frontend together (Docker)
- `local-backend` — Run backend locally (requires Python env)
- `local-frontend` — Run frontend locally (requires Node env)
- `docker-build` — Build all Docker images
- `docker-up` — Start all services with Docker Compose
- `docker-down` — Stop all Docker Compose services
- `docker-logs` — Show logs for all Docker Compose services
- `docker-backend-init` — Init backend DB via Docker
- `docker-backend-scrape` — Run scraping via Docker
- `docker-backend-analyze` — Run analysis via Docker
- `docker-backend-report` — Run report via Docker
- `docker-backend-test` — Run backend tests via Docker

> **Note:** The Docker service is named `job-market` as defined in `docker-compose.yml`.

---

## CLI Commands (Alternative to Makefile)

- `scrape`: Collect jobs from static or dynamic URLs
- `analyze`: Clean, deduplicate, and generate statistics
- `report`: Create HTML report from analyzed data

Example:
```bash
python -m src.cli.interface scrape --static-url "https://careers.example.com/jobs"
python -m src.cli.interface scrape --dynamic-url "https://example.com/jobs"
```

---

## Configuration

- Global settings → `config/settings.yaml`
- Scraper targets → `config/scrapers.yaml`

Adjust URLs, selectors, and database configuration as needed.

---

## Static vs Dynamic URL Sources

TalentTrek supports scraping from both **static** and **dynamic** web sources. Understanding the difference is important for configuring your scraping targets and troubleshooting issues.

### What is a Static URL Source?
- **Static URLs** point to web pages where job data is present in the initial HTML response from the server.
- These pages do **not** require JavaScript execution to display job listings.
- Scraping is performed using lightweight tools like `requests` and `BeautifulSoup`.
- Example: Most traditional job boards, company career pages, or any site where you can "View Source" and see the job data in the HTML.
- In configuration: Static URLs are listed under the `static_urls` key in `config/urls.json`.

### What is a Dynamic URL Source?
- **Dynamic URLs** point to web pages where job data is loaded or rendered **after** the initial page load, typically via JavaScript (AJAX, React, etc.).
- These pages require a browser automation tool (like Selenium) to render and extract job listings.
- Example: Sites like LinkedIn Jobs, or any site where job listings appear only after the page loads and JavaScript runs.
- In configuration: Dynamic URLs are listed under the `dynamic_urls` key in `config/urls.json`.

### How TalentTrek Handles Them
- **Static URLs** are scraped using the `StaticScraper` (BeautifulSoup-based).
- **Dynamic URLs** are scraped using the `SeleniumScraper` (headless Chrome via Selenium).
- The CLI, API, and frontend dashboard allow you to add, remove, and list both types of URLs.
- The backend automatically chooses the correct scraper based on the URL's type (as stored in `urls.json`).

### How to Distinguish and Manage
- If you can see all job data in the page's HTML (right-click → View Source), it's likely static.
- If job data only appears after the page loads, or you see empty HTML but jobs appear in the browser, it's dynamic.
- Use the dashboard or API to add URLs to the correct category. If unsure, try static first; if it fails to find jobs, try dynamic.

---

## Reports

HTML reports and charts are saved in `data_output/reports/`.
Open them with your web browser to view insights.

---

## Frontend (React Dashboard)

The `app/` directory contains the modern React (Vite) frontend for TalentTrek.

### Features
- Modern dashboard UI (Material-UI)
- Trigger backend actions (scrape, analyze, report, test)
- Show status and notifications
- Visualize reports (JSON, charts coming soon)
- Manage static and dynamic URLs for scraping

### API Endpoints
The frontend communicates with the backend via the following endpoints:
- `POST /api/scrape` — Run the scraping process
- `POST /api/analyze` — Run the analysis process
- `POST /api/report` — Generate the report
- `POST /api/test` — Run backend tests
- `GET /api/urls` — Get static and dynamic URLs
- `POST /api/urls/static` — Add a static URL
- `POST /api/urls/dynamic` — Add a dynamic URL
- `DELETE /api/urls/static` — Remove a static URL
- `DELETE /api/urls/dynamic` — Remove a dynamic URL

All endpoints return JSON responses. The frontend expects the backend to be available at `/api` (proxied to port 8000 in development).

### Development
1. Install dependencies:
   ```sh
   cd app
   npm install
   ```
2. Start the dev server:
   ```sh
   npm run dev
   ```
   The app will be available at http://localhost:5173
   - API requests to `/api` are proxied to the backend at http://localhost:8000

### Production
The Dockerfile in `app/` builds and serves the app with nginx. Use Docker Compose to run both frontend and backend together:
```sh
make up
```

### Dependencies
- React (Vite)
- Material-UI (MUI)
- Axios
- Recharts (for future data visualization)

---

## Testing

Run all tests:
```
```

## Authentication System

TalentTrek now includes a comprehensive authentication system that allows users to:

- **Register** new accounts with email, username, and password
- **Login** with email and password
- **Save personalized reports** to their account
- **Manage their saved reports** (view, delete)
- **Secure access** to all platform features

### Authentication Features

- **Supabase Auth** as primary authentication (email verification, password reset, social login)
- **Local JWT authentication** as fallback option
- **Password hashing** using bcrypt for local auth
- **User-specific report storage** in the database
- **Session management** with automatic token validation
- **Protected API endpoints** requiring authentication
- **Simplified schemas** - Core auth handled by Supabase, minimal local user data

### Schema Simplification

Since Supabase Auth handles core authentication, we've simplified our schemas:
- **Removed**: `UserCreate`, `UserLogin`, `TokenData` schemas (handled by Supabase)
- **Kept**: `UserResponse`, `Token`, `UserReportCreate`, `UserReportResponse` (for app functionality)
- **Added**: Simple request models (`RegisterRequest`, `LoginRequest`) for API validation
- **Local Database**: Minimal user records for linking to reports and app-specific data

### User Management

Users can:
- Create accounts with unique email and username
- Login securely with their credentials
- View their profile information
- Logout and clear their session
- Save reports with custom titles and descriptions
- View all their saved reports
- Delete reports they no longer need

### API Endpoints

#### Authentication (Supabase Auth - Primary)
- `POST /api/supabase-auth/register` — Register a new user with Supabase Auth
- `POST /api/supabase-auth/login` — Login user with Supabase Auth
- `GET /api/supabase-auth/me` — Get current user information

#### Authentication (Local JWT - Fallback)
- `POST /api/auth/register` — Register a new user with local JWT
- `POST /api/auth/login` — Login user with local JWT
- `GET /api/auth/me` — Get current user information

#### User Reports (Supabase Auth)
- `POST /api/supabase-auth/reports` — Save a new report
- `GET /api/supabase-auth/reports` — Get all user reports
- `GET /api/supabase-auth/reports/{report_id}` — Get specific report
- `DELETE /api/supabase-auth/reports/{report_id}` — Delete a report

#### User Reports (Local JWT)
- `POST /api/auth/reports` — Save a new report
- `GET /api/auth/reports` — Get all user reports
- `GET /api/auth/reports/{report_id}` — Get specific report
- `DELETE /api/auth/reports/{report_id}` — Delete a report

## Database Migrations

TalentTrek uses Alembic for database migrations, providing version-controlled schema changes and safe database updates.

### Migration Files

- `0001_initial_schema.py` - Creates the initial database schema with all tables
- `0002_migrate_old_reports.py` - Migrates old report structure to new simplified structure

### How to Use Migrations

#### Initial Setup (New Project)
```bash
# 1. Apply all migrations to create tables
make dev-backend-migrate

# 2. (Optional) Create sample data for testing
make dev-backend-seed
```

#### Apply All Migrations
```bash
# Development
make dev-backend-migrate

# Production
make prod-backend-migrate
```

#### Migration Management Commands
```bash
# Check migration status
make dev-backend-migrate-status

# Show migration history
make dev-backend-migrate-history

# Create new migration (after model changes)
make dev-backend-migrate-create "Description of changes"
```

#### Manual Migration Commands
```bash
# Apply all pending migrations
alembic upgrade head

# Apply specific migration
alembic upgrade 0002

# Rollback one migration
alembic downgrade -1

# Rollback to specific migration
alembic downgrade 0001

# Check current migration status
alembic current

# Show migration history
alembic history
```

### Migration Workflow

1. **Make model changes** in `server/src/data/models.py`
2. **Generate migration**: `make dev-backend-migrate-create "Description"`
3. **Review generated migration** in `server/migrations/versions/` directory
4. **Test migration**: `make dev-backend-migrate` (dev)
5. **Apply to production**: `make prod-backend-migrate` (prod)

### Migration Best Practices

1. **Always test migrations** on development database first
2. **Backup production data** before applying migrations
3. **Write reversible migrations** - include both upgrade and downgrade
4. **Use descriptive names** for migration files
5. **Test rollback procedures** before production deployment

### Troubleshooting

#### Migration Conflicts
If you get conflicts between migrations:
1. Check migration history: `alembic history`
2. Identify conflicting migrations
3. Resolve conflicts manually in migration files
4. Test thoroughly before applying

#### Database Connection Issues
- Ensure database URL is correct in environment variables
- Check Supabase configuration
- Verify network connectivity

#### Rollback Issues
- Always test rollback procedures
- Keep backups before major migrations
- Consider data loss implications

---

## Environment Variables

TalentTrek uses environment variables for configuration, especially for sensitive data such as credentials. These are typically set in a `.env` file at the project root or in the `server/` directory.

### Required Variables

For LinkedIn scraping, you must provide your LinkedIn credentials:

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
```

- **LINKEDIN_EMAIL**: The email address for your LinkedIn account (used for automated login).
- **LINKEDIN_PASSWORD**: The password for your LinkedIn account.

### Authentication Variables

For the authentication system, you must provide a secret key:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
```

- **SECRET_KEY**: A secure random string used for JWT token signing. **Change this in production!**

### Supabase Configuration (Optional)

To use Supabase PostgreSQL instead of SQLite:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your-supabase-anon-key
SUPABASE_SERVICE_ROLE_KEY=your-supabase-service-role-key
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-ID].supabase.co:5432/postgres
USE_SUPABASE_AUTH=true
```

- **SUPABASE_URL**: Your Supabase project URL
- **SUPABASE_ANON_KEY**: Your Supabase anonymous key (public)
- **SUPABASE_SERVICE_ROLE_KEY**: Your Supabase service role key (private)
- **DATABASE_URL**: PostgreSQL connection string for Supabase
- **USE_SUPABASE_AUTH**: Set to `true` to use Supabase Auth (default), `false` for local JWT auth

### Database Configuration

```env
DATABASE_URL=sqlite:///data_output/jobs.db
```

- **DATABASE_URL**: Database connection string
  - Default: SQLite (`sqlite:///data_output/jobs.db`)
  - Supabase: PostgreSQL connection string
  - Other: Any SQLAlchemy-compatible database URL

### Usage
- For **local development**, create a `.env` file in the `server/` directory with the above variables.
- For **Docker Compose**, the `.env` file is automatically loaded if present in the `server/` directory. You can also specify an `env_file` in your `docker-compose.yml`.

> **Note:** Never commit your real credentials to version control. Use a `.env` file and add it to `.gitignore`.

If you add more environment-based configuration (e.g., database URLs, API keys), document them here as well.