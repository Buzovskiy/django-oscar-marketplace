from django.test import SimpleTestCase
from ..utils import validate_sizes, get_sizes_list_from_range


class ValidateSizesTestCase(SimpleTestCase):

    def test_validate_sizes(self):
        """
        python manage.py test application.catalogue.tests.test_utils.ValidateSizesTestCase.test_validate_sizes
        """
        self.assertTrue(validate_sizes('20-30'))
        self.assertTrue(validate_sizes('20.5-30'))
        self.assertTrue(validate_sizes('20-30.5'))
        self.assertTrue(validate_sizes('20.5-30.5'))

        self.assertFalse(validate_sizes('20,5-30'))
        self.assertFalse(validate_sizes('20-30,5'))
        self.assertFalse(validate_sizes('20,5-30,5'))
        self.assertFalse(validate_sizes('a-b'))
        self.assertFalse(validate_sizes('5-30'))
        self.assertFalse(validate_sizes('200-30.5'))
        self.assertFalse(validate_sizes('20.59-30.5'))
        self.assertFalse(validate_sizes('20,59-30'))
        self.assertFalse(validate_sizes('20-30,59'))
        self.assertFalse(validate_sizes('20,59-930,59'))
        self.assertFalse(validate_sizes(' 20-30'))
        self.assertFalse(validate_sizes('20'))
        self.assertFalse(validate_sizes('20 - 30'))
        self.assertFalse(validate_sizes('20, 30, 40'))
        self.assertFalse(validate_sizes('20 30 40'))
        self.assertFalse(validate_sizes('30-20'))

    def test_get_sizes_list_from_range(self):
        """
        python manage.py test application.catalogue.tests.test_utils.ValidateSizesTestCase.test_get_sizes_list_from_range
        """
        self.assertEqual(get_sizes_list_from_range('20-25'), ['20', '21', '22', '23', '24', '25'])
        self.assertEqual(get_sizes_list_from_range('20-25.5'), ['20', '21', '22', '23', '24', '25.5'])
        self.assertEqual(get_sizes_list_from_range('20.5-25'), ['20.5', '21', '22', '23', '24', '25'])
        self.assertEqual(get_sizes_list_from_range('20.5-25.5'), ['20.5', '21', '22', '23', '24', '25.5'])
        self.assertEqual(get_sizes_list_from_range('20-21'), ['20', '21'])
        self.assertEqual(get_sizes_list_from_range('20.5-21'), ['20.5', '21'])
        self.assertEqual(get_sizes_list_from_range('20-21.5'), ['20', '21.5'])
        self.assertEqual(get_sizes_list_from_range('20-20'), ['20', '20'])