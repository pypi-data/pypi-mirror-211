#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sre_parse import expand_template
from unittest import TestCase, mock
from datetime import date, datetime
from fhirclient.models import organization
from requests.sessions import session
from inspqcommun.hl7.fhir import LocationFHIR, OperationOutcomeFHIR, OrganizationFHIR, ParameterFHIR, PatientFHIR, BundleFHIR, ImmunizationFHIR, ConditionFHIR, MedicationFHIR, PractitionerFHIR, ValueSetFHIR
from tests.mock_fhir_server import mocked_fhir_requests_post, mocked_fhir_requests_get, mocked_get_medication_by_tradename, mocked_search_practitioner, mocked_get_value_set, mocked_get_organization_by_url
from fhirclient.models.organization import Organization
from fhirclient.models.medication import Medication, MedicationProductBatch
from fhirclient.models.quantity import Quantity
from fhirclient.models.practitioner import Practitioner
from fhirclient.models.fhirreference import FHIRReference

import json
import copy
import os

bundle_operation_outcome_business_rule = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": [
        {
            "resource": {
                "resourceType": "OperationOutcome",
                "issue": [
                    {
                        "severity": "error",
                        "code": "business-rule",
                        "details": {
                            "coding": [
                                {
                                    "code": "412",
                                    "display": "L'Usager n'a pas fourni les bonnes informations sur sa vaccination"
                                }
                            ]
                        }
                    }
                ]
            },
            "response": {
                "status": "412"
            }
        }
    ]
}
empty_bundle = {
    "resourceType": "Bundle",
    "type": "collection",
    "entry": []
}

bundle_example = {
  "resourceType": "Bundle",
  "entry": [
    {
      "resource": {
        "resourceType": "Patient",
        "id": "10456258",
        "meta": {
          "extension": [
            {
              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
              "valueString": "chpi1800@santepublique.rtss.qc.ca"
            },
            {
              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
              "valueString": "SERVICE2"
            },
            {
              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
              "valueDate": "2021-04-19"
            }
          ],
          "versionId": "1",
          "lastUpdated": "2021-04-20T18:13:37.000-04:00",
          "profile": [
            "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqPatient.structuredefinition.xml"
          ]
        },
        "extension": [
          {
            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#patient/matchramq",
            "valueBoolean": False
          }
        ],
        "identifier": [
          {
            "extension": [
              {
                "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#patient/healthcardorigin",
                "valueCodeableConcept": {
                  "coding": [
                    {
                      "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                      "version": "1.0.0",
                      "code": "QC",
                      "display": "Carte assurance maladie du Québec"
                    }
                  ]
                }
              }
            ],
            "type": {
              "coding": [
                {
                  "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                  "version": "1.0.0",
                  "code": "NAM",
                  "display": "Numéro d'assurance maladie"
                }
              ]
            },
            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary/identifierType?code=NAM",
            "value": "MAUG36121215"
          }
        ],
        "active": True,
        "name": [{ "family": ["Mauve"], "given": ["Guy"] }],
        "telecom": [{ "system": "phone", "value": "+14389218338" }],
        "gender": "female",
        "birthDate": "1936-12-12",
        "deceasedBoolean": False,
        "address": [
          {
            "line": ["3954 de bullion"],
            "city": "Lévis",
            "state": "Québec",
            "postalCode": "h2w2e4",
            "country": "Canada"
          }
        ]
      }
    },
    {
      "resource": {
        "resourceType": "Bundle",
        "meta": {
          "profile": [
            "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/ImmunizationBundle"
          ]
        },
        "type": "collection",
        "entry": [
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83683832",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "agja9320@dev.psc.secursante"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "agja9320@dev.psc.secursante"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T13:49:26.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 1 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T13:49:26.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684833",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:03:11.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 2 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:03:11.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684834",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:03:23.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 3 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:03:23.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684835",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:04:15.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 4 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:04:15.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684836",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:04:30.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 5 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:04:30.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684837",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:04:41.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 6 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:04:41.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684838",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:04:51.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 7 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:04:51.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684839",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:10:06.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 8 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:10:06.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684840",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:10:23.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 9 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:10:23.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684841",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:10:50.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 10 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:10:50.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684842",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:13:15.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 11 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:13:15.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684843",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:13:29.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 12 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:13:29.000-04:00"
            }
          },
          {
            "resource": {
              "resourceType": "Immunization",
              "id": "83684844",
              "meta": {
                "extension": [
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                    "valueDate": "2021-04-20"
                  },
                  {
                    "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                    "valueString": "coma1800@santepublique.rtss.qc.ca"
                  }
                ],
                "versionId": "1",
                "lastUpdated": "2021-04-20T18:13:38.000-04:00",
                "profile": [
                  "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqImmunization.structuredefinition.xml"
                ]
              },
              "contained": [
                {
                  "resourceType": "Organization",
                  "id": "12241",
                  "meta": {
                    "extension": [
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                        "valueString": "ephs.PERMISSIONS"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                        "valueDate": "2015-03-10"
                      },
                      {
                        "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                        "valueString": "ephs.SERVICE2"
                      }
                    ]
                  },
                  "extension": [
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
                      "valuePeriod": { "start": "2015-03-10T00:00:00-04:00" }
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
                      "valueString": "66023"
                    },
                    {
                      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
                      "valueString": "06"
                    }
                  ],
                  "active": True,
                  "name": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
                  "address": [
                    {
                      "id": "37650",
                      "extension": [
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                          "valueString": "1"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                          "valueString": "ephs.PERMISSIONS"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                          "valueDate": "2015-03-10"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                          "valueString": "ephs.SERVICE2"
                        },
                        {
                          "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                          "valueDate": "2018-02-28"
                        }
                      ],
                      "use": "work",
                      "type": "physical",
                      "line": ["3745", "boulevard Saint-Laurent"],
                      "city": "Montréal",
                      "state": "Québec",
                      "country": "CA",
                      "period": { "start": "2015-03-10T00:00:00-04:00" }
                    }
                  ],
                  "partOf": { "reference": "Organization/13" },
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
                          "id": "42171",
                          "extension": [
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                              "valueString": "1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                              "valueString": "ephs.PERMISSIONS"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                              "valueDate": "2015-03-10"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                              "valueString": "ephs.SERVICE1"
                            },
                            {
                              "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                              "valueDate": "2015-03-10"
                            }
                          ],
                          "system": "phone",
                          "value": "+15148436697",
                          "use": "work"
                        }
                      ],
                      "address": {
                        "id": "35440",
                        "extension": [
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "1"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "ephs.PERMISSIONS"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2015-03-10"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "ephs.SERVICE2"
                          },
                          {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2018-02-28"
                          }
                        ],
                        "use": "work",
                        "type": "physical",
                        "line": ["3745", "boulevard Saint-Laurent"],
                        "city": "Montréal",
                        "state": "Québec",
                        "country": "CA",
                        "period": { "start": "2015-03-10T00:00:00-04:00" }
                      }
                    }
                  ]
                }
              ],
              "extension": [
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus",
                  "valueCodeableConcept": {
                    "coding": [
                      {
                        "id": "1324422",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "FV",
                        "display": "Valide"
                      }
                    ]
                  }
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid",
                  "valueString": "5467"
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus",
                  "extension": [
                    {
                      "url": "antigen",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324777",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "840536004",
                            "display": "SRAS-CoV-2"
                          }
                        ]
                      }
                    },
                    { "url": "doseNumber", "valueInteger": 13 },
                    {
                      "url": "status",
                      "valueCodeableConcept": {
                        "coding": [
                          {
                            "id": "1324422",
                            "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                            "version": "1.0.0",
                            "code": "FV",
                            "display": "Valide"
                          }
                        ]
                      }
                    }
                  ]
                },
                {
                  "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename",
                  "valueString": "MOD COVID-19"
                }
              ],
              "status": "completed",
              "date": "2021-04-19T00:00:00-04:00",
              "vaccineCode": {
                "coding": [
                  {
                    "id": "1324776",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "QCSNOMED00124",
                    "display": "COVID-19"
                  }
                ]
              },
              "patient": { "reference": "10456258" },
              "reported": False,
              "performer": { "reference": "172645", "display": "Ragy Chouha" },
              "location": {
                "reference": "12570",
                "display": "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
              },
              "lotNumber": "3001652",
              "expirationDate": "2021-10-06",
              "site": {
                "coding": [
                  {
                    "id": "433254",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "LLFA",
                    "display": "Bras Gauche"
                  }
                ]
              },
              "route": {
                "coding": [
                  {
                    "id": "433437",
                    "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                    "version": "1.0.0",
                    "code": "IM",
                    "display": "Intramusculaire"
                  }
                ]
              },
              "doseQuantity": {
                "value": 0.5,
                "unit": "ml",
                "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                "code": "INV.UnitOfMeasure2"
              },
              "explanation": {
                "reason": [
                  {
                    "coding": [
                      {
                        "id": "1324784",
                        "system": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
                        "version": "1.0.0",
                        "code": "CoV-AUTRES",
                        "display": "06 - COVID-19 - Autres raisons"
                      }
                    ]
                  }
                ]
              }
            },
            "response": {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:13:38.000-04:00"
            }
          }
        ]
      }
    }
  ]
}
condition_test = {
	"resourceType":"Condition",
	"id":"317158",
	"meta":{
		"versionId":"0",
		"profile":["http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqCondition.structuredefinition.xml"]
		},
	"extension":[
		{
			"url":"http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#condition/agent",
			"valueCodeableConcept":{
				"coding":[
					{
						"system":"http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
						"version":"1.0.0",
						"code":"QCSNOMED00124",
						"display":"COVID-19"}
					]
				}
			},
		{
			"url":"http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#condition/antigen",
			"valueCodeableConcept":{
				"coding":[
					{
						"system":"http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
						"version":"1.0.0",
						"code":"'840536004'",
						"display":"SRAS-CoV-2"}
					]
				}
			}
        ],
	"patient":{"reference":"8455472"},
	"code":{
		"coding":[
			{
				"system":"http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
				"version":"1.0.0",
				"code":"54fdb993c540810bb87ee624762744b1401eb5e2615e0834a3948ef19f077b48"}
			]
		},
	"category":{
		"coding":[
			{
				"system":"http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary",
				"version":"1.0.0",
				"code":"contraindicationPrecaution"}
			]
		}
	}

test_location = {
    'resourceType': 'Location',
    'id': '8879',
    'meta': {
        'extension': [
            {
                'url': 'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby',
                'valueString': 'ephs.lormar01'
            },
            {
                'url': 'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate',
                'valueDate': '2015-03-10'
            },
            {
                'url': 'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby',
                'valueString': 'ephs.SERVICE1'
            }
        ],
        'versionId': '1',
        'lastUpdated': '2015-03-10T15:32:50.000-04:00',
        'profile': [
            'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqLocation.structuredefinition.xml'
        ]
    },
    'contained': [
        {
            'resourceType': 'Organization',
            'id': '11463',
            'meta': {
                'extension': [
                    {
                        'url': 'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby',
                        'valueString': 'ephs.ngukel01'
                    },
                    {
                        'url': 'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate',
                        'valueDate': '2015-03-10'
                    },
                    {
                        'url': 'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby',
                        'valueString': 'ephs.SERVICE2'
                    }
                ],
                'versionId': '1',
                'lastUpdated': '2015-03-10T15:32:50.000-04:00',
                'profile': [
                    'http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/profiles/InspqLocation.structuredefinition.xml'
                ]
            },
            'extension': [
                {
                    'url': 'http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period',
                    'valuePeriod': {
                        'start': '2015-03-10T00:00:00-04:00'
                    }
                }
            ],
            'active': True,
            'name': '03 CENTRE RÉADAPTATION DÉFICIENCE INTELLECT. DE QUÉBEC (CENTRE ADMIN)'
        }
    ],
    'extension': [
        {
            'url': 'http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period',
            'valuePeriod': {
                'start': '2015-03-10T00:00:00-04:00'
            }
        }
    ],
    'status': 'active',
    'name': '03 CENTRE DE JOUR DE DONNACONA',
    'managingOrganization': {
        'reference': 'Organization/11463',
        'display': '03 CENTRE RÉADAPTATION DÉFICIENCE INTELLECT. DE QUÉBEC (CENTRE ADMIN)'
    }
}
location_rrss_dict = {
  "resourceType": "Location",
  "id": "1054029",
  "meta": {
    "extension": [
      {
        "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#meta/dateCreation",
        "valueDate": "2021-11-02"
      }
    ],
    "lastUpdated": "2021-11-02T00:00:00.000-04:00"
  },
  "extension": [
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
      "valueCoding": {
        "code": "15",
        "display": "Laurentides"
      }
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
      "valueString": "75017"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#location/numero",
      "valueString": "0"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Adulte"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Personne âgée/aînée"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Accident vasculaire cérébral"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Accidenté de la route"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Amputé"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Arthrite/arthrose"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Brûlé"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Déficience physique"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Paralysie cérébrale"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Perte d'autonomie"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Traumatisme crânien"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Encéphalopathies"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Fatigue chronique"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Fibromyalgie"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Parkinson"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Sclérose en plaques"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Sclérose latérale amyotrophique"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Adaptation sociale"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Aide technique"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Suivi"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Éducation spécialisée"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Ergothérapie"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Infirmier/Infirmière auxiliaire"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Infirmier/Infirmière clinicienne"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Nutrition"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Orthophonie"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Physiothérapie"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Préposé aux bénéficiaires"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Psychologie"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Réadaptation physique"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Sexologie"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Soins infirmiers"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Travail social"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "CR - Centre de réadaptation"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#location/manager",
      "valueHumanName": {
        "family": [
          "Hénault"
        ],
        "given": [
          "Sara"
        ]
      }
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#location/manager",
      "valueHumanName": {
        "family": [
          "Couture"
        ],
        "given": [
          "Anie"
        ]
      }
    },
    {
        "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
        "valuePeriod": {
            "start": "2012-04-27T00:00:00-04:00",
            "end": "3022-01-01T00:00:00-05:00"
        }
    }
  ],
  "identifier": [
    {
      "system": "https://pro.consultation.rrss.rtss.qc.ca",
      "value": "urn:msss:rrss:1054029"
    }
  ],
  "status": "active",
  "name": "15 CENTRE RÉADAPTATION DÉFICIENCE PHYSIQUE ET DE SERV.EXT. POUR LES AÎNÉS D'YOUVILLE",
  "type": {
    "coding": [
      {
        "code": "1601",
        "display": "CR - Centre de réadaptation"
      }
    ]
  },
  "telecom": [
    {
      "system": "phone",
      "value": "+14504322777",
      "use": "work"
    },
    {
      "system": "phone",
      "value": "+14505609898",
      "use": "work"
    }
  ],
  "address": {
    "use": "work",
    "type": "physical",
    "line": [
      "531",
      "Rue Laviolette"
    ],
    "city": "Saint-Jérôme",
    "state": "Québec",
    "postalCode": "J7Y2T8",
    "country": "CA",
    "period": {
      "start": "2021-10-11T20:00:00-04:00"
    }
  },
  "physicalType": {
    "coding": [
      {
        "code": "15",
        "display": "Installations"
      }
    ]
  },
  "managingOrganization": {
    "reference": "767246",
    "display": "CISSS DES LAURENTIDES"
  }
}

organization_rrss_dict = {
  "resourceType": "Organization",
  "id": "852354",
  "meta": {
    "extension": [
      {
        "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#meta/dateCreation",
        "valueDate": "2017-09-21"
      }
    ],
    "lastUpdated": "2017-09-21T00:00:00.000-04:00"
  },
  "extension": [
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/regionAdministrative",
      "valueCoding": {
        "code": "12",
        "display": "Chaudière-Appalaches"
      }
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#address/city-code",
      "valueString": "25213"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#organization/categorie",
      "valueInteger": 14
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#organization/numero",
      "valueString": "224774"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Immunisation"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Médecin désengagé / Hors RAMQ"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Vaccination"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Omnipratique"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Autres cliniques"
    },
    {
      "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/#motscles",
      "valueString": "Clinique médicale"
    },
    {
        "url": "http://www.santepublique.rtss.qc.ca/sipmi/rrss/1.0.0/extensions/period",
        "valuePeriod": {
            "start": "2022-07-01T00:00:00-04:00",
            "end": "3022-07-06T00:00:00-04:00"
        }
    }
  ],
  "identifier": [
    {
      "system": "https://pro.consultation.rrss.rtss.qc.ca",
      "value": "urn:msss:rrss:852354"
    }
  ],
  "active": True,
  "type": {
    "coding": [
      {
        "code": "1807",
        "display": "Autres cliniques"
      }
    ]
  },
  "name": "12 CLINIQUE MÉDICALE PRIVÉE ADMEDICA",
  "telecom": [
    {
      "system": "phone",
      "value": "+14189038899",
      "use": "work"
    }
  ],
  "address": [
    {
      "use": "work",
      "type": "physical",
      "line": [
        "1200",
        "Boulevard Guillaume-Couture"
      ],
      "city": "Lévis",
      "state": "Québec",
      "postalCode": "G6W0R9",
      "country": "CA",
      "period": {
        "start": "2018-09-25T20:00:00-04:00"
      }
    }
  ],
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
                    "id": "14",
                    "extension": [
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/versionid",
                            "valueString": "3"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby",
                            "valueString": "service-account-rrssautomatisationapprovisionnementpanoramalocal"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/creationdate",
                            "valueDate": "2022-04-11"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby",
                            "valueString": "service-account-rrssautomatisationapprovisionnementpanoramalocal"
                        },
                        {
                            "url": "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedate",
                            "valueDate": "2022-04-11"
                        }
                    ],
                    "system": "phone",
                    "value": "+14182850344",
                    "use": "work"
                }
            ]
        }
    ]
}

class FHIRTestCase(TestCase):
    test_patient = {
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
        }
        
    def testSiJeGenereUnUsagerSansParentAdresseNiTelephone_JObtiensUneRessourceFHIRPatientSansParentAddresseNiTelephone(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.nam = self.test_patient['nam']
    
        patient = usager.getFhirResource()
        self.assertEqual(patient['name'][0]['given'][0], 
                         usager.given_name, 
                         "Le given_name {0} n'est pas {1}".format(
                             patient['name'][0]['given'][0], 
                             usager.given_name))
        self.assertEqual(patient['name'][0]['family'][0], 
                         usager.family_name, 
                         "Le family_name {0} n'est pas {1}".format(
                             patient['name'][0]['family'][0], 
                             usager.family_name))
        self.assertEqual(patient['gender'], 
                         usager.gender, 
                         "Le gender {0} n'est pas {1}".format(
                             patient['gender'], 
                             usager.gender))
        self.assertEqual(datetime.strptime(patient['birthDate'], '%Y-%m-%d'), 
                         datetime.strptime(usager.birth_date, '%Y-%m-%d'), 
                         "Le birth_date {0} n'est pas {1}".format(
                             patient['birthDate'], 
                             usager.birth_date))
        nam = list(
            filter(
                lambda identifier: identifier['system'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary/identifierType?code=NAM",
                patient['identifier']))
        self.assertEqual(nam[0]['value'], 
                         usager.nam, 
                         "Le nam {0} n'est pas {1}".format(
                             nam[0]['value'], 
                             usager.nam))
        self.assertFalse(('contact' in patient and len(patient['contact']) == 0),
                        "Le patient ne devrait pas avoir de contact: {}")
        self.assertNotIn('telecom', 
                         patient, 
                         "Le patient ne devrait pas avoir de téléphone: {}".format(
                             str(patient)))
        self.assertNotIn('address', 
                         patient, 
                         "Le patient ne devrait pas avoir d'adresse: {}".format(
                             str(patient)))
    def testCreerPatient_EstActifParDefaut(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.nam = self.test_patient['nam']
    
        patient = usager.getFhirResource()
        self.assertTrue(patient['active'], 
                        "Le patient n'est pas actif par défaut")
        
    def testCreerPatientInactif_JeRecoitParDefautInactif(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.nam = self.test_patient['nam']
        usager.active = False
        patient = usager.getFhirResource()
        self.assertFalse(patient['active'], 
                         "Le patient est actif mais aurait du être inactif")

    def testSiJeGenereUnUsagerAvecNIU_JObtiensUneRessourceFHIRPatientAvecNIU(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.niu = self.test_patient['niu']
        ressource = usager.getFhirResource()
        niu = list(
            filter(
                lambda identifier: identifier['system'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary/identifierType?code=NIUU",
                ressource['identifier']))
        self.assertTrue(len(niu) > 0, "Aucun niu retrouvé dans la ressource")
        self.assertEqual(niu[0]["value"],
                         self.test_patient['niu'], 
                         "Le niu {0} est incorrect. il aurait du être {1}".format(
                             niu[0]["value"],
                             self.test_patient['niu']))

    def testSiJeGenereUnUsagerSansParentsAvecTelephone_JObtiensUneRessourceFHIRPatientSansParentsMaisAvecTelephone(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.nam = self.test_patient['nam']
        usager.phone_number = self.test_patient['phone_number']
    
        patient = usager.getFhirResource()
        self.assertIn('telecom', 
                         patient, 
                         "Le patient devrait avoir un muméro de téléphone: {}".format(
                             str(patient)))
        self.assertEqual(patient['telecom'][0]['value'], 
                         "+1{}".format(usager.phone_number), 
                         "Le numéro de téléphone est {0} mais devrait être {1}".format(
                             patient['telecom'][0]['value'], usager.phone_number))
        
    def testSiJeGenereUnUsagerAvecParents_JObtiensUneRessourceFHIRPatientAvecParents(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.nam = self.test_patient['nam']
        usager.mother_given_name = self.test_patient['mother_given_name']
        usager.mother_family_name = self.test_patient['mother_family_name']
        usager.father_given_name = self.test_patient['father_given_name']
        usager.father_family_name = self.test_patient['father_family_name']
    
        patient = usager.getFhirResource()
        self.assertGreater(len(patient['contact']),
                        0, 
                        "Le patient devrait avoir des contacts: {}".format(
                            str(patient['contact'])))
        contact_mere = False
        contact_pere = False
        for contact in patient['contact']:
            for relationship in contact['relationship']:
                for coding in relationship['coding']:
                    if coding['code'] == 'MERE':
                        contact_mere = True
                        break
                    if coding['code'] == 'PERE':
                        contact_pere = True
                        break
                if contact_mere or contact_pere:
                    break
            if contact_mere:
                self.assertEqual(contact['name']['given'][0], 
                                usager.mother_given_name,
                                "Prénom de la mère {0} incorrect: {1}".format(
                                    usager.mother_given_name,
                                    contact['name']['given'][0]))
                self.assertEqual(contact['name']['family'][0], 
                                usager.mother_family_name,
                                "Nom de famille de la mère {0} incorrect: {1}".format(
                                    usager.mother_family_name,
                                    contact['name']['family'][0]))
            elif contact_pere:
                self.assertEqual(contact['name']['given'][0], 
                                usager.father_given_name,
                                "Prénom du père {0} incorrect: {1}".format(
                                    usager.father_given_name,
                                    contact['name']['given'][0]))
                self.assertEqual(contact['name']['family'][0], 
                                usager.father_family_name,
                                "Nom de famille du père {0} incorrect: {1}".format(
                                    usager.father_family_name,
                                    contact['name']['family'][0]))
            if contact_pere and contact_mere:
                break
        self.assertTrue(contact_mere, "Contact MERE absent")
        self.assertTrue(contact_pere, "Contact PERE absent")

    def testSiJeGenereUnUsagerAvecAdresse_JObtiensUneRessourceFHIRPatientAvecAdresse(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.nam = self.test_patient['nam']
        usager.address_line = self.test_patient['address_line']
        usager.address_city = self.test_patient['address_city']
        usager.address_state = self.test_patient['address_state']
        usager.address_postal_code = self.test_patient['address_postal_code']
        usager.address_country = self.test_patient['address_country']
    
        patient = usager.getFhirResource()
        self.assertIn('address', 
                         patient, 
                         "Le patient devrait avoir un adresse: {}".format(
                             str(patient)))
        self.assertEqual(patient['address'][0]['line'][0], 
                         usager.address_line, 
                         "La ligne de l'adresse {0} aurait du être: {1}".format(
                             patient['address'][0]['line'][0],
                             usager.address_line))
        self.assertEqual(patient['address'][0]['city'], 
                         usager.address_city, 
                         "L'état {0} aurait du être: {1}".format(
                             patient['address'][0]['city'],
                             usager.address_city))
        self.assertEqual(patient['address'][0]['state'], 
                         usager.address_state, 
                         "L'état {0} aurait du être: {1}".format(
                             patient['address'][0]['state'],
                             usager.address_state))
        self.assertEqual(patient['address'][0]['postalCode'], 
                         usager.address_postal_code, 
                         "Le code postal {0} aurait du être: {1}".format(
                             patient['address'][0]['postalCode'],
                             usager.address_postal_code))
        self.assertEqual(patient['address'][0]['country'], 
                         usager.address_country, 
                         "Le pays {0} aurait du être: {1}".format(
                             patient['address'][0]['country'],
                             usager.address_country))
    
    def testSiJeGenereUneRessourcePourUnClientSansNAM_JAiAucunDansLesIdentifiants(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        patient = usager.getFhirResource()
        self.assertEqual(patient['identifier'][0]['system'], 
                         "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary/identifierType?code=AUCUN", 
                         "Le system {0} n'est pas {1}".format(
                             patient['identifier'][0]['system'], 
                             "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/vocabulary/identifierType?code=AUCUN"))
        
    @mock.patch('inspqcommun.hl7.fhir.requests.post', side_effect=mocked_fhir_requests_post)
    def testSiJeCreeUnUsagerQuiNExistaitPasDansLeServeur_JeRecoisUneReponseConfirmantLaCreation(self, mock_post):
        token = {}
        token['Authorization'] = "Bearer {}".format('UnToken')
        usager = PatientFHIR(base_url='http://fhir.server.url/fhir/dstu2', token=token, patient_dict=self.test_patient)
        response = usager.Create()
        self.assertEqual(response.status_code, 200, "La ressource n'a pas été créée: {}".format(response.status_code))
        ressource = json.loads(response.content.decode())
        self.assertEqual("Patient", ressource["resourceType"], "Mavaise resource recu: {} != Patient".format(ressource["resourceType"]))
        self.assertIn("id", ressource, "Le patient n'a pas d'id")
        self.assertFalse(usager.id is None, "L'usager n'a pas de id")
        self.assertEqual(self.test_patient["given_name"], ressource["name"][0]["given"][0], "given_name {0} incorrect: {1}".format(self.test_patient["given_name"], ressource["name"][0]["given"][0]))
        self.assertEqual(self.test_patient["family_name"], ressource["name"][0]["family"][0], "family_name {0} incorrect: {1}".format(self.test_patient["family_name"], ressource["name"][0]["family"][0]))
        
    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_fhir_requests_get)
    def testSiJeDemandeUnUsagerParSonId_JeRecoisSesInformationsDemographiques(self, mocked_fhir_requests_get):
        token = {}
        token['Authorization'] = "Bearer {}".format('UnToken')
        usager = PatientFHIR(base_url='http://fhir.server.url/fhir/dstu2', token=token)
        response = usager.GetById(patient_id=1)
        self.assertEqual(response.status_code, 200, "Erreur dans obtenir usager par id: {}".format(response.status_code))
        ressource = json.loads(response.content.decode())
        self.assertEqual("Patient", ressource["resourceType"], "Mavaise resource recu: {} != Patient".format(ressource["resourceType"]))
        self.assertEqual(ressource["id"], "1", "Le patient id {0} n'est pas le bon, il devrait être {1}".format(ressource["id"], "1"))
        self.assertFalse(usager.id is None, "L'usager n'a pas de id")
    @mock.patch('inspqcommun.hl7.fhir.requests.post', side_effect=mocked_fhir_requests_post)
    def testSiJApparieUnUsagerQuiExisteDansLeServeur_JeRecoisLUsagerApparie(self, mock_post):
        token = {}
        token['Authorization'] = "Bearer {}".format('UnToken')
        usager = PatientFHIR(base_url='http://fhir.server.url/fhir/dstu2', token=token, patient_dict=self.test_patient)
        response = usager.Match()
        self.assertEqual(response.status_code, 200, "La ressource n'a pas été apariée: {}".format(response.status_code))
        ressource = json.loads(response.content.decode())
        self.assertEqual("Parameters", ressource["resourceType"], "Mauvaise resource recu: {} != Parameters".format(ressource["resourceType"]))
        self.assertFalse(usager.id is None, "L'usager n'a pas de id")
    @mock.patch('inspqcommun.hl7.fhir.requests.post', side_effect=mocked_fhir_requests_post)
    def testSiJApparieUnUsagerQuiNExistePasDansLeServeur_JeRecoisUn204(self, mock_post):
        token = {}
        token['Authorization'] = "Bearer {}".format('UnToken')
        patient_introuvable = copy.deepcopy(self.test_patient)
        patient_introuvable["nam"] = "ERR204"
        usager = PatientFHIR(base_url='http://fhir.server.url/fhir/dstu2', token=token, patient_dict=patient_introuvable)
        response = usager.Match()
        self.assertEquals(response.status_code, 204, "La ressource ne devrait pas avoir été appariée: {}".format(response.status_code))
    @mock.patch('inspqcommun.hl7.fhir.requests.post', side_effect=mocked_fhir_requests_post)
    def testSiJApparieUnUsagerQuiAUnNIU_LExtensionMatchRAMQEstTrue(self, mock_post):
        token = {}
        token['Authorization'] = "Bearer {}".format('UnToken')
        usager = PatientFHIR(base_url='http://fhir.server.url/fhir/dstu2', token=token, patient_dict=self.test_patient)
        response = usager.Match()
        self.assertEqual(response.status_code, 200, "La ressource n'a pas été appariée: {}".format(response.status_code))
        ressource = json.loads(response.content.decode())
        self.assertEqual("Parameters", ressource["resourceType"], "Mauvaise resource recu: {} != Parameters".format(ressource["resourceType"]))
        self.assertTrue(usager.matchramq , "L'usager n'est pas apparié RAMQ mais aurait dû l'être.")

    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_fhir_requests_get)
    def testSiJeRechecheUnUsagerQuiExisteParSonNAM_JObtiensCetUsager(self, mock_get):
        token = {}
        token['Authorization'] = "Bearer {}".format('UnToken')
        usager = PatientFHIR(base_url='http://fhir.server.url/fhir/dstu2', token=token, patient_dict=self.test_patient)
        response = usager.Search()
        self.assertEqual(response.status_code, 200, "La ressource n'a pas été trouvée: {}".format(response.status_code))
        ressource = json.loads(response.content.decode())
        self.assertEqual("Bundle", ressource["resourceType"], "Mauvaise resource recu: {} != Bundle".format(ressource["resourceType"]))
        self.assertEqual("searchset", ressource["type"], "Mauvaise type recu: {} != searchset".format(ressource["type"]))
        self.assertEqual(1, ressource["total"], "La recherche a retourné un résulat différent de 1: {}".format(str(ressource["total"])))

    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_fhir_requests_get)
    def testSiJeFaitUneRechercheUsagerParnomPrenomDateDeNaissanceSexe_JObtiensPlusieurUsagers(self, mock_get):
        token = {}
        token['Authorization'] = "Bearer {}".format('UnToken')
        usager = PatientFHIR(base_url='http://fhir.server.url/fhir/dstu2', token=token)
        response = usager.Search(given=self.test_patient['given_name'], family=self.test_patient['family_name'], gender=self.test_patient['gender'], birthdate=self.test_patient['birth_date'])
        self.assertEqual(response.status_code, 200, "La ressource n'a pas été trouvée: {}".format(response.status_code))
        ressource = json.loads(response.content.decode())
        self.assertEqual("Bundle", ressource["resourceType"], "Mauvaise resource recu: {} != Bundle".format(ressource["resourceType"]))
        self.assertEqual("searchset", ressource["type"], "Mauvaise type recu: {} != searchset".format(ressource["type"]))
        self.assertEqual(2, ressource["total"], "La recherche a retourné un résulat différent de 1: {}".format(str(ressource["total"])))
        usager.from_json(json.dumps(ressource['entry'][0]['resource']))
        self.assertEqual(usager.given_name, self.test_patient['given_name'], "Prénom incorrect {0} != {1}".format(usager.given_name, self.test_patient['given_name']))

    def test_convertir_une_ressource_JSON_en_objet_bundle(self):
        data = bundle_example
        bndl = BundleFHIR(resource=data)
        
        self.assertEqual(
            bndl.entries[0]['resource'].resource_type,
            'Patient', 
            "La première resource devrait être Patient mais est: {0}".format(bndl.entries[0]['resource'].resource_type))
        self.assertEqual(
            bndl.entries[1]['resource'].entries[0]['response']['status'],
            "200",
            "Response status incorrect: {}".format(bndl.entries[1]['resource'].entries[0]['response']['status'])
        )
        self.assertEqual(
            bndl.entries[1]['resource'].resource_type,
            'Bundle', 
            "La deuxième resource devrait être Bundle mais est: {0}".format(bndl.entries[1]['resource'].resource_type))
        self.assertEqual(
            bndl.entries[1]['resource'].type,
            'collection', 
            "La deuxième Bundle est de type: {0}".format(bndl.entries[1]['resource'].type))

        
    def test_convertir_un_objet_bundle_avec_un_patient_en_ressource_fhir(self):
        usager = PatientFHIR()
        usager.given_name = self.test_patient['given_name']
        usager.family_name = self.test_patient['family_name']
        usager.gender = self.test_patient['gender']
        usager.birth_date = self.test_patient['birth_date']
        usager.nam = self.test_patient['nam']

        response = {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:03:11.000-04:00"
        }
        bundle = BundleFHIR()
        bundle.type = 'collection'
        bundle.add_entry(resource=usager.getFhirResource(), response=response)

        dict_bundle = bundle.getFhirResource()
        self.assertEqual(dict_bundle['resourceType'], 
            'Bundle', 
            "Le type {0} de la ressource aurait du être Bundle".format(dict_bundle['resourceType']))
        self.assertEqual(dict_bundle['type'], 
            'collection', 
            "Le type {0} du bundle aurait du être collection".format(dict_bundle['type']))
        self.assertEqual(dict_bundle['entry'][0]['resource']['resourceType'], 
            'Patient',
            "Le type {0} de la ressource aurait du être Patient".format(dict_bundle['entry'][0]['resource']['resourceType']))
        self.assertEqual(
            dict_bundle['entry'][0]['response']['status'],
            "200",
            "Le statut de la reponse est incorrect: {0}".format(dict_bundle['entry'][0]['response']['status'])
        )
        bundle = BundleFHIR()
        bundle.add_entry(resource=usager)

        dict_bundle = bundle.getFhirResource()
        self.assertEqual(dict_bundle['resourceType'], 
            'Bundle', 
            "Le type {0} de la ressource aurait du être Bundle".format(dict_bundle['resourceType']))
        self.assertEqual(dict_bundle['entry'][0]['resource']['resourceType'], 
            'Patient',
            "Le type {0} de la ressource aurait du être Patient".format(dict_bundle['entry'][0]['resource']['resourceType']))

    def test_definir_une_quantite_pour_une_ressource_immunization(self):
        code = 'INV.mesure'
        unit = 'ml'
        value = 0.5

        quantity = Quantity()
        quantity.code = code
        quantity.unit = unit
        quantity.value = value

        imms = ImmunizationFHIR()
        imms.set_dose_quantity(quantity=quantity)
        self.assertEqual(imms.get_dose_quantity().code, code)
        self.assertEqual(imms.get_dose_quantity().unit, unit)
        self.assertEqual(imms.get_dose_quantity().value, value)

        imms.set_dose_quantity(quantity_code=code, quantity_unit=unit, quantity_value=value)
        self.assertEqual(imms.get_dose_quantity().code, code)
        self.assertEqual(imms.get_dose_quantity().unit, unit)
        self.assertEqual(imms.get_dose_quantity().value, value)



    def test_definir_un_lot_pour_une_ressource_immunization(self):
        imm = ImmunizationFHIR()
        batch = MedicationProductBatch()
        batch.id = '1234'
        batch.lotNumber = 'lot123445'
        imm.set_lot_number(lot_number=batch.lotNumber)
        self.assertEqual(imm.get_lot_number(), batch.lotNumber)
        imm.set_lot_id(lot_id=batch.id)
        self.assertEqual(imm.get_lot_id(), batch.id)


    def test_definir_date_pour_une_ressource_immunization(self):
        aujourdhui = datetime.today()
        imm = ImmunizationFHIR()
        imm.set_date(date_to_set=aujourdhui)
        self.assertEqual(imm.get_date().date.strftime('%Y-%m-%d'), aujourdhui.strftime('%Y-%m-%d'))
        
    def test_convertir_un_objet_immunization_en_ressource_fhir(self):
        imm = ImmunizationFHIR()
        imm.id = '1234'
        imm.updated_by = "unuserbidon"
        imm.created_by = "unuseraussibidon"
        imm.version_id = "1"
        imm.creation_date = date.today()
        imm.last_updated = datetime.now()
        imm.override_status_code = "FV"
        imm.override_status_display = "Valide"
        imm.antigen_code = "840536004"
        imm.antigen_display = "SRAS-CoV-2"
        imm.antigen_dose_number = 1
        imm.antigen_status_code = "FV"
        imm.antigen_status_display = "Valide"
        imm.lot_id = "5467"
        imm.trade_name = "MOD COVID-19"
        imm.vaccine_code_code = "QCSNOMED00124"
        imm.vaccine_code_display = "COVID-19"
        imm.patient_reference = "10456258"
        imm.performer_reference = "172645"
        imm.performer_display = "Ragy Chouha"
        imm.organization = Organization(jsondict=bundle_example['entry'][1]['resource']['entry'][0]['resource']['contained'][0])
        imm.location_reference = "12570"
        imm.location_display = "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)"
        imm.lot_number = "3001652"
        imm.expiration_date = "2021-10-06"
        imm.site_code = "LLFA"
        imm.site_display = "Bras Gauche"
        imm.route_code = "IM"
        imm.route_display = "Intramusculaire"
        imm.dose_quantity_value = 0.5
        imm.dose_quantity_unit = 'ml'
        imm.dose_quantity_code = "INV.UnitOfMeasure2"
        imm.reason = [{"code": "CoV-AUTRES", "display": "06 - COVID-19 - Autres raisons"}]
        imm.status = "completed"
        imm.date = date.today()

        res = imm.getFhirResource()

        self.assertEqual(
            res['resourceType'],
            "Immunization",
            "Type de ressource {0} incorrect".format(res['resourceType'])
            )
        updated_by_ok = False
        created_by_ok = False
        creation_date_ok = False
        for meta_ext in res['meta']['extension']:
            if meta_ext['url'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/updatedby":
                updated_by_ok = True if meta_ext['valueString'] == imm.updated_by else False
            if meta_ext['url'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#common/createdby":
                created_by_ok = True if meta_ext['valueString'] == imm.created_by else False
            if meta_ext['url'] == imm.creation_date_url:
                creation_date_ok = True if meta_ext['valueDate'] == imm.creation_date else False
        self.assertTrue(
            created_by_ok,
            "Created by invalide")
        self.assertTrue(
            updated_by_ok,
            "Updated by invalide")
        self.assertTrue(
            creation_date_ok, 
            "creation_date invalide")
        
        version_id_ok = True if 'versionId' in res['meta'] and res['meta']['versionId'] == imm.version_id else False
        last_updated_ok = True if 'lastUpdated' in res['meta'] and res['meta']['lastUpdated'] == imm.last_updated else False
        profile_ok = True if 'profile' in res['meta'] and imm.profile_url in res['meta']['profile'] else False
        self.assertTrue(version_id_ok, "Meta versionId incorrect")
        self.assertTrue(last_updated_ok, "Meta lastUpdated incorrect")
        self.assertTrue(profile_ok, "Meta profile incorrect")
        imm_id_ok = True if 'id' in res and res['id'] == imm.id else False
        self.assertTrue(imm_id_ok, "Immunization Id incorrect")
        
        organization_ok = False
        if res['contained'] is not None and len(res['contained']) > 0:
            for contained in res['contained']:
                if ( contained is not None and
                    'resourceType' in contained 
                    and contained['resourceType'] == 'Organization'
                    and 'id' in contained 
                    and (
                        (type(imm.organization) is Organization and contained['id'] == imm.organization.id) or
                        (type(imm.organization) is dict and contained['id'] == imm.organization['id']))):

                    organization_ok = True
                    break
        self.assertTrue(organization_ok, "Organization invalide")
        override_status_ok = False
        lot_id_ok = False
        antigen_status_ok = False
        trade_name_ok = False
        dose_number_ok = False
        for ext in res['extension']:
            if ext['url'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/overridestatus":
                for coding in ext['valueCodeableConcept']['coding']:
                    if coding['system'] == imm.coding_system:
                        override_status_ok = True if (coding['code'] == imm.override_status_code and coding['display'] == imm.override_status_display) else False
            elif ext['url'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/lotid":
                lot_id_ok = True if ext["valueString"] == imm.lot_id else False
            elif ext['url'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/antigenstatus":
                for antigen_status_ext in ext['extension']:
                    if antigen_status_ext['url'] == "antigen":
                        for coding in antigen_status_ext["valueCodeableConcept"]["coding"]:
                            if coding['system'] == imm.coding_system:
                                antigen_status_ok = True if coding['code'] == imm.antigen_code and coding['display'] == imm.antigen_display else False
                    elif antigen_status_ext['url'] == "doseNumber":
                        dose_number_ok = True if antigen_status_ext['valueInteger'] == imm.antigen_dose_number else False
                    elif antigen_status_ext['url'] == "status":
                        for coding in antigen_status_ext["valueCodeableConcept"]["coding"]:
                            if coding['system'] == imm.coding_system:
                                antigen_status_ok = True if coding['code'] == imm.antigen_status_code and coding['display'] == imm.antigen_status_display else False
            elif ext['url'] == "http://www.santepublique.rtss.qc.ca/sipmi/fa/1.0.0/extensions/#immunization/tradename":
                trade_name_ok = True if ext['valueString'] == imm.trade_name else False
        self.assertTrue(
            override_status_ok,
            "override_status_ok by invalide")
        self.assertTrue(
            lot_id_ok,
            "lot_id_ok by invalide")
        self.assertTrue(
            antigen_status_ok,
            "antigen_status_ok by invalide")
        self.assertTrue(
            trade_name_ok,
            "trade_name_ok by invalide")
        self.assertTrue(
            dose_number_ok,
            "dose_number_ok by invalide")

        vaccine_code_ok = False
        for vaccine_code_coding in res['vaccineCode']['coding']:
            if vaccine_code_coding['system'] == imm.coding_system:
                vaccine_code_ok = True if vaccine_code_coding['code'] == imm.vaccine_code_code and vaccine_code_coding['display'] == imm.vaccine_code_display else False
        self.assertTrue(
            vaccine_code_ok,
            "vaccine_code_ok by invalide")
        self.assertEqual(
            res['patient']['reference'],
            imm.patient_reference,
            "Reference patient {0} invalide".format(res['patient']['reference'])
        )
        self.assertTrue(
            (res['performer']['reference'] == imm.performer_reference and res['performer']['display'] == imm.performer_display),
            "Performer invalide {0} {1}".format(
                res['performer']['reference'],
                res['performer']['display']
            )
        )
        self.assertTrue(
            (res['location']['reference'] == imm.location_reference and res['location']['display'] == imm.location_display),
            "Location invalide {0} {1}".format(
                res['location']['reference'],
                res['location']['display']
            )
        )
        self.assertEqual(
            res['lotNumber'],
            imm.lot_number,
            "Numéro de lot {0} invalide".format(res['lotNumber'])
        )
        self.assertEqual(
            datetime.strftime(res['expirationDate'], "%Y-%m-%d"),
            imm.expiration_date,
            "expirationDate {0} invalide".format(res['expirationDate'])
        )
        site_ok = False
        for coding in res['site']['coding']:
            if coding['system'] == imm.coding_system:
                site_ok = True if coding['code'] == imm.site_code and coding['display'] == imm.site_display else False
        self.assertTrue(
            site_ok,
            "site non valide"
        )
        self.assertEqual(
            res['doseQuantity']['value'],
            imm.dose_quantity_value,
            "Dose quantité {0} invalide {1}".format(
                res['doseQuantity']['value'],
                imm.dose_quantity_value
            )
        )
        self.assertEqual(
            res['doseQuantity']['unit'],
            imm.dose_quantity_unit,
            "Dose unité {0} invalide {1}".format(
                res['doseQuantity']['unit'],
                imm.dose_quantity_unit
            )
        )
        self.assertEqual(
            res['doseQuantity']['code'],
            imm.dose_quantity_code,
            "Dose code {0} invalide {1}".format(
                res['doseQuantity']['code'],
                imm.dose_quantity_code
            )
        )
        all_reasons_ok = True
        for reason in imm.reason:
            reason_ok = False
            for ressource_reason in res['explanation']['reason']:
                if 'coding' in ressource_reason:
                    for coding in ressource_reason['coding']:
                        if (coding["system"] == imm.coding_system
                                and coding['code'] == reason['code']
                                and coding['display'] == reason['display']):
                            reason_ok = True
                            break
                else:
                    if (ressource_reason["system"] == imm.coding_system
                            and ressource_reason['code'] == reason['code']
                            and ressource_reason['display'] == reason['display']):
                        reason_ok = True
                        break

            if not reason_ok:
                all_reasons_ok = False
                break
        self.assertTrue(
            all_reasons_ok,
            "Raisons vaccination invalide"
        )
        self.assertEqual(res['status'],
            imm.status,
            "Status {0} invalide: {1}".format(res['status'], imm.status))
        self.assertEqual(res['date'],
            imm.date,
            "Date {0} invalide: {1}".format(
                res['date'],
                imm.date))

    def test_convertir_une_ressource_fhir_en_objet_immunization(self):
        data = None
        for entry in bundle_example['entry']:
            if entry['resource']['resourceType'] == 'Immunization':
                data = entry['resource']
                break
            elif entry['resource']['resourceType'] == 'Bundle':
                for sub_entry in entry['resource']['entry']:
                    if sub_entry['resource']['resourceType'] == 'Immunization':
                        data = sub_entry['resource']
                        break
                    
        self.assertTrue(data is not None)
        imm = ImmunizationFHIR(imm_dict=data)
        self.assertEqual(imm.resource_type, 'Immunization')
        self.assertEqual(
            imm.updated_by,
            "agja9320@dev.psc.secursante",
            "Updated by incorrect {0}".format(
                imm.updated_by
            )
        )
        self.assertEqual(
            imm.created_by,
            "agja9320@dev.psc.secursante",
            "Create by incorrect {0}".format(
                imm.created_by
            )
        )
        self.assertEqual(
            imm.creation_date,
            "2021-04-20",
            "Creation date incorrect {0}".format(
                imm.creation_date
            )
        )
        self.assertEqual(
            imm.version_id,
            '1',
            "Version Id incorrect {0}".format(
                str(imm.version_id)
            )
        )
        self.assertEqual(
            imm.last_updated,
            "2021-04-20T13:49:26-04:00",
            "Last updated incorrect {0}".format(
                str(imm.last_updated)
            )
        )
        self.assertEqual(
            imm.override_status_code,
            "FV",
            "Override status code invalode {0}".format(imm.override_status_code)
        )
        self.assertEqual(
            imm.override_status_id,
            "1324422",
            "Override status id invalode {0}".format(imm.override_status_id)
        )
        self.assertEqual(
            imm.override_status_display,
            "Valide",
            "Override status display invalide {0}".format(imm.override_status_display)
        )
        self.assertEqual(
            imm.lot_id,
            "5467",
            "Lot Id invalide {0}".format(imm.lot_id)
        )
        self.assertEqual(
            imm.antigen_code,
            "840536004",
            "Antigen Code invalide {0}".format(imm.antigen_code)
        )
        self.assertEqual(
            imm.antigen_display,
            "SRAS-CoV-2",
            "Antigen Display invalide {0}".format(imm.antigen_display)
        )
        self.assertEqual(
            imm.antigen_id,
            "1324777",
            "Antigen ID invalide {0}".format(imm.antigen_id)
        )
        self.assertEqual(
            imm.antigen_dose_number,
            1,
            "Antigen Dose number invalide {0}".format(str(imm.antigen_dose_number))
        )
        self.assertEqual(
            imm.antigen_status_id,
            "1324422",
            "Antigen Status Id invalide {0}".format(imm.antigen_status_id)
        )
        self.assertEqual(
            imm.antigen_status_display,
            "Valide",
            "Antigen Status Display invalide {0}".format(imm.antigen_status_display)
        )
        self.assertEqual(
            imm.antigen_status_code,
            "FV",
            "Antigen Status Code invalide {0}".format(imm.antigen_status_code)
        )
        self.assertEqual(
            imm.trade_name,
            "MOD COVID-19",
            "Trade Name invalide {0}".format(imm.trade_name)
        )
        self.assertEqual(
            imm.status,
            "completed",
            "Status invalide {0}".format(imm.status)
        )
        self.assertEqual(
            imm.date,
            "2021-04-19T00:00:00-04:00",
            "Date invalide {0}".format(imm.date)
        )
        self.assertEqual(
            imm.vaccine_code_code,
            "QCSNOMED00124",
            "Vaccine code Code invalide {0}".format(imm.vaccine_code_code)
        )
        self.assertEqual(
            imm.vaccine_code_display,
            "COVID-19",
            "Vaccine code Display invalide {0}".format(imm.vaccine_code_display)
        )
        self.assertEqual(
            imm.vaccine_code_id,
            "1324776",
            "Vaccine code Id invalide {0}".format(imm.vaccine_code_id)
        )
        self.assertEqual(
            imm.patient_reference,
            "10456258",
            "Patient reference invalide {0}".format(imm.patient_reference)
        )
        self.assertFalse(
            imm.reported,
            "Reported invalide {0}".format(str(imm.reported))
        )
        self.assertEqual(
            imm.performer_reference,
            "172645",
            "Performer reference invalide {0}".format(imm.performer_reference)
        )
        self.assertEqual(
            imm.performer_display,
            "Ragy Chouha",
            "Performer display invalide {0}".format(imm.performer_display)
        )
        self.assertEqual(
            imm.location_reference,
            "12570",
            "Location reference invalide {0}".format(imm.location_reference)
        )
        self.assertEqual(
            imm.location_display,
            "06 PHARM JEAN-COUTU DAVE LAROUCHE ET VY KY LINH LE (SAINT-LAURENT)",
            "Location display invalide {0}".format(imm.location_display)
        )
        self.assertEqual(
            imm.lot_number,
            "3001652",
            "Lot number invalide {0}".format(imm.lot_number)
        )
        self.assertEqual(
            imm.expiration_date,
            "2021-10-06",
            "Expiration date invalide {0}".format(imm.expiration_date)
        )
        self.assertEqual(
            imm.site_code,
            "LLFA",
            "Site code invalide {0}".format(imm.site_code)
        )
        self.assertEqual(
            imm.site_display,
            "Bras Gauche",
            "Site display invalide {0}".format(imm.site_display)
        )
        self.assertEqual(
            imm.site_id,
            "433254",
            "Site Id invalide {0}".format(imm.site_id)
        )
        self.assertEqual(
            imm.route_code,
            "IM",
            "Route code invalide {0}".format(imm.route_code)
        )
        self.assertEqual(
            imm.route_display,
            "Intramusculaire",
            "Route display invalide {0}".format(imm.route_display)
        )
        self.assertEqual(
            imm.route_id,
            "433437",
            "Route Id invalide {0}".format(imm.route_id)
        )
        self.assertEqual(
            imm.dose_quantity_value,
            0.5,
            "Dose quantity value invalide {0}".format(imm.dose_quantity_value)
        )
        self.assertEqual(
            imm.dose_quantity_unit,
            "ml",
            "Dose quantity unit invalide {0}".format(imm.dose_quantity_unit)
        )
        self.assertEqual(
            imm.dose_quantity_code,
            "INV.UnitOfMeasure2",
            "Dose quantity code invalide {0}".format(imm.dose_quantity_code)
        )
        self.assertEqual(
            imm.reason[0]['code'],
            "CoV-AUTRES",
            "Reason code invalide {0}".format(imm.reason[0]['code'])
        )
        self.assertEqual(
            imm.reason[0]['display'],
            "06 - COVID-19 - Autres raisons",
            "Reason display invalide {0}".format(imm.reason[0]['display'])
        )
        self.assertEqual(
            imm.reason[0]['id'],
            "1324784",
            "Reason Id invalide {0}".format(imm.reason[0]['id'])
        )
        
    def test_si_je_compte_le_nombre_d_entres_dans_le_bundle_alors_j_obtiens_2(self):
        bundle = BundleFHIR(resource=bundle_example)

        # Compter le nombre total d'entrés dans le bundle
        nb_entries = bundle.count_entries()
        self.assertEqual(
            nb_entries,
            2,
            "Le nombre d'entre n'est pas valide: {0}".format(nb_entries)
        )
        
    def test_si_je_compte_le_nombre_d_entres_recursivement_dans_le_bundle_alors_j_obtiens_15(self):
        bundle = BundleFHIR(resource=bundle_example)

        # Compter le nombre total d'entrés dans le bundle
        nb_entries = bundle.count_entries(recurse=True)
        self.assertEqual(
            nb_entries,
            15,
            "Le nombre d'entre n'est pas valide: {0}".format(nb_entries)
        )
        
    def test_si_je_compte_le_nombre_d_entres_immunization_recursivement_dans_le_bundle_alors_j_obtiens_13(self):
        bundle = BundleFHIR(resource=bundle_example)

        # Compter le nombre total d'entrés dans le bundle
        nb_entries = bundle.count_entries(recurse=True, resource_type='Immunization')
        self.assertEqual(
            nb_entries,
            13,
            "Le nombre d'entre n'est pas valide: {0}".format(nb_entries)
        )

    def test_si_je_compte_le_nombre_d_entres_patient_recursivement_dans_le_bundle_alors_j_obtiens_1(self):
        bundle = BundleFHIR(resource=bundle_example)

        # Compter le nombre total d'entrés dans le bundle
        nb_entries = bundle.count_entries(recurse=True, resource_type='Patient')
        self.assertEqual(
            nb_entries,
            1,
            "Le nombre d'entre n'est pas valide: {0}".format(nb_entries)
        )

    def test_convertir_une_ressource_operation_outcome_en_objet(self):
        oo = bundle_operation_outcome_business_rule['entry'][0]['resource']
        ooo = OperationOutcomeFHIR(resource=oo)

        self.assertEqual(
            ooo.get_issue_code(),
            'business-rule',
            "Le code d'erreur du OperationOutcome est incorrect {0}".format(ooo.get_issue_code())
        )

        self.assertEqual(
            ooo.get_issue_details().code,
            "412",
            "Details de l'erreur incorrect {0}".format(ooo.get_issue_details().code)
        )

        self.assertEqual(
            ooo.get_issue_details_code(),
            "412",
            "Details de l'erreur incorrect {0}".format(ooo.get_issue_details_code())
        )

    def test_convertir_une_ressource_bundle_contenant_un_outcome_en_objet(self):
        bundle = BundleFHIR(resource=bundle_operation_outcome_business_rule)
        ooo = bundle.entries[0]['resource']

        self.assertEqual(
            ooo.get_issue_code(),
            'business-rule',
            "Le code d'erreur du OperationOutcome est incorrect {0}".format(ooo.get_issue_code())
        )

        self.assertEqual(
            ooo.get_issue_details().code,
            "412",
            "Details de l'erreur incorrect {0}".format(ooo.get_issue_details().code)
        )

    def test_si_je_recherche_les_entres_patient_dans_le_bundle_alors_j_obtiens_guy_mauve(self):
        bundle = BundleFHIR(resource=bundle_example)

        # Compter le nombre total d'entrés dans le bundle
        patients = bundle.get_entries(recurse=True, resource_type='Patient')
        self.assertEqual(
            patients[0].id,
            "10456258",
            "Le patient n'est pas valide: {0}".format(patients[0].id)
        )
        self.assertEqual(
            patients[0].given_name,
            "Guy",
            "Le prenom du patient n'est pas valide: {0}".format(patients[0].given_name)
        )
        self.assertEqual(
            patients[0].family_name,
            "Mauve",
            "Le nom du patient n'est pas valide: {0}".format(patients[0].family_name)
        )

    def test_si_je_recherche_les_entres_imms_dans_le_bundle_alors_j_en_obtiens_13(self):
        bundle = BundleFHIR(resource=bundle_example)

        # Compter le nombre total d'entrés dans le bundle
        imms = bundle.get_entries(recurse=True, resource_type='Immunization')
        self.assertEqual(
            len(imms),
            13,
            "Le nombre d'immunization n'est pas valide: {0}".format(len(imms))
        )

    def test_convertir_une_ressource_condition_en_objet(self):
        condition = ConditionFHIR(resource=condition_test)

        self.assertEqual(
            condition.get_code()['code'],
            '54fdb993c540810bb87ee624762744b1401eb5e2615e0834a3948ef19f077b48',
            "Le code de la ressource Condition est incorrect {0}".format(condition.get_code()['code'])
        )

        self.assertEqual(
            condition.get_code_code(),
            '54fdb993c540810bb87ee624762744b1401eb5e2615e0834a3948ef19f077b48',
            "Le code de la ressource Condition est incorrect {0}".format(condition.get_code_code())
        )

        self.assertEqual(
            condition.get_category()['code'],
            "contraindicationPrecaution",
            "Categorie de la ressource Condition est incorrecte {0}".format(condition.get_category()['code'])
        )

        self.assertEqual(
            condition.get_category_code(),
            "contraindicationPrecaution",
            "Categorie de la ressource Condition est incorrecte {0}".format(condition.get_category_code())
        )

        self.assertEqual(
            condition.get_agent()['display'],
            "COVID-19",
            "L'agent de la ressource Condition est incorrecte {0}".format(condition.get_agent()['display'])
        )

        self.assertEqual(
            condition.get_agent_display(),
            "COVID-19",
            "L'agent de la ressource Condition est incorrecte {0}".format(condition.get_agent_display())
        )

        self.assertEqual(
            condition.get_antigen()['display'],
            "SRAS-CoV-2",
            "L'antigene de la ressource Condition est incorrecte {0}".format(condition.get_agent()['display'])
        )

        self.assertEqual(
            condition.get_antigen_display(),
            "SRAS-CoV-2",
            "L'antigene de la ressource Condition est incorrecte {0}".format(condition.get_antigen_display())
        )

    def test_convertir_une_ressource_bundle_contenant_une_ressource_condition_en_objet(self):
        cond_entry = {}
        cond_entry['resource'] = condition_test
        cond_entry['response'] = {
              "status": "200",
              "etag": "1",
              "lastModified": "2021-04-20T18:13:29.000-04:00"
            }
        dict_bundle = empty_bundle.copy()
        dict_bundle['entry'].append(cond_entry)
        bundle = BundleFHIR(resource=dict_bundle)
        condition = bundle.entries[0]['resource']

        self.assertEqual(
            condition.get_category()['code'],
            "contraindicationPrecaution",
            "Categorie de la ressource Condition est incorrecte {0}".format(condition.get_category()['code'])
        )

    def test_convertir_patient_fhir_visiteur_en_patien_fhir(self):
        visitor1 = PatientFHIR(patient_dict=self.test_patient)
        ress = visitor1.getFhirResource()
        visitor2 = PatientFHIR(patient_resource_dict=ress)

        self.assertEqual(
            visitor1.given_name, 
            visitor2.get_given_name(),
                "{0} not {1}".format(
                    visitor1.given_name, 
                    visitor2.get_given_name()))

        self.assertEqual(
            visitor1.get_given_name(), 
            visitor2.get_given_name(),
                "{0} not {1}".format(
                    visitor1.get_given_name(), 
                    visitor2.get_given_name()))

        self.assertEqual(
            visitor1.given_name, 
            visitor2.given_name,
                "{0} not {1}".format(
                    visitor1.given_name, 
                    visitor2.given_name))

    def test_convertir_organization_json_en_organization_fhir_visisteur(self):
        organisation_dict = bundle_example['entry'][1]['resource']['entry'][0]['resource']['contained'][0]
        org_visitor = OrganizationFHIR(resource=organisation_dict)

        self.assertEqual(
            organisation_dict['name'],
            org_visitor.get_name(),
            "Name {0} invalide: {1}".format(
                organisation_dict['name'],
                org_visitor.get_name(),
            ))
            
    def test_getter_et_setter_organization_fhir_visiteur(self):
        org_visitor = OrganizationFHIR()
        name_to_set = '03 CSSS DE LA VIEILLE-CAPITALE'
        org_visitor.set_name(name=name_to_set)
        name = org_visitor.get_name()
        self.assertEqual(
            name_to_set,
            name,
            "Name {0} invalide: {1}".format(
                name_to_set,
                name,
            ))

    def test_convertir_location_json_en_location_fhir_visiteur(self):
        location_visitor = LocationFHIR(resource=test_location)
        self.assertEqual(
            location_visitor.get_name(),
            test_location['name'],
            "Le nom du LDS {0} est invalide: {1}".format(
                test_location['name'],
                location_visitor.get_name()
            )
        )

    def test_getter_setter_location_fhir_visiteur(self):
        location_visitor = LocationFHIR()
        name_to_set = '03 CENTRE DONACONA'
        location_visitor.set_name(name=name_to_set)
        self.assertEqual(
            location_visitor.get_name(),
            name_to_set,
            "Nom LDS {0}, invalide: {1}".format(
                name_to_set,
                location_visitor.get_name()
            )
        )

    def test_convertir_un_parameter_avec_patient_en_json_dict(self):
        patient = PatientFHIR(patient_dict=self.test_patient)
        param = ParameterFHIR()
        param.add_parameter(patient)

        json_param = param.getFhirResource()
        all_parameters_are_dict = True
        for param in json_param['parameter']:
            if type(param['resource']) is not dict:
                all_parameters_are_dict = False
                break
        self.assertTrue(all_parameters_are_dict)

    def test_convertir_un_location_rrss_en_location_fhir_visitor(self):
        location = LocationFHIR(resource=location_rrss_dict)
        id_rrss = location_rrss_dict['identifier'][0]['value']
        self.assertEqual(
            location.get_id_rrss(),
            id_rrss,
            f"Identifiant RRSS invalide {location.get_id_rrss()} != {id_rrss}")
        location_id = location_rrss_dict['id']
        self.assertEqual(
            location.get_id(),
            location_id,
            f"Identifiant RRSS invalide {location.get_id()} != {location_id}")

        mot_cle = "Vaccination"
        self.assertFalse(
            location.have_mot_cle(mot_cle=mot_cle),
            f"Le location a le mot cle {mot_cle} mais n'aurait pas du"
        )
        mot_cle = "Accident vasculaire cérébral"
        self.assertTrue(
            location.have_mot_cle(mot_cle=mot_cle),
            f"Le location n'a pas le mot cle {mot_cle} mais aurait du"
        )
        visitor_effective_from = location.get_effective_from().isostring
        visitor_effective_to = location.get_effective_to().isostring
        dict_effective_from = None
        dict_effective_to = None
        for ext in location_rrss_dict["extension"]:
            if "url" in ext and ext["url"] == location.period_url and "valuePeriod" in ext:
                if "start" in ext["valuePeriod"]:
                    dict_effective_from = ext["valuePeriod"]["start"]
                if "end" in ext["valuePeriod"]:
                    dict_effective_to = ext["valuePeriod"]["end"]
        self.assertEqual(
            visitor_effective_from,
            dict_effective_from
        )
        self.assertEqual(
            visitor_effective_to,
            dict_effective_to
        )

        is_active = location.is_active()
        status_bool = False
        if location_rrss_dict["status"] == "active":
            status_bool = True
        self.assertEqual(
            is_active,
            status_bool,
            "Le status {0} n'est pas valide. Il aurait dû être {1}".format(
                is_active,
                status_bool
            )
        )

    def test_obtenir_numeros_de_telephones_location(self):
        loc = LocationFHIR(resource=location_rrss_dict)
        telephones = loc.get_phones()
        self.assertGreaterEqual(len(telephones), 1, "Le LDS n'a pas de numéro de téléphone")
        telephone_trouve = False
        for telecom in location_rrss_dict["telecom"]:
            for tel in telephones:
                if tel["value"] == telecom["value"]:
                    telephone_trouve = True
            self.assertTrue(telephone_trouve, "Le numéro de téléphone du LDS n'est pas dans la liste")

    def test_convertir_un_organization_rrss_en_organization_fhir_visitor(self):
        org = OrganizationFHIR(resource=organization_rrss_dict)
        id_rrss = organization_rrss_dict['identifier'][0]['value']
        self.assertEqual(
            org.get_id_rrss(),
            id_rrss,
            f"Identifiant RRSS invalide {org.get_id_rrss()} != {id_rrss}")
        org_id = organization_rrss_dict['id']
        self.assertEqual(
            org.get_id(),
            org_id,
            f"Identifiant RRSS invalide {org.get_id()} != {org_id}")
        mot_cle = "Vaccination"
        self.assertTrue(
            org.have_mot_cle(mot_cle=mot_cle),
            f"Le organization n'a pas le mot cle {mot_cle} mais aurait du"
        )
        mot_cle = "Extraction des dents"
        self.assertFalse(
            org.have_mot_cle(mot_cle=mot_cle),
            f"Le organization a le mot cle {mot_cle} mais n'aurait pas du"
        )
        
        visitor_effective_from = org.get_effective_from().isostring
        visitor_effective_to = org.get_effective_to().isostring
        dict_effective_from = None
        dict_effective_to = None
        for ext in organization_rrss_dict["extension"]:
            if "url" in ext and ext["url"] == org.period_url and "valuePeriod" in ext:
                if "start" in ext["valuePeriod"]:
                    dict_effective_from = ext["valuePeriod"]["start"]
                if "end" in ext["valuePeriod"]:
                    dict_effective_to = ext["valuePeriod"]["end"]
        self.assertEqual(
            visitor_effective_from,
            dict_effective_from
        )
        self.assertEqual(
            visitor_effective_to,
            dict_effective_to
        )
        
        is_active = org.is_active()
        self.assertEqual(
            is_active,
            organization_rrss_dict["active"],
            "Le statut {0} est incorrect".format(is_active))
        

    def test_obtenir_numeros_de_telephones_organization(self):
        org = OrganizationFHIR(resource=organization_rrss_dict)
        telephones = org.get_phones()
        self.assertGreaterEqual(len(telephones), 1, "L'organisation n'a pas de numéro de téléphone")
        telephone_trouve = False
        for tel in telephones:
            if tel["value"] == organization_rrss_dict["telecom"][0]["value"]:
                telephone_trouve = True
        self.assertTrue(telephone_trouve, "Le numéro de téléphone de l'organisation n'est pas dans la liste")

    def test_obtenir_numeros_de_telephones_contact_organization(self):
        org = OrganizationFHIR(resource=organization_rrss_dict)
        telephones = org.get_contacts_phones()
        self.assertGreaterEqual(len(telephones), 1, "L'organisation n'a pas de contact qui on de numéro de téléphone")
        telephone_trouve = False
        for tel in telephones:
            if tel["value"] == organization_rrss_dict["contact"][0]["telecom"][0]["value"]:
                telephone_trouve = True
        self.assertTrue(telephone_trouve, "Le numéro de téléphone du contaclt de l'organisation n'est pas dans la liste")

    def test_convertir_un_dictionnaire_en_medication_fhir_visitor(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        f = open("{0}/exemples/medication.json".format(this_dir),"r")
        medication_dict = json.loads(f.read())
        f.close()
        medication = MedicationFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer yfsadfsdf="},
            validate_certs=False,
            resource=medication_dict)
        self.assertTrue(type(medication.fhir_resource) is Medication)
        liste_batches = medication.get_batches()
        self.assertGreater(len(liste_batches), 0)
        for batch in liste_batches:
            self.assertIsNotNone(batch.lotNumber)

    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_get_medication_by_tradename)
    def test_obtenir_medication_fhir_visitor_par_trade_name(self, mocked_get_medication_by_tradename):
        medication = MedicationFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer yfsadfsdf="},
            validate_certs=False)
        medication.get_by_trade_name(trade_name="TWINRIX")
        self.assertTrue(type(medication.fhir_resource) is Medication)

    def test_obtenir_default_quantity_for_medication_batch(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        f = open("{0}/exemples/medication.json".format(this_dir),"r")
        medication_dict = json.loads(f.read())
        f.close()
        medication = MedicationFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer yfsadfsdf="},
            validate_certs=False,
            resource=medication_dict)
        self.assertTrue(type(medication.fhir_resource) is Medication)
        liste_batches = medication.get_batches()
        batch = liste_batches[0]
        default_quantity = medication.get_default_quantity_for_batch(batch=batch)
        self.assertEqual(default_quantity.value, 0.5)
        self.assertEqual(default_quantity.unit, "ml")

    def test_convertir_un_dictionnaire_en_practitioner_fhir_visitor(self):
        this_dir = os.path.dirname(os.path.abspath(__file__))
        f = open("{0}/exemples/practitioner.json".format(this_dir),"r")
        practitioner_dict = json.loads(f.read())
        f.close()
        practitioner = PractitionerFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer yfsadfsdf="},
            validate_certs=False,
            resource=practitioner_dict)
        self.assertTrue(type(practitioner.fhir_resource) is Practitioner)

    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_search_practitioner)
    def test_rechercher_practitioner(self, mocked_search_practitioner):
        practitioner = PractitionerFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer yfsadfsdf="},
            validate_certs=False)
        bundle = practitioner.search(given="toto", family="tutu")
        self.assertTrue(type(bundle) is BundleFHIR)
        practitioner_entries = bundle.get_entries(recurse=True, resource_type='Practitioner')
        self.assertGreater(len(practitioner_entries), 0)
        self.assertEqual(practitioner_entries[0].get_given()[0],"toto")
        self.assertEqual(practitioner_entries[0].get_family()[0],"tutu")

    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_get_value_set)
    def test_obtenir_valueset(self, mocked_get_value_set):
        value_set = ValueSetFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer yfsadfsdf="},
            validate_certs=False)
        value_set_response = value_set.get_administrationsite()
        self.assertEqual(value_set_response.status_code, 200)
        self.assertEqual(value_set.fhir_resource.name, "SiteAdministration")

    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_get_value_set)
    def test_rechercher_coded_concept_valueset(self, mocked_get_value_set):
        value_set = ValueSetFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer yfsadfsdf="},
            validate_certs=False)
        value_set_response = value_set.get_administrationsite()
        self.assertEqual(value_set_response.status_code, 200)
        code_a_rechercher = "LLFA"
        display_a_rechercher = "Bras Gauche"
        coded_concept = value_set.search_code_system_concept(code=code_a_rechercher)
        self.assertEqual(coded_concept.code, code_a_rechercher)
        coded_concept = value_set.search_code_system_concept(display=display_a_rechercher)
        self.assertEqual(coded_concept.display, display_a_rechercher)
 
    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_get_organization_by_url)
    def test_obtenir_organisation_par_id(self, mocked_get_organization_by_url):
        id_to_get = "10"
        organization = OrganizationFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer eysdfsdf"},
            validate_certs=False
        )
        organization.get_by_id(org_id=id_to_get)
        self.assertEqual(id_to_get, organization.get_id())

    @mock.patch('inspqcommun.hl7.fhir.requests.get', side_effect=mocked_get_organization_by_url)
    def test_obtenir_organisation_par_reference(self, mocked_get_organization_by_url):
        id_to_get = "10"
        fhir_reference = FHIRReference()
        fhir_reference.reference = "Organization/{0}".format(id_to_get)
        organization = OrganizationFHIR(
            base_uri="/fhir/dstu2",
            base_url="http://fhir.server",
            token_header={"Authorization": "bearer eysdfsdf"},
            validate_certs=False
        )
        organization.get_by_reference(reference=fhir_reference)
        self.assertEqual(id_to_get, organization.get_id())

    def test_definir_organization_period(self):
        org_avec_extension = OrganizationFHIR(resource=organization_rrss_dict)
        date_a_definir = "2000-01-01"
        org_avec_extension.set_effective_from(effective_from=date_a_definir)
        org_effective_from = org_avec_extension.get_effective_from().isostring
        self.assertEquals(date_a_definir,org_effective_from)
        org_avec_extension.set_effective_to(effective_to=date_a_definir)
        org_effective_to = org_avec_extension.get_effective_to().isostring
        self.assertEquals(date_a_definir,org_effective_to)
        org_sans_extension = OrganizationFHIR()
        org_sans_extension.set_effective_from(effective_from=date_a_definir)
        org_effective_from = org_sans_extension.get_effective_from().isostring
        self.assertEquals(date_a_definir,org_effective_from)
        org_sans_extension = OrganizationFHIR()
        org_sans_extension.set_effective_to(effective_to=date_a_definir)
        org_effective_to = org_sans_extension.get_effective_to().isostring
        self.assertEquals(date_a_definir,org_effective_to)

    def test_definir_location_period(self):
        loc_avec_extension = LocationFHIR(resource=location_rrss_dict)
        date_a_definir = "2000-01-01"
        loc_avec_extension.set_effective_from(effective_from=date_a_definir)
        loc_effective_from = loc_avec_extension.get_effective_from().isostring
        self.assertEquals(date_a_definir,loc_effective_from)
        loc_avec_extension.set_effective_to(effective_to=date_a_definir)
        loc_effective_to = loc_avec_extension.get_effective_to().isostring
        self.assertEquals(date_a_definir,loc_effective_to)
        org_sans_extension = LocationFHIR()
        org_sans_extension.set_effective_from(effective_from=date_a_definir)
        loc_effective_from = org_sans_extension.get_effective_from().isostring
        self.assertEquals(date_a_definir,loc_effective_from)
        org_sans_extension = LocationFHIR()
        org_sans_extension.set_effective_to(effective_to=date_a_definir)
        loc_effective_to = org_sans_extension.get_effective_to().isostring
        self.assertEquals(date_a_definir,loc_effective_to)

