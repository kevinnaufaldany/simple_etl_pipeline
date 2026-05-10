import unittest
from unittest.mock import Mock, patch, MagicMock
from bs4 import BeautifulSoup
from datetime import datetime
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import fetching_content, extract_fashion_data, scrape_fashion_data


class TestFetchingContent(unittest.TestCase):
    """Test untuk fungsi fetching_content"""
    
    @patch('utils.extract.requests.Session')
    def test_fetching_content_success(self, mock_session):
        """Test fetching_content berhasil mendapatkan konten"""
        mock_response = Mock()
        mock_response.content = b'<html><body>Test</body></html>'
        mock_response.raise_for_status.return_value = None
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        result = fetching_content('http://example.com')
        
        self.assertIsNotNone(result)
        self.assertEqual(result, b'<html><body>Test</body></html>')
        mock_session_instance.get.assert_called_once()
    
    @patch('utils.extract.requests.Session')
    def test_fetching_content_error(self, mock_session):
        """Test fetching_content menangani error dengan baik"""
        mock_session_instance = Mock()
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = Exception("Connection error")
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        result = fetching_content('http://invalid-url.com')
        
        self.assertIsNone(result)
    
    @patch('utils.extract.requests.Session')
    def test_fetching_content_with_headers(self, mock_session):
        """Test fetching_content menggunakan headers yang benar"""
        mock_response = Mock()
        mock_response.content = b'<html></html>'
        mock_response.raise_for_status.return_value = None
        
        mock_session_instance = Mock()
        mock_session_instance.get.return_value = mock_response
        mock_session.return_value = mock_session_instance
        
        fetching_content('http://example.com')
        
        call_args = mock_session_instance.get.call_args
        self.assertIsNotNone(call_args[1]['headers'])
        self.assertIn('User-Agent', call_args[1]['headers'])


class TestExtractFashionData(unittest.TestCase):
    """Test untuk fungsi extract_fashion_data"""
    
    def setUp(self):
        """Setup HTML mock untuk test"""
        self.valid_html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Stylish T-Shirt</h3>
                <div class="price-container">
                    <span class="price">$50.00</span>
                </div>
                <p>Rating: ⭐ 4.5 / 5</p>
                <p>3 Colors</p>
                <p>Size: M</p>
                <p>Gender: Male</p>
            </div>
        </div>
        """
        
        self.invalid_html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Unknown Product</h3>
                <div class="price-container">
                    <span class="price">$50.00</span>
                </div>
            </div>
        </div>
        """
        
        self.missing_price_html = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Good Product</h3>
            </div>
        </div>
        """
    
    def test_extract_fashion_data_success(self):
        """Test extract_fashion_data berhasil extract data"""
        soup = BeautifulSoup(self.valid_html, 'html.parser')
        card = soup.find('div', class_='collection-card')
        
        timestamp = datetime.now()
        result = extract_fashion_data(card, timestamp)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['title'], 'Stylish T-Shirt')
        self.assertEqual(result['price'], '$50.00')
        self.assertEqual(result['rating'], '4.5')
        self.assertEqual(result['colors'], '3')
        self.assertEqual(result['size'], 'M')
        self.assertEqual(result['gender'], 'Male')
        self.assertEqual(result['timestamp'], timestamp)
    
    def test_extract_fashion_data_unknown_product(self):
        """Test extract_fashion_data menolak Unknown Product"""
        soup = BeautifulSoup(self.invalid_html, 'html.parser')
        card = soup.find('div', class_='collection-card')
        
        result = extract_fashion_data(card)
        
        self.assertIsNone(result)
    
    def test_extract_fashion_data_missing_price(self):
        """Test extract_fashion_data menolak data tanpa price"""
        soup = BeautifulSoup(self.missing_price_html, 'html.parser')
        card = soup.find('div', class_='collection-card')
        
        result = extract_fashion_data(card)
        
        self.assertIsNone(result)
    
    def test_extract_fashion_data_returns_dict_structure(self):
        """Test extract_fashion_data mengembalikan struktur dict yang benar"""
        soup = BeautifulSoup(self.valid_html, 'html.parser')
        card = soup.find('div', class_='collection-card')
        
        result = extract_fashion_data(card)
        
        required_keys = ['title', 'price', 'rating', 'colors', 'size', 'gender', 'timestamp']
        for key in required_keys:
            self.assertIn(key, result)
    
    def test_extract_fashion_data_with_missing_fields(self):
        """Test extract_fashion_data menangani missing fields"""
        html_missing_fields = """
        <div class="collection-card">
            <div class="product-details">
                <h3 class="product-title">Test Product</h3>
                <div class="price-container">
                    <span class="price">$100.00</span>
                </div>
            </div>
        </div>
        """
        soup = BeautifulSoup(html_missing_fields, 'html.parser')
        card = soup.find('div', class_='collection-card')
        
        result = extract_fashion_data(card)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['colors'], 'Colors not found')
        self.assertEqual(result['size'], 'Size not found')
        self.assertEqual(result['gender'], 'Gender not found')


class TestScrapeFashionData(unittest.TestCase):
    """Test untuk fungsi scrape_fashion_data"""
    
    @patch('utils.extract.fetching_content')
    @patch('utils.extract.time.sleep')
    def test_scrape_fashion_data_single_page(self, mock_sleep, mock_fetch):
        """Test scrape_fashion_data untuk single page"""
        html_content = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Product 1</h3>
                    <div class="price-container">
                        <span class="price">$50.00</span>
                    </div>
                    <p>Rating: ⭐ 4.5 / 5</p>
                    <p>3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Male</p>
                </div>
            </body>
        </html>
        """
        
        mock_fetch.return_value = html_content.encode('utf-8')
        
        result = scrape_fashion_data('http://example.com/page{}.html', start_page=1, delay=0)
        
        self.assertIsInstance(result, list)
        self.assertEqual(mock_fetch.call_count, 1)
    
    @patch('utils.extract.fetching_content')
    def test_scrape_fashion_data_network_error(self, mock_fetch):
        """Test scrape_fashion_data menangani network error"""
        mock_fetch.return_value = None
        
        result = scrape_fashion_data('http://invalid-url.com/page{}.html', start_page=1, delay=0)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 0)
    
    @patch('utils.extract.fetching_content')
    def test_scrape_fashion_data_returns_list(self, mock_fetch):
        """Test scrape_fashion_data mengembalikan list"""
        html_content = """
        <html>
            <body>
                <div class="collection-card">
                    <h3 class="product-title">Product 1</h3>
                    <div class="price-container">
                        <span class="price">$50.00</span>
                    </div>
                    <p>Rating: ⭐ 4.5 / 5</p>
                    <p>3 Colors</p>
                    <p>Size: M</p>
                    <p>Gender: Male</p>
                </div>
            </body>
        </html>
        """
        
        mock_fetch.return_value = html_content.encode('utf-8')
        
        result = scrape_fashion_data('http://example.com/page{}.html', start_page=1, delay=0)
        
        self.assertIsInstance(result, list)
    
    @patch('utils.extract.fetching_content')
    @patch('utils.extract.time.sleep')
    def test_scrape_fashion_data_error_handling(self, mock_sleep, mock_fetch):
        """Test scrape_fashion_data error handling"""
        mock_fetch.return_value = None
        
        try:
            result = scrape_fashion_data('http://example.com/page{}.html', start_page=1, delay=0)
            self.assertIsInstance(result, list)
        except Exception as e:
            self.fail(f"scrape_fashion_data raised {type(e).__name__} unexpectedly!")


class TestExtractDataQuality(unittest.TestCase):
    """Test untuk quality checking extraction"""
    
    def setUp(self):
        """Setup data untuk quality test"""
        self.html = """
        <div class="collection-card">
            <h3 class="product-title">Premium Shirt</h3>
            <div class="price-container">
                <span class="price">$75.50</span>
            </div>
            <p>Rating: ⭐ 4.8 / 5</p>
            <p>5 Colors</p>
            <p>Size: L</p>
            <p>Gender: Female</p>
        </div>
        """
    
    def test_extracted_data_not_empty(self):
        """Test extracted data tidak kosong"""
        soup = BeautifulSoup(self.html, 'html.parser')
        card = soup.find('div', class_='collection-card')
        result = extract_fashion_data(card)
        
        self.assertTrue(all(result.values()))
    
    def test_extracted_data_types(self):
        """Test extracted data memiliki tipe yang benar"""
        soup = BeautifulSoup(self.html, 'html.parser')
        card = soup.find('div', class_='collection-card')
        result = extract_fashion_data(card)
        
        self.assertIsInstance(result['title'], str)
        self.assertIsInstance(result['price'], str)
        self.assertIsInstance(result['rating'], str)
        self.assertIsInstance(result['colors'], str)
        self.assertIsInstance(result['size'], str)
        self.assertIsInstance(result['gender'], str)


if __name__ == '__main__':
    unittest.main()
