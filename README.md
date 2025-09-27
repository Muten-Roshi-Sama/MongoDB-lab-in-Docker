





### Full file structure:

mongoDB_project/
├── .gitignore/
├── README.md
├── CRUD_Indexing_Aggregation/
└── storeApi/



# CRUD, Indexation & Aggregation :

### Project Structure

CRUD_Indexing_Aggregation/
├── docker-compose.yml
├── data/                         # Raw data files (JSON, CSV)
│   └── movies.json
├── exercises/                    # Python scripts
│   ├── db_connect.py                   # definition of functions like : get_db, showDB, cleanup
│   ├── importData.py                   # CALLABLE : populate DB from movies.json
│   ├── showDB.py                       # CALLABLE : show all collections contents
│   ├── cleanup.py                      # CALLABLE : drop all collections
│   ├── 
│   ├── x1.py                           # all $ operators implementation examples
│   ├── x2.py                           # Indexation
│   ├── x3.py                           # Pipeline Aggregation
│   ├── 
│   └── requirements.txt                # pymongo, dnspython, request, ...
└── js_scripts/


Note :
    CALLABLE means script from terminal to interact with db.




# Store API:

### Structure :
storeApi/
├── /venv
├── app/
│   ├── app.py
│   ├── test_routes.py
│   ├── data/
│   │   ├── games.json
│   │   └── clients.json
├── Dockerfile
├── docker-compose.yml
└── requirements.txt


To launch the storeAPI app :
>> docker compose up -d         # or docker build if needed
this will automatically launch the Flask app.py server.

To test/interact (test_routes.py) :
>> docker exec -it mypython bash
>> python test_routes.py  # in another terminal

Modify (comment/Uncomment) the test_routes.py for your testing purposes.



Setup venv (Open powershell as admin):
>> cd "C:\Users\user\Desktop\ ..."
>> cd storeAPI
>> python -m venv venv
Activate venv:
>> .\venv\Scripts\Activate.ps1
Install Dependencies :
>> pip install -r requirements.txt




## Docker Installation Procedure on Windows:
1. Install WSL
>> wsl --install
(in admin Powershell)
Restart PC
2. Download Docker Desktop
3. Run:
>> docker-compose up -d
(in the folder where your docker-compose.yml is)