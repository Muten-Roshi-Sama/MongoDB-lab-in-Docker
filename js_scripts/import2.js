// scripts/01_import_data.js - Advanced method
db = db.getSiblingDB('movies');

print("=== IMPORTING MOVIES FROM JSON ===");

// Read and parse JSON file
var jsonData = cat("/shared_data/movies.json");
var movieData = JSON.parse(jsonData);

db.movies.deleteMany({});
var result = db.movies.insertMany(movieData);
print("✅ Imported " + result.insertedCount + " movies");