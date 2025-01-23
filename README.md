## Quickstart with Weaviate and PromptQL for Semantic and Keyword Search

This tutorial shows you how to connect your Weaviate cluster and perform semantic search with PromptQL.

## Add your API keys for Weaviate and Cohere

We'll be using the Cohere API key to create embeddings for our unstructured data via Weaviate Client. We also need the Weaviate Cloud URL and Weaviate API Key. Both can be obtained from Weaviate Cloud.

In your project directory, add the key to your `.env` file.

First, copy  the `env.sample` file to `.env`

```bash copy
cp env.sample .env
```

Now, update the API Keys

```bash copy
APP_PYTHON_COHERE_API_KEY='....'
APP_PYTHON_WCD_URL='....'
APP_PYTHON_WCD_API_KEY='....'
```

**Note**: Feel free to modify the embedding configuration in Weaviate Client to use something other than Cohere and configure the API key accordingly.

## Create a collection and load data

After configuring the `.env` values with the above credentials, continue with the data loading.

Head to `app/connector/python` and execute
```bash copy
python3 load-data.py
```

This will create a movie collection and load sample movie data with vector embedding using Cohere.

## Write custom functions

In `mysupergraph/app/connector/mypython/functions.py`, add additional functions based on requirements.

We already have two functions.

`semantic_search` and `keyword_search`. They are exposed as functions to PromptQL.

## Introspect your connector

Make sure Docker is running, then execute:

```bash copy
ddn connector introspect python
```

Tip: Run in debug mode with the `--log-level DEBUG` to understand what is going on with the introspection:

## Build your supergraph

Create your supergraph build locally:

```bash copy
ddn supergraph build local
```

## Start your supergraph locally

```bash copy
ddn run docker-start
```

## Head to your local DDN console

Run the following from your project's directory:

```bash copy
ddn console --local
```

## Talk to your data

Now, you can ask semantic questions on your data:

```text copy
> Movies with dystopian future
> Historical movies
```