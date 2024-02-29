from rest_framework.test import APITestCase


class CurrencyConvertTestCase(APITestCase):

    def test_currencyconvert(self):
        res = self.client.get('/api/convert/USD/INVALID/10/')
        self.assertEqual(res.status_code, 400)

        res = self.client.get('/api/convert/USD/BRL/10err/')
        self.assertEqual(res.status_code, 400)

        res = self.client.get('/api/convert/USD/BRL/1000,345/')
        self.assertEqual(res.status_code, 400)
        self.assertContains(res, 'valid number is required', status_code=400)

        res = self.client.get('/api/convert/USD/BRL/1000.345/')
        self.assertEqual(res.status_code, 200)
