from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from books.models import Book, BookType, BookStatus

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_book(self):
        payload = {
            'title': 'The Clockmaker Key',
            'premise': 'A young clockmaker discovers a key that unlocks secret passages through time.',
            'book_type': BookType.FICTION,
            'target_word_count': 50000
        }
        url = reverse('book-list')
        response = self.client.post(url, payload, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        
        book_id = response.data['id']
        book = Book.objects.get(id=book_id)
        self.assertEqual(book.target_word_count, 50000)
        self.assertEqual(book.title, 'The Clockmaker Key')

    def test_get_book(self):
        book = Book.objects.create(
            title='Testing status API',
            premise='Testing status API premise',
            book_type=BookType.FICTION,
            status=BookStatus.DRAFT
        )
        url = reverse('book-detail', kwargs={'pk': book.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], BookStatus.DRAFT)

