# TalentTrek Makefile - Development and Production Commands

# =============================================================================
# DEVELOPMENT COMMANDS (with auto-reload)
# =============================================================================

dev:
	docker-compose -f assembly/dev/docker-compose.dev.yml up --build

dev-build:
	docker-compose -f assembly/dev/docker-compose.dev.yml build

dev-up:
	docker-compose -f assembly/dev/docker-compose.dev.yml up -d

dev-down:
	docker-compose -f assembly/dev/docker-compose.dev.yml down

dev-logs:
	docker-compose -f assembly/dev/docker-compose.dev.yml logs -f

dev-restart:
	docker-compose -f assembly/dev/docker-compose.dev.yml restart


# =============================================================================
# BACKEND TASKS (Development)
# =============================================================================

dev-backend-init:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server python main.py

dev-backend-init-auth:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server python init_auth_db.py

dev-migrate:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server alembic upgrade head

dev-migrate-create:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server alembic revision --autogenerate -m

dev-backend-migrate-status:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server alembic current

dev-backend-migrate-history:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server alembic history

dev-backend-seed:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server python src/supabase/seed_data.py

dev-backend-scrape:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server python -m src.cli.interface scrape

dev-backend-test:
	docker-compose -f assembly/dev/docker-compose.dev.yml run server pytest

# =============================================================================
# PRODUCTION COMMANDS
# =============================================================================

prod:
	docker-compose -f assembly/prod/docker-compose.yml up -d --build

prod-build:
	docker-compose -f assembly/prod/docker-compose.yml build

prod-up:
	docker-compose -f assembly/prod/docker-compose.yml up -d

prod-down:
	docker-compose -f assembly/prod/docker-compose.yml down

prod-logs:
	docker-compose -f assembly/prod/docker-compose.yml logs -f

prod-restart:
	docker-compose -f assembly/prod/docker-compose.yml restart

prod-init-db:
	docker-compose -f assembly/prod/docker-compose.yml run server python src/supabase/init_supabase_db.py

# =============================================================================
# BACKEND TASKS (Production)
# =============================================================================

prod-backend-init:
	docker-compose -f assembly/prod/docker-compose.yml run server python main.py

prod-backend-init-auth:
	docker-compose -f assembly/prod/docker-compose.yml run server python init_auth_db.py

prod-migrate:
	docker-compose -f assembly/prod/docker-compose.yml run server alembic upgrade head

prod-migrate-status:
	docker-compose -f assembly/prod/docker-compose.yml run server alembic current

prod-backend-migrate-history:
	docker-compose -f assembly/prod/docker-compose.yml run server alembic history

prod-backend-seed:
	docker-compose -f assembly/prod/docker-compose.yml run server python src/supabase/seed_data.py

prod-backend-scrape:
	docker-compose -f assembly/prod/docker-compose.yml run server python -m src.cli.interface scrape

prod-backend-test:
	docker-compose -f assembly/prod/docker-compose.yml run server pytest

# =============================================================================
# UTILITY COMMANDS
# =============================================================================

clean:
	docker-compose -f assembly/prod/docker-compose.yml down -v --remove-orphans
	docker-compose -f assembly/dev/docker-compose.dev.yml down -v --remove-orphans
	docker system prune -f

clean-dev:
	docker-compose -f assembly/dev/docker-compose.dev.yml down -v --remove-orphans

clean-prod:
	docker-compose -f assembly/prod/docker-compose.yml down -v --remove-orphans

dev-expose-host:
	@echo "Starting LinkedIn OAuth with host networking..."
	@echo "This will expose port 5173 to your host machine"
	@echo "Make sure your LinkedIn app redirect URL is set to: http://YOUR_HOST_IP:5173/callback"
	@echo ""
	@echo "Note: You need to manually set HOST_IP environment variable"
	@echo "Example: HOST_IP=192.168.1.100 make dev-expose-host"
	@echo ""
	docker-compose -f env/docker-compose.dev.yml run --network host server python -c "from src.utils.linkedin_auth import linkedin_auth; linkedin_auth.generate_token()"

prod-expose-host:
	@echo "Starting LinkedIn OAuth with host networking..."
	@echo "This will expose port 5173 to your host machine"
	@echo "Make sure your LinkedIn app redirect URL is set to: http://YOUR_HOST_IP:5173/callback"
	@echo ""
	@echo "Note: You need to manually set HOST_IP environment variable"
	@echo "Example: HOST_IP=192.168.1.100 make prod-expose-host"
	@echo ""
	docker-compose -f assembly/prod/docker-compose.yml run --network host server python -c "from src.utils.linkedin_auth import linkedin_auth; linkedin_auth.generate_token()"

check-host-ip:
	@echo "Your host machine IP addresses:"
	@echo "================================"
	@echo ""
	@echo "Windows: Run 'ipconfig' in PowerShell to see your IP addresses"
	@echo "Linux/Mac: Run 'hostname -I' in terminal to see your IP addresses"
	@echo ""
	@echo "For LinkedIn OAuth:"
	@echo "1. Look for your local network IP (usually starts with 192.168.x.x or 10.x.x.x)"
	@echo "2. Update your LinkedIn app redirect URL to: http://YOUR_IP:5173/callback"
	@echo "3. Example: http://192.168.1.100:5173/callback"

# =============================================================================
# HELP
# =============================================================================

.PHONY: help dev dev-build dev-up dev-down dev-logs dev-restart dev-init-db \
        prod prod-build prod-up prod-down prod-logs prod-restart prod-init-db \
        prod-backend-init prod-backend-init-auth \
        prod-backend-migrate prod-backend-migrate-status prod-backend-migrate-history prod-backend-seed prod-backend-scrape prod-backend-test \
        dev-backend-init dev-backend-init-auth \
        dev-backend-migrate dev-backend-migrate-create dev-backend-migrate-status dev-backend-migrate-history dev-backend-seed dev-backend-scrape dev-backend-test \
        dev-expose-host prod-expose-host check-host-ip \
        clean clean-dev clean-prod

help:
	@echo "TalentTrek Makefile Commands"
	@echo "============================"
	@echo ""
	@echo "DEVELOPMENT COMMANDS (with auto-reload):"
	@echo "  dev                  Start development environment with auto-reload"
	@echo "  dev-build            Build development containers"
	@echo "  dev-up               Start development environment in background"
	@echo "  dev-down             Stop development environment"
	@echo "  dev-logs             Show development logs"
	@echo "  dev-restart          Restart development environment"
	@echo "  dev-init-db          Initialize database tables (dev)"
	@echo ""
	@echo "BACKEND TASKS (Development):"
	@echo "  dev-backend-init     Initialize backend (dev)"
	@echo "  dev-backend-init-auth Initialize auth database (dev)"
	@echo "  dev-migrate   Apply all migrations (dev)"
	@echo "  dev-migrate-create Create new migration (dev)"
	@echo "  dev-backend-migrate-status Check migration status (dev)"
	@echo "  dev-backend-migrate-history Show migration history (dev)"
	@echo "  dev-backend-seed     Create sample data (dev)"
	@echo "  dev-backend-scrape   Run scraping (dev)"
	@echo "  dev-backend-test     Run backend tests (dev)"
	@echo ""
	@echo "PRODUCTION COMMANDS:"
	@echo "  prod                 Start production environment"
	@echo "  prod-build           Build production containers"
	@echo "  prod-up              Start production environment in background"
	@echo "  prod-down            Stop production environment"
	@echo "  prod-logs            Show production logs"
	@echo "  prod-restart         Restart production environment"
	@echo "  prod-init-db         Initialize database tables (prod)"
	@echo ""
	@echo "BACKEND TASKS (Production):"
	@echo "  prod-backend-init    Initialize backend (prod)"
	@echo "  prod-backend-init-auth Initialize auth database (prod)"
	@echo "  prod-migrate  Apply all migrations (prod)"
	@echo "  prod-migrate-status Check migration status (prod)"
	@echo "  prod-backend-migrate-history Show migration history (prod)"
	@echo "  prod-backend-seed    Create sample data (prod)"
	@echo "  prod-backend-scrape  Run scraping (prod)"
	@echo "  prod-backend-test    Run backend tests (prod)"
	@echo ""
	@echo "UTILITY COMMANDS:"
	@echo "  clean                Clean all containers and volumes"
	@echo "  clean-dev            Clean development containers and volumes"
	@echo "  clean-prod           Clean production containers and volumes"
	@echo "  check-host-ip        Show your host machine IP addresses"
	@echo "  dev-expose-host      Start OAuth with host networking (dev)"
	@echo "  prod-expose-host     Start OAuth with host networking (prod)"
	@echo ""
	@echo "URLs:"
	@echo "  Development:"
	@echo "    Frontend: http://localhost:5173"
	@echo "    Backend:  http://localhost:8000"
	@echo "    API Docs: http://localhost:8000/docs"
	@echo "  Production:"
	@echo "    Frontend: http://localhost:3000"
	@echo "    Backend:  http://localhost:8000"
	@echo "    API Docs: http://localhost:8000/docs" 