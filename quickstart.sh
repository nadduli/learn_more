#!/bin/bash
# Quick Start Script for Learn More API

echo "🚀 Learn More API - Quick Start"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please update .env with your database credentials!"
    echo ""
    exit 1
fi

echo "1️⃣  Installing dependencies..."
uv sync
echo "✅ Dependencies installed"
echo ""

echo "2️⃣  Running database migrations..."
alembic upgrade head
echo "✅ Migrations applied"
echo ""

echo "3️⃣  Seeding initial roles..."
uv run python -m app.db.init_db
echo "✅ Roles seeded"
echo ""

echo "4️⃣  Running tests..."
uv run python test_phase1.py
echo ""

echo "================================"
echo "✨ Setup complete!"
echo ""
echo "To start the server, run:"
echo "  uv run python main.py"
echo ""
echo "Then visit:"
echo "  📚 API Docs: http://localhost:8000/api/v1/docs"
echo "  📖 ReDoc: http://localhost:8000/api/v1/redoc"
echo "  🏠 API: http://localhost:8000"
echo ""
