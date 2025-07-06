# Assembly Directory

This directory contains all environment and deployment-related files for the TalentTrek project, organized by environment type.

## Directory Structure

```
assembly/
├── dev/                    # Development environment files
│   ├── dev.sh             # Development startup script for Linux/macOS
│   ├── dev.bat            # Development startup script for Windows
│   └── docker-compose.dev.yml  # Development Docker Compose configuration
└── prod/                   # Production environment files
    ├── prod.sh            # Production startup script for Linux/macOS
    ├── prod.bat           # Production startup script for Windows
    └── docker-compose.yml # Production Docker Compose configuration
```

## Files

### Development Environment (`dev/`)
- **`dev.sh`** - Development startup script for Linux/macOS
- **`dev.bat`** - Development startup script for Windows
- **`docker-compose.dev.yml`** - Development Docker Compose configuration with auto-reload

### Production Environment (`prod/`)
- **`prod.sh`** - Production startup script for Linux/macOS
- **`prod.bat`** - Production startup script for Windows
- **`docker-compose.yml`** - Production Docker Compose configuration

## Usage

### Development Environment
```bash
# Linux/macOS
./assembly/dev/dev.sh

# Windows
assembly/dev/dev.bat
```

### Production Environment
```bash
# Linux/macOS
./assembly/prod/prod.sh

# Windows
assembly/prod/prod.bat
```

### Manual Docker Compose Commands
```bash
# Development
docker-compose -f assembly/dev/docker-compose.dev.yml up --build

# Production
docker-compose -f assembly/prod/docker-compose.yml up -d
```

## Features

### Development Environment
- Auto-reload for both frontend and backend
- Volume mounts for live code editing
- Development dependencies included
- Hot reload enabled

### Production Environment
- Optimized builds
- No auto-reload (performance focused)
- Production-ready configuration
- Detached mode operation

## Ports

### Development
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Production
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs 