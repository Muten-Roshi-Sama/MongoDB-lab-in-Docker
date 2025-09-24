// scripts/05_complex_queries.js
db = db.getSiblingDB('movies');

print("=== COMPLEX QUERIES AND AGGREGATIONS ===");

// Basic find queries
print("\n1. Movies after 2000 with rating > 8.5:");
db.movies.find({
    year: {$gt: 2000},
    rating: {$gt: 8.5}
}, {title: 1, year: 1, rating: 1, _id: 0}).sort({rating: -1}).forEach(printjson);

// Aggregation pipeline - Average rating by genre
print("\n2. Average rating by genre:");
db.movies.aggregate([
    {$group: {
        _id: "$genre",
        averageRating: {$avg: "$rating"},
        movieCount: {$sum: 1}
    }},
    {$sort: {averageRating: -1}}
]).forEach(printjson);

// Text search (if text index exists)
print("\n3. Movies with 'Dark' in title:");
db.movies.find({
    title: {$regex: "Dark", $options: "i"}
}, {title: 1, year: 1, _id: 0}).forEach(printjson);

// Complex condition with $or
print("\n4. Movies by Nolan OR before 1980:");
db.movies.find({
    $or: [
        {director: "Christopher Nolan"},
        {year: {$lt: 1980}}
    ]
}, {title: 1, director: 1, year: 1, _id: 0}).sort({year: 1}).forEach(printjson);