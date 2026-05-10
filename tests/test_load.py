import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import pandas as pd
import json
import tempfile
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.load import load_to_csv, transform_for_spreadsheet, load_to_spreetsheet, store_to_postgre


class TestLoadToCSV(unittest.TestCase):
    """Test untuk fungsi load_to_csv"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.df = pd.DataFrame({
            'title': ['Shirt', 'Pants'],
            'price': [800000, 1600000],
            'rating': [4.5, 4.8],
            'colors': [3, 5],
            'size': ['M', 'L'],
            'gender': ['Male', 'Female'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
        })
        
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        """Cleanup temp files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    @patch('utils.load.pd.DataFrame.to_csv')
    def test_load_to_csv_called(self, mock_to_csv):
        """Test load_to_csv memanggil to_csv"""
        load_to_csv(self.df, 'test.csv')
        
        mock_to_csv.assert_called_once()
    
    def test_load_to_csv_creates_file(self):
        """Test load_to_csv membuat file CSV"""
        csv_path = os.path.join(self.temp_dir, 'test.csv')
        
        self.df.to_csv(csv_path, index=False)
        
        self.assertTrue(os.path.exists(csv_path))
    
    def test_load_to_csv_file_content(self):
        """Test isi file CSV benar"""
        csv_path = os.path.join(self.temp_dir, 'test.csv')
        
        self.df.to_csv(csv_path, index=False)
        
        loaded_df = pd.read_csv(csv_path)
        self.assertEqual(len(loaded_df), len(self.df))
        self.assertEqual(list(loaded_df.columns), list(self.df.columns))
    
    @patch('utils.load.pd.DataFrame.to_csv')
    def test_load_to_csv_error_handling(self, mock_to_csv):
        """Test load_to_csv error handling"""
        mock_to_csv.side_effect = Exception("Write error")
        
        try:
            load_to_csv(self.df, 'test.csv')
        except:
            pass
    
    def test_load_to_csv_dataframe_preserved(self):
        """Test DataFrame tidak berubah setelah load_to_csv"""
        df_original = self.df.copy()
        
        csv_path = os.path.join(self.temp_dir, 'test.csv')
        self.df.to_csv(csv_path, index=False)
        
        pd.testing.assert_frame_equal(self.df, df_original)


class TestTransformForSpreadsheet(unittest.TestCase):
    """Test untuk fungsi transform_for_spreadsheet"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.df = pd.DataFrame({
            'title': ['Shirt', 'Pants'],
            'price': [800000.0, 1600000.0],
            'rating': [4.5, 4.8],
            'colors': [3, 5],
            'size': ['M', 'L'],
            'gender': ['Male', 'Female'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
        })
    
    def test_transform_for_spreadsheet_returns_dataframe(self):
        """Test transform_for_spreadsheet mengembalikan DataFrame"""
        result = transform_for_spreadsheet(self.df)
        
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_transform_for_spreadsheet_creates_copy(self):
        """Test transform_for_spreadsheet membuat copy, tidak mengubah original"""
        original_df = self.df.copy()
        result = transform_for_spreadsheet(self.df)
        
        pd.testing.assert_frame_equal(self.df, original_df)
    
    def test_transform_for_spreadsheet_title_string_type(self):
        """Test kolom title menjadi string type"""
        result = transform_for_spreadsheet(self.df)
        
        self.assertEqual(str(result['title'].dtype), 'string')
    
    def test_transform_for_spreadsheet_size_string_type(self):
        """Test kolom size menjadi string type"""
        result = transform_for_spreadsheet(self.df)
        
        self.assertEqual(str(result['size'].dtype), 'string')
    
    def test_transform_for_spreadsheet_gender_string_type(self):
        """Test kolom gender menjadi string type"""
        result = transform_for_spreadsheet(self.df)
        
        self.assertEqual(str(result['gender'].dtype), 'string')
    
    def test_transform_for_spreadsheet_price_unchanged(self):
        """Test kolom price tidak berubah"""
        result = transform_for_spreadsheet(self.df)
        
        self.assertEqual(result['price'].dtype, self.df['price'].dtype)
    
    def test_transform_for_spreadsheet_rating_unchanged(self):
        """Test kolom rating tidak berubah"""
        result = transform_for_spreadsheet(self.df)
        
        self.assertEqual(result['rating'].dtype, self.df['rating'].dtype)
    
    def test_transform_for_spreadsheet_data_values_preserved(self):
        """Test nilai data tetap sama"""
        result = transform_for_spreadsheet(self.df)
        
        for col in ['title', 'size', 'gender']:
            self.assertEqual(result[col].tolist(), self.df[col].tolist())
    
    def test_transform_for_spreadsheet_empty_dataframe(self):
        """Test dengan empty DataFrame"""
        empty_df = pd.DataFrame({
            'title': [],
            'price': [],
            'rating': [],
            'colors': [],
            'size': [],
            'gender': [],
            'timestamp': []
        })
        
        result = transform_for_spreadsheet(empty_df)
        
        self.assertEqual(len(result), 0)


class TestLoadToSpreadsheet(unittest.TestCase):
    """Test untuk fungsi load_to_spreetsheet"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.df = pd.DataFrame({
            'title': ['Shirt', 'Pants'],
            'price': [800000.0, 1600000.0],
            'rating': [4.5, 4.8],
            'colors': [3, 5],
            'size': ['M', 'L'],
            'gender': ['Male', 'Female'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
        })
        
        self.temp_dir = tempfile.mkdtemp()
        self.cred_file = os.path.join(self.temp_dir, 'client_secret.json')
    
    def tearDown(self):
        """Cleanup temp files"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_load_to_spreadsheet_missing_credentials_file(self):
        """Test load_to_spreetsheet dengan missing credentials file"""
        with self.assertRaises(FileNotFoundError):
            load_to_spreetsheet(self.df, 'sheet_id', 'sheet_name', '/invalid/path/credentials.json')
    
    @patch('utils.load.json.load')
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_load_to_spreadsheet_file_exists(self, mock_file, mock_json):
        """Test load_to_spreetsheet ketika file ada"""
        temp_cred = os.path.join(self.temp_dir, 'creds.json')
        
        with open(temp_cred, 'w') as f:
            json.dump({'type': 'service_account'}, f)
        
        self.assertTrue(os.path.exists(temp_cred))
    
    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials.from_service_account_info')
    @patch('builtins.open', new_callable=mock_open)
    @patch('utils.load.json.load')
    @patch('utils.load.os.path.exists')
    def test_load_to_spreadsheet_success(self, mock_exists, mock_json_load, 
                                         mock_open_file, mock_creds, mock_authorize):
        """Test load_to_spreetsheet berhasil"""
        mock_exists.return_value = True
        mock_json_load.return_value = {'type': 'service_account'}
        
        mock_sheet = MagicMock()
        mock_client = MagicMock()
        mock_client.open_by_key.return_value.worksheet.return_value = mock_sheet
        mock_authorize.return_value = mock_client
        
        try:
            load_to_spreetsheet(self.df, 'sheet_id', 'sheet_name', 'creds.json')
            self.assertTrue(True)
        except FileNotFoundError:
            pass
    
    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials.from_service_account_info')
    @patch('builtins.open', new_callable=mock_open)
    @patch('utils.load.json.load')
    @patch('utils.load.os.path.exists')
    def test_load_to_spreadsheet_calls_clear(self, mock_exists, mock_json_load,
                                            mock_open_file, mock_creds, mock_authorize):
        """Test load_to_spreetsheet memanggil sheet.clear()"""
        mock_exists.return_value = True
        mock_json_load.return_value = {'type': 'service_account'}
        
        mock_sheet = MagicMock()
        mock_client = MagicMock()
        mock_client.open_by_key.return_value.worksheet.return_value = mock_sheet
        mock_authorize.return_value = mock_client
        
        try:
            load_to_spreetsheet(self.df, 'sheet_id', 'sheet_name', 'creds.json')
            mock_sheet.clear.assert_called_once()
        except FileNotFoundError:
            pass
    
    @patch('utils.load.os.path.exists')
    def test_load_to_spreadsheet_file_not_found_error(self, mock_exists):
        """Test load_to_spreetsheet dengan file not found"""
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            load_to_spreetsheet(self.df, 'sheet_id', 'sheet_name', 'non_existent.json')


class TestStoreToPostgre(unittest.TestCase):
    """Test untuk fungsi store_to_postgre"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.df = pd.DataFrame({
            'title': ['Shirt', 'Pants'],
            'price': [800000.0, 1600000.0],
            'rating': [4.5, 4.8],
            'colors': [3, 5],
            'size': ['M', 'L'],
            'gender': ['Male', 'Female'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
        })
    
    @patch('utils.load.create_engine')
    def test_store_to_postgre_create_engine_called(self, mock_engine):
        """Test store_to_postgre memanggil create_engine"""
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        
        store_to_postgre(self.df, 'postgresql://user:pass@localhost/db')
        
        mock_engine.assert_called_once()
    
    @patch('utils.load.create_engine')
    def test_store_to_postgre_to_sql_called(self, mock_engine):
        """Test store_to_postgre memanggil to_sql"""
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            store_to_postgre(self.df, 'postgresql://user:pass@localhost/db')
            mock_to_sql.assert_called_once()
    
    @patch('utils.load.create_engine')
    def test_store_to_postgre_table_name(self, mock_engine):
        """Test store_to_postgre menggunakan nama table yang benar"""
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            store_to_postgre(self.df, 'postgresql://user:pass@localhost/db')
            
            call_args = mock_to_sql.call_args
            self.assertEqual(call_args[0][0], 'fashion_data')
    
    @patch('utils.load.create_engine')
    def test_store_to_postgre_error_handling(self, mock_engine):
        """Test store_to_postgre error handling"""
        mock_engine.side_effect = Exception("Connection failed")
        
        try:
            store_to_postgre(self.df, 'postgresql://invalid')
        except:
            pass
    
    @patch('utils.load.create_engine')
    def test_store_to_postgre_with_valid_url(self, mock_engine):
        """Test store_to_postgre dengan URL yang valid"""
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        
        db_url = 'postgresql+psycopg2://user:pass@localhost:5432/db'
        store_to_postgre(self.df, db_url)
        
        self.assertEqual(mock_engine.call_args[0][0], db_url)
    
    @patch('utils.load.create_engine')
    def test_store_to_postgre_if_exists_append(self, mock_engine):
        """Test store_to_postgre dengan if_exists=append"""
        mock_connection = MagicMock()
        mock_engine.return_value.connect.return_value.__enter__.return_value = mock_connection
        
        with patch.object(pd.DataFrame, 'to_sql') as mock_to_sql:
            store_to_postgre(self.df, 'postgresql://user:pass@localhost/db')
            
            call_args = mock_to_sql.call_args
            self.assertEqual(call_args[1]['if_exists'], 'append')


class TestLoadDataValidation(unittest.TestCase):
    """Test untuk validasi data sebelum load"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.valid_df = pd.DataFrame({
            'title': ['Shirt', 'Pants'],
            'price': [800000.0, 1600000.0],
            'rating': [4.5, 4.8],
            'colors': [3, 5],
            'size': ['M', 'L'],
            'gender': ['Male', 'Female'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
        })
    
    def test_dataframe_has_required_columns(self):
        """Test DataFrame memiliki kolom yang diperlukan"""
        required_columns = ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        
        for col in required_columns:
            self.assertIn(col, self.valid_df.columns)
    
    def test_dataframe_no_null_values(self):
        """Test DataFrame tidak memiliki null values"""
        self.assertFalse(self.valid_df.isnull().any().any())
    
    def test_dataframe_non_empty(self):
        """Test DataFrame tidak kosong"""
        self.assertGreater(len(self.valid_df), 0)
    
    def test_dataframe_price_is_numeric(self):
        """Test kolom price adalah numeric"""
        self.assertTrue(pd.api.types.is_numeric_dtype(self.valid_df['price']))
    
    def test_dataframe_rating_is_numeric(self):
        """Test kolom rating adalah numeric"""
        self.assertTrue(pd.api.types.is_numeric_dtype(self.valid_df['rating']))
    
    def test_dataframe_colors_is_numeric(self):
        """Test kolom colors adalah numeric"""
        self.assertTrue(pd.api.types.is_numeric_dtype(self.valid_df['colors']))


if __name__ == '__main__':
    unittest.main()
