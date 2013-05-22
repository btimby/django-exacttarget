import jwt


from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model


UserModel = get_user_model()


JSON_USER = {
    'id': 10083350,
    'oauthToken': 'w35ch4cxkrb2kqd33ujq2dde',
    'internalOauthToken': '0bUh1dFrbTcU1MXj7VvrAbc3w1365Hecw6qSgL0caJzOjHepT9XHSEllucoDBAdNW',
    'refreshToken': '2e33rrhev847jg97zt2zx333',
    'expiresIn': 3600,
    'email': 'jmeketa@exacttarget.com',
    'culture': 'en-US',
    'timezone':
    {
        'longName': '(GMT-06:00) Central Time (No Daylight Saving)',
        'shortName': 'CST',
        'offset': -6.0,
        'dst': False
    }
}

JSON = {
   'exp': 1366605874,
   'iss': 'https://imh.exacttarget.com',
   'request':
   {
      'claimsVersion': 1,
      'user': JSON_USER,
      'organization':
      {
         'id': 10088797,
         'enterpriseId': 10088797,
         'dataContext': 'core',
         'stackKey': 'S1'
      },
      'application':
      {
         'id': '7a755360-c283-4671-bfe4-6a3b752d3655',
         'package': 'sandbox.SSO_APP',
         'redirectUrl': 'https://localhost/CSharpSSOExample/Home.aspx',
         'features':
         {
         },
         'userPermissions':
         [
            {
               'Key': 'sandbox.SSO_APP.custompermission1',
               'Name': 'CustomPermission1'
            },
            {
               'Key': 'sandbox.SSO_APP.custompermission2',
               'Name': 'CustomPermission2'
            }
         ]
      }
   }
}
JWT_SECRET = 'test-secret-1234'
JWT = jwt.encode(JSON, JWT_SECRET)


class ClientTestCase(TestCase):
    def setUp(self):
        super(ClientTestCase, self).setUp()
        self.client = Client()


class LoginTestCase(ClientTestCase):
    fixtures = (
        'test_data',
    )

    def test_login_exacttarget(self):
        "Ensure that a valid JWT can be decoded, and the user created."
        with (self.settings(API_KEYS={'exacttarget': {'secret': JWT_SECRET},
              'smartfile': {'key': 'foo', 'password': 'bar'}})):
            r = self.client.post('/login/', {'JWT': JWT})
        self.assertRedirects(r, '/')
        # Ensure the new user exists, and verify their API credentials.
        user = UserModel.objects.get(email=JSON_USER['email'])
        self.assertEqual(user.exacttarget.oauthToken, JSON_USER['oauthToken'])
        self.assertEqual(user.exacttarget.internalOauthToken,
                         JSON_USER['internalOauthToken'])
        self.assertEqual(user.exacttarget.refreshToken, JSON_USER['refreshToken'])
        self.assertEqual(user.smartfile.key, 'foo')
        self.assertEqual(user.smartfile.password, 'bar')

    def test_login_django(self):
        "Ensure logging in by email works."
        r = self.client.post('/login/', {'username': 'test@example.com',
                             'password': 'xxxx'})
        self.assertRedirects(r, '/')
