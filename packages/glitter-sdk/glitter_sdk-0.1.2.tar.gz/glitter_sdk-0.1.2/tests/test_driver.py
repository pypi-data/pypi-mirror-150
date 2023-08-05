# rename to test_driver.py

# Copyright 2022-present glitter, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Test the Glitter driver module."""

import unittest
from glitter_sdk import GlitterClient


class GlitterClientUnitTest(unittest.TestCase):
    glitter_client: GlitterClient
    schema_name = "sample__2"

    @classmethod
    def setUpClass(cls):
        url = 'http://sg1.testnet.glitter.link:26659'
        cls.glitter_client = GlitterClient(url)

    def test_create_schema(self):
        fields = [
            {
                "name": "user_id",
                "type": "string",
                "primary": "true",
                "index": {
                    "type": "keyword"
                }
            },
            {
                "name": "user_name",
                "type": "string",
                "index": {
                    "type": "text"
                }
            },
            {
                "name": "email_address",
                "type": "string",
                "index": {
                    "type": "text",
                    "index": "false"
                }
            }
        ]
        res = self.glitter_client.db.create_schema(self.schema_name, fields)
        self.assertEqual(res['code'], 0)

    def test_get_schema(self):
        res = self.glitter_client.db.get_schema(self.schema_name)
        self.assertEqual(res['code'], 0)

    def test_list_schema(self):
        res = self.glitter_client.db.list_schema()
        self.assertEqual(res['code'], 0)
        self.assertIsNotNone(res['data'].get(self.schema_name))

    def test_put_doc(self):
        demo_doc = {
            "user_id": "123",
            "user_name": "Bob",
            "email_address": "Bob@gmail.com"
        }

        res = self.glitter_client.db.put_doc(self.schema_name, demo_doc)
        self.assertEqual(res['code'], 0)
        self.assertIsNotNone(res['tx'])

    def test_get_docs(self):
        primary_key = "123"
        res = self.glitter_client.db.get_docs(self.schema_name, [primary_key])
        self.assertEqual(res["code"], 0)
        self.assertGreaterEqual(res["data"]["total"], 1)
        self.assertEqual(res["data"]["hits"][primary_key]
                         ["user_id"], primary_key)

    def test_search(self):
        query_word = "Bob"
        query_field = ["user_name"]
        res = self.glitter_client.db.search(
            self.schema_name, query_word, query_field)
        self.assertEqual(res["code"], 0)
        self.assertGreaterEqual(res["data"]["meta"]["page"]["size"], 1)

    def test_app_status(self):
        res = self.glitter_client.db.app_status()
        self.assertEqual(res['code'], 0)
        self.assertEqual(res["code"], 0)

    def test_tx_search(self):
        res = self.glitter_client.chain.tx_search(
            query="tx.hash='EAD611D65C4269A87F6C53E0BBE42381A33763F360A673CC984"
                  "FC8F54971DBE8'")
        self.assertIsNotNone(res['result'])

    def test_block(self):
        res = self.glitter_client.chain.block()
        self.assertIsNotNone(res['result'])

    def test_block_search(self):
        res = self.glitter_client.chain.block_search(
            query="block.height = 12530")
        self.assertIsNotNone(res['result'])


if __name__ == '__main__':
    unittest.main()
