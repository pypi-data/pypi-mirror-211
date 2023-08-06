#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase
from datetime import datetime
from inspqcommun.identity.keycloak_tools import KeycloakEnvironment, KeycloakAPI
import socket
import json
import os
import unittest

class TestIntegrationKeycloak(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

        self.env = os.environ['ENV'] if 'ENV' in os.environ else 'LOCAL'
        self.default_auth_client_id = "faius{0}".format(self.env.lower())
        self.default_auth_realm = 'msss'
        self.default_auth_user = 'sx5talend'
        self.default_auth_password = 'sx5talend'
        self.default_keycloak_url = "{protocol}://{host}:{port}/auth".format(
                protocol="http",
                host=socket.getfqdn(),
                port="18081")

    def setUp(self):
        self.kc = KeycloakEnvironment(
            defaultAuthClientId=self.default_auth_client_id,
            defaultAuthRealm=self.default_auth_realm,
            defaultAuthUser=self.default_auth_user,
            defaultAuthPassword=self.default_auth_password)
        
        self.api = KeycloakAPI(auth_keycloak_url=self.default_keycloak_url,
            auth_realm=self.default_auth_realm,
            auth_client_id=self.default_auth_client_id,
            auth_client_secret=self.kc.get_client_secret(client_id=self.default_auth_client_id, realm=self.default_auth_realm),
            auth_username=self.default_auth_user,
            auth_password=self.default_auth_password
        )

    def test_authenticate_by_username_password(self):
        auth_headers = self.kc.authenticateByUsernamePassword()
        self.assertIn(member="Authorization", container=auth_headers)

    def test_authenticate_by_service_account(self):
        auth_headers = self.kc.authenticateByServiceAccount()
        self.assertIn(member="Authorization", container=auth_headers)

    def test_get_token_url(self):
        token_url = self.kc.get_token_url()
        self.assertIsNotNone(token_url)
        self.assertIn(member="/token", container=token_url)

    def test_get_client_secret(self):
        client = self.kc.keycloak_auth_client_id
        realm = self.kc.keycloak_auth_realm
        client_secret = self.kc.get_client_secret(client_id=client, realm=realm)
        self.assertIsNotNone(client_secret)

    def test_obtenir_utilisateurs(self):
        users = self.api.get_users(self.default_auth_realm)
        self.assertIsNotNone(users)
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0]['id'], 'bf43845c-2de1-49c4-9791-274451fc3b8c')

    def test_obtenir_utilisateur_par_id(self):
        user = self.api.get_user_by_id('bf43845c-2de1-49c4-9791-274451fc3b8c', self.default_auth_realm)
        self.assertIsNotNone(user)
        self.assertEqual(user['id'], 'bf43845c-2de1-49c4-9791-274451fc3b8c')

    def test_obtenir_credentiels_utilisateur_par_id(self):
        credentials = self.api.get_user_credentials_by_id('bf43845c-2de1-49c4-9791-274451fc3b8c', self.default_auth_realm)
        self.assertIsNotNone(credentials)
        self.assertEqual(len(credentials), 1)
        self.assertEqual(credentials[0]["id"], '3bd5f3d9-8914-4aa5-b287-6f27005d83ea')

    def test_retirer_credentiels_utilisateur_par_ids(self):
        resultat = self.api.delete_user_credentials_by_id('6f61ee70-2972-477b-a028-9c931525e638', 'd17b9491-f989-4754-963d-c6519cc9d023', self.default_auth_realm)
        self.assertTrue(resultat)
        credentials = self.api.get_user_credentials_by_id('6f61ee70-2972-477b-a028-9c931525e638', self.default_auth_realm)
        self.assertEqual(len(credentials), 0)
        

    def test_get_client_faiuslocal(self):
        client = self.kc.kc.get_client_by_clientid(client_id="faiuslocal", realm="msss")
        self.assertEqual(client["clientId"], "faiuslocal")

if __name__ == '__main__':
    unittest.main()