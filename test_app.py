```python
import unittest
from app import app

class TestFlaskApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_create_task(self):
        response = self.app.post('/api/tasks', json={'title': 'Test Task', 'description': 'Test Description'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Test Task', response.get_json()['title'])

    def test_get_tasks(self):
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

if __name__ == '__main__':
    unittest.main()
```