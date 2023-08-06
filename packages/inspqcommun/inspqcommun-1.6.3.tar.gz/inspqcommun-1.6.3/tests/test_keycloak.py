#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, mock
from inspqcommun.identity.keycloak import get_token, get_service_account_token, KeycloakAPI, isDictEquals, remove_arguments_with_value_none
from inspqcommun.identity.keycloak_tools import KeycloakEnvironment

from tests.mock_keycloak_server import mocked_open_url, mock_json_load, mocked_requests_post, mocked_requests_get, mocked_requests_delete

import jwt
import os

class KeycloakTestCase(TestCase):
    
    keycloak_base_url = "https://keycloak.server.url"
    keycloak_auth_realm = "master"
    keycloak_auth_user = "monusername"
    keycloak_auth_password = "monmotdepasse"
    keycloak_auth_client_id = "monclientid"
    keycloak_auth_client_secret = "monclientsecret"
    keycloak_admin_auth_user = "admin"
    keycloak_admin_auth_password = "admin"
    keycloak_admin_auth_realm = "master"
    jwt_secret = 'secret'
    jwt_algo = 'HS256'
    validate_certs = False
    maxDiff = None

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

    def setUp(self):
        os.environ['KEYCLOAK_BASE_URL'] = self.keycloak_base_url
        os.environ['KEYCLOAK_AUTH_REALM'] = self.keycloak_auth_realm
        os.environ['KEYCLOAK_ENABLED'] = "true"
        os.environ['KEYCLOAK_AUTH_CLIENT_ID'] = self.keycloak_auth_client_id
        os.environ['KEYCLOAK_ADMIN_AUTH_USER'] = self.keycloak_admin_auth_user
        os.environ['KEYCLOAK_ADMIN_AUTH_PASSWORD'] = self.keycloak_admin_auth_password
        os.environ['KEYCLOAK_ADMIN_AUTH_REALM'] = self.keycloak_admin_auth_realm
        self.keycloak_url = "{0}/auth".format(self.keycloak_base_url)

    def tearDown(self):
        if 'KEYCLOAK_BASE_URL' in os.environ:
            del os.environ['KEYCLOAK_BASE_URL']
        if 'KEYCLOAK_AUTH_REALM' in os.environ:
            del os.environ['KEYCLOAK_AUTH_REALM']
        if 'KEYCLOAK_ENABLED' in os.environ:
            del os.environ['KEYCLOAK_ENABLED']
        if 'KEYCLOAK_ADMIN_AUTH_USER' in os.environ:
            del os.environ['KEYCLOAK_ADMIN_AUTH_USER']
        if 'KEYCLOAK_ADMIN_AUTH_PASSWORD' in os.environ:
            del os.environ['KEYCLOAK_ADMIN_AUTH_PASSWORD']
        if 'KEYCLOAK_ADMIN_AUTH_REALM' in os.environ:
            del os.environ['KEYCLOAK_ADMIN_AUTH_REALM']
        if 'KEYCLOAK_AUTH_CLIENT_SECRET' in os.environ:
            del os.environ['KEYCLOAK_AUTH_CLIENT_SECRET']

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testObtenirUnAccessTokenValide(self, mocked_requests_post, mocked_requests_get):
        authorization_header = get_token(
            base_url=self.keycloak_url,
            auth_realm=self.keycloak_auth_realm,
            client_id=self.keycloak_auth_client_id,
            auth_username=self.keycloak_auth_user,
            auth_password=self.keycloak_auth_password,
            client_secret=self.keycloak_auth_client_secret,
            validate_certs=self.validate_certs)
        access_token = authorization_header['Authorization'].split(' ')[1]
        decoded_access_token = jwt.decode(access_token, self.jwt_secret, algorithms=[self.jwt_algo], verify=False)
        self.assertEqual(decoded_access_token["preferred_username"], self.keycloak_auth_user, "L'utilisateur authentifié n'est pas le bon: {}".format(decoded_access_token["preferred_username"]))
        
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testObtenirUnAccessTokenValideAvecUnComteDeService(self, mocked_requests_post, mocked_requests_get):
        authorization_header = get_service_account_token(
            base_url=self.keycloak_url,
            auth_realm=self.keycloak_auth_realm,
            client_id=self.keycloak_auth_client_id,
            client_secret=self.keycloak_auth_client_secret,
            validate_certs=self.validate_certs)
        access_token = authorization_header['Authorization'].split(' ')[1]
        decoded_access_token = jwt.decode(access_token, self.jwt_secret, algorithms=[self.jwt_algo], verify=False)
        self.assertEqual(decoded_access_token["preferred_username"], self.keycloak_auth_user, "L'utilisateur authentifié n'est pas le bon: {}".format(decoded_access_token["preferred_username"]))

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def testCreerUnObjetKeycloakAvecToken(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakAPI(auth_keycloak_url=self.keycloak_url,
                 auth_client_id=self.keycloak_auth_client_id,
                 auth_username=self.keycloak_auth_user,
                 auth_password=self.keycloak_auth_password,
                 auth_realm=self.keycloak_auth_realm,
                 auth_client_secret=self.keycloak_auth_client_secret,
                 validate_certs=self.validate_certs)
        access_token = kc.restheaders['Authorization'].split(' ')[1]
        decoded_access_token = jwt.decode(access_token, self.jwt_secret, algorithms=[self.jwt_algo], verify=False)
        self.assertEqual(decoded_access_token["preferred_username"], self.keycloak_auth_user, "L'utilisateur authentifié n'est pas le bon: {}".format(decoded_access_token["preferred_username"]))

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_authenticate_by_username_password(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakEnvironment()
        auth_headers = kc.authenticateByUsernamePassword()
        self.assertIn(member="Authorization", container=auth_headers)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_authenticate_by_service_account(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakEnvironment()
        auth_headers = kc.authenticateByServiceAccount()
        self.assertIn(member="Authorization", container=auth_headers)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_token_url(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakEnvironment()
        token_url = kc.get_token_url()
        self.assertIsNotNone(token_url)
        self.assertIn(member="/token", container=token_url)

    def test_get_token_url_sans_admin_auth(self):
        del os.environ['KEYCLOAK_ADMIN_AUTH_USER']
        del os.environ['KEYCLOAK_ADMIN_AUTH_PASSWORD']
        kc = KeycloakEnvironment(defaultAdminAuthUser=None, defaultAdminAuthPassword=None)
        token_url = kc.get_token_url()
        self.assertIsNotNone(token_url)
        self.assertIn(member="/token", container=token_url)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_get_client_secret(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakEnvironment()
        client = kc.keycloak_auth_client_id
        realm = kc.keycloak_auth_realm
        client_secret = kc.get_client_secret(client_id=client, realm=realm)
        self.assertIsNotNone(client_secret)
        self.assertEqual(client_secret, "monsecret")

    def test_creer_un_keycloak_environment_sans_admin_auth_ni_client_secret(self):
        del os.environ['KEYCLOAK_ADMIN_AUTH_USER']
        del os.environ['KEYCLOAK_ADMIN_AUTH_PASSWORD']
        kc = KeycloakEnvironment(defaultAdminAuthUser=None, defaultAdminAuthPassword=None)
        self.assertIsNone(kc.kc)
        token = kc.authenticateByServiceAccount()
        self.assertDictEqual(token, {})
        token = kc.authenticateByUsernamePassword()
        self.assertDictEqual(token, {})

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_creer_un_keycloak_environment_sans_admin_auth_avec_client_secret(self, mocked_requests_post, mocked_requests_get):
        del os.environ['KEYCLOAK_ADMIN_AUTH_USER']
        del os.environ['KEYCLOAK_ADMIN_AUTH_PASSWORD']
        os.environ['KEYCLOAK_AUTH_CLIENT_SECRET'] = 'MonClientSecret'
        kc = KeycloakEnvironment(defaultAdminAuthUser=None, defaultAdminAuthPassword=None)
        self.assertIsNone(kc.kc)
        auth_headers = kc.authenticateByServiceAccount()
        self.assertIn(member="Authorization", container=auth_headers)
        auth_headers = kc.authenticateByUsernamePassword()
        self.assertIn(member="Authorization", container=auth_headers)

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_obtenir_utilisateurs(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakAPI(auth_keycloak_url=self.keycloak_url,
                 auth_client_id=self.keycloak_auth_client_id,
                 auth_username=self.keycloak_auth_user,
                 auth_password=self.keycloak_auth_password,
                 auth_realm=self.keycloak_auth_realm,
                 auth_client_secret=self.keycloak_auth_client_secret,
                 validate_certs=self.validate_certs)
        users = kc.get_users()
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]["id"], '07f54653-a138-40a2-8759-81c76299ee35')

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_obtenir_utilisateur_par_id(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakAPI(auth_keycloak_url=self.keycloak_url,
                 auth_client_id=self.keycloak_auth_client_id,
                 auth_username=self.keycloak_auth_user,
                 auth_password=self.keycloak_auth_password,
                 auth_realm=self.keycloak_auth_realm,
                 auth_client_secret=self.keycloak_auth_client_secret,
                 validate_certs=self.validate_certs)
        user = kc.get_user_by_id('07f54653-a138-40a2-8759-81c76299ee35')
        self.assertIsNotNone(user)
        self.assertEqual(user['id'], '07f54653-a138-40a2-8759-81c76299ee35')

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_obtenir_credentiels_utilisateur_par_id(self, mocked_requests_post, mocked_requests_get):
        kc = KeycloakAPI(auth_keycloak_url=self.keycloak_url,
                 auth_client_id=self.keycloak_auth_client_id,
                 auth_username=self.keycloak_auth_user,
                 auth_password=self.keycloak_auth_password,
                 auth_realm=self.keycloak_auth_realm,
                 auth_client_secret=self.keycloak_auth_client_secret,
                 validate_certs=self.validate_certs)
        credentials = kc.get_user_credentials_by_id('07f54653-a138-40a2-8759-81c76299ee35')
        self.assertIsNotNone(credentials)
        self.assertEqual(len(credentials), 1)
        self.assertEqual(credentials[0]['id'], '68f9955e-4755-464e-8971-f25c8334b1d6')

    @mock.patch('requests.post', side_effect=mocked_requests_post)
    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.delete', side_effect=mocked_requests_delete)
    def test_supprimer_credentials_utilisateur_par_ids(self, mocked_requests_post, mocked_requests_get, mocked_requests_delete):
        kc = KeycloakAPI(auth_keycloak_url=self.keycloak_url,
                 auth_client_id=self.keycloak_auth_client_id,
                 auth_username=self.keycloak_auth_user,
                 auth_password=self.keycloak_auth_password,
                 auth_realm=self.keycloak_auth_realm,
                 auth_client_secret=self.keycloak_auth_client_secret,
                 validate_certs=self.validate_certs)
        reponse = kc.delete_user_credentials_by_id('07f54653-a138-40a2-8759-81c76299ee35', '68f9955e-4755-464e-8971-f25c8334b1d6')
        self.assertTrue(reponse)


class KeycloakIsDictEqualsTestCase(TestCase):
    dict1 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='test1',
            test2='test2'
            ),
        test3 = ['test1',dict(test='test1',test2='test2')]         
        )
    dict2 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='test1',
            test2='test2',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test2'),'test3'],
        test4 = 'test4'         
        )
    dict3 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='test1',
            test2='test23',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test23'),'test3'],
        test4 = 'test4'         
        )

    dict5 = dict(
        test1 = 'test1',
        test2 = dict(
            test1=True,
            test2='test23',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test23'),'test3'],
        test4 = 'test4'         
        )

    dict6 = dict(
        test1 = 'test1',
        test2 = dict(
            test1='true',
            test2='test23',
            test3='test3'
            ),
        test3 = ['test1',dict(test='test1',test2='test23'),'test3'],
        test4 = 'test4'         
        )
    dict7 = [{'roles': ['view-clients', 'view-identity-providers', 'view-users', 'query-realms', 'manage-users'], 'clientid': 'master-realm'}, {'roles': ['manage-account', 'view-profile', 'manage-account-links'], 'clientid': 'account'}]
    dict8 = [{'roles': ['view-clients', 'query-realms', 'view-users'], 'clientid': 'master-realm'}, {'roles': ['manage-account-links', 'view-profile', 'manage-account'], 'clientid': 'account'}]
    dict9 = {"accents":"Écrevisse"}
    dict10 = {"accents": 'Ecrevisse'}
    dict11 = {"accents": ["Écrevisse"]}

    def test_utf8(self):
        self.assertTrue(isDictEquals(self.dict9, self.dict9))
        self.assertFalse(isDictEquals(self.dict9, self.dict10))
        self.assertTrue(isDictEquals(self.dict11, self.dict11))
        self.assertFalse(isDictEquals(self.dict9, self.dict11))

    def test_trivial(self):
        self.assertTrue(isDictEquals(self.dict1,self.dict1))

    def test_equals_with_dict2_bigger_than_dict1(self):
        self.assertTrue(isDictEquals(self.dict1,self.dict2))

    def test_not_equals_with_dict2_bigger_than_dict1(self):
        self.assertFalse(isDictEquals(self.dict2,self.dict1))

    def test_not_equals_with_dict1_different_than_dict3(self):
        self.assertFalse(isDictEquals(self.dict1,self.dict3))

    def test_equals_with_dict5_contain_bool_and_dict6_contain_true_string(self):
        self.assertFalse(isDictEquals(self.dict5,self.dict6))
        self.assertFalse(isDictEquals(self.dict6,self.dict5))

    def test_not_equals_dict7_dict8_compare_dict7_with_list_bigger_than_dict8_but_reverse_equals(self):
        self.assertFalse(isDictEquals(self.dict7,self.dict8))
        self.assertTrue(isDictEquals(self.dict8,self.dict7))
        
class KeycloakRemoveNoneValuesFromDictTest(TestCase):
    test1 = {
        "key1": "value1",
        "key2": None
        }
    expected1 = {
        "key1": "value1"
    }
    test2 = {
        "key1": "value1",
        "list1": [{
            "list1key1": None,
            "list1key2": "list1value2"
            }
        ]
    }
    expected2 = {
        "key1": "value1",
        "list1": [{
            "list1key2": "list1value2"
            }
        ]
    }
    test3 = {
        "key1": "value1",
        "list1": [{
            "list1key1": None,
            "list1key2": "list1value2",
            "list1list1": [{
                "list1list1key1": "list1list1value1",
                "list1list1key2": None
                }]
            },
            "list1value1",
            None
        ],
        "dict1": {
            "dict1key1": "dict1value1",
            "dict1key2": None,
            "dict1dict1": [{
                "dict1dict1key1": None,
                "dict1dict1key2": "dict1dict1Value2"
            }]
        }
    }
    expected3 = {
        "key1": "value1",
        "list1": [{
            "list1key2": "list1value2",
            "list1list1": [{
                "list1list1key1": "list1list1value1"
                }]
            },
            "list1value1",
        ],
        "dict1": {
            "dict1key1": "dict1value1",
            "dict1dict1": [{
                "dict1dict1key2": "dict1dict1Value2"
            }]
        }
    }
    def testSimpleDictWithOneNoneValue(self):
        result1 = remove_arguments_with_value_none(self.test1)
        self.assertDictEqual(result1, self.expected1, str(result1))

    def testDictWithListContainingOneNoneValue(self):
        result2 = remove_arguments_with_value_none(self.test2)
        self.assertDictEqual(result2, self.expected2, str(result2))

    def testDictWithListAndDictThreeLevel(self):
        result3 = remove_arguments_with_value_none(self.test3)
        self.assertDictEqual(result3, self.expected3, str(result3))
    