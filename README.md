# High-Performance RAG Solution with Pgvectorscale and Python

This project demonstrates setting up and using `pgvectorscale` with Docker and Python, leveraging Gemini's `gemini-1.5-flash` model for embeddings. It combines advanced retrieval techniques with intelligent answer generation based on the retrieved context, using PostgreSQL as a vector database.

## Pgvectorscale Documentation

For more information about using PostgreSQL as a vector database in AI applications with Timescale, check out these resources:

- [GitHub Repository: pgvectorscale](https://github.com/timescale/pgvectorscale)
- [Blog Post: PostgreSQL and Pgvector: Now Faster Than Pinecone, 75% Cheaper, and 100% Open Source](https://www.timescale.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost/)
- [Blog Post: RAG Is More Than Just Vector Search](https://www.timescale.com/blog/rag-is-more-than-just-vector-search/)
- [Blog Post: A Python Library for Using PostgreSQL as a Vector Database in AI Applications](https://www.timescale.com/blog/a-python-library-for-using-postgresql-as-a-vector-database-in-ai-applications/)

## Why PostgreSQL?

Using PostgreSQL with pgvectorscale as your vector database offers several key advantages:

- PostgreSQL is a robust, open-source database with a rich ecosystem of tools, drivers, and connectors.
- Manage both relational and vector data within a single database, reducing operational complexity.
- Pgvectorscale enhances pgvector with faster search capabilities, higher recall, and efficient time-based filtering.

## Prerequisites

- Docker
- Python 3.7+
- Gemini API key
- PostgreSQL GUI client

## Steps

1. Set up Docker environment
2. Connect to the database using a PostgreSQL GUI client
3. In docker db, run command `CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;`
3. Insert document chunks as vectors using embeddings
4. Perform similarity search

## Usage

1. Create a copy of `example.env` and rename it to `.env`
2. Fill in your Gemini API key in `.env`
3. Run the Docker container
4. Install the required Python packages using `pip install -r requirements.txt`
5. Execute `insert_vectors.py` to populate the database
6. Use `similarity_search.py` to perform similarity searches

## Using ANN Search Indexes

Timescale Vector offers indexing options to accelerate similarity queries, particularly beneficial for large vector datasets:

1. Supported indexes:
   - timescale_vector_index (default): A DiskANN-inspired graph index
   - pgvector's HNSW: Hierarchical Navigable Small World graph index
   - pgvector's IVFFLAT: Inverted file index

2. The DiskANN-inspired index provides improved performance. Refer to the [Timescale Vector explainer blog](https://www.timescale.com/blog/pgvector-is-now-as-fast-as-pinecone-at-75-less-cost/) for detailed information and benchmarks.

For optimal query performance, creating an index on the embedding column is recommended, especially for large vector datasets.

## Cosine Similarity in Vector Search

Cosine similarity measures the cosine of the angle between two vectors in a multi-dimensional space. It's a measure of orientation rather than magnitude.

- Range: -1 to 1 (for normalized vectors)
- 1: Vectors point in the same direction (most similar)
- 0: Vectors are orthogonal (unrelated)
- -1: Vectors point in opposite directions (most dissimilar)

### Cosine Distance

In pgvector, the `<=>` operator computes cosine distance, which is 1 - cosine similarity.

- Range: 0 to 2
- 0: Identical vectors (most similar)
- 1: Orthogonal vectors
- 2: Opposite vectors (most dissimilar)

### Interpreting Results

- Lower distance values indicate higher similarity.
- A distance of 0 would mean an exact match.
- Distances closer to 0 indicate high similarity.
- Distances around 1 suggest little to no similarity.
- Distances approaching 2 indicate opposite meanings.
