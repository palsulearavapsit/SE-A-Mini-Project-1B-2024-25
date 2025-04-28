from database_manager import DatabaseManager

def add_mathematics_questions():
    """Add all mathematics questions to the database"""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Check if database connection is successful
        if not hasattr(db_manager, 'connection') or not db_manager.connection:
            print("Database connection failed. Please check your database configuration.")
            return False
            
        # Mathematics questions (30 questions)
        mathematics_questions = [
            # First 10 mathematics questions
            {
                "question_text": "If the lines 2x + 3y = 5 and 3x + ky = 8 are perpendicular to each other, then the value of k is:",
                "option_a": "-2",
                "option_b": "2",
                "option_c": "-2/3",
                "option_d": "2/3",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Coordinate Geometry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The integral ∫(1/x)dx is equal to:",
                "option_a": "log|x| + C",
                "option_b": "log(x) + C",
                "option_c": "1/log(x) + C",
                "option_d": "x log(x) + C",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Easy"
            },
            {
                "question_text": "The value of ∫₀¹ x²e^x dx is:",
                "option_a": "e - 2",
                "option_b": "2e - 5",
                "option_c": "e - 3",
                "option_d": "e - 1",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Hard"
            },
            {
                "question_text": "If sin θ + sin² θ = 1, then cos⁴ θ - cos² θ equals:",
                "option_a": "0",
                "option_b": "1",
                "option_c": "-1",
                "option_d": "None of these",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Trigonometry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The area of the region bounded by the parabola y² = 4x and its latus rectum is:",
                "option_a": "4/3 square units",
                "option_b": "8/3 square units",
                "option_c": "16/3 square units",
                "option_d": "32/3 square units",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Coordinate Geometry",
                "difficulty": "Hard"
            },
            {
                "question_text": "The number of solutions of the equation tan x = x in the interval [0, 2π] is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "3",
                "option_d": "4",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Medium"
            },
            {
                "question_text": "If A and B are two events such that P(A) = 0.4, P(B) = 0.3 and P(A∩B) = 0.2, then P(A|B) is:",
                "option_a": "0.5",
                "option_b": "0.6",
                "option_c": "2/3",
                "option_d": "3/4",
                "correct_answer": "C",
                "subject": "Mathematics",
                "topic": "Probability",
                "difficulty": "Medium"
            },
            {
                "question_text": "The locus of the point of intersection of perpendicular tangents to the ellipse x²/a² + y²/b² = 1 is:",
                "option_a": "x²/a² - y²/b² = 1",
                "option_b": "x²/a² + y²/b² = 1",
                "option_c": "x²/a⁴ + y²/b⁴ = 1/a²b²",
                "option_d": "x²/a⁴ - y²/b⁴ = 1/a²b²",
                "correct_answer": "C",
                "subject": "Mathematics",
                "topic": "Coordinate Geometry",
                "difficulty": "Hard"
            },
            {
                "question_text": "The value of the determinant |2 3 1; 0 1 -1; 4 2 3| is:",
                "option_a": "6",
                "option_b": "8",
                "option_c": "10",
                "option_d": "12",
                "correct_answer": "C",
                "subject": "Mathematics",
                "topic": "Linear Algebra",
                "difficulty": "Medium"
            },
            {
                "question_text": "The sum of the series 1 + 1/2 + 1/4 + 1/8 + ... to infinity is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "4",
                "option_d": "Diverges",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Infinite Series",
                "difficulty": "Easy"
            }
        ]
        
        # Add next 10 mathematics questions
        mathematics_questions.extend([
            {
                "question_text": "If f(x) = x³ - 12x + 1, then f'(2) is equal to:",
                "option_a": "-1",
                "option_b": "0",
                "option_c": "1",
                "option_d": "12",
                "correct_answer": "D",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Easy"
            },
            {
                "question_text": "The general solution of the differential equation dy/dx + y.tan x = sin x is:",
                "option_a": "y.cos x = sin x + C",
                "option_b": "y.cos x = cos x + C",
                "option_c": "y.cos x = sin² x + C",
                "option_d": "y.sin x = cos x + C",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Differential Equations",
                "difficulty": "Hard"
            },
            {
                "question_text": "The rank of the matrix {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}} is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "3",
                "option_d": "0",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Linear Algebra",
                "difficulty": "Medium"
            },
            {
                "question_text": "The distance of the point (2, 3, 4) from the plane x + y + z = 6 is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "3/√3",
                "option_d": "√3",
                "correct_answer": "C",
                "subject": "Mathematics",
                "topic": "3D Geometry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The value of ∫₀^(π/2) sin⁵x.cos⁴x dx is:",
                "option_a": "1/9",
                "option_b": "2/9",
                "option_c": "1/18",
                "option_d": "2/63",
                "correct_answer": "D",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Hard"
            },
            {
                "question_text": "The normal to the curve x² + y² - 2x - 4y + 4 = 0 at the point (0, 0) is:",
                "option_a": "x - y = 0",
                "option_b": "x + 2y = 0",
                "option_c": "2x + y = 0",
                "option_d": "x + y = 0",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Differential Calculus",
                "difficulty": "Medium"
            },
            {
                "question_text": "If z = x + iy is a complex number such that |z + 1| = |z - 1|, then z lies on the:",
                "option_a": "Imaginary axis",
                "option_b": "Real axis",
                "option_c": "Circle |z| = 1",
                "option_d": "Circle |z - 1| = 1",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Complex Numbers",
                "difficulty": "Medium"
            },
            {
                "question_text": "The equation of the plane passing through the point (1, 2, 3) and perpendicular to the planes x + y + z = 6 and 2x + 3y - z = 5 is:",
                "option_a": "x - 4y + 5z = 16",
                "option_b": "4x - y - 5z = -16",
                "option_c": "5x - 4y + z = 0",
                "option_d": "4x + 5y - z = 14",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "3D Geometry",
                "difficulty": "Hard"
            },
            {
                "question_text": "The order and degree of the differential equation d²y/dx² + (dy/dx)³ = sin(d³y/dx³) is:",
                "option_a": "Order = 3, Degree = 1",
                "option_b": "Order = 2, Degree = 3",
                "option_c": "Order = 3, Degree = 3",
                "option_d": "Order = 1, Degree = 3",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Differential Equations",
                "difficulty": "Medium"
            },
            {
                "question_text": "The domain of the function f(x) = √(9 - x²) is:",
                "option_a": "[-3, 3]",
                "option_b": "(-3, 3)",
                "option_c": "[0, 3]",
                "option_d": "(0, 3)",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Functions",
                "difficulty": "Easy"
            }
        ])
        
        # Add last 10 mathematics questions
        mathematics_questions.extend([
            {
                "question_text": "lim(n→∞) (1 + 3/n)^n is equal to:",
                "option_a": "e",
                "option_b": "e²",
                "option_c": "e³",
                "option_d": "∞",
                "correct_answer": "C",
                "subject": "Mathematics",
                "topic": "Limits",
                "difficulty": "Medium"
            },
            {
                "question_text": "If a matrix A satisfies the equation A² - 5A + 7I = O, where I is the identity matrix, then A⁻¹ is equal to:",
                "option_a": "(5I - A)/7",
                "option_b": "(A - 5I)/7",
                "option_c": "(A - 7I)/5",
                "option_d": "(5I + A)/7",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Linear Algebra",
                "difficulty": "Hard"
            },
            {
                "question_text": "The value of the integral ∫₀^∞ e^-x^2 dx is:",
                "option_a": "1",
                "option_b": "√π",
                "option_c": "√π/2",
                "option_d": "π/2",
                "correct_answer": "C",
                "subject": "Mathematics",
                "topic": "Definite Integrals",
                "difficulty": "Hard"
            },
            {
                "question_text": "The minimum value of the function f(x) = 2x³ - 15x² + 36x - 10 in the interval [0, 5] is:",
                "option_a": "-10",
                "option_b": "0",
                "option_c": "13",
                "option_d": "23",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Medium"
            },
            {
                "question_text": "The radius of convergence of the power series Σ n²x^n from n=0 to ∞ is:",
                "option_a": "0",
                "option_b": "1",
                "option_c": "2",
                "option_d": "∞",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Series",
                "difficulty": "Hard"
            },
            {
                "question_text": "If the vectors ā = (1, 2, 3), b̄ = (0, 1, -1), and c̄ = (λ, 1, 1) are coplanar, then the value of λ is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "3",
                "option_d": "4",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Vectors",
                "difficulty": "Medium"
            },
            {
                "question_text": "The sum of the series 1 + 1/1! + 1/2! + 1/3! + ... to infinity is:",
                "option_a": "e",
                "option_b": "e - 1",
                "option_c": "e²",
                "option_d": "1/(e-1)",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Infinite Series",
                "difficulty": "Easy"
            },
            {
                "question_text": "The area enclosed by the curve y = sin x, the x-axis and the ordinates x = 0 and x = π is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "π",
                "option_d": "2π",
                "correct_answer": "B",
                "subject": "Mathematics",
                "topic": "Calculus",
                "difficulty": "Medium"
            },
            {
                "question_text": "If f(x) = {x² if x ≤ 1, ax + b if x > 1} is continuous and differentiable at x = 1, then the values of a and b are:",
                "option_a": "a = 2, b = -1",
                "option_b": "a = 2, b = 1",
                "option_c": "a = -2, b = 3",
                "option_d": "a = 2, b = 0",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Continuity and Differentiability",
                "difficulty": "Medium"
            },
            {
                "question_text": "The solution of the differential equation dy/dx = y² with y(0) = 1 is:",
                "option_a": "y = 1/(1-x)",
                "option_b": "y = 1/(1+x)",
                "option_c": "y = -1/x",
                "option_d": "y = tan x",
                "correct_answer": "A",
                "subject": "Mathematics",
                "topic": "Differential Equations",
                "difficulty": "Medium"
            }
        ])
        
        # Insert mathematics questions into database
        print("Adding Mathematics questions to the database...")
        for question in mathematics_questions:
            insert_question(db_manager, question)
        print(f"Added {len(mathematics_questions)} Mathematics questions successfully!")
        
        return True
        
    except Exception as e:
        print(f"Error adding mathematics questions to database: {e}")
        return False

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

if __name__ == "__main__":
    add_mathematics_questions() 