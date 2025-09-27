## Docker Installation Procedure
1. Install WSL
>> wsl --install
(in admin Powershell)
Restart PC
2. Download Docker Desktop
3. Run:
>> docker-compose up -d
(in the folder where your docker-compose.yml is)


### Full file structure:

mongoDB_project/
├── .gitignore/
├── CRUD_Indexing_Aggregation/
└── storeApi/
│   ├── venv/
│   ├── data/  
│   ├── Dockerfile
│   ├── docker-compose.yml
│   ├── requirements.txt
│   └── app.py






# CRUD, Indexation & Aggregation :

### Recommended Project Structure

CRUD_Indexing_Aggregation/
├── docker-compose.yml
├── data/                         # Raw data files (JSON, CSV)
│   └── movies.json
├── exercises/                    # Python scripts
│   ├── db_connect.py                   # functions like : get_db, showDB, cleanup
│   ├── importData.py                   # populate DB from movies.json
│   ├── x1.py
│   ├── x2.py
│   ├── x3.py
│   ├── cleanup.py                      # callable script from terminal to interact with db
│   └── requirements.txt                # pymongo, dnspython
├── js_scripts/                    # Javascript scripts
│   ├── import_data.js
│   ├── queries.js
│   ├── updates.js
│   └── cleanup.js
└── README.md


# Store API:

### Structure :
storeApi/
├── /venv
├── app/
│   ├── app.py
│   ├── data/
│   │   ├── games.json
│   │   └── clients.json
├── Dockerfile
├── docker-compose.yml
└── requirements.txt



Setup venv (Open powershell as admin):
>> cd "C:\Users\user\Desktop\"
>> cd storeAPI
>> python -m venv venv
Activate venv:
>> .\venv\Scripts\Activate.ps1
Install Dependencies :
>> pip install -r requirements.txt

Launch:
>> docker compose up -d
>> docker exec -it mypython bash
>> python app.py
