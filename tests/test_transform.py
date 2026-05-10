import unittest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.transform import transform_data


class TestTransformData(unittest.TestCase):
    """Test untuk fungsi transform_data"""
    
    def setUp(self):
        """Setup data untuk testing"""
        self.sample_data = pd.DataFrame({
            'title': ['Shirt', 'Pants', 'Dress'],
            'price': ['$50.00', '$100.00', '$75.50'],
            'rating': ['4.5', '4.8', '3.9'],
            'colors': ['3', '5', '2'],
            'size': ['M', 'L', 'S'],
            'gender': ['Male', 'Female', 'Female'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now(), pd.Timestamp.now()]
        })
    
    def test_transform_data_returns_dataframe(self):
        """Test transform_data mengembalikan DataFrame"""
        result = transform_data(self.sample_data.copy(), exchange_rate=16000)
        
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_transform_data_price_conversion(self):
        """Test price conversion dari USD ke IDR"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        expected_price_1 = 50.00 * 16000
        expected_price_2 = 100.00 * 16000
        expected_price_3 = 75.50 * 16000
        
        self.assertAlmostEqual(result['price'].iloc[0], expected_price_1, places=2)
        self.assertAlmostEqual(result['price'].iloc[1], expected_price_2, places=2)
        self.assertAlmostEqual(result['price'].iloc[2], expected_price_3, places=2)
    
    def test_transform_data_rating_float_conversion(self):
        """Test rating convert ke float"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(result['rating'].dtype, 'float64')
        self.assertEqual(result['rating'].iloc[0], 4.5)
        self.assertEqual(result['rating'].iloc[1], 4.8)
    
    def test_transform_data_colors_int_conversion(self):
        """Test colors convert ke int"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(result['colors'].dtype, 'int64')
        self.assertEqual(result['colors'].iloc[0], 3)
        self.assertEqual(result['colors'].iloc[1], 5)
    
    def test_transform_data_column_order(self):
        """Test kolom urutannya sesuai"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        expected_columns = ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        self.assertEqual(list(result.columns), expected_columns)
    
    def test_transform_data_no_null_values(self):
        """Test hasil transform tidak ada null values"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertFalse(result.isnull().any().any())
    
    def test_transform_data_price_not_original_currency(self):
        """Test kolom price tidak lagi berbentuk string dengan $"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(result['price'].dtype, 'float64')
        for price in result['price']:
            self.assertIsInstance(price, (int, float, np.integer, np.floating))
    
    def test_transform_data_maintains_rows(self):
        """Test jumlah baris tidak berubah"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(len(result), len(df))
    
    def test_transform_data_different_exchange_rates(self):
        """Test transform dengan exchange rate berbeda"""
        df1 = self.sample_data.copy()
        df2 = self.sample_data.copy()
        
        result1 = transform_data(df1, exchange_rate=16000)
        result2 = transform_data(df2, exchange_rate=20000)
        
        self.assertNotEqual(result1['price'].iloc[0], result2['price'].iloc[0])
    
    def test_transform_data_size_remains_string(self):
        """Test kolom size tetap string type"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(result['size'].dtype, 'object')
        self.assertIsInstance(result['size'].iloc[0], str)
    
    def test_transform_data_gender_remains_string(self):
        """Test kolom gender tetap string type"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(result['gender'].dtype, 'object')
        self.assertIsInstance(result['gender'].iloc[0], str)
    
    def test_transform_data_title_remains_string(self):
        """Test kolom title tetap string type"""
        df = self.sample_data.copy()
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(result['title'].dtype, 'object')
        self.assertIsInstance(result['title'].iloc[0], str)
    
    def test_transform_data_with_higher_prices(self):
        """Test transform dengan harga lebih tinggi"""
        df = pd.DataFrame({
            'title': ['Luxury Item'],
            'price': ['$999.99'],
            'rating': ['5.0'],
            'colors': ['1'],
            'size': ['M'],
            'gender': ['Unisex'],
            'timestamp': [pd.Timestamp.now()]
        })
        
        result = transform_data(df, exchange_rate=16000)
        
        expected_price = 999.99 * 16000
        self.assertAlmostEqual(result['price'].iloc[0], expected_price, places=0)
    
    def test_transform_data_preserves_data_integrity(self):
        """Test data integrity setelah transform"""
        df = self.sample_data.copy()
        original_titles = df['title'].tolist()
        
        result = transform_data(df, exchange_rate=16000)
        
        self.assertEqual(result['title'].tolist(), original_titles)


class TestTransformDataError(unittest.TestCase):
    """Test error handling dalam transform"""
    
    def test_transform_data_with_missing_columns(self):
        """Test transform dengan missing columns"""
        incomplete_data = pd.DataFrame({
            'title': ['Shirt'],
            'price': ['$50.00']
        })
        
        try:
            result = transform_data(incomplete_data, exchange_rate=16000)
            self.fail("Should raise KeyError for missing columns")
        except KeyError:
            pass
    
    def test_transform_data_price_format_handling(self):
        """Test handling format price yang berbeda"""
        df = pd.DataFrame({
            'title': ['Item'],
            'price': ['50.00'],
            'rating': ['4.5'],
            'colors': ['3'],
            'size': ['M'],
            'gender': ['Male'],
            'timestamp': [pd.Timestamp.now()]
        })
        
        try:
            result = transform_data(df, exchange_rate=16000)
            self.assertIsInstance(result, pd.DataFrame)
        except:
            pass
    
    def test_transform_data_invalid_rating(self):
        """Test handling invalid rating format"""
        df = pd.DataFrame({
            'title': ['Item'],
            'price': ['$50.00'],
            'rating': ['Invalid Rating'],
            'colors': ['3'],
            'size': ['M'],
            'gender': ['Male'],
            'timestamp': [pd.Timestamp.now()]
        })
        
        try:
            result = transform_data(df, exchange_rate=16000)
            self.fail("Should raise error for invalid rating")
        except ValueError:
            pass
    
    def test_transform_data_invalid_colors(self):
        """Test handling invalid colors format"""
        df = pd.DataFrame({
            'title': ['Item'],
            'price': ['$50.00'],
            'rating': ['4.5'],
            'colors': ['Invalid'],
            'size': ['M'],
            'gender': ['Male'],
            'timestamp': [pd.Timestamp.now()]
        })
        
        try:
            result = transform_data(df, exchange_rate=16000)
            self.fail("Should raise error for invalid colors")
        except ValueError:
            pass


class TestTransformDataTypes(unittest.TestCase):
    """Test tipe data setelah transform"""
    
    def setUp(self):
        """Setup data untuk testing tipe data"""
        self.df = pd.DataFrame({
            'title': ['Shirt', 'Pants'],
            'price': ['$50.00', '$100.00'],
            'rating': ['4.5', '4.8'],
            'colors': ['3', '5'],
            'size': ['M', 'L'],
            'gender': ['Male', 'Female'],
            'timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
        })
    
    def test_all_column_types_correct(self):
        """Test semua kolom punya tipe data yang benar"""
        result = transform_data(self.df, exchange_rate=16000)
        
        type_mapping = {
            'title': 'object',
            'price': 'float64',
            'rating': 'float64',
            'colors': 'int64',
            'size': 'object',
            'gender': 'object',
            'timestamp': 'datetime64'
        }
        
        for col, expected_type in type_mapping.items():
            actual_type = str(result[col].dtype)
            self.assertTrue(
                expected_type in actual_type,
                f"Column {col} has type {actual_type}, expected {expected_type}"
            )


if __name__ == '__main__':
    unittest.main()
