# Facebook Clone

This is a Facebook clone project built with Django. It replicates some of the core features of Facebook, including user authentication, posting updates, commenting, and liking posts and many other features.

## Features

- **User Authentication**: Users can sign up, log in, and log out securely.
- **News Feed**: Users can post updates visible to their friends.
- **Commenting**: Users can comment on posts,like comments and replies.
- **Reply comment**: Users can reply comment on posts,like replies.
- **Liking Posts**: Users can like posts.
- **Friend Requests**: Users can send and accept friend requests.

## Technologies Used

- **Django**: A high-level Python web framework.
- **HTML/CSS**: For frontend presentation and styling.
- **SQLite**: As the database management system.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/facebook-clone.git
2. Navigate to the project directory:


   cd facebook-clone
3. Create a virtual environment:


   python3 -m venv env
4. Activate the virtual environment:

    - **On macOS and Linux**: source env/bin/activate.


     
    - ** On Windows**: .\env\Scripts\activate


   
5. Install the dependencies:


   pip install -r requirements.txt
6. Apply the database migrations:


   python manage.py migrate
7. Run the development server:


   python manage.py runserver
8. Access the application in your web browser at http://localhost:8000.

