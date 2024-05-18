# Facebook Clone

This is a Facebook clone project built with Django. It replicates some of the core features of Facebook, including user authentication, posting updates, commenting, and liking posts and many other features.

## Features

- **User Authentication**: Users can sign up, log in, and log out securely.
- **News Feed**: Users can post updates visible to their friends.
- **Commenting**: Users can comment on posts,like comments and replies.
- **Reply comment**: Users can reply comment on posts,like replies.
- **Liking Posts**: Users can like posts.
- **Friend Requests**: Users can send and accept friend requests.
- **Add Story**: Users can add story.

## Technologies Used

- **Django**: A high-level Python web framework.
- **HTML/CSS**: For frontend presentation and styling.
- **SQLite**: As the database management system.

## Installation

Follow these steps to set up the Django blog application:

1. Clone the repository:

   ```bash
   git clone https://github.com/Draglow/facebook-clone.git
   ```

2. Navigate to the project directory:

   ```bash
   cd faceclone
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:

   ```bash
   python manage.py migrate
   ```

5. Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Visit `http://localhost:8000` in your browser to view the blog.

## Customization

Customize facebook clone to suit your needs:

- **Static Files**: Replace static files (CSS, JavaScript) in the `static` directory.
- **Templates**: Customize HTML templates in the `templates` directory.
- **Settings**: Adjust settings in the `settings.py` file to configure database, email, and other functionalities.
- **Admin Panel**: Personalize the Django admin panel by modifying admin models in the `admin.py` file.




## Acknowledgements

Special thanks to the Django community for their continuous support and contributions.

---

Feel free to reach out if you have any questions or suggestions! Happy Blogging! 📝
