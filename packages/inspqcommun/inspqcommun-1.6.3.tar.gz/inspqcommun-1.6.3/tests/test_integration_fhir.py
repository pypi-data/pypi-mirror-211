#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase
from datetime import datetime
from inspqcommun.hl7.fhir import LocationFHIR, OperationOutcomeFHIR, OrganizationFHIR, PatientFHIR, BundleFHIR, ImmunizationFHIR, ConditionFHIR, ParameterFHIR
from inspqcommun.identity.keycloak_tools import KeycloakEnvironment
import json
import os
import unittest

class TestIntegrationFHIR(TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName=methodName)

        self.test_patients = [
            {
                "given_name": "James",
                "family_name": "Bond",
                "gender": 'male',
                "birth_date": "2007-10-07",
                "nam": "BONJ07100718",
                "niu": "12312312323",
                "phone_number": "5555678910",
                "deceased_boolean": "false",
                "address_line": "1000, Route de l'Église",
                "address_city": "Québec",
                "address_state": "QC",
                "address_postal_code": "H2C3V9",
                "address_country": "Canada",
                "mother_given_name": "Gretta",
                "mother_family_name": "Thunderbird",
                "father_given_name": "Yvan",
                "father_family_name": "Potvin-Bond"
                },
            {
                "given_name": "Yvan",
                "family_name": "Potvin",
                "gender": 'male',
                "birth_date": "2017-11-08",
                "nam": "POTY17110811",
                "niu": "12314442323",
                "phone_number": "4187331234",
                "deceased_boolean": "false",
                "address_line": "1020, Route de l'Église",
                "address_city": "Québec",
                "address_state": "QC",
                "address_postal_code": "H2C3V9",
                "address_country": "Canada",
                "mother_given_name": "Anita",
                "mother_family_name": "Lamothe",
                "father_given_name": "Hiboué",
                "father_family_name": "Potvin"
                },
            {
                "given_name": "Caroline",
                "family_name": "Tremblay",
                "gender": 'female',
                "birth_date": "1999-09-09",
                "nam": "TREC99590919",
                },
            {
                "id": 8456803
            }

        ]
        self.JAMES_BOND = 0
        self.YVAN_POTVIN = 1
        self.CAROLINE_TREMBLAY = 2
        self.NORMAND_LESSARD = 3

        self.env = os.environ['ENV'] if 'ENV' in os.environ else 'LOCAL'
        self.base_url = os.environ['FA_BASE_URL'] if 'FA_BASE_URL' in os.environ else 'http://localhost:14001'
        self.base_uri = os.environ['FA_BASE_URI'] if 'FA_BASE_URI' in os.environ else '/fa-services'
        self.default_auth_client_id = "faius{0}".format(self.env.lower())
        self.default_auth_realm = 'msss'
        self.default_auth_user = 'sx5talend'
        self.default_auth_password = 'sx5talend'
        self.RESSOURCE_ORG_CISSS_GASPESIE = {
            "resourceType": "Organization",
            "meta": {
                "extension": [
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2018-02-28"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "service-account-rrssautomatisationdev"
                    }
                ],
            },
            "extension": [
                {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                    "valuePeriod": {
                        "start": "2015-12-19T00:00:00-05:00"
                    }
                },
                {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                    "valueString": "3005"
                },
                {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                    "valueString": "11"
                }
            ],
            "identifier": [
                {
                    "system": "https://pro.consultation.rrss.rtss.qc.ca",
                    "value": "urn:msss:rrss:767237"
                }
            ],
            "active": True,
            "name": "11 CISSS DE LA GASPÉSIE",
            "address": [
                {
                    "extension": [
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "12"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2018-02-28"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "service-account-rrssautomatisationdev"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2022-06-01"
                        }
                    ],
                    "use": "work",
                    "type": "physical",
                    "line": [
                        "215",
                        "Boulevard de York Ouest"
                    ],
                    "city": "Gaspé",
                    "state": "Québec",
                    "postalCode": "G4X2W2",
                    "country": "CA",
                    "period": {
                        "start": "2018-09-25T20:00:00-04:00"
                    }
                }
            ],
            "partOf": {
                "reference": "Organization/50"
            },
            "contact": [
                {
                    "purpose": {
                        "coding": [
                            {
                                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                                "version": "1.0.0",
                                "code": "ADMIN",
                                "display": "Administrative"
                            }
                        ]
                    },
                    "telecom": [
                        {
                            "extension": [
                                {
                                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                                    "valueString": "12"
                                },
                                {
                                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                                    "valueString": "ephs.PERMISSIONS"
                                },
                                {
                                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                                    "valueDate": "2018-02-28"
                                },
                                {
                                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                                    "valueString": "service-account-rrssautomatisationdev"
                                },
                                {
                                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                                    "valueDate": "2022-06-01"
                                }
                            ],
                            "system": "phone",
                            "value": "+14183683301",
                            "use": "work"
                        }
                    ],
                    "address": {
                        "extension": [
                            {
                                "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                                "valueString": "12"
                            },
                            {
                                "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                                "valueString": "ephs.PERMISSIONS"
                            },
                            {
                                "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                                "valueDate": "2018-02-28"
                            },
                            {
                                "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                                "valueString": "service-account-rrssautomatisationdev"
                            },
                            {
                                "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                                "valueDate": "2022-06-01"
                            }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": [
                            "215",
                            "Boulevard de York Ouest"
                        ],
                        "city": "Gaspé",
                        "state": "Québec",
                        "postalCode": "G4X2W2",
                        "country": "CA",
                        "period": {
                            "start": "2018-09-25T20:00:00-04:00"
                        }
                    }
                }
            ]
        }
        self.RESSOURCE_LOCATION_HOPITAL_BAIE_ST_PAUL = {
            "resourceType": "Location",
            "meta": {
                "extension": [
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2012-04-10"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "service-account-rrssautomatisationdev"
                    }
                ],
                "profile": [
                    "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqLocation.structuredefinition.xml"
                ]
            },
            "extension": [
                {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#location/numero",
                    "valueString": "1190"
                },
                {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                    "valuePeriod": {
                        "start": "2012-03-19T00:00:00-04:00"
                    }
                }
            ],
            "identifier": [
                {
                    "system": "https://pro.consultation.rrss.rtss.qc.ca",
                    "value": "urn:msss:rrss:1190"
                }
            ],
            "status": "active",
            "name": "03 HOPITAL DE BAIE-ST-PAUL",
            "telecom": [
                {
                    "extension": [
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "3"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2012-04-10"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "service-account-rrssautomatisationdev"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2022-06-08"
                        }
                    ],
                    "system": "phone",
                    "value": "+14184355150",
                    "use": "work"
                }
            ],
            "address": {
                "extension": [
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                        "valueString": "4"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2012-04-10"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "service-account-rrssautomatisationdev"
                    },
                    {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                        "valueDate": "2022-06-08"
                    }
                ],
                "use": "work",
                "type": "physical",
                "line": [
                    "88",
                    "rue Racine"
                ],
                "city": "Baie-Saint-Paul",
                "state": "Québec",
                "postalCode": "G3Z0K3",
                "country": "CA",
                "period": {
                    "start": "2022-06-06T16:46:05-04:00"
                }
            },
            "managingOrganization": {
                "reference": "Organization/16544",
                "display": "03 CIUSSS DE LA CAPITALE-NATIONALE"
            }
        }

    def setUp(self):
        kc = KeycloakEnvironment(
            defaultAuthClientId=self.default_auth_client_id,
            defaultAuthRealm=self.default_auth_realm,
            defaultAuthUser=self.default_auth_user,
            defaultAuthPassword=self.default_auth_password)
        self.auth_headers = kc.authenticateByUsernamePassword()

    def test_etantdonneeyvanpotvinnonexistantdansregistre_quandoncreelusager_onrecoituncode200(self):
        patient = PatientFHIR(
            base_url=self.base_url,
            base_uri=self.base_uri, 
            patient_dict=self.test_patients[self.YVAN_POTVIN],
            token=self.auth_headers)
        response = patient.Create()

        self.assertEqual(response.status_code, 200)

    def test_etantdonneecarolinetremblayquiexistedansleregistre_quandrecherche_usagertrouve(self):
        patient = PatientFHIR(
            base_url=self.base_url,
            base_uri=self.base_uri, 
            patient_dict=self.test_patients[self.CAROLINE_TREMBLAY],
            token=self.auth_headers)
        response = patient.Search()
        self.assertEqual(response.status_code, 200)

        response_bundle = BundleFHIR(resource=json.loads(response.content.decode()))
        patient_found = response_bundle.get_entries(recurse=True, resource_type='Patient')[0]
        self.assertEqual(patient_found.id, '8456902', "Id Caroline Tremblay invalide: {0}".format(patient_found.id))

    def test_etantdonneecarolinetremblayquiexistedansleregistre_quandapparie_usagertrouve(self):
        patient = PatientFHIR(
            base_url=self.base_url,
            base_uri=self.base_uri, 
            patient_dict=self.test_patients[self.CAROLINE_TREMBLAY],
            token=self.auth_headers)
        response = patient.Match()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(patient.id, '8456902', "Id Caroline Tremblay invalide: {0}".format(patient.id))

    def test_etantdonneenormadlessardquiexistedansleregistre_quandobtenirparid_usagerobtenu(self):
        patient = PatientFHIR(
            base_url=self.base_url,
            base_uri=self.base_uri, 
            token=self.auth_headers)
        response = patient.GetById(patient_id=self.test_patients[self.NORMAND_LESSARD]['id'])
        self.assertEqual(response.status_code, 200)
        self.assertEqual(patient.given_name, 'Normand', "Mauvais prénom pour Normand: {0}".format(patient.given_name))
        self.assertEqual(patient.family_name, 'Lessard', "Mauvais nom pour Normand Lessard: {0}".format(patient.family_name))

    def test_rechercher_organisation_par_nom(self):
        org_to_search = '03 CIUSSS DE LA CAPITALE-NATIONALE'
        org_visitor = OrganizationFHIR(
            base_url=self.base_url,
            base_uri=self.base_uri, 
            token_header=self.auth_headers
            )
        resource = org_visitor.search(name=org_to_search)
        self.assertTrue(type(resource) is BundleFHIR, "{0}".format(type(resource)))
        organizations_found = resource.get_entries(recurse=True, resource_type='Organization')
        org_found = False
        for org in organizations_found:
            if org.get_name() == org_to_search:
                org_found = True
                break

        self.assertTrue(
            org_found,
            "Organisation non trouvee"
        )

    def test_rechercher_un_lds_par_nom(self):
        lds_a_rechercher = '03 CENTRE DE JOUR DE DONNACONA'
        lds_visitor = LocationFHIR(
            base_url=self.base_url,
            base_uri = self.base_uri,
            token_header=self.auth_headers)

        resource = lds_visitor.search(name=lds_a_rechercher)

        self.assertTrue(type(resource) is BundleFHIR, "{0}".format(type(resource)))
        locations_found = resource.get_entries(recurse=True, resource_type='Location')
        location_found = False
        for loc in locations_found:
            if loc.get_name() == lds_a_rechercher:
                location_found = True
                break

        self.assertTrue(
            location_found,
            "LDS non trouve"
        )
    
    def test_creer_modifier_et_supprimer_organisation(self):
        org_visitor = OrganizationFHIR(
            base_url=self.base_url,
            base_uri=self.base_uri, 
            token_header=self.auth_headers,
            resource=self.RESSOURCE_ORG_CISSS_GASPESIE
            )
        response = org_visitor.create()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(org_visitor.get_id(), "Le id de l'organisation créé n'est pas défini")
        nouveau_nom = "Nouveau nom"
        org_visitor.set_name(name=nouveau_nom)
        response = org_visitor.update()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(org_visitor.get_name(),nouveau_nom,"L'organisation n'a pas le bon nom: {0} != {1}".format(org_visitor.get_name(), nouveau_nom))
        response = org_visitor.delete()
        self.assertEqual(response.status_code, 405)

    def test_creer_modifier_et_supprimer_lds(self):
        loc_visitor = LocationFHIR(
            base_url=self.base_url,
            base_uri=self.base_uri, 
            token_header=self.auth_headers,
            resource=self.RESSOURCE_LOCATION_HOPITAL_BAIE_ST_PAUL
            )
        response = loc_visitor.create()
        self.assertEqual(response.status_code, 201)
        self.assertIsNotNone(loc_visitor.get_id(), "Le id du LDS créé n'est pas défini")
        nouveau_nom = "Nouveau nom"
        loc_visitor.set_name(name=nouveau_nom)
        response = loc_visitor.update()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(loc_visitor.get_name(),nouveau_nom,"Le LDS n'a pas le bon nom: {0} != {1}".format(loc_visitor.get_name(), nouveau_nom))
        response = loc_visitor.delete()
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()