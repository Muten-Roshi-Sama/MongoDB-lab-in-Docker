// scripts/04_delete_movies.js
db = db.getSiblingDB('movies');

print("=== DELETING MOVIES ===");

// Show current state
var beforeCount = db.movies.countDocuments();
print("📊 Movies before deletion: " + beforeCount);

// Delete single movie
print("\n1. Deleting single movie - Pulp Fiction:");
var deleteSingle = db.movies.deleteOne({title: "Pulp Fiction"});
print("✅ Deleted " + deleteSingle.deletedCount + " movie");

// Delete multiple movies by condition
print("\n2. Deleting all movies before 1990:");
var deleteMultiple = db.movies.deleteMany({year: {$lt: 1990}});
print("✅ Deleted " + deleteMultiple.deletedCount + " movies from before 1990");

// Delete by genre
print("\n3. Deleting all Crime genre movies:");
var deleteByGenre = db.movies.deleteMany({genre: "Crime"});
print("✅ Deleted " + deleteByGenre.deletedCount + " Crime movies");

// Show remaining movies
var afterCount = db.movies.countDocuments();
print("\n📊 Movies after deletion: " + afterCount);

print("\n🎬 Remaining movies:");
db.movies.find({}, {title: 1, year: 1, genre: 1, _id: 0}).sort({year: 1}).forEach(printjson);