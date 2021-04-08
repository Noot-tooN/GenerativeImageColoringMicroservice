from django.test import TestCase
from Proba.models import Person

# Create your tests here.
class ProbaTestCase(TestCase):
    def setUp(self):
        Person.objects.create(first_name="Aleksa", last_name="Novcic")
    
    def test_person_first_name(self):
        p = Person.objects.get(first_name="Aleksa")
        self.assertEqual(p.last_name, "Novcic")
    
    def test_person_last_name(self):
        p = Person.objects.get(last_name="Novcic")
        self.assertEqual(p.first_name, "Aleksa")
    
    # Add this if you want tests to fail
    def test_person_fail(self):
        self.assertEqual(False, True)