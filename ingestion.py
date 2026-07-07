from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_community.graphs import Neo4jGraph
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document
from config import Config


def process_and_ingest_text(raw_text):
    # Validate input text
    if not raw_text or not raw_text.strip():
        print("No text provided for ingestion")
        return

    try:
        # Initialize Google Gemini LLM with zero temperature for deterministic output
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0
        )

        # Initialize graph transformer with allowed relations from config
        transformer = LLMGraphTransformer(
            llm=llm,
            allowed_relationships=Config.ALLOWED_RELATIONS
        )

        # Connect to Neo4j graph database
        graph = Neo4jGraph(
            url=Config.NEO4J_URI,
            username=Config.NEO4J_USERNAME,
            password=Config.NEO4J_PASSWORD
        )

        print("Processing text and converting to graph documents...")

        # Wrap raw text in Document object for processing
        documents = [Document(page_content=raw_text)]

        # Convert documents into graph documents using the transformer
        graph_documents = transformer.convert_to_graph_documents(documents)

        print(f"Generated {len(graph_documents)} graph documents")

        # Ingest graph documents into Neo4j database
        if graph_documents:
            graph.add_graph_documents(graph_documents)
            print("Successfully ingested graph documents into database")
        else:
            print("No graph documents were generated from the text")

    except Exception as e:
        print(f"Error during text processing and ingestion: {str(e)}")
        raise
