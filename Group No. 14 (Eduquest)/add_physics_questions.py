def insert_question(db_manager, question):
    """Insert a single question into the database"""
    query = """
        INSERT INTO questions (
            question_text, option_a, option_b, option_c, option_d,
            correct_answer, subject, topic, difficulty
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        AS new_values
        ON DUPLICATE KEY UPDATE
            option_a = new_values.option_a,
            option_b = new_values.option_b,
            option_c = new_values.option_c,
            option_d = new_values.option_d,
            correct_answer = new_values.correct_answer,
            topic = new_values.topic,
            difficulty = new_values.difficulty
    """
    
    params = (
        question["question_text"],
        question["option_a"],
        question["option_b"],
        question["option_c"],
        question["option_d"],
        question["correct_answer"],
        question["subject"],
        question["topic"],
        question["difficulty"]
    )
    
    db_manager.execute_query(query, params) 