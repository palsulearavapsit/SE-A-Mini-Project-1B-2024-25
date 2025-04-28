from database_manager import DatabaseManager

def add_chemistry_questions():
    """Add all chemistry questions to the database"""
    try:
        # Initialize database manager
        db_manager = DatabaseManager()
        
        # Check if database connection is successful
        if not hasattr(db_manager, 'connection') or not db_manager.connection:
            print("Database connection failed. Please check your database configuration.")
            return False
            
        # Chemistry questions (30 questions)
        chemistry_questions = [
            # First 10 chemistry questions
            {
                "question_text": "The IUPAC name of CH₃-CH=CH-CHO is:",
                "option_a": "2-Butenal",
                "option_b": "But-2-enal",
                "option_c": "But-2-en-1-al",
                "option_d": "1-Oxo-2-butene",
                "correct_answer": "C",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following species has the highest bond order?",
                "option_a": "O₂⁺",
                "option_b": "O₂",
                "option_c": "O₂⁻",
                "option_d": "O₂²⁻",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Chemical Bonding",
                "difficulty": "Medium"
            },
            {
                "question_text": "The number of sigma and pi bonds in pent-2-en-4-yne is:",
                "option_a": "8 sigma, 3 pi",
                "option_b": "10 sigma, 3 pi",
                "option_c": "11 sigma, 2 pi",
                "option_d": "9 sigma, 3 pi",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Chemical Bonding",
                "difficulty": "Hard"
            },
            {
                "question_text": "Which of the following has the highest boiling point?",
                "option_a": "CH₃CH₂CH₃",
                "option_b": "CH₃CH₂OH",
                "option_c": "(CH₃)₃N",
                "option_d": "CH₃OCH₃",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Physical Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "In the reaction: MnO₄⁻ + Fe²⁺ + H⁺ → Mn²⁺ + Fe³⁺ + H₂O, the number of electrons transferred is:",
                "option_a": "1",
                "option_b": "3",
                "option_c": "5",
                "option_d": "7",
                "correct_answer": "C",
                "subject": "Chemistry",
                "topic": "Redox Reactions",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following compounds will undergo racemization on treatment with dilute NaOH?",
                "option_a": "CH₃CH(OH)COOH",
                "option_b": "CH₃CH(Cl)COOH",
                "option_c": "CH₃CH(Br)COOH",
                "option_d": "CH₃CH(NH₂)COOH",
                "correct_answer": "C",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Hard"
            },
            {
                "question_text": "The hybridization of carbon in carbon dioxide is:",
                "option_a": "sp",
                "option_b": "sp²",
                "option_c": "sp³",
                "option_d": "dsp²",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Chemical Bonding",
                "difficulty": "Easy"
            },
            {
                "question_text": "The correct order of decreasing S_N1 reactivity is:",
                "option_a": "3° > 2° > 1° > CH₃X",
                "option_b": "CH₃X > 1° > 2° > 3°",
                "option_c": "3° > 1° > 2° > CH₃X",
                "option_d": "2° > 1° > 3° > CH₃X",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The maximum number of isomers for an alkene with molecular formula C₅H₁₀ is:",
                "option_a": "5",
                "option_b": "6",
                "option_c": "7",
                "option_d": "8",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The reagent used to distinguish between acetaldehyde and acetone is:",
                "option_a": "Fehling's solution",
                "option_b": "Tollen's reagent",
                "option_c": "Benedict's solution",
                "option_d": "All of these",
                "correct_answer": "D",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Easy"
            }
        ]
        
        # Add next 10 chemistry questions
        chemistry_questions.extend([
            {
                "question_text": "Which of the following has the highest lattice energy?",
                "option_a": "NaCl",
                "option_b": "MgO",
                "option_c": "KCl",
                "option_d": "CaO",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Chemical Bonding",
                "difficulty": "Medium"
            },
            {
                "question_text": "The equivalent conductance of a weak electrolyte at infinite dilution is 400 ohm⁻¹cm²equiv⁻¹. If its degree of dissociation at a particular concentration is 0.8, the equivalent conductance at this concentration is:",
                "option_a": "320 ohm⁻¹cm²equiv⁻¹",
                "option_b": "400 ohm⁻¹cm²equiv⁻¹",
                "option_c": "500 ohm⁻¹cm²equiv⁻¹",
                "option_d": "250 ohm⁻¹cm²equiv⁻¹",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Electrochemistry",
                "difficulty": "Hard"
            },
            {
                "question_text": "For a first order reaction, the time required for 75% completion of the reaction is:",
                "option_a": "2 times the half-life",
                "option_b": "3 times the half-life",
                "option_c": "log₂3 times the half-life",
                "option_d": "ln 3 times the half-life",
                "correct_answer": "D",
                "subject": "Chemistry",
                "topic": "Chemical Kinetics",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following species does not exist?",
                "option_a": "SiF₆²⁻",
                "option_b": "SiCl₆²⁻",
                "option_c": "PCl₆⁻",
                "option_d": "SF₆",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Inorganic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The electronic configuration of Cr (Z = 24) is:",
                "option_a": "[Ar] 3d⁴ 4s²",
                "option_b": "[Ar] 3d⁵ 4s¹",
                "option_c": "[Ar] 3d³ 4s²",
                "option_d": "[Ar] 3d⁶ 4s⁰",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Atomic Structure",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following pairs represents isotones?",
                "option_a": "¹⁸O and ²⁰Ne",
                "option_b": "¹⁴N and ¹⁴C",
                "option_c": "³²S and ³⁶Ar",
                "option_d": "⁴⁰Ar and ³⁹K",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Nuclear Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following oxides is amphoteric in nature?",
                "option_a": "MgO",
                "option_b": "CO₂",
                "option_c": "Al₂O₃",
                "option_d": "SO₂",
                "correct_answer": "C",
                "subject": "Chemistry",
                "topic": "Inorganic Chemistry",
                "difficulty": "Easy"
            },
            {
                "question_text": "What will be the pH of a buffer solution containing 0.1 M NH₄Cl and 0.1 M NH₄OH? (pKb of NH₄OH = 4.7)",
                "option_a": "4.7",
                "option_b": "9.3",
                "option_c": "7.0",
                "option_d": "2.3",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Acid-Base Equilibria",
                "difficulty": "Medium"
            },
            {
                "question_text": "In the extraction of copper, the slag formed is:",
                "option_a": "Cu₂O",
                "option_b": "FeS",
                "option_c": "FeSiO₃",
                "option_d": "CuFeS₂",
                "correct_answer": "C",
                "subject": "Chemistry",
                "topic": "Metallurgy",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following has the highest magnetic moment?",
                "option_a": "[Ni(NH₃)₆]²⁺",
                "option_b": "[NiCl₄]²⁻",
                "option_c": "[Ni(CO)₄]",
                "option_d": "[Ni(CN)₄]²⁻",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Coordination Compounds",
                "difficulty": "Hard"
            }
        ])
        
        # Add last 10 chemistry questions
        chemistry_questions.extend([
            {
                "question_text": "The number of possible isomers for a compound with the formula [Co(NH₃)₄Cl₂]⁺ is:",
                "option_a": "1",
                "option_b": "2",
                "option_c": "3",
                "option_d": "4",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Coordination Compounds",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following polymers is not formed by addition polymerization?",
                "option_a": "Polyethylene",
                "option_b": "Polystyrene",
                "option_c": "Nylon 6,6",
                "option_d": "Polyvinyl chloride",
                "correct_answer": "C",
                "subject": "Chemistry",
                "topic": "Polymers",
                "difficulty": "Easy"
            },
            {
                "question_text": "Williamson's synthesis is used for the preparation of:",
                "option_a": "Alcohols",
                "option_b": "Ethers",
                "option_c": "Aldehydes",
                "option_d": "Carboxylic acids",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The major product formed in the reaction of benzene with acetyl chloride in the presence of anhydrous AlCl₃ is:",
                "option_a": "Benzaldehyde",
                "option_b": "Acetophenone",
                "option_c": "Benzoic acid",
                "option_d": "Benzyl chloride",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "The basicity of pyridine compared to aliphatic amines is:",
                "option_a": "Higher",
                "option_b": "Lower",
                "option_c": "Same",
                "option_d": "Cannot be compared",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "In Gabriel phthalimide synthesis, the product formed is:",
                "option_a": "Primary amine",
                "option_b": "Secondary amine",
                "option_c": "Tertiary amine",
                "option_d": "Quaternary ammonium salt",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Medium"
            },
            {
                "question_text": "Which of the following is not a reducing sugar?",
                "option_a": "Glucose",
                "option_b": "Maltose",
                "option_c": "Lactose",
                "option_d": "Sucrose",
                "correct_answer": "D",
                "subject": "Chemistry",
                "topic": "Carbohydrates",
                "difficulty": "Easy"
            },
            {
                "question_text": "Which of the following amino acids is not optically active?",
                "option_a": "Alanine",
                "option_b": "Glycine",
                "option_c": "Serine",
                "option_d": "Leucine",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Amino Acids",
                "difficulty": "Easy"
            },
            {
                "question_text": "The increasing order of acidic strength of the following compounds is: Phenol, o-nitrophenol, p-nitrophenol",
                "option_a": "Phenol < p-nitrophenol < o-nitrophenol",
                "option_b": "Phenol < o-nitrophenol < p-nitrophenol",
                "option_c": "p-nitrophenol < o-nitrophenol < phenol",
                "option_d": "o-nitrophenol < phenol < p-nitrophenol",
                "correct_answer": "A",
                "subject": "Chemistry",
                "topic": "Organic Chemistry",
                "difficulty": "Hard"
            },
            {
                "question_text": "During nuclear fission, the mass defect is converted to:",
                "option_a": "Chemical energy",
                "option_b": "Nuclear energy",
                "option_c": "Electrical energy",
                "option_d": "Mechanical energy",
                "correct_answer": "B",
                "subject": "Chemistry",
                "topic": "Nuclear Chemistry",
                "difficulty": "Easy"
            }
        ])
        
        # Insert chemistry questions into database
        print("Adding Chemistry questions to the database...")
        for question in chemistry_questions:
            insert_question(db_manager, question)
        print(f"Added {len(chemistry_questions)} Chemistry questions successfully!")
        
        return True
        
    except Exception as e:
        print(f"Error adding chemistry questions to database: {e}")
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
    add_chemistry_questions() 