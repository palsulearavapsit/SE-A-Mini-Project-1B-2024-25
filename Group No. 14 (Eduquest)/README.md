# EduQuest - Educational Exam Preparation Application

EduQuest is a comprehensive exam preparation application designed for students preparing for various entrance exams like JEE, NEET, GATE, and other competitive exams.

## Features

- **Mock Tests**: Practice with simulated exams
- **Previous Year Questions**: Access to past exam questions
- **Calendar & Study Planner**: Organize your study schedule
- **Reports & Analysis**: Get detailed performance insights
- **News & Updates**: Stay informed about exam-related news
- **User Accounts**: Track your progress over time

## Installation

### Prerequisites

- Python 3.7 or higher
- SQLite (included with Python)

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/eduquest.git
   cd eduquest
   ```

2. Install dependencies:
   ```
   python install_dependencies.py
   ```
   
   Or manually install using pip:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

To start the application, run:
```
python main.py
```

## News API Setup

The application uses NewsAPI to fetch exam-related news. A demo API key is included, but you may want to register for your own free key at [newsapi.org](https://newsapi.org/) if you plan to use the application extensively.

To update the API key:
1. Register at [newsapi.org](https://newsapi.org/) to get your own API key
2. Replace the API key in `pages/news_page.py` and `pages/dashboard_news_widget.py`

## Database

The application uses MySQL for user authentication and data storage. Follow these steps to set up the database:

1. Install MySQL Server if you haven't already
2. Configure your database credentials in `database_config.py`:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',  # default is often 'root'
       'password': 'your_password',
       'database': 'eduquest',
       'raise_on_warnings': True
   }
   ```
3. Run the database setup script:
   ```
   python setup_database.py
   ```

This will create the necessary database and tables for the application.

## License
