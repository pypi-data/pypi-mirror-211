#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase, mock
from inspqcommun.userprovisioning.scim import SCIMClient, User
from tests.mock_scim_server import mocked_scim_requests_get, mocked_scim_requests_put, mocked_scim_requests_post, mocked_scim_requests_delete

import json

class SCIMTestCase(TestCase):
    testUser = {
        "schemas":[
            "urn:ietf:params:scim:schemas:core:2.0:User",
            "urn:sadupanorama:scim:api:messages:2.0:AppartenancesOrganisationnelles"
            ],
        "id":"pefl1800@santepublique.rtss.qc.ca",
        "externalId":None,
        "meta":{
            "resourceType":None,
            "created":"2020-02-24T05:00:00.000+0000",
            "lastModified":None,
            "location":"http://inspq-6673.inspq.qc.ca:14103/scim/v2/Users/pefl1800@santepublique.rtss.qc.ca",
            "version":None
            },
        "userName":"pefl1800@santepublique.rtss.qc.ca",
        "name":{
            "formatted":None,
            "familyName":"Petit",
            "givenName":"Florence",
            "middleName":None,
            "honorificPrefix":None,
            "honorificSuffix":None
            },
        "displayName":None,
        "nickName":None,
        "profileUrl":None,
        "title":None,
        "userType":None,
        "preferredLanguage":None,
        "locale":None,
        "timezone":None,
        "active":None,
        "password":None,
        "emails":[
            {
                "value":"florence.petit@inspq.qc.ca",
                "display":None,
                "type":None,
                "primary":None
                }
            ],
        "phoneNumbers":[
            {
                "value":"4186543020",
                "display":None,
                "type":None,
                "primary":None
                }
            ],
        "ims":[
            {
                "value":"icqelfdasjf",
                "display":"icq adsa as",
                "type":"icq",
                "primary":None
                }
            ],
        "photos":[
            {
                "value":"http://flikr.com/maphoto",
                "display":"MaPhoto",
                "type":"photo",
                "primary":None
                }
            ],
        "addresses":[
            {
                "value":"icqelfdasjf",
                "display":"icq adsa as",
                "type":"icq",
                "primary":None
                }
            ],
        "groups":[
            {
                "value":"PanoramaLOCAL",
                "display":"Panorama LOCAL",
                "type":None,
                "$ref":None
                },
            {
                "value":"GUSPPilote",
                "display":"Pilotage GUSP",
                "type":None,
                "$ref":None
                },
            {
                "value":"PanoramaTESTINT",
                "display":"Panorama TESTINT",
                "type":None,
                "$ref":None
                },
            {
                "value":"IUS",
                "display":"IUS",
                "type":None,
                "$ref":None
                },
            {
                "value":"PEFIDev3",
                "display":"PEFI Dev3",
                "type":None,
                "$ref":None
                }
            ],
        "entitlements":[
            "MD",
            "INF"
            ],
        "roles":[
            {
                "value":"Accès Accueil",
                "display":None,
                "type":None,
                "primary":None
                },
            {
                "value":"acces-panorama",
                "display":None,
                "type":None,
                "primary":None
                }
            ],
        "x509Certificates":None,
        "urn:sadupanorama:scim:api:messages:2.0:AppartenancesOrganisationnelles":{
            "appartenancesOrganisationnelles":[
                {
                    "organisation":"MSSS",
                    "lieuxDispensationServices":[
                        "MSSS - QUEBEC"
                        ],
                    "roles":[
                        {
                            "nom":"Accès Accueil",
                            "rolePrefere":True
                            }
                        ],
                    "courriel":"florence.petit@inspq.qc.ca",
                    "numeroTelephone":"4186543020"
                    }
                ]
            }
        }
    testUsers = [
        {
            "id": "test01",
            "externalId": "asdasdasds",
            "userName": "test01",
            "name": {
                "familyName":"Test1",
                "givenName":"Test1",
                "middleName":None
                },
            "roles":[
                {
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ]
            },
        {
            "id": "test02",
            "externalId": "asddfggdasds",
            "userName": "test02",
            "name": {
                "familyName":"Test2",
                "givenName":"Test2",
                "middleName":None
                },
            "roles":[
                {
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ]
            },
        {
            "id": "test03",
            "externalId": "asdfafwegg",
            "userName": "test03",
            "name": {
                "familyName":"Test3",
                "givenName":"Test3",
                "middleName":None
                },
            "roles":[
                {
                    "display":"FA-SAISIE",
                    "type":None,
                    "primary":None
                }
            ]
            }
        
        ]
    config = {
        "scim_server_url": "http://scim.server.url/scim/v2",
        "access_token": "eyasdasfasd"
        }
    
    def testTousLesChampsSontAccessibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        self.assertEqual(utilisateurSCIM.id, self.testUser["id"], "id {} n'est pas {}".format(utilisateurSCIM.id, self.testUser["id"]))
        self.assertEqual(utilisateurSCIM.externalId, self.testUser["externalId"], "externalId {} n'est pas {}".format(utilisateurSCIM.externalId, self.testUser["externalId"]))
        self.assertEqual(utilisateurSCIM.userName, self.testUser["userName"], "userName {} n'est pas {}".format(utilisateurSCIM.userName, self.testUser["userName"]))
        self.assertEqual(utilisateurSCIM.displayName, self.testUser["displayName"], "displayName {} n'est pas {}".format(utilisateurSCIM.displayName, self.testUser["displayName"]))
        self.assertEqual(utilisateurSCIM.nickName, self.testUser["nickName"], "nickName {} n'est pas {}".format(utilisateurSCIM.nickName, self.testUser["nickName"]))
        self.assertEqual(utilisateurSCIM.profileUrl, self.testUser["profileUrl"], "profileUrl {} n'est pas {}".format(utilisateurSCIM.profileUrl, self.testUser["profileUrl"]))
        self.assertEqual(utilisateurSCIM.title, self.testUser["title"], "title {} n'est pas {}".format(utilisateurSCIM.title, self.testUser["title"]))
        self.assertEqual(utilisateurSCIM.userType, self.testUser["userType"], "userType {} n'est pas {}".format(utilisateurSCIM.userType, self.testUser["userType"]))
        self.assertEqual(utilisateurSCIM.preferredLanguage, self.testUser["preferredLanguage"], "preferredLanguage {} n'est pas {}".format(utilisateurSCIM.preferredLanguage, self.testUser["preferredLanguage"]))
        self.assertEqual(utilisateurSCIM.locale, self.testUser["locale"], "locale {} n'est pas {}".format(utilisateurSCIM.locale, self.testUser["locale"]))
        self.assertEqual(utilisateurSCIM.timezone, self.testUser["timezone"], "timezone {} n'est pas {}".format(utilisateurSCIM.timezone, self.testUser["timezone"]))
        self.assertEqual(utilisateurSCIM.active, self.testUser["active"], "active {} n'est pas {}".format(utilisateurSCIM.active, self.testUser["active"]))
        self.assertEqual(utilisateurSCIM.password, self.testUser["password"], "password {} n'est pas {}".format(utilisateurSCIM.password, self.testUser["password"]))
        self.assertEqual(utilisateurSCIM.x509Certificates, self.testUser["x509Certificates"], "x509Certificates {} n'est pas {}".format(utilisateurSCIM.x509Certificates, self.testUser["x509Certificates"]))

    def testTousLesSchemasSonDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        self.assertTrue(utilisateurSCIM.schemas.sort() == self.testUser["schemas"].sort(), "Les schemas {} n'est pas dans la liste: {}".format(utilisateurSCIM.schemas, str(self.testUser["schemas"])))

    def testTousLesMetaSonDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        self.assertTrue(utilisateurSCIM.meta == self.testUser["meta"], "Les meta {} ne sont pas complètes: {}".format(utilisateurSCIM.meta, str(self.testUser["meta"])))

    def testTousLesNameSonDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        self.assertTrue(utilisateurSCIM.name == self.testUser["name"], "Les name {} ne sont pas complètes: {}".format(utilisateurSCIM.name, str(self.testUser["name"])))

    def testTousLesRolesSontDisponibles(self):  
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        if self.testUser["roles"] is not None and utilisateurSCIM.roles is not None:
            tousLesRolesSontDansLaListe = True
            for role in self.testUser["roles"]:
                scimRole = next((item for item in utilisateurSCIM.roles if item["value"] == role["value"]), {})
                if scimRole != role:
                    tousLesRolesSontDansLaListe = False
            self.assertTrue(tousLesRolesSontDansLaListe, "Role {} non trouvée.".format(role))
        else:
            self.assertEqual(self.testUser["roles"], utilisateurSCIM.roles, "roles {} différent de {}".format(str(self.testUser["roles"]),str(utilisateurSCIM.roles)))

    def testTousLesEmailsSontDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        if self.testUser["emails"] is not None and utilisateurSCIM.emails is not None:
            tousLesEmailsSontDansLaListe = True
            for email in self.testUser["emails"]:
                scimEmail = next((item for item in utilisateurSCIM.emails if item["value"] == email["value"]), {})
                if scimEmail != email:
                    tousLesEmailsSontDansLaListe = False
            self.assertTrue(tousLesEmailsSontDansLaListe, "EMail {} non trouvée.".format(email))
        else:
            self.assertEqual(self.testUser["emails"], utilisateurSCIM.emails, "emails {} différent de {}".format(str(self.testUser["emails"]),str(utilisateurSCIM.emails)))

    def testTousLesPhoneNumbersSontDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        if self.testUser["phoneNumbers"] is not None and utilisateurSCIM.phoneNumbers is not None:
            tousLesPhoneNumbersSontDansLaListe = True
            for phoneNumbers in self.testUser["phoneNumbers"]:
                scimPhoneNumbers = next((item for item in utilisateurSCIM.phoneNumbers if item["value"] == phoneNumbers["value"]), {})
                if scimPhoneNumbers != phoneNumbers:
                    tousLesPhoneNumbersSontDansLaListe = False
            self.assertTrue(tousLesPhoneNumbersSontDansLaListe, "PhoneNumber {} non trouvée.".format(phoneNumbers))
        else:
            self.assertEqual(self.testUser["phoneNumbers"], utilisateurSCIM.phoneNumbers, "phoneNumbers {} différent de {}".format(str(self.testUser["phoneNumbers"]),str(utilisateurSCIM.phoneNumbers)))

    def testTousLesImsSontDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        tousLesImsSontDansLaListe = True
        if self.testUser["ims"] is not None and utilisateurSCIM.ims is not None:
            for ims in self.testUser["ims"]:
                scimIms = next((item for item in utilisateurSCIM.ims if item["value"] == ims["value"]), {})
                if scimIms != ims:
                    tousLesImsSontDansLaListe = False
            self.assertTrue(tousLesImsSontDansLaListe, "Ims {} non trouvée.".format(ims))
        else:
            self.assertEqual(self.testUser["ims"], utilisateurSCIM.ims, "Ims {} différent de {}".format(str(self.testUser["ims"]),str(utilisateurSCIM.ims)))

    def testTousLesPhotosSontDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        tousLesPhotosSontDansLaListe = True
        if self.testUser["photos"] is not None and utilisateurSCIM.photos is not None:
            for photos in self.testUser["photos"]:
                scimphotos = next((item for item in utilisateurSCIM.photos if item["value"] == photos["value"]), {})
                if scimphotos != photos:
                    tousLesPhotosSontDansLaListe = False
            self.assertTrue(tousLesPhotosSontDansLaListe, "Photos {} non trouvée.".format(photos))
        else:
            self.assertEqual(self.testUser["photos"], utilisateurSCIM.photos, "Photos {} différent de {}".format(str(self.testUser["photos"]),str(utilisateurSCIM.photos)))

    def testTousLesAddressesSontDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        tousLesAddressesSontDansLaListe = True
        if self.testUser["addresses"] is not None and utilisateurSCIM.addresses is not None:
            for addresses in self.testUser["addresses"]:
                scimaddresses = next((item for item in utilisateurSCIM.addresses if item["value"] == addresses["value"]), {})
                if scimaddresses != addresses:
                    tousLesAddressesSontDansLaListe = False
            self.assertTrue(tousLesAddressesSontDansLaListe, "addresses {} non trouvée.".format(addresses))
        else:
            self.assertEqual(self.testUser["addresses"], utilisateurSCIM.addresses, "Addresses {} différent de {}".format(str(self.testUser["addresses"]),str(utilisateurSCIM.addresses)))

    def testTousLesGroupsSontDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        tousLesGroupsSontDansLaListe = True
        if self.testUser["groups"] is not None and utilisateurSCIM.groups is not None:
            for groups in self.testUser["groups"]:
                scimgroups = next((item for item in utilisateurSCIM.groups if item["value"] == groups["value"]), {})
                if scimgroups != groups:
                    tousLesGroupsSontDansLaListe = False
            self.assertTrue(tousLesGroupsSontDansLaListe, "groups {} non trouvée.".format(groups))
        else:
            self.assertEqual(self.testUser["groups"], utilisateurSCIM.groups, "groups {} différent de {}".format(str(self.testUser["groups"]),str(utilisateurSCIM.groups)))

    def testTousLesEntitlementsSonDisponibles(self):
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        self.assertTrue(utilisateurSCIM.entitlements.sort() == self.testUser["entitlements"].sort(), "Les entitlements {} ne sont pas dans la liste: {}".format(utilisateurSCIM.entitlements, str(self.testUser["entitlements"])))

    def testExtensionsTousLesAppartenanceOrganisationnellesSontDisponibles(self):    
        utilisateurSCIM = User.from_json(json.dumps(self.testUser))
        if self.testUser["urn:sadupanorama:scim:api:messages:2.0:AppartenancesOrganisationnelles"] is not None:
            for appOrg in utilisateurSCIM.appartenancesOrganisationnelles:
                orgTrouve = False
                for testAppOrg in self.testUser["urn:sadupanorama:scim:api:messages:2.0:AppartenancesOrganisationnelles"]["appartenancesOrganisationnelles"]:
                    if appOrg["organisation"] == testAppOrg["organisation"] and appOrg["courriel"] == testAppOrg["courriel"] and appOrg["courriel"] == testAppOrg["courriel"]:
                        orgTrouve = True
                        for role in testAppOrg["roles"]:
                            scimRole = next((item for item in appOrg["roles"] if item["nom"] == role["nom"]), {})
                            if scimRole != role:
                                orgTrouve = False
                        if testAppOrg["lieuxDispensationServices"].sort() != appOrg["lieuxDispensationServices"].sort():
                            orgTrouve = False
                self.assertTrue(orgTrouve, "Appartenance organisationnelle pour {} non trouvée.".format(testAppOrg["organisation"]))

        utilisateur_json = json.loads(utilisateurSCIM.to_json())
        self.assertTrue('urn:sadupanorama:scim:api:messages:2.0:AppartenancesOrganisationnelles' in utilisateur_json.keys())
        self.assertEqual(
            utilisateur_json['urn:sadupanorama:scim:api:messages:2.0:AppartenancesOrganisationnelles'],
            self.testUser["urn:sadupanorama:scim:api:messages:2.0:AppartenancesOrganisationnelles"])
        self.assertFalse('appartenancesOrganisationnelles' in utilisateur_json.keys())

    @mock.patch('inspqcommun.userprovisioning.scim.requests.get', side_effect=mocked_scim_requests_get)
    def testObtenirMonUtilisateurSCIM(self, mock_post):
        testUser = self.testUsers[0].copy()
        authentification_gusp = {}
        authentification_gusp["iv-user"] = testUser["userName"]
        scimClient = SCIMClient(base_url=self.config["scim_server_url"], additionnal_headers=authentification_gusp)
        scimUser = scimClient.getMe()
        self.assertEqual(testUser["userName"], scimUser.userName, "Mon utilisateur n'est pas le bon: {}".format(scimUser.userName))

    @mock.patch('inspqcommun.userprovisioning.scim.requests.get', side_effect=mocked_scim_requests_get)
    def testObtenirUnUtilisateurSCIMparId(self, mock_post):
        testUser = self.testUsers[0].copy()
        scimClient = SCIMClient(base_url=self.config["scim_server_url"], access_token=self.config["access_token"])
        scimUser = scimClient.getUserById(testUser["id"])
        self.assertEqual(testUser["id"], scimUser.id, "L'utilisateur obtenu par id n'est pas le bon: {}".format(scimUser.id))

    @mock.patch('inspqcommun.userprovisioning.scim.requests.post', side_effect=mocked_scim_requests_post)
    def testCreerNouvelUtilisateurSCIM(self, mock_post):
        testUser = self.testUsers[2].copy()
        scimClient = SCIMClient(base_url=self.config["scim_server_url"], access_token=self.config["access_token"])
        scimUser = User.from_json(json.dumps(testUser))
        user = scimClient.createUser(scimUser)
        self.assertDictContainsSubset(testUser, json.loads(scimUser.to_json()), "L'utilisateur créé n'est pas valide: {}".format(user.to_json()))
        
    @mock.patch('inspqcommun.userprovisioning.scim.requests.post', side_effect=mocked_scim_requests_post)
    def testRechercherUnUtilisateurSCIM(self, mock_post):
        testUser = self.testUsers[0].copy()
        scimClient = SCIMClient(base_url=self.config["scim_server_url"], access_token=self.config["access_token"])
        scimUser = scimClient.searchUserByUserName(testUser["userName"])
        self.assertEqual(testUser["userName"], scimUser.userName, "L'utilisateur recherché n'est pas le bon: {}".format(scimUser.userName))

    @mock.patch('inspqcommun.userprovisioning.scim.requests.put', side_effect=mocked_scim_requests_put)
    def testModifierUnUtilisateurSCIM(self, mock_put):
        testUser = self.testUsers[1].copy()
        testUser["displayName"] = "Test 02"
        scimUser = User.from_json(json.dumps(testUser))
        scimClient = SCIMClient(base_url=self.config["scim_server_url"], access_token=self.config["access_token"])
        user = scimClient.updateUser(scimUser)
        self.assertDictContainsSubset(testUser, json.loads(scimUser.to_json()), "L'utilisateur créé n'est pas valide: {}".format(scimUser.to_json()))

    @mock.patch('inspqcommun.userprovisioning.scim.requests.delete', side_effect=mocked_scim_requests_delete)
    def testSupprimerUnUtilisateurSCIM(self, mock_delete):
        testUser = self.testUsers[0].copy()
        scimClient = SCIMClient(base_url=self.config["scim_server_url"], access_token=self.config["access_token"])
        scimUser = User.from_json(json.dumps(testUser))
        response = scimClient.deleteUser(scimUser)
        self.assertEqual(response.status_code, 204, "Le status de la suppression n'est pas 204: {}".format(response.status_code))
                
        