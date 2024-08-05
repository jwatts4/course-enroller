# Course Enroller

Final project for CP317. It is a Django application intended to be run locally.

---

# Instructions

In order to run this application, you must follow these steps:

1. **Ensure you have Python 3.12.4 installed**:

   - You can download it from the official [Python website](https://www.python.org/downloads/release/python-3124/)

2. **Clone the repository**:

   ```sh
   git clone <repository-url>
   cd <repository-directory>
   ```

3. **Create and activate a virtual environment**:

   ```sh
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   ```

4. **Install the dependencies**:

   ```sh
   pip install -r requirements.txt
   ```

5. **Navigate into project and apply migrations**:

   ```sh
   python manage.py migrate
   ```

6. **Seed the database with initial data (in `courses.txt`)**:

   ```sh
   python manage.py seed_courses
   ```

7. **Run the development server**:

   ```sh
   python manage.py runserver
   ```

8. **Access the application**:
   - Open your web browser and go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
