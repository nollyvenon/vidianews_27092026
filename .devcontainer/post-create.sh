#!/bin/bash
set -e

echo "🚀 Setting up vidianews development environment..."

# Backend setup
echo "📦 Setting up backend (FastAPI)..."
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install ipython ipdb
cd ..

# Frontend setup
echo "📦 Setting up frontend (Next.js)..."
cd frontend
npm install
cd ..

# Mobile setup (if available)
if [ -d "mobile" ]; then
  echo "📱 Setting up mobile (Flutter)..."
  cd mobile
  flutter pub get
  cd ..
fi

# Create .env files from examples
echo "⚙️  Creating environment configuration..."
if [ ! -f "backend/.env" ] && [ -f "backend/.env.example" ]; then
  cp backend/.env.example backend/.env
  echo "✅ Created backend/.env"
fi

# Initialize database
echo "🗄️  Initializing PostgreSQL..."
sleep 5  # Wait for postgres to start
cd backend
alembic upgrade head || echo "⚠️  Database migrations may already be applied"
cd ..

# Start services in background
echo "🔄 Starting services..."
docker-compose up -d postgres redis

# Wait for services
echo "⏳ Waiting for services to start..."
sleep 10

# Run tests to verify setup
echo "🧪 Running tests to verify setup..."
cd backend
pytest tests/ -x --tb=short || echo "⚠️  Some tests may be failing - check logs"
cd ..

# Install pre-commit hooks
echo "🪝 Installing git hooks..."
pip install pre-commit
pre-commit install || echo "⚠️  Pre-commit setup incomplete"

echo ""
echo "✅ Development environment ready!"
echo ""
echo "📚 Next steps:"
echo "  1. Backend:  cd backend && uvicorn app.main:app --reload"
echo "  2. Frontend: cd frontend && npm run dev"
echo "  3. Mobile:   cd mobile && flutter run"
echo ""
echo "🔗 Services available at:"
echo "  • Frontend:  http://localhost:3000"
echo "  • Backend:   http://localhost:8000"
echo "  • API Docs:  http://localhost:8000/docs"
echo "  • Redis:     localhost:6379"
echo "  • Postgres:  localhost:5432"
echo ""
echo "💡 Tips:"
echo "  • Use 'git branch -b module/X-feature-name' for module development"
echo "  • Run tests before committing: pytest tests/ --cov=app"
echo "  • Check linting: flake8 app && mypy app"
echo ""
