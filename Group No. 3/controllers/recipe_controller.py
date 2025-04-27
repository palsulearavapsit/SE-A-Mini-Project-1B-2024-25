from db_helper import execute_query, fetch_all, fetch_one

def add_recipe(name, category, ingredients, instructions, recipe_link):
    """Insert a new recipe into the database."""
    query = """INSERT INTO recipes (name, category, ingredients, instructions, recipe_link)
               VALUES (%s, %s, %s, %s, %s, %s)"""
    execute_query(query, (name, category, ingredients, instructions, recipe_link))

def get_recipes():
    """Fetch all recipes."""
    return fetch_all("SELECT * FROM recipes")

def search_recipes(keyword, mode):
    """Search recipes by dish name or ingredients, ensuring any order of ingredients matches."""
    if mode == "dish":
        query = "SELECT * FROM recipes WHERE name LIKE %s"
        params = (f"%{keyword}%",)
    elif mode == "ingredients":
        ingredients_list = keyword.split(",")  # Split ingredients by comma
        conditions = " AND ".join(["ingredients LIKE %s" for _ in ingredients_list])
        query = f"SELECT * FROM recipes WHERE {conditions}"
        params = tuple(f"%{ingredient.strip()}%" for ingredient in ingredients_list)
    else:
        return []  # Return empty list if mode is invalid
    
    return fetch_all(query, params)

def get_recipe_by_id(recipe_id):
    """Fetch a single recipe by its ID."""
    query = "SELECT * FROM recipes WHERE recipe_id = %s"
    return fetch_one(query, (recipe_id,))

def get_categories():
    """Fetch distinct categories from the recipes table."""
    query = "SELECT DISTINCT category FROM recipes"
    return [row['category'] for row in fetch_all(query)]

def search_by_category(category):
    """Fetch recipes that belong to the selected category."""
    query = "SELECT * FROM recipes WHERE category = %s"
    return fetch_all(query, (category,))