import unittest
from app import app, db, User

class BloglyTests(unittest.TestCase):

    def setUp(self):
        """Set up the test client and database"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
        self.client = app.test_client()

        # Connect to the database and create the tables
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up the database after each test"""
        with app.app_context():
            db.session.rollback()
            db.session.remove()
            db.drop_all()

    def test_homepage_redirect(self):
        """Test if the homepage redirects to /users"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, 'http://localhost/users')

    def test_users_index(self):
        """Test if the users index page returns a 200 status code"""
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)

    def test_new_user_form(self):
        """Test if the new user form page returns a 200 status code"""
        response = self.client.get('/users/new')
        self.assertEqual(response.status_code, 200)

    def test_create_new_user(self):
        """Test if creating a new user redirects to /users"""
        response = self.client.post('/users/new', data={
            'first_name': 'John',
            'last_name': 'Doe',
            'image_url': 'http://example.com/image.jpg'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_user_detail_page(self):
        """Test if the user detail page returns a 200 status code"""
        user = User(first_name='Jane', last_name='Doe')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/users/{user.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane Doe', response.data)

    def test_edit_user_form(self):
        """Test if the edit user form page returns a 200 status code"""
        user = User(first_name='Jane', last_name='Doe')
        db.session.add(user)
        db.session.commit()

        response = self.client.get(f'/users/{user.id}/edit')
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        """Test if updating a user redirects to /users"""
        user = User(first_name='Jane', last_name='Doe')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'/users/{user.id}/edit', data={
            'first_name': 'UpdatedName',
            'last_name': 'UpdatedLastName',
            'image_url': 'http://example.com/updated.jpg'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'UpdatedName UpdatedLastName', response.data)

    def test_delete_user(self):
        """Test if deleting a user redirects to /users"""
        user = User(first_name='Jane', last_name='Doe')
        db.session.add(user)
        db.session.commit()

        response = self.client.post(f'/users/{user.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Jane Doe', response.data)

if __name__ == '__main__':
    unittest.main()
