# Filesystem Indexer

A Python-based tool that recursively scans a folder, extracts file metadata, and stores it in a PostgreSQL database for efficient querying and analysis.

## Features
- Recursive filesystem scanning
- Stores file metadata (path, size, timestamps, extension)
- PostgreSQL-backed index
- Safe insert/update/delete with transactional integrity
- Query-ready data for disk usage analysis

## Project Structure
src/
├── main.py # orchestration
├── scanner.py # filesystem scanning
├── repository.py # DB insert/update/delete logic
├── queries.py # read-only insight queries
├── database.py # engine + session handling
├── orm.py # SQLAlchemy models
└── utils.py # helpers

## Requirements
- Python 3.10+
- PostgreSQL 
- SQLAlchemy
- python-dotenv

## Usage
1. Configure database credentials in `.env`
2. Run the indexer:
   ```bash
   python src/main.py
