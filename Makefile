# Both server and frontend together

setup:
	docker-compose build server app
	docker-compose up -d server app

up:
	docker-compose up -d server app

build:
	docker-compose build server app

down:
	docker-compose down

restart:
	docker-compose down
	docker-compose up -d server app

rebuild:
	docker-compose down
	docker-compose build server app

re:
	docker-compose down
	docker-compose build server app
	docker-compose up -d server app

# Development with auto-reload
dev:
	docker-compose -f docker-compose.dev.yml up --build

dev-build:
	docker-compose -f docker-compose.dev.yml build

dev-up:
	docker-compose -f docker-compose.dev.yml up -d

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-logs:
	docker-compose -f docker-compose.dev.yml logs -f

dev-restart:
	docker-compose -f docker-compose.dev.yml restart

dev-init-db:
	docker-compose -f docker-compose.dev.yml exec -T server python init_supabase_db.py

# Local development
local-backend:
	cd server && uvicorn src.api.v1:app --reload --host 0.0.0.0 --port 8000

local-frontend:
	cd app && npm run dev

# Docker Compose

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Backend tasks via Docker Compose

docker-backend-init:
	docker-compose run server python main.py

docker-backend-init-auth:
	docker-compose run server python init_auth_db.py

docker-backend-init-supabase:
	docker-compose run server python init_supabase_db.py

docker-backend-scrape:
	docker-compose run server python -m src.cli.interface scrape

docker-backend-analyze:
	docker-compose run server python -m src.cli.interface analyze

docker-backend-report:
	docker-compose run server python -m src.cli.interface report

docker-backend-test:
	docker-compose run server pytest

# Makefile for TalentTrek: Local and Docker-based commands
.PHONY: help local-backend local-frontend docker-build docker-up docker-down docker-logs \
        docker-backend-init docker-backend-init-auth docker-backend-init-supabase docker-backend-scrape docker-backend-analyze docker-backend-report docker-backend-test \
        dev dev-build dev-up dev-down dev-logs dev-restart

help:
	@echo "Available targets:"
	@echo ""
	@echo "Production (Docker):"
	@echo "  setup                Build and start both server and frontend (Docker)"
	@echo "  up                   Start both server and frontend together (Docker)"
	@echo "  build                Build both server and frontend together (Docker)"
	@echo "  down                 Stop both server and frontend together (Docker)"
	@echo "  restart              Restart both server and frontend together (Docker)"
	@echo "  rebuild              Rebuild both server and frontend together (Docker) and start"
	@echo "  re                   Rebuild and restart both server and frontend together (Docker)"
	@echo ""
	@echo "Development (Auto-reload):"
	@echo "  dev                  Start development environment with auto-reload"
	@echo "  dev-build            Build development containers"
	@echo "  dev-up               Start development environment"
	@echo "  dev-down             Stop development environment"
	@echo "  dev-logs             Show development logs"
	@echo "  dev-restart          Restart development environment"
	@echo "  dev-init-db          Initialize database tables"
	@echo ""
	@echo "Local Development:"
	@echo "  local-backend        Run backend locally (requires Python env)"
	@echo "  local-frontend       Run frontend locally (requires Node env)"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build         Build all Docker images"
	@echo "  docker-up            Start all services with Docker Compose"
	@echo "  docker-down          Stop all Docker Compose services"
	@echo "  docker-logs          Show logs for all Docker Compose services"
	@echo "  docker-backend-init  Init backend DB via Docker"
	@echo "  docker-backend-init-auth Init backend DB with authentication via Docker"
	@echo "  docker-backend-init-supabase Init backend DB with Supabase PostgreSQL via Docker"
	@echo "  docker-backend-scrape Run scraping via Docker"
	@echo "  docker-backend-analyze Run analysis via Docker"
	@echo "  docker-backend-report Run report via Docker"
	@echo "  docker-backend-test  Run backend tests via Docker"
