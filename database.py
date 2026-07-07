from neo4j import GraphDatabase
from config import Config

# Global driver instance for database connections
driver = None


def initialize_db_connection():
    global driver

    try:
        # Create Neo4j driver instance with credentials from config
        driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD)
        )

        # Verify connectivity by running a simple query
        driver.verify_connectivity()

        print(f"Successfully connected to Neo4j at {Config.NEO4J_URI}")
        return driver

    except Exception as e:
        print(f"Failed to initialize database connection: {str(e)}")
        driver = None
        raise


def close_db_connection():
    global driver

    try:
        if driver is not None:
            driver.close()
            print("Database connection closed successfully")
            driver = None
        else:
            print("No active database connection to close")

    except Exception as e:
        print(f"Error while closing database connection: {str(e)}")


def reset_graph_database():
    global driver

    try:
        # Ensure driver is initialized
        if driver is None:
            print("Database driver not initialized. Attempting to connect...")
            initialize_db_connection()

        # Execute query to delete all nodes and relationships
        with driver.session() as session:
            result = session.run("MATCH (n) DETACH DELETE n")
            result.consume()
            print("Graph database has been completely reset")

    except Exception as e:
        print(f"Failed to reset graph database: {str(e)}")
        raise
