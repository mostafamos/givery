from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for recipes
recipes = [
    {
        "id": 1,
        "title": "Chicken Curry",
        "making_time": "45 min",
        "serves": "4 people",
        "ingredients": "onion, chicken, seasoning",
        "cost": "1000"
    },
    {
        "id": 2,
        "title": "Rice Omelette",
        "making_time": "30 min",
        "serves": "2 people",
        "ingredients": "onion, egg, seasoning, soy sauce",
        "cost": "700"
    }
]
recipe_id_counter = 3

# Get all recipes
@app.route('/recipes', methods=['GET'])
def get_recipes():
    return jsonify({"recipes": recipes}), 200

# Get a recipe by ID
@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if recipe:
        return jsonify({
            "message": "Recipe details by id",
            "recipe": [recipe]
        }), 200
    return jsonify({"message": "No recipe found"}), 404

# Add a new recipe
@app.route('/recipes', methods=['POST'])
def add_recipe():
    global recipe_id_counter
    data = request.json
    required_fields = ["title", "making_time", "serves", "ingredients", "cost"]
    if not all(field in data for field in required_fields):
        return jsonify({
            "message": "Recipe creation failed!",
            "required": "title, making_time, serves, ingredients, cost"
        }), 400
    new_recipe = {
        "id": recipe_id_counter,
        "title": data["title"],
        "making_time": data["making_time"],
        "serves": data["serves"],
        "ingredients": data["ingredients"],
        "cost": data["cost"],
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    recipes.append(new_recipe)
    recipe_id_counter += 1
    return jsonify({
        "message": "Recipe successfully created!",
        "recipe": [new_recipe]
    }), 201

# Update a recipe by ID
@app.route('/recipes/<int:recipe_id>', methods=['PUT'])
def update_recipe(recipe_id):
    data = request.json
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if recipe:
        recipe.update({
            "title": data.get("title", recipe["title"]),
            "making_time": data.get("making_time", recipe["making_time"]),
            "serves": data.get("serves", recipe["serves"]),
            "ingredients": data.get("ingredients", recipe["ingredients"]),
            "cost": data.get("cost", recipe["cost"]),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        return jsonify({
            "message": "Recipe successfully updated!",
            "recipe": [recipe]
        }), 200
    return jsonify({"message": "No recipe found"}), 404

# Delete a recipe by ID
@app.route('/recipes/<int:recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id):
    global recipes
    recipe = next((r for r in recipes if r["id"] == recipe_id), None)
    if recipe:
        recipes = [r for r in recipes if r["id"] != recipe_id]
        return jsonify({"message": "Recipe successfully removed!"}), 200
    return jsonify({"message": "No recipe found"}), 404

if __name__ == '__main__':
    app.run(debug=True)