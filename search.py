from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from neo4j import GraphDatabase
from config import Config


def query_knowledge_graph(user_query):
    # Validate input query
    if not user_query or not user_query.strip():
        print("No query provided")
        return ""

    try:
        print(f"Processing query: {user_query}")

        # Initialize embeddings for query
        embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=Config.GOOGLE_API_KEY
        )

        # Embed the user query
        query_embedding = embeddings.embed_query(user_query)

        # Connect to Neo4j directly
        driver = GraphDatabase.driver(
            Config.NEO4J_URI,
            auth=(Config.NEO4J_USERNAME, Config.NEO4J_PASSWORD)
        )

        # Query Neo4j to retrieve graph structure with nodes and relationships
        with driver.session() as session:
            # Get nodes and their relationships from the knowledge graph
            result = session.run("""
                MATCH (n)-[r]-(m)
                RETURN n, r, m
                LIMIT 100
            """)

            # Format context as [NodeA] -RELATION-> [NodeB]
            context_parts = []
            seen_triples = set()

            for record in result:
                n = record["n"]
                r = record["r"]
                m = record["m"]

                # Extract node labels and IDs
                n_label = list(n.labels)[0] if n.labels else "Node"
                m_label = list(m.labels)[0] if m.labels else "Node"
                n_id = n.get("id", "")
                m_id = m.get("id", "")
                r_type = r.type

                # Format as [Entity: ID] -RELATIONSHIP-> [Entity: ID]
                triple = f"[{n_label}: {n_id}] -{r_type}-> [{m_label}: {m_id}]"

                # Avoid duplicate triples
                if triple not in seen_triples:
                    seen_triples.add(triple)
                    context_parts.append(triple)

            # Join all triples into context string
            context = "\n".join(context_parts)

        driver.close()

        # Check if we have any context
        if not context:
            print("No graph data found in database")
            return "The knowledge graph is empty. Please run ingestion first with: python main.py --cron"

        # Initialize LLM
        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=Config.GOOGLE_API_KEY,
            temperature=0
        )

        # Build prompt with graph structure
        system_prompt = (
            "You are a knowledge graph assistant. "
            "Answer the user's question using ONLY the graph structure provided below. "
            "The graph shows entities and their relationships in the format: [Entity: Name] -RELATIONSHIP-> [Entity: Name]. "
            "Use only the facts explicitly stated in this graph structure. "
            "If the graph does not contain enough information to answer the question, "
            "clearly state: 'I don't have enough information in the knowledge graph to answer that question.'"
        )

        # Combine system prompt, context, and user query
        full_prompt = f"{system_prompt}\n\nKnowledge Graph:\n{context}\n\nUser Question: {user_query}\n\nAnswer:"

        # Get response from LLM
        response = llm.invoke(full_prompt)
        answer = response.content if hasattr(response, 'content') else str(response)

        print("Query processed successfully")
        return answer

    except Exception as e:
        print(f"Error processing query: {str(e)}")
        raise
