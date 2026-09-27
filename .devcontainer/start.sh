#!/bin/bash
set -e

echo "🚀 VidiNews Platform - Starting Services in GitHub Codespaces"
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Start PostgreSQL and Redis in background
echo -e "${BLUE}Starting PostgreSQL and Redis...${NC}"
docker-compose up -d postgres redis

# Wait for database to be ready
echo -e "${BLUE}Waiting for PostgreSQL to be ready...${NC}"
sleep 5

# Run migrations
echo -e "${BLUE}Running database migrations...${NC}"
cd backend
python -m alembic upgrade head
cd ..

# Start backend
echo -e "${BLUE}Starting FastAPI backend...${NC}"
cd backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > backend.log 2>&1 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"
cd ..

# Wait for backend to start
echo -e "${BLUE}Waiting for backend to start...${NC}"
sleep 5

# Start frontend
echo -e "${BLUE}Starting Next.js frontend...${NC}"
cd frontend
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"
cd ..

echo ""
echo -e "${GREEN}✅ All services started!${NC}"
echo ""
echo -e "${YELLOW}📚 Services Available:${NC}"
echo -e "  ${GREEN}Frontend:${NC}  http://localhost:3000"
echo -e "  ${GREEN}Backend:${NC}   http://localhost:8000"
echo -e "  ${GREEN}API Docs:${NC}  http://localhost:8000/docs"
echo -e "  ${GREEN}Postgres:${NC}  localhost:5432"
echo -e "  ${GREEN}Redis:${NC}     localhost:6379"
echo ""
echo -e "${YELLOW}🔗 Logs:${NC}"
echo -e "  ${GREEN}Backend:${NC}   tail -f backend/backend.log"
echo -e "  ${GREEN}Frontend:${NC}  tail -f frontend/frontend.log"
echo ""
echo -e "${YELLOW}🛑 To stop services:${NC}"
echo -e "  kill $BACKEND_PID  # Stop backend"
echo -e "  kill $FRONTEND_PID # Stop frontend"
echo -e "  docker-compose down"
echo ""
echo -e "${YELLOW}📖 Documentation:${NC}"
echo -e "  - API Spec: http://localhost:8000/docs (Swagger UI)"
echo -e "  - API ReDoc: http://localhost:8000/redoc"
echo -e "  - Module 10: docs/MODULE_10_CONTENT_MANAGEMENT.md"
echo ""
