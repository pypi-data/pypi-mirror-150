.. _quickstart:

====================
Quickstart
====================

Simple introduction to glitter.

1.Connection
---------------
Connect Glitter network using glitter_sdk package.

.. code-block:: python

     from glitter_sdk import GlitterClient
     client = GlitterClient()

2.Data model
------------------------
In the example below we create a schema which is used to describe data model.
After creation success, you will be able to check the detail of the schema info `here <https://scan.testnet.glitterprotocol.io/txs/D4D9F93B60770952A33BD3C7A8C0F70A72CB78F800AD1C100CA73EBCF2825BDC>`__.

.. tabs::

    .. tab:: Code

        .. code-block:: python

            # Create a schema with a url and title.
            schema = [
                {
                    "name": "url",
                    "type": "string",
                    "primary": "true",
                    "index": {
                        "type": "keyword"
                    }
                },
                {
                    "name": "title",
                    "type": "string",
                    "index": {
                        "type": "text"
                    }
                }
            ]
            res = client.db.create_schema("sample", schema)
            # Get the schema you create.
            client.db.get_schema("sample")


    .. tab:: Output

        .. code-block:: python

            {
              "code": 0,
              "message": "ok",
              "data": {
                "fields": [
                  {
                    "index": {
                      "type": "keyword"
                    },
                    "name": "url",
                    "primary": "true",
                    "type": "string"
                  },
                  {
                    "index": {
                      "type": "text"
                    },
                    "name": "title",
                    "type": "string"
                  }
                ],
                "name": "sample",
                "type": "record"
              }
            }


3.Put doc
------------------------
Put_doc is used to insert a record into the schema you created earlier.
Once success, you will be able to see the details of the transaction `here <https://scan.testnet.glitterprotocol.io/txs/8A62859FD12A9A4D678812D65CE280501595C0B947C150E7182B7F099B213B01>`__.

.. tabs::

    .. tab:: Code

        .. code-block:: python

            put_res = client.db.put_doc("sample", {
                    "url": "https://glitterprotocol.io/",
                    "title": "A Decentralized Content Indexing Network",
                })

    .. tab:: Output

        .. code-block:: python

            # tx is the transaction ID.
            {
              "code": 0,
              "message": "ok",
              "tx": "8A62859FD12A9A4D678812D65CE280501595C0B947C150E7182B7F099B213B01"
            }

4.Search
------------------------
Performing a full-text search which allows you to search for query_word the index.

.. tabs::

    .. tab:: Code

        .. code-block:: python

            # search doc
            search_res = client.db.search(schema_name="sample", query_word="Content Indexing Network")

    .. tab:: Output

        .. code-block:: python

            {
                "code": 0,
                "message": "ok",
                "tx": "",
                "data": {
                    "search_time": 7,
                    "index": "sample",
                    "meta": {
                        "page": {
                            "current_page": 1,
                            "total_pages": 1,
                            "total_results": 1,
                            "size": 10,
                            "sorted_by": ""
                        }
                    },
                    "items": [{
                        "highlight": {
                            "title": ["A Decentralized <span>Content</span> <span>Indexing</span> <span>Network</span>"]
                        },
                        "data": {
                            "_creator": "test_broks",
                            "_schema_name": "sample",
                            "title": "A Decentralized Content Indexing Network",
                            "url": "https://glitterprotocol.io/"
                        }
                    }],
                    "facet": {}
                }
            }

5. Other search examples
------------------------
Below is a list of examples for searching data in rss.

.. code-block:: python

    # Standard query for performing a full-text search.
    client.db.search(schema_name="rss", query_word="oppo")
    # Search 'oppo' in the 'title' query_field.
    client.db.search(schema_name="rss", query_word="oppo", query_field=['title'])
    # Search 'Mobile' in the 'tags' query_field.
    client.db.search(schema_name="rss", query_word="Mobile", query_field=['tags'])
    # Aggregate search result by the "tags" field defined in the schema.
    client.db.search(schema_name="rss", query_word="oppo", query_field=['title', 'description'], filters=[],
                     aggs_field=["tags"])

