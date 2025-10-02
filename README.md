
# MongoDB Projects

MongoDB + Docker implementation lab with sample data and scripts for learning and experimentation.

### Full file structure:
```
mongoDB_project/
├── CRUD_Indexing_Aggregation/
└── storeApi/
```
- **CRUD_Indexing_Aggregation**: MongoDB exercises - basic operations, indexing, aggregation pipelines.
- **Store API**: Full Flask REST API with MongoDB - CRUD operations for a game store.

Both use MongoDB in Docker containers.

---

## CRUD, Indexation & Aggregation Project

### Project Structure

```
CRUD_Indexing_Aggregation/
├── docker-compose.yml
├── data/                         # Raw data files (JSON, CSV)
│   └── movies.json
├── exercises/                    # Python scripts
│   ├── db_connect.py            # DB functions: get_db, showDB, cleanup
│   ├── importData.py            # CALLABLE: populate DB from movies.json
│   ├── showDB.py                # CALLABLE: show all collections contents
│   ├── cleanup.py               # CALLABLE: drop all collections
│   ├── x1.py                    # All $ operators implementation examples
│   ├── x2.py                    # Indexation
│   ├── x3.py                    # Pipeline Aggregation
│   └── requirements.txt         # pymongo, dnspython, requests, ...
└── js_scripts/
```

**Note:**  
- CALLABLE = scripts you can run from terminal to interact with DB  
- Just run the Python files to see what they do :

**Quick start:**
```bash
docker-compose up -d
python exercises/importData.py    # Populate the DB
python exercises/showDB.py        # Check what's in there
```

---
---

## Store API Project

### Structure

```
storeApi/
├── /venv
├── app/
│   ├── app.py                    # Main Flask app
│   ├── test_routes.py            # Testing script
│   ├── data/
│   │   ├── games.json
│   │   └── clients.json
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

### How to run this thing:

**Launch the API:**
```bash
docker compose up -d         # or docker build if you changed stuff
```
This starts the Flask server automatically.

**To test/interact:**
```bash
docker exec -it mypython bash    # Get into the container
python test_routes.py           # Run tests in another terminal
```
**Pro tip:** Comment/uncomment stuff in `test_routes.py` depending on what you want to test.

### Local dev setup (if you don't wanna use Docker):

**Setup venv (Open PowerShell as admin):**
```bash
cd "C:\Users\user\Desktop\..."    # Wherever you put this
cd storeApi
python -m venv venv
```

**Activate venv:**
```bash
.\venv\Scripts\Activate.ps1
```

**Install what you need:**
```bash
pip install -r requirements.txt
```

---

## Docker Installation on Windows (if you need it):

1. **Install WSL:**
   ```bash
   wsl --install    # Run in admin PowerShell
   ```
   Then restart your PC.

2. **Download Docker Desktop** and install it.

3. **Run your projects:**
   ```bash
   docker-compose up -d    # In the folder with docker-compose.yml
   ```

---

