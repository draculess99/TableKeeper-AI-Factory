# Stage 1 - TableKeeper Reservation Service

This is a complete, buildable Stage 1 implementation of the TableKeeper service. It contains everything needed to run, test, and deploy the service independently.

## Quick Start

### Prerequisites
- Python 3.8+ or Docker

### Local Development (Windows PowerShell)

**1. Set up virtual environment:**
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**2. Run the service:**
```powershell
python app.py
```
The service will start on `http://localhost:5000`

**3. Run tests:**
```powershell
pytest test_app.py -v
```

**Expected output:** 15 tests pass

### Docker Deployment

**1. Build the image:**
```powershell
docker build -t tablekeeper-stage1 .
```

**2. Run the container:**
```powershell
docker run -p 5000:5000 tablekeeper-stage1
```

**3. Verify:**
Visit `http://localhost:5000` in your browser

## Service Structure

```
stage-1/
├── app.py              # Main Flask application
├── test_app.py         # Pytest suite (15 tests)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container image definition
├── templates/
│   └── index.html      # Web UI
└── README.md           # This file
```

## Architecture

- **Backend**: Python 3.x with Flask
- **Database**: SQLite (embedded, file-based)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Testing**: pytest with 15 comprehensive tests

## Features Verified

✅ Create reservations with validation  
✅ Prevent double-booking (conflict detection)  
✅ List existing reservations  
✅ Delete reservations  
✅ Party size validation  
✅ Time range validation  
✅ Table capacity validation  

## Testing

The service includes 15 automated tests covering:

**API Endpoints:**
- GET /api/restaurants
- GET /api/tables/{restaurant_id}
- GET /api/reservations
- POST /api/reservations (create)
- DELETE /api/reservations/{id} (delete)

**Business Logic:**
- Successful reservation creation
- Overlap detection (double-booking prevention)
- Capacity validation
- Time validation
- Deletion workflow

**Run tests:**
```powershell
pytest test_app.py -v
```

## Configuration

Environment variables:
- `FLASK_ENV`: Set to `production` by default
- `FLASK_DEBUG`: Set to `false` by default (set to `true` for local debugging)
- `PORT`: Defaults to 5000 (auto-configured in containerized environments)

## Known Limitations (Stage 1)

- SQLite database is ephemeral (resets on restart)
- Designed for demo/hackathon use
- No persistent storage (suitable for time-limited demonstrations)
- Single-process deployment

For production use, migrate to a persistent database (PostgreSQL/MySQL) and multi-process deployment.

## Troubleshooting

**Port already in use:**
```powershell
# Set custom port
$env:PORT = 5001
python app.py
```

**Clean database:**
```powershell
Remove-Item tablekeeper.db -Force
python app.py
```

**Virtual environment issues:**
```powershell
deactivate
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Deployment

### Railway
1. Push this folder to a GitHub repository
2. Connect to Railway
3. No environment variables required (defaults handle everything)

### Local Docker
```powershell
docker build -t tablekeeper-stage1 .
docker run -p 5000:5000 tablekeeper-stage1
```

## Support

For issues or questions, refer to the comprehensive test suite in `test_app.py` for usage examples.
