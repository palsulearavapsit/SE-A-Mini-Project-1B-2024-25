from db_helper import execute_query, fetch_all

def add_rating(user_id, recipe_id, rating, review):
    query = "INSERT INTO ratings (user_id, recipe_id, rating, review) VALUES (%s, %s, %s, %s)"
    execute_query(query, (user_id, recipe_id, rating, review))

def get_ratings(recipe_id):
    return fetch_all("SELECT * FROM ratings WHERE recipe_id = %s", (recipe_id,))
