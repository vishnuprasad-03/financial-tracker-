#!/bin/sh

echo "🚀 Starting Finance Tracker..."

echo "📦 Creating database tables..."
python -m src.create_db

echo "🌐 Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 app:app