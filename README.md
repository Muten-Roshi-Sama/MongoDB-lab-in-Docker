## Docker Installation Procedure
1. Install WSL
>> wsl --install
(in admin Powershell)
Restart PC
2. Download Docker Desktop
3. Run:
>> docker-compose up -d
(in the folder where your docker-compose.yml is)

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
├── data/                        
│   ├── games.json
│   └── clients.json
├── app.py # Main Flask application
├── requirements.txt
├── Dockerfile
└── docker-compose.yml


Setup venv (Open powershell as admin):
>> cd "C:\Users\user\Desktop\"
>> cd storeAPI
>> python -m venv venv
Activate venv:
>> .\venv\Scripts\Activate.ps1
Install Dependencies :
>> pip install -r requirements.txt


