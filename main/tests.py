from django.test import TestCase
from django.contrib.auth.models import User
from main.views import tabular_data_present


# Create your tests here.
class AuxMethodTests(TestCase):
    def test_empty_data_method(self):
        empty = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]
        not_empty = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ]

        data_present_empty = tabular_data_present(empty)
        data_present_not_empty = tabular_data_present(not_empty)

        self.assertFalse( data_present_empty, "There should be no data in the empty dataset")
        self.assertTrue( data_present_not_empty, "There should be data in the not empty dataset")
