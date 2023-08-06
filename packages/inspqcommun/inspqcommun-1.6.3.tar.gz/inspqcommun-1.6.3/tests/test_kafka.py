#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from unittest import TestCase
from inspqcommun.kafka.producteur import obtenirConfigurationsProducteurDepuisVariablesEnvironnement, creerProducteur, publierMessage
from inspqcommun.kafka.consommateur import obtenirConfigurationsConsommateurDepuisVariablesEnvironnement, creerConsommateur, consommerTopics, decode_from_bytes
import json
class KafkaTestCase(TestCase):
    def test_creer_producteur(self):
        producer_kafka_config = obtenirConfigurationsProducteurDepuisVariablesEnvironnement()
        producer = creerProducteur(config=producer_kafka_config)
    def test_produire_message(self):
        producer_kafka_config = obtenirConfigurationsProducteurDepuisVariablesEnvironnement()
        producer = creerProducteur(config=producer_kafka_config)
        message = {}
        message['key'] = "1".encode()
        message['value'] = "test".encode()
        publierMessage(producteur=producer,message=message,topic='test')

    def test_produire_message_non_encode(self):
        producer_kafka_config = obtenirConfigurationsProducteurDepuisVariablesEnvironnement()
        producer = creerProducteur(config=producer_kafka_config)
        message = {}
        message['key'] = "1"
        message['value'] = {"id": 1, "value": "test"}
        publierMessage(producteur=producer,message=message,topic='test')

    def test_produire_message_sans_cle(self):
        producer_kafka_config = obtenirConfigurationsProducteurDepuisVariablesEnvironnement()
        producer = creerProducteur(config=producer_kafka_config)
        message = {}
        message['value'] = {"id": 1, "value": "test"}
        publierMessage(producteur=producer,message=message,topic='test')

    def test_produire_message_cle_nulle(self):
        producer_kafka_config = obtenirConfigurationsProducteurDepuisVariablesEnvironnement()
        producer = creerProducteur(config=producer_kafka_config)
        message = {}
        message['key'] = None
        message['value'] = {"id": 1, "value": "test"}
        publierMessage(producteur=producer,message=message,topic='test')

    def test_creer_consommateur(self):
        consumer_kafka_config = obtenirConfigurationsConsommateurDepuisVariablesEnvironnement()
        consumer = creerConsommateur(config=consumer_kafka_config.kafka, topics=['test'])

    def test_consommer_message(self):
        consumer_kafka_config = obtenirConfigurationsConsommateurDepuisVariablesEnvironnement()
        consumer = creerConsommateur(config=consumer_kafka_config.kafka, topics=['test'])
        messages = consommerTopics(consommateur=consumer, topics=['test'])

        for message in messages['test']:
            self.assertTrue("value" in message)

    def test_decode_string(self):
        value = "e".encode()
        decoded = decode_from_bytes(value=value)
        self.assertEquals(value.decode(),decoded)

    def test_decode_dict(self):
        dict_to_decode = {
            "id": 1,
            "value": "test"
        }
        value = json.dumps(dict_to_decode).encode()
        decoded = decode_from_bytes(value=value)
        self.assertEquals(dict_to_decode,decoded)