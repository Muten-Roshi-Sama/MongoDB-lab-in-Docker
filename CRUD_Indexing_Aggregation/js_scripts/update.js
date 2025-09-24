// scripts/03_update_movies.js
db = db.getSiblingDB('movies');

print("=== UPDATING MOVIES ===");

// Update single movie
print("\n1. Updating single movie - Adding award to The Godfather:");
var updateSingle = db.movies.updateOne(
    {title: "The Godfather"},
    {$set: {awards: ["Best Picture", "Best Actor"]}}
);
print("✅ Updated " + updateSingle.modifiedCount + " document");

// Update multiple movies
print("\n2. Adding 'classic' tag to movies before 2000:");
var updateMultiple = db.movies.updateMany(
    {year: {$lt: 2000}},
    {$set: {tags: ["classic"]}}
);
print("✅ Added classic tag to " + updateMultiple.modifiedCount + " movies");

// Increment ratings for specific director
print("\n3. Increasing ratings for Christopher Nolan movies:");
var incrementUpdate = db.movies.updateMany(
    {director: "Christopher Nolan"},
    {$inc: {rating: 0.2}}  // Increase rating by 0.2
);
print("✅ Updated ratings for " + incrementUpdate.modifiedCount + " Nolan movies");

// Add to array (actors)
print("\n4. Adding new actor to The Matrix:");
var arrayUpdate = db.movies.updateOne(
    {title: "The Matrix"},
    {$push: {actors: "Hugo Weaving"}}
);
print("✅ Added Hugo Weaving to The Matrix cast");

// Show updates
print("\n📊 Updated movies:");
db.movies.find(
    {$or: [
        {title: "The Godfather"},
        {director: "Christopher Nolan"},
        {title: "The Matrix"}
    ]}, 
    {title: 1, director: 1, rating: 1, awards: 1, tags: 1, actors: 1, _id: 0}
).forEach(printjson);