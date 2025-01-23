"""
functions.py

This is an example of how you can use the Python SDK's built-in Function connector to easily write Python code.
When you add a Python Lambda connector to your Hasura project, this file is generated for you!

In this file you'll find code examples that will help you get up to speed with the usage of the Hasura lambda connector.
If you are an old pro and already know what is going on you can get rid of these example functions and start writing your own code.
"""
import os
import weaviate
from weaviate.classes.init import Auth
import weaviate.classes.config as wc
import weaviate.classes.query as wq

from hasura_ndc import start
from hasura_ndc.function_connector import FunctionConnector
from pydantic import BaseModel, Field # You only need this import if you plan to have complex inputs/outputs, which function similar to how frameworks like FastAPI do
from hasura_ndc.errors import UnprocessableContent
from typing import Annotated

# Weaviate Environment Variables
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
cohere_api_key = os.environ["COHERE_API_KEY"]

client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,                                    # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(wcd_api_key),             # Replace with your Weaviate Cloud key
    headers={"X-Cohere-Api-Key": cohere_api_key}
)

connector = FunctionConnector()

class Movies(BaseModel):
  title: str

# Semantic search to find similar entities in weaviate
@connector.register_query # This is how you register a query
def semantic_search(query: str) -> list[Movies]:
    # do near by search with weaviate python client
    # Get the collection
    movies = client.collections.get("Movie")

    # Perform query
    response = movies.query.near_text(
        query=query, limit=5, return_metadata=wq.MetadataQuery(distance=True)
    )

    movies_list = []
    # Inspect the response
    for o in response.objects:
        print("XXXXXXX")
        print(o.properties)
        print(o.properties["release_date"])
        print(
            o.properties["title"]
        )  # Print the title and release year (note the release date is a datetime object)
        movies_list.append(Movies(title=o.properties["title"]))
        print(
            f"Distance to query: {o.metadata.distance:.3f}\n"
        )  # Print the distance of the object from the query

    return movies_list

# This is an example of a keyword search function which uses the BM25 algorithm to find the most relevant Movie entities in Weaviate
@connector.register_query # This is how you register a query
def keyword_search(query: str) -> list[Movies]:
    # Get the collection
    movies = client.collections.get("Movie")

    # Perform query
    response = movies.query.bm25(
        query="history", limit=5, return_metadata=wq.MetadataQuery(score=True)
    )

    movies_list = []
    # Inspect the response
    for o in response.objects:
        print(
            o.properties["title"]
        )  # Print the title and release year (note the release date is a datetime object)
        movies_list.append(Movies(title=o.properties["title"]))
        print(
            f"BM25 score: {o.metadata.score:.3f}\n"
        )  # Print the BM25 score of the object from the query
    return movies_list

if __name__ == "__main__":
    start(connector)
