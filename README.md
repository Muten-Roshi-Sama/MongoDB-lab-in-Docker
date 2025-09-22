## Installation Procedure
1. Install WSL
>> wsl --install
(in admin Powershell)
Restart PC
2. Download Docker Desktop
3. Run:
>> docker-compose up -d
(in the folder where your docker-compose.yml is)




## Recommended Project Structure

mongodb-project/
├── docker-compose.yml
├── data/                         # Raw data files (JSON, CSV)
│   └── movies.json
├── python_scripts/                    # Python scripts
│   ├── 01_import_data.py
│   ├── 02_add_movies.py
│   ├── 03_update_movies.py
│   ├── 04_delete_movies.py
│   ├── 05_complex_queries.py
│   ├── 99_cleanup.py
│   └── requirements.txt
├── js_scripts/                            # Javascript scripts
│   ├── import_data.js
│   ├── queries.js
│   ├── updates.js
│   └── cleanup.js
└── README.md


