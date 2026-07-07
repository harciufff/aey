import argparse
import sys
import asyncio
from crawler import run_web_crawler
from ingestion import process_and_ingest_text
from search import query_knowledge_graph
from database import initialize_db_connection, close_db_connection


async def run_ingestion_flow():
    # Execute nightly ingestion flow: crawl web pages and ingest into knowledge graph
    print("\n=== Starting Nightly Ingestion Flow ===\n")

    # Run async web crawler to fetch content from target URLs
    crawled_texts = await run_web_crawler()

    # Check if any content was successfully crawled
    if not crawled_texts:
        print("No content was crawled. Exiting ingestion flow.")
        return

    print(f"\n=== Processing {len(crawled_texts)} crawled pages ===\n")

    # Process and ingest each crawled page into the knowledge graph
    for index, raw_text in enumerate(crawled_texts, 1):
        print(f"Processing page {index}/{len(crawled_texts)}...")
        try:
            process_and_ingest_text(raw_text)
            print(f"Successfully ingested page {index}")
        except Exception as e:
            print(f"Failed to ingest page {index}: {str(e)}")
            continue

    print("\n=== Ingestion Flow Complete ===\n")


def run_interactive_chat():
    # Start interactive query loop for real-time knowledge graph queries
    print("\n=== Starting Interactive Chat Flow ===\n")
    print("Ask questions about the knowledge graph. Type 'exit' to quit.\n")

    while True:
        # Get user query from terminal input
        try:
            user_input = input("Your query: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting chat...")
            break

        # Check for exit command
        if user_input.lower() == 'exit':
            print("Exiting chat...")
            break

        # Skip empty queries
        if not user_input:
            continue

        # Query the knowledge graph and display the answer
        try:
            answer = query_knowledge_graph(user_input)
            print(f"\nAnswer: {answer}\n")
        except Exception as e:
            print(f"Error processing query: {str(e)}\n")


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Knowledge Graph RAG System")
    parser.add_argument(
        '--cron',
        action='store_true',
        help='Run in nightly ingestion mode (crawl and ingest data)'
    )
    args = parser.parse_args()

    # Initialize database connection before any operations
    print("Initializing database connection...")
    try:
        initialize_db_connection()
    except Exception as e:
        print(f"Failed to initialize database connection: {str(e)}")
        sys.exit(1)

    try:
        # Execute appropriate flow based on command line arguments
        if args.cron:
            # Run nightly ingestion flow (crawl and ingest)
            asyncio.run(run_ingestion_flow())
        else:
            # Run interactive chat flow (query loop)
            run_interactive_chat()

    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

    finally:
        # Clean up database connection on exit
        close_db_connection()
        print("System shutdown complete")


if __name__ == "__main__":
    main()
