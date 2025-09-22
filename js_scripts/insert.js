// scripts/02_add_movies.js
db = db.getSiblingDB('movies');

print("=== ADDING NEW MOVIES ===");

// Add single movie
print("\n1. Adding single movie:");
var singleResult = db.movies.insertOne({
    "title": "Inception",
    "director": "Christopher Nolan",
    "year": 2010,
    "genre": "Science Fiction",
    "actors": ["Leonardo DiCaprio", "Joseph Gordon-Levitt", "Elliot Page"],
    "rating": 8.8
});
print("✅ Added: Inception (2010)");

// Add multiple movies
print("\n2. Adding multiple movies:");
var multipleResult = db.movies.insertMany([
    {
        "title": "Parasite",
        "director": "Bong Joon-ho", 
        "year": 2019,
        "genre": "Thriller",
        "actors": ["Song Kang-ho", "Choi Woo-shik", "Park So-dam"],
        "rating": 8.6
    },
    {
        "title": "The Dark Knight",
        "director": "Christopher Nolan",
        "year": 2008, 
        "genre": "Action",
        "actors": ["Christian Bale", "Heath Ledger", "Aaron Eckhart"],
        "rating": 9.0
    }
]);
print("✅ Added " + multipleResult.insertedCount + " more movies");

// Show current count
var totalCount = db.movies.countDocuments();
print("\n📊 Total movies in database: " + totalCount);

// Show newly added movies
print("\n🎬 Newly added movies:");
db.movies.find({year: {$gte: 2008}}, {title: 1, year: 1, director: 1, _id: 0}).sort({year: -1}).forEach(printjson);