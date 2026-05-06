# UPTM Housing Hub

A centralized housing platform for UPTM students built with Django and MariaDB.

## Features
- Full-Text Search using MariaDB FULLTEXT indexing
- Listing History using MariaDB System Versioning (Temporal Tables)
- Housing listings with map view
- User profiles and admin moderation

## Requirements
- Docker
- Docker Compose

## Setup

1. Clone the repo
   git clone <your-repo-url>
   cd UPTM-Housing-Hub

2. Copy and fill in environment variables
   cp .env.example .env

3. Add default profile image to media folder
   mkdir -p media
   (add a default.jpg to the media/ folder)

4. Start the app
   sudo docker-compose up --build

5. Create admin user (first time only)
   sudo docker-compose exec web python manage.py createsuperuser

6. Visit http://localhost:8000
