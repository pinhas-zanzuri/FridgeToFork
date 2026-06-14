# קובץ המלאי והלוגיקה של התוכנית

import os
import json
from flask import Flask, jsonify, request

app = Flask(__name__) # יצרת השרת שישמש אותנו

USER_NAME = os.environ.get("USER_NAME", "Guest") # שליפת שם המשתמש

# הפונקציה שניגשת למלאי ומחזירה את המוצרים הזמינים
def read_inventory():
    try:
        with open("/data/inventory.txt", "r") as f:
            items = [line.strip().lower() for line in f if line.strip()]
        return items
    except FileNotFoundError:
        return []

# קריאת המתכונים מקובץ JSON - נקראים בכל בקשה כדי לאפשר עדכון בזמן ריצה
def read_recipes():
    try:
        with open("/data/recipes.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# מחזיר את המתכון הכי מתאים - קודם מחפש התאמה מלאה, אחר כך חלקית
# מחזיר: שם מתכון, כמות מצרכים שנמצאו, רשימת מצרכים חסרים, האם התאמה מלאה
def suggest_recipe(inventory, recipes, meal_type=None):
    best_recipe = None
    best_score = 0
    best_missing = []

    for recipe_name, data in recipes.items():
        ingredients = data["ingredients"]
        recipe_type = data["type"]

        if meal_type and meal_type != "any" and recipe_type != meal_type:
            continue

        matched = [i for i in ingredients if i in inventory]
        score = len(matched)

        if score > best_score:
            best_score = score
            best_recipe = recipe_name
            best_missing = [i for i in ingredients if i not in inventory]

    is_full_match = (best_recipe is not None and len(best_missing) == 0)
    return best_recipe, best_score, best_missing, is_full_match

@app.route("/api") #  משתמש endpoint קיים - משתמש במלאי מהקובץ (לטסטים)
def api():
    inventory = read_inventory()
    recipes = read_recipes()
    recipe, score, missing, is_full = suggest_recipe(inventory, recipes)

    if not recipe or score == 0:
        return jsonify({"user": USER_NAME, "message": "No ingredients found to suggest a recipe", "inventory": inventory})
    return jsonify({"user": USER_NAME, "recipe": recipe, "matched_ingredients": score, "missing": missing, "full_match": is_full, "inventory": inventory})

# מחזיר את כל המצרכים הייחודיים מכל המתכונים
@app.route("/api/ingredients")
def ingredients():
    recipes = read_recipes()
    all_ingredients = sorted({i for data in recipes.values() for i in data["ingredients"]})
    return jsonify({"ingredients": all_ingredients})

@app.route("/api/suggest", methods=["POST"]) # יצירת Endpoint חדש המקבל מהמשתמש מצרכים וסוג.
def suggest():
    body = request.get_json()
    if not body or "ingredients" not in body:
        return jsonify({"error": "Missing ingredients list"}), 400

    inventory = [i.strip().lower() for i in body["ingredients"]]
    meal_type = body.get("type", "any") # ברירת מחדל: לא משנה

    recipes = read_recipes()
    recipe, score, missing, is_full = suggest_recipe(inventory, recipes, meal_type)

    if not recipe or score == 0:
        return jsonify({"user": USER_NAME, "message": "No recipe found for the given ingredients and type", "inventory": inventory})
    return jsonify({"user": USER_NAME, "recipe": recipe, "matched_ingredients": score, "missing": missing, "full_match": is_full, "inventory": inventory})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
