# UPTM Housing Hub

A centralized web platform for UPTM (Universiti Poly-Tech Malaysia) students to find and post housing listings near campus. Built as a Final Year Project and extended with advanced MariaDB features for a hackathon.

## Features

### Core Features
- Browse and search housing listings
- Post new housing listings with multiple images
- Map view showing all listings locations
- User registration, login and profile management
- Admin moderation and listing verification

### MariaDB Advanced Features
- **Full-Text Search** — Intelligent relevance-ranked search across title, description, address, facilities, accessibilities, furnished type and gender using MariaDB native FULLTEXT indexing
- **System Versioning (Temporal Tables)** — Automatic tracking of every change made to a listing at the database level, allowing students to view the full price and detail history of any listing

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10 |
| Framework | Django 5.0 |
| Database | MariaDB 10.11 |
| Frontend | HTML, CSS, Bootstrap 4 |
| Maps | Folium + OpenStreetMap |
| Forms | Django Crispy Forms |
| Filtering | Django Filter |
| Containerization | Docker + Docker Compose |

## Requirements

- Docker
- Docker Compose
- Git

## Quick Start

### 1. Clone the repository
git clone -b hackathon https://github.com/syedaidid/UPTM-Housing-Hub.git
cd UPTM-Housing-Hub

### 2. Setup environment variables
cp .env.example .env

Open `.env` and fill in your values if needed. Default values work out of the box for local development.

### 3. Start the application
sudo docker-compose up --build

Wait for both containers to be healthy. You should see:
web-1  | Watching for file changes with StatReloader

### 4. Create admin user (first time only)
Open a new terminal:
sudo docker-compose exec web python manage.py createsuperuser

### 5. Visit the app
http://localhost:8000

## Usage

### Running the app
```bash
# Start
sudo docker-compose up

# Start in background
sudo docker-compose up -d

# Stop
sudo docker-compose down

# View logs
sudo docker-compose logs -f
```

### Reset everything (wipe database)
```bash
sudo docker-compose down -v
sudo docker-compose up --build
```

## MariaDB Features Demo

### Full-Text Search
1. Click **Search** in the navbar
2. Try searching:
   - `furnished` — finds all furnished listings
   - `female WiFi` — finds female listings with WiFi
   - `Cheras` — finds listings in Cheras area
   - `swimming pool` — finds listings with that facility
3. Combine with price filter for advanced search
   - Search `furnished` + Max price 600

### Listing History (Temporal Tables)
1. Go to any listing detail page
2. Click **View History** button
3. See the complete history of all changes made to that listing including price changes over time
4. This is powered entirely by MariaDB System Versioning — zero extra application code needed

## Project Structure
UPTM-Housing-Hub/
├── UPTMHousingHub/        # Django project settings and URLs
├── post/                  # Housing listings app
│   ├── models.py          # HousingPost and Image models
│   ├── views.py           # All views including search and history
│   ├── migrations/        # Database migrations including FULLTEXT and System Versioning
│   └── templates/post/    # HTML templates
├── users/                 # User profiles app
├── static_pages/          # Static pages (home, about) and base template
├── Dockerfile             # Docker image definition
├── docker-compose.yml     # Multi-container setup (Django + MariaDB)
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variables template

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| SECRET_KEY | Django secret key | (required) |
| DB_NAME | Database name | UPTMHH |
| DB_USER | Database user | root |
| DB_PASSWORD | Database password | (empty) |
| DB_HOST | Database host | db |
| DB_PORT | Database port | 3306 |
| EMAIL_HOST_USER | Gmail address for password reset | (optional) |
| EMAIL_HOST_PASSWORD | Gmail app password | (optional) |

## Author

Syed Amer Aidid bin Syed Mohd Bakri
Universiti Poly-Tech Malaysia (UPTM)
Diploma in Computer Science
