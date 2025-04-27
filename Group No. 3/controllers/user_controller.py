import bcrypt
from db_helper import execute_query, fetch_all

def create_user(username, email, password):
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
    execute_query(query, (username, email, hashed_password))

def authenticate_user(email, password):
    users = fetch_all("SELECT * FROM users WHERE email = %s", (email,))
    if users and bcrypt.checkpw(password.encode(), users[0]["password_hash"].encode()):
        return users[0]
    return None

