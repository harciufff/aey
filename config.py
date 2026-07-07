import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Google API configuration
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

    # Neo4j database configuration
    NEO4J_URI = os.getenv('NEO4J_URI', 'bolt://localhost:7687')
    NEO4J_USERNAME = os.getenv('NEO4J_USERNAME', 'neo4j')
    NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

    # Target URLs to scan
    TARGET_URLS = os.getenv('SITI_DA_SCANSIONARE', '').split(',') if os.getenv('SITI_DA_SCANSIONARE') else []

    # Allowed semantic relations between entities
    ALLOWED_RELATIONS = ["EXTENDS", "CONTRADICTS", "SUPPORTS", "EXEMPLIFIES", "LINKS_TO"]
