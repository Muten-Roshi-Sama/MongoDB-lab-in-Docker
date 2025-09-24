// scripts/99_cleanup.js
db = db.getSiblingDB('movies');

print("=== DATABASE CLEANUP ===");

// Show before state
var beforeCount = db.movies.countDocuments();
print("📊 Movies before cleanup: " + beforeCount);

// Method 1: Delete all documents but keep collection
print("\n1. Deleting all documents...");
var deleteResult = db.movies.deleteMany({});
print("✅ Deleted " + deleteResult.deletedCount + " movies");

// Method 2: Drop the entire collection (more thorough)
// print("\nDropping entire collection...");
// db.movies.drop();
// print("✅ Collection dropped");

// Method 3: Drop the entire database
// db.dropDatabase();
// print("✅ Database dropped");

// Show after state
// var afterCount = db.movies.countDocuments();
// print("📊 Movies after cleanup: " + afterCount);
// print("✅ Cleanup completed!");