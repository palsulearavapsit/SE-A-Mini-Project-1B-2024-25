from add_questions_to_db import add_questions_to_database
from add_chemistry_questions import add_chemistry_questions
from add_mathematics_questions import add_mathematics_questions
import time

def add_all_questions_to_db():
    """Add all 90 questions to the database"""
    
    print("Starting to add all 90 questions to the database...")
    print("=" * 50)
    
    # Add physics questions
    print("\nAdding Physics questions...")
    physics_success = add_questions_to_database()
    
    if physics_success:
        print("Physics questions added successfully!")
    else:
        print("Failed to add Physics questions.")
    
    # Add a slight delay
    time.sleep(1)
    
    # Add chemistry questions
    print("\nAdding Chemistry questions...")
    chemistry_success = add_chemistry_questions()
    
    if chemistry_success:
        print("Chemistry questions added successfully!")
    else:
        print("Failed to add Chemistry questions.")
    
    # Add a slight delay
    time.sleep(1)
    
    # Add mathematics questions
    print("\nAdding Mathematics questions...")
    mathematics_success = add_mathematics_questions()
    
    if mathematics_success:
        print("Mathematics questions added successfully!")
    else:
        print("Failed to add Mathematics questions.")
    
    # Summary
    print("\n" + "=" * 50)
    if physics_success and chemistry_success and mathematics_success:
        print("All 90 questions have been successfully added to the database!")
        print("Your mock tests now use questions from the database.")
        print("You can add more questions by modifying these scripts.")
    else:
        print("Some questions could not be added to the database.")
        print("Please check the error messages above.")
    
    print("=" * 50)

if __name__ == "__main__":
    add_all_questions_to_db() 