from unittest.mock import patch, Mock
from rest_framework.test import APITestCase


class CurrencyConvertTestCase(APITestCase):
    '''Currency Convert API tests'''
    def setUp(self) -> None:
        self.currencies_response = {
            'BRLUSD': {'bid': 0.2018},
            'EURUSD': {'bid': 1.0837},
            'BTCUSD': {'bid': 62600}
        }
        return super().setUp()

    def test_currencyconvert_invalid_tgt(self):
        '''Try an invalid currency code'''
        res = self.client.get('/api/convert/USD/INVALID/10/')
        self.assertEqual(res.status_code, 403)

    def test_currencyconvert_invalid_amount(self):
        '''Try an invalid amount input 2'''
        res = self.client.get('/api/convert/USD/BRL/10err/')
        self.assertEqual(res.status_code, 403)

    def test_currencyconvert_invalid_amount2(self):
        '''Try an invalid amount input 2'''
        res = self.client.get('/api/convert/USD/BRL/1000,345/')
        self.assertContains(res, 'inválido', status_code=403)

    @patch('converter.services.requests.get')
    def test_currencyconvert_valid(self, mock_get):
        '''Simple convertion from USD to BRL'''
        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.currencies_response
        convert_amount = 1000.345
        res = self.client.get(f'/api/convert/USD/BRL/{convert_amount}/')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()['converted_amount'],
                         convert_amount *
                         (1 / self.currencies_response['BRLUSD']['bid']))

    @patch('converter.services.requests.get')
    def test_currencyconvert_nonusd(self, mock_get):
        '''Convertion between non USD currencies'''
        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.currencies_response
        convert_amount = 100.5
        res = self.client.get(f'/api/convert/EUR/BRL/{convert_amount}/')
        self.assertEqual(res.status_code, 200)

        converted_amount = (
            (self.currencies_response['EURUSD']['bid'] * convert_amount) *
            (1 / self.currencies_response['BRLUSD']['bid']))
        self.assertEqual(converted_amount, res.json()['converted_amount'])

    @patch('converter.services.requests.get')
    def test_currencyconvert_fid_to_crypto(self, mock_get):
        '''Convert Fid to Crypto'''
        mock_get.return_value = Mock()
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = self.currencies_response
        convert_amount = 140200
        res = self.client.get(f'/api/convert/BRL/BTC/{convert_amount}/')
        self.assertEqual(res.status_code, 200)
        converted_amount = (
            (self.currencies_response['BRLUSD']['bid'] * convert_amount) *
            (1 / self.currencies_response['BTCUSD']['bid']))
        self.assertEqual(converted_amount, res.json()['converted_amount'])
