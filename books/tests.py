from django.test import TestCase, Client
from django.urls import reverse
from .models import Book
from pymongo import MongoClient
import environ
import random
import string

env = environ.Env()
environ.Env.read_env()

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))     

#Defining global variables
book_id = get_random_string(8)
username = get_random_string(6)

# Create your tests here.

class BookTestCase(TestCase):
    order = ['test_welcome', 'test_book_creation', 'test_library_retrieval',
             'test_book_retrieval', 'test_book_deletion', 'tear_down']

    def setUp(self):
        self.client = Client()
        self.book_data = {
            'book_id': book_id
        }
        self.username = username
        self.mongo_client = MongoClient(env('DATABASE_URL'))
        self.db = self.mongo_client.test_lib
        self.collection = self.db.libraries
        self.book = Book.objects.create(**self.book_data)

    #Testing welcome page works
    def test1_welcome(self):
        url = reverse('welcome')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #Testing book creation
    def test2_book_creation(self):
        url = reverse('books.user', kwargs={'user': self.username})
        response = self.client.post(url, self.book_data)
        self.assertEqual(response.status_code, 201)

    #testing library retrival
    def test3_library_retrieval(self):
        url = reverse('books.user', kwargs={'user': self.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['book_ids'][0], self.book.book_id)
    
    #testing book retrival
    def test4_book_retrieval(self):
        url = reverse('books.user.b_id', kwargs={'user': self.username, 'b_id': self.book.book_id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['book_ids'][0], self.book.book_id)
        
    #testing book deletion        
    def test5_book_deletion(self):
        url = reverse('books.user.b_id', kwargs={'user': self.username, 'b_id': self.book.book_id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        
    
    def test6_tearDown(self):
        self.collection.drop()
        self.mongo_client.close()