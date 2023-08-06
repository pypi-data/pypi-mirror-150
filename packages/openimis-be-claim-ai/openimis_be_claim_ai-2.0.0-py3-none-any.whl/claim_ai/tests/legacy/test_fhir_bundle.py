socket_data = {
        "resourceType": "Bundle",
        "entry": [
            {
                "fullUrl": "http://localhost:8001/api_fhir_r4/Claim/EA07F16E-1556-4BA6-95AB-38784D058994",
                "resource": {
                    "resourceType": "Claim",
                    "billablePeriod": {
                        "end": "2020-05-03",
                        "start": "2020-05-03"
                    },
                    "created": "2020-05-03",
                    "diagnosis": [
                        {
                            "diagnosisReference": {
                                "identifier": 4,
                                "reference": "Condition/A02",
                                "type": "Condition"
                            },
                            "sequence": 1,
                            "type": [
                                {
                                    "coding": [
                                        {
                                            "code": "icd_0"
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                    "enterer": {
                        "identifier": {
                            "type": {
                                "coding": [
                                    {
                                        "code": "UUID"
                                    }
                                ]
                            },
                            "use": "usual",
                            "value": "99B9C21B-E7B9-455E-9A23-560109FBBB55"
                        },
                        "reference": "Practitioner/99B9C21B-E7B9-455E-9A23-560109FBBB55",
                        "type": "Practitioner"
                    },
                    "facility": {
                        "identifier": {
                            "type": {
                                "coding": [
                                    {
                                        "code": "UUID"
                                    }
                                ]
                            },
                            "use": "usual",
                            "value": "EF9E8621-42E8-4C81-BB41-00A55F4DF467"
                        },
                        "reference": "VIDS001/EF9E8621-42E8-4C81-BB41-00A55F4DF467",
                        "type": "VIDS001"
                    },
                    "id": "EA07F16E-1556-4BA6-95AB-38784D058994",
                    "identifier": [
                        {
                            "type": {
                                "coding": [
                                    {
                                        "code": "UUID"
                                    }
                                ]
                            },
                            "use": "usual",
                            "value": "EA07F16E-1556-4BA6-95AB-38784D058994"
                        },
                        {
                            "type": {
                                "coding": [
                                    {
                                        "code": "MR"
                                    }
                                ]
                            },
                            "use": "usual",
                            "value": "CID00001"
                        }
                    ],
                    "insurance": [
                        {
                            "coverage": {
                                "identifier": {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "UUID"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "AB2442D3-E430-4C9F-A78D-F35ACD9B6AE8"
                                },
                                "reference": "Coverage/AB2442D3-E430-4C9F-A78D-F35ACD9B6AE8",
                                "type": "Coverage"
                            },
                            "focal": True,
                            "sequence": 0
                        }
                    ],
                    "item": [
                        {
                            "category": {
                                "text": "item"
                            },
                            "extension": [
                                {
                                    "url": "Medication",
                                    "valueReference": {
                                        "identifier": {
                                            "type": {
                                                "coding": [
                                                    {
                                                        "code": "UUID"
                                                    }
                                                ]
                                            },
                                            "use": "usual",
                                            "value": "00B4F099-6122-4327-B033-0872FB1027D8"
                                        },
                                        "reference": "Medication/00B4F099-6122-4327-B033-0872FB1027D8",
                                        "type": "Medication"
                                    }
                                }
                            ],
                            "productOrService": {
                                "text": "0182"
                            },
                            "quantity": {
                                "value": 2.0
                            },
                            "sequence": 1,
                            "unitPrice": {
                                "currency": "$",
                                "value": 10.0
                            }
                        },
                        {
                            "category": {
                                "text": "service"
                            },
                            "extension": [
                                {
                                    "url": "ActivityDefinition",
                                    "valueReference": {
                                        "identifier": {
                                            "type": {
                                                "coding": [
                                                    {
                                                        "code": "UUID"
                                                    }
                                                ]
                                            },
                                            "use": "usual",
                                            "value": "9FD65C19-6889-46D8-9572-A586D17CF286"
                                        },
                                        "reference": "ActivityDefinition/9FD65C19-6889-46D8-9572-A586D17CF286",
                                        "type": "ActivityDefinition"
                                    }
                                }
                            ],
                            "productOrService": {
                                "text": "A1"
                            },
                            "quantity": {
                                "value": 1.0
                            },
                            "sequence": 2,
                            "unitPrice": {
                                "currency": "$",
                                "value": 400.0
                            }
                        }
                    ],
                    "patient": {
                        "identifier": {
                            "type": {
                                "coding": [
                                    {
                                        "code": "UUID"
                                    }
                                ]
                            },
                            "use": "usual",
                            "value": "CB8497C2-44E6-4E55-97B5-A88B6C3DEDB3"
                        },
                        "reference": "105000002/CB8497C2-44E6-4E55-97B5-A88B6C3DEDB3",
                        "type": "105000002"
                    },
                    "priority": {
                        "coding": [
                            {
                                "code": "normal"
                            }
                        ]
                    },
                    "provider": {
                        "identifier": {
                            "type": {
                                "coding": [
                                    {
                                        "code": "UUID"
                                    }
                                ]
                            },
                            "use": "usual",
                            "value": "99B9C21B-E7B9-455E-9A23-560109FBBB55"
                        },
                        "reference": "PractitionerRole/99B9C21B-E7B9-455E-9A23-560109FBBB55",
                        "type": "PractitionerRole"
                    },
                    "status": "active",
                    "total": {
                        "currency": "$",
                        "value": 1670.0
                    },
                    "type": {
                        "text": "O"
                    },
                    "use": "claim",
                    "contained": [
                        {
                            "resourceType": "Patient",
                            "address": [
                                {
                                    "text": "",
                                    "type": "physical",
                                    "use": "home"
                                },
                                {
                                    "text": "0.0 0.0",
                                    "type": "both",
                                    "use": "home"
                                }
                            ],
                            "birthDate": "1993-06-09",
                            "extension": [
                                {
                                    "url": "https://openimis.atlassian.net/wiki/spaces/OP/pages/960069653/isHead",
                                    "valueBoolean": False
                                },
                                {
                                    "url": "https://openimis.atlassian.net/wiki/spaces/OP/pages/960331779/registrationDate",
                                    "valueDateTime": "2018-03-27T07:48:52.510000"
                                },
                                {
                                    "url": "https://openimis.atlassian.net/wiki/spaces/OP/pages/960495619/locationCode",
                                    "valueReference": {
                                        "identifier": {
                                            "type": {
                                                "coding": [
                                                    {
                                                        "code": "UUID"
                                                    }
                                                ]
                                            },
                                            "use": "usual",
                                            "value": "63A90675-1BC9-42C6-967B-4D6EE36D4073"
                                        },
                                        "reference": "Location/63A90675-1BC9-42C6-967B-4D6EE36D4073",
                                        "type": "Location"
                                    }
                                },
                                {
                                    "url": "https://openimis.atlassian.net/wiki/spaces/OP/pages/960069653/group",
                                    "valueReference": {
                                        "identifier": {
                                            "type": {
                                                "coding": [
                                                    {
                                                        "code": "UUID"
                                                    }
                                                ]
                                            },
                                            "use": "usual",
                                            "value": "A3029606-76E6-4A7B-9A2A-2435B61B25A1"
                                        },
                                        "reference": "Group/A3029606-76E6-4A7B-9A2A-2435B61B25A1",
                                        "type": "Group"
                                    }
                                }
                            ],
                            "gender": "female",
                            "id": "Patient/CB8497C2-44E6-4E55-97B5-A88B6C3DEDB3",
                            "identifier": [
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "UUID"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "CB8497C2-44E6-4E55-97B5-A88B6C3DEDB3"
                                },
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "SB"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "105000002"
                                },
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "PPN"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": ""
                                }
                            ],
                            "link": [
                                {
                                    "other": {
                                        "identifier": {
                                            "type": {
                                                "coding": [
                                                    {
                                                        "code": "UUID"
                                                    }
                                                ]
                                            },
                                            "use": "usual",
                                            "value": "E428D2A2-3115-4E0E-B4B4-00D536EBC99B"
                                        },
                                        "reference": "Patient/E428D2A2-3115-4E0E-B4B4-00D536EBC99B",
                                        "type": "Patient"
                                    },
                                    "type": "Spouse"
                                }
                            ],
                            "name": [
                                {
                                    "family": "Ilina",
                                    "given": [
                                        "Doni"
                                    ],
                                    "use": "usual"
                                }
                            ],
                            "photo": [
                                {
                                    "creation": "2018-03-27",
                                    "url": "Images\\Updated\\105000002_E00001_20180327_0.0_0.0.jpg"
                                }
                            ],
                            "telecom": [
                                {
                                    "use": "home",
                                    "value": ""
                                },
                                {
                                    "use": "home",
                                    "value": ""
                                }
                            ]
                        },
                        {
                            "resourceType": "Condition",
                            "code": {
                                "coding": [
                                    {
                                        "code": "A02"
                                    }
                                ],
                                "text": "Other salmonella infections"
                            },
                            "id": "Condition/4",
                            "identifier": [
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "ACSN"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "4"
                                },
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "DC"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "A02"
                                }
                            ],
                            "recordedDate": "2018-03-19T07:02:37.970000",
                            "subject": {
                                "type": "Patient"
                            }
                        },
                        {
                            "resourceType": "HealthcareService",
                            "category": [
                                {
                                    "coding": [
                                        {
                                            "code": "COMM"
                                        }
                                    ],
                                    "text": "Dispensary"
                                }
                            ],
                            "extraDetails": "Uitly road 1",
                            "id": "HealthService/EF9E8621-42E8-4C81-BB41-00A55F4DF467",
                            "identifier": [
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "UUID"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "EF9E8621-42E8-4C81-BB41-00A55F4DF467"
                                },
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "FI"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "VIDS001"
                                }
                            ],
                            "location": [
                                {
                                    "identifier": {
                                        "type": {
                                            "coding": [
                                                {
                                                    "code": "UUID"
                                                }
                                            ]
                                        },
                                        "use": "usual",
                                        "value": "841419DF-29AB-48DC-B40D-E5A6DE8B1E1E"
                                    },
                                    "reference": "Location/841419DF-29AB-48DC-B40D-E5A6DE8B1E1E",
                                    "type": "Location"
                                }
                            ],
                            "name": "Viru Dispensary",
                            "program": [
                                {
                                    "coding": [
                                        {
                                            "code": "G"
                                        }
                                    ],
                                    "text": "Government"
                                }
                            ],
                            "type": [
                                {
                                    "coding": [
                                        {
                                            "code": "O"
                                        }
                                    ],
                                    "text": "Out-patient"
                                }
                            ]
                        },
                        {
                            "resourceType": "Practitioner",
                            "birthDate": "1977-11-13",
                            "id": "Practitioner/99B9C21B-E7B9-455E-9A23-560109FBBB55",
                            "identifier": [
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "UUID"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "99B9C21B-E7B9-455E-9A23-560109FBBB55"
                                },
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "FILL"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "VIDS0011"
                                }
                            ],
                            "name": [
                                {
                                    "family": "Duikolau",
                                    "given": [
                                        "Juolpio"
                                    ],
                                    "use": "usual"
                                }
                            ]
                        },
                        {
                            "resourceType": "Medication",
                            "code": {
                                "coding": [
                                    {
                                        "code": "0182"
                                    }
                                ],
                                "text": "PARACETAMOL TABS 500 MG"
                            },
                            "extension": [
                                {
                                    "url": "unitPrice",
                                    "valueMoney": {
                                        "currency": "$",
                                        "value": 10.0
                                    }
                                },
                                {
                                    "url": "frequency",
                                    "valueInteger": 0
                                },
                                {
                                    "url": "topic",
                                    "valueCodeableConcept": {
                                        "coding": [
                                            {
                                                "code": "DefinitionTopic"
                                            }
                                        ],
                                        "text": "D"
                                    }
                                },
                                {
                                    "url": "useContextGender",
                                    "valueUsageContext": {
                                        "code": {
                                            "code": "gender"
                                        },
                                        "valueCodeableConcept": {
                                            "coding": [
                                                {
                                                    "code": "M",
                                                    "display": "Male"
                                                },
                                                {
                                                    "code": "F",
                                                    "display": "Female"
                                                }
                                            ],
                                            "text": "Male or Female"
                                        }
                                    }
                                },
                                {
                                    "url": "useContextAge",
                                    "valueUsageContext": {
                                        "code": {
                                            "code": "age"
                                        },
                                        "valueCodeableConcept": {
                                            "coding": [
                                                {
                                                    "code": "A",
                                                    "display": "Adult"
                                                },
                                                {
                                                    "code": "K",
                                                    "display": "Kid"
                                                }
                                            ],
                                            "text": "Adult or Kid"
                                        }
                                    }
                                },
                                {
                                    "url": "useContextVenue",
                                    "valueUsageContext": {
                                        "code": {
                                            "code": "venue"
                                        },
                                        "valueCodeableConcept": {
                                            "coding": [
                                                {
                                                    "code": "O",
                                                    "display": "Out-patient"
                                                }
                                            ],
                                            "text": "Clinical Venue"
                                        }
                                    }
                                },
                                {
                                    "url": "useContextLevel",
                                    "valueUsageContext": {
                                        "code": {
                                            "code": "level"
                                        },
                                        "valueCodeableConcept": {
                                            "coding": [
                                                {
                                                    "code": "M",
                                                    "display": "Medication"
                                                }
                                            ],
                                            "text": "Item Level"
                                        }
                                    }
                                }
                            ],
                            "form": {
                                "coding": [
                                    {
                                        "code": "package"
                                    }
                                ],
                                "text": "1000 TABLETS"
                            },
                            "id": "Medication/00B4F099-6122-4327-B033-0872FB1027D8",
                            "identifier": [
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "UUID"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "00B4F099-6122-4327-B033-0872FB1027D8"
                                },
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "IC"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "0182"
                                }
                            ]
                        },
                        {
                            "resourceType": "ActivityDefinition",
                            "date": "2017-01-01T00:00:00",
                            "extension": [
                                {
                                    "url": "unitPrice",
                                    "valueMoney": {
                                        "currency": "$",
                                        "value": 400.0
                                    }
                                },
                                {
                                    "url": "frequency",
                                    "valueInteger": 0
                                }
                            ],
                            "id": "ActivityDefinition/9FD65C19-6889-46D8-9572-A586D17CF286",
                            "identifier": [
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "UUID"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "9FD65C19-6889-46D8-9572-A586D17CF286"
                                },
                                {
                                    "type": {
                                        "coding": [
                                            {
                                                "code": "SC"
                                            }
                                        ]
                                    },
                                    "use": "usual",
                                    "value": "A1"
                                }
                            ],
                            "name": "A1",
                            "status": "active",
                            "title": "General Consultation",
                            "topic": [
                                {
                                    "coding": [
                                        {
                                            "code": "DefinitionTopic"
                                        }
                                    ],
                                    "text": "P"
                                }
                            ],
                            "useContext": [
                                {
                                    "code": {
                                        "code": "useContextGender"
                                    },
                                    "valueCodeableConcept": {
                                        "coding": [
                                            {
                                                "code": "F",
                                                "display": "Female"
                                            }
                                        ],
                                        "text": "Male or Female"
                                    }
                                },
                                {
                                    "code": {
                                        "code": "useContextAge"
                                    },
                                    "valueCodeableConcept": {
                                        "coding": [
                                            {
                                                "code": "A",
                                                "display": "Adult"
                                            }
                                        ],
                                        "text": "Adult or Kid"
                                    }
                                },
                                {
                                    "code": {
                                        "code": "useContextVenue"
                                    },
                                    "valueCodeableConcept": {
                                        "coding": [
                                            {
                                                "code": "O",
                                                "display": "Out-patient"
                                            }
                                        ],
                                        "text": "Clinical Venue"
                                    }
                                },
                                {
                                    "code": {
                                        "code": "useContextLevel"
                                    },
                                    "valueCodeableConcept": {
                                        "coding": [
                                            {
                                                "code": "S",
                                                "display": "Simple Service"
                                            }
                                        ],
                                        "text": "Service Level"
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        ]
}
