import io
import unittest
from unittest.mock import MagicMock, patch, ANY
import logging

from hopara.hopara import Hopara
from hopara.table import Table


logging.getLogger('pyhopara').setLevel(logging.WARNING)


class HoparaCase(unittest.TestCase):
    def setUp(self):
        self.hopara = Hopara()
        self.hopara.config = MagicMock()
        self.hopara.config.get_dataset_url = lambda: 'https://test.hopara.py/'
        self.hopara.config.get_resource_url = lambda: 'https://resource.test.hopara.py/'
        self.hopara.request = MagicMock()

    def test_urls(self):
        self.assertEqual(self.hopara.get_table_url(Table('table1')),
                         r"https://test.hopara.py/table/table1/")
        self.assertEqual(self.hopara.get_row_url(Table('table1')),
                         r"https://test.hopara.py/table/table1/row?dataSource=hopara")

    @patch('requests.put')
    def test_upload_resource_from_memory(self, mock_put):
        mock_put.return_value.status_code = 200

        self.hopara.upload_resource_from_memory(io.BytesIO(b'any image buffer'), 'image', 'any_name', 'any_library')
        mock_put.assert_called_with(
            'https://resource.test.hopara.py/tenant/hopara.io/image-library/any_library/image/any_name',
            files={'file': ANY})

        self.hopara.upload_resource_from_memory(io.BytesIO(b'any icon buffer'), 'icon', 'any_name', 'any_library')
        mock_put.assert_called_with(
            'https://resource.test.hopara.py/tenant/hopara.io/icon-library/any_library/icon/any_name',
            files={'file': ANY})

        self.hopara.upload_resource_from_memory(io.BytesIO(b'any model buffer'), 'model', 'any_name', None)
        mock_put.assert_called_with(
            'https://resource.test.hopara.py/tenant/hopara.io/model/any_name',
            files={'file': ANY})


if __name__ == '__main__':
    unittest.main()
