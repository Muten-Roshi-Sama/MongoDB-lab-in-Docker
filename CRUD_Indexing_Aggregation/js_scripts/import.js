// scripts/01_import_data.js
db = db.getSiblingDB('movies');

print("=== IMPORTING MOVIES FROM JSON FILE ===");

// Load the JSON data file
load("/shared_data/movies.json");




// Insert the new data
var result = db.movies.insertMany(movieData);
print("✅ Successfully imported " + result.insertedCount + " movies");
