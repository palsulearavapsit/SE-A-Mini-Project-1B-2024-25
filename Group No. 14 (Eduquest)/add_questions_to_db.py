import sys
import os
import mysql.connector
from database_manager import DatabaseManager

def add_questions_to_database():
    """Add all 90 questions from the mock tests to the database"""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Check if database connection is successful
        if not hasattr(db_manager, 'connection') or not db_manager.connection:
            print("Database connection failed. Please check your database configuration.")
            return False
            
        # Physics questions (30 questions)
        physics_questions = [
            # First 10 physics questions
            {
                "question_text": "A particle moves in a straight line with constant acceleration. If it has velocity v₁ at time t₁ and velocity v₂ at time t₂, then its velocity at time (t₁+t₂)/2 is:",
                "option_a": "(v₁+v₂)/2",
                "option_b": "√(v₁v₂)",
                "option_c": "2v₁v₂/(v₁+v₂)",
                "option_d": "None of these",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Kinematics",
                "difficulty": "Medium"
            },
            {
                "question_text": "The escape velocity from Earth's surface is 11.2 km/s. The escape velocity from a planet having twice the radius and same mean density as Earth is:",
                "option_a": "5.6 km/s",
                "option_b": "11.2 km/s",
                "option_c": "15.8 km/s",
                "option_d": "22.4 km/s",
                "correct_answer": "D",
                "subject": "Physics",
                "topic": "Gravitation",
                "difficulty": "Medium"
            },
            {
                "question_text": "A body of mass 1 kg is thrown upwards with a velocity of 20 m/s. The kinetic energy at the highest point reached is:",
                "option_a": "0 J",
                "option_b": "100 J",
                "option_c": "200 J",
                "option_d": "400 J",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Energy",
                "difficulty": "Easy"
            },
            {
                "question_text": "Two particles are moving in uniform circular motion in the same circle. The angular velocity of the first particle is twice that of the second. The ratio of the centripetal acceleration of the first particle to that of the second is:",
                "option_a": "1:1",
                "option_b": "2:1",
                "option_c": "1:2",
                "option_d": "4:1",
                "correct_answer": "D",
                "subject": "Physics",
                "topic": "Circular Motion",
                "difficulty": "Medium"
            },
            {
                "question_text": "A simple pendulum has a time period T. If its length is increased by 20% and the acceleration due to gravity decreases by 20%, the new time period will be:",
                "option_a": "0.9T",
                "option_b": "1.1T",
                "option_c": "1.2T",
                "option_d": "1.34T",
                "correct_answer": "D",
                "subject": "Physics",
                "topic": "Oscillations",
                "difficulty": "Hard"
            },
            {
                "question_text": "A ball is dropped from a height of 20m. If the coefficient of restitution is 0.5, the height to which it rises after the first bounce is:",
                "option_a": "2.5 m",
                "option_b": "5 m",
                "option_c": "10 m",
                "option_d": "15 m",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Collision",
                "difficulty": "Medium"
            },
            {
                "question_text": "The work done by all forces on a body moving with uniform velocity is:",
                "option_a": "Positive",
                "option_b": "Negative",
                "option_c": "Zero",
                "option_d": "Cannot be determined",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "Work and Energy",
                "difficulty": "Easy"
            },
            {
                "question_text": "The electric potential at a point due to a point charge is 10 V. The electric field at that point is 5 N/C. The distance of that point from the charge is:",
                "option_a": "0.5 m",
                "option_b": "1 m",
                "option_c": "2 m",
                "option_d": "5 m",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "Electrostatics",
                "difficulty": "Medium"
            },
            {
                "question_text": "Two parallel infinite line charges with linear charge densities +λ and -λ are placed at a distance d apart. The electric field at a point which is at a distance d from both the lines is:",
                "option_a": "Zero",
                "option_b": "λ/(πε₀d)",
                "option_c": "λ/(2πε₀d)",
                "option_d": "2λ/(πε₀d)",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "Electrostatics",
                "difficulty": "Hard"
            },
            {
                "question_text": "A wire of resistance 12Ω is bent to form a circle. The effective resistance between two diametrically opposite points of the circle is:",
                "option_a": "3Ω",
                "option_b": "4Ω",
                "option_c": "6Ω",
                "option_d": "12Ω",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Current Electricity",
                "difficulty": "Medium"
            }
        ]
        
        # Add next 10 physics questions
        physics_questions.extend([
            {
                "question_text": "A body initially at rest moves with constant acceleration. The power delivered to it is proportional to:",
                "option_a": "t⁻¹",
                "option_b": "t⁰",
                "option_c": "t¹",
                "option_d": "t²",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "Work and Power",
                "difficulty": "Medium"
            },
            {
                "question_text": "Two particles of masses m and 2m are moving with equal kinetic energies. The ratio of their momenta is:",
                "option_a": "1:√2",
                "option_b": "1:2",
                "option_c": "√2:1",
                "option_d": "2:1",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Momentum",
                "difficulty": "Medium"
            },
            {
                "question_text": "A car accelerates from rest at a constant rate α for some time, after which it decelerates at a constant rate β and comes to rest. The maximum velocity attained by the car is proportional to:",
                "option_a": "α",
                "option_b": "β",
                "option_c": "α/β",
                "option_d": "√(αβ)",
                "correct_answer": "D",
                "subject": "Physics",
                "topic": "Kinematics",
                "difficulty": "Hard"
            },
            {
                "question_text": "A body of mass m slides down a rough inclined plane making an angle θ with the horizontal. The coefficient of kinetic friction is μ. The acceleration of the body is:",
                "option_a": "g(sinθ + μcosθ)",
                "option_b": "g(sinθ - μcosθ)",
                "option_c": "g(cosθ - μsinθ)",
                "option_d": "g(cosθ + μsinθ)",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Friction",
                "difficulty": "Medium"
            },
            {
                "question_text": "A cylindrical vessel of radius r and height h is filled with a liquid of density ρ. The force exerted by the liquid on the curved surface of the vessel is:",
                "option_a": "ρghπr²",
                "option_b": "ρgh²πr",
                "option_c": "2ρgh²πr",
                "option_d": "ρgπr²h²",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Fluid Mechanics",
                "difficulty": "Medium"
            },
            {
                "question_text": "The moment of inertia of a uniform circular disc of mass M and radius R about an axis perpendicular to the disc and passing through a point on its edge is:",
                "option_a": "(3/2)MR²",
                "option_b": "MR²",
                "option_c": "(1/2)MR²",
                "option_d": "(5/4)MR²",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Rotational Dynamics",
                "difficulty": "Medium"
            },
            {
                "question_text": "A meter stick is balanced at the 30 cm mark. If the mass per unit length of the portion of the stick to the left of the balance point is twice that of the portion to the right, where is the center of mass located?",
                "option_a": "40 cm",
                "option_b": "45 cm",
                "option_c": "50 cm",
                "option_d": "60 cm",
                "correct_answer": "D",
                "subject": "Physics",
                "topic": "Center of Mass",
                "difficulty": "Hard"
            },
            {
                "question_text": "Two identical springs of spring constant k are attached to a block of mass m and to fixed supports as shown. The frequency of oscillation of the mass is:",
                "option_a": "(1/2π)√(k/m)",
                "option_b": "(1/2π)√(2k/m)",
                "option_c": "(1/π)√(k/m)",
                "option_d": "(1/π)√(2k/m)",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Oscillations",
                "difficulty": "Medium"
            },
            {
                "question_text": "In Young's double slit experiment, the separation between the slits is halved and the distance between the screen and the slits is doubled. The fringe width will:",
                "option_a": "Remain unchanged",
                "option_b": "Become half",
                "option_c": "Become double",
                "option_d": "Become four times",
                "correct_answer": "D",
                "subject": "Physics",
                "topic": "Wave Optics",
                "difficulty": "Medium"
            },
            {
                "question_text": "A lens forms a real image of an object placed at 15 cm from it. When the object is moved 5 cm towards the lens, the image shifts by 20 cm. The focal length of the lens is:",
                "option_a": "5 cm",
                "option_b": "10 cm",
                "option_c": "15 cm",
                "option_d": "20 cm",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Ray Optics",
                "difficulty": "Medium"
            }
        ])
        
        # Add last 10 physics questions
        physics_questions.extend([
            {
                "question_text": "The de Broglie wavelength of an electron accelerated through a potential difference of 100 V is approximately:",
                "option_a": "0.123 nm",
                "option_b": "0.01 nm",
                "option_c": "1.23 nm",
                "option_d": "12.3 nm",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Quantum Physics",
                "difficulty": "Hard"
            },
            {
                "question_text": "In the Bohr model of hydrogen atom, the energy of an electron in the nth orbit is proportional to:",
                "option_a": "n",
                "option_b": "n²",
                "option_c": "1/n",
                "option_d": "1/n²",
                "correct_answer": "D",
                "subject": "Physics",
                "topic": "Atomic Physics",
                "difficulty": "Medium"
            },
            {
                "question_text": "A rod of length L expands by ΔL when the temperature rises by ΔT. The coefficient of linear expansion of the material of the rod is:",
                "option_a": "ΔL/(L·ΔT)",
                "option_b": "L/(ΔL·ΔT)",
                "option_c": "ΔT/(L·ΔL)",
                "option_d": "L·ΔT/ΔL",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Thermal Properties",
                "difficulty": "Easy"
            },
            {
                "question_text": "The efficiency of a Carnot engine operating between temperatures T₁ and T₂ (T₁ > T₂) is:",
                "option_a": "T₁/T₂",
                "option_b": "T₂/T₁",
                "option_c": "(T₁-T₂)/T₁",
                "option_d": "(T₁-T₂)/T₂",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "Thermodynamics",
                "difficulty": "Medium"
            },
            {
                "question_text": "A capacitor of capacitance C is charged to a potential difference V and then disconnected from the charging source. If a dielectric of dielectric constant K is inserted completely into the capacitor, the energy stored in the capacitor will become:",
                "option_a": "KCV²/2",
                "option_b": "CV²/(2K)",
                "option_c": "CV²/2",
                "option_d": "CV²K²/2",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Electrostatics",
                "difficulty": "Medium"
            },
            {
                "question_text": "A conductor of length L moves with velocity v perpendicular to a magnetic field B. The induced emf across the conductor is:",
                "option_a": "BLv",
                "option_b": "BL/v",
                "option_c": "B/Lv",
                "option_d": "BvL²",
                "correct_answer": "A",
                "subject": "Physics",
                "topic": "Electromagnetic Induction",
                "difficulty": "Medium"
            },
            {
                "question_text": "In an LCR circuit, the resonant frequency is f₀. If the inductance is doubled, the new resonant frequency will be:",
                "option_a": "f₀/2",
                "option_b": "2f₀",
                "option_c": "f₀/√2",
                "option_d": "√2f₀",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "AC Circuits",
                "difficulty": "Medium"
            },
            {
                "question_text": "A Zener diode is used for:",
                "option_a": "Amplification",
                "option_b": "Rectification",
                "option_c": "Voltage regulation",
                "option_d": "Oscillation",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "Semiconductor Devices",
                "difficulty": "Easy"
            },
            {
                "question_text": "The half-life of a radioactive element is 30 days. After 90 days, the fraction of the initial amount that would have decayed is:",
                "option_a": "1/2",
                "option_b": "3/4",
                "option_c": "7/8",
                "option_d": "1/8",
                "correct_answer": "C",
                "subject": "Physics",
                "topic": "Nuclear Physics",
                "difficulty": "Medium"
            },
            {
                "question_text": "The binding energy per nucleon is maximum for:",
                "option_a": "¹H",
                "option_b": "⁵⁶Fe",
                "option_c": "²³⁵U",
                "option_d": "²³⁸U",
                "correct_answer": "B",
                "subject": "Physics",
                "topic": "Nuclear Physics",
                "difficulty": "Medium"
            }
        ])
        
        # Insert physics questions into database
        print("Adding Physics questions to the database...")
        for question in physics_questions:
            insert_question(db_manager, question)
        print(f"Added {len(physics_questions)} Physics questions successfully!")
        
        print("\nAll questions have been added to the database!")
        return True
        
    except Exception as e:
        print(f"Error adding questions to database: {e}")
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
    add_questions_to_database() 