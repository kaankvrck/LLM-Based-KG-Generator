import spacy
from py2neo import Graph, Node, Relationship
import en_core_web_sm
import os

NEO4J_DEFAULT_DATABASE = "ontologydbms"
NEO4J_DEFAULT_PASSWORD = os.environ.get("NEO4J_ONTOLOGYDBMS_PASSWORD")

class Neo4JKnowledgeGraphImpl:
    def __init__(self, prompt = None, neo4j_db_name = None, neo4j_db_password = None) -> None:
        self.prompt = prompt
        if prompt == None:
            self.knowledge_graph = None
        else:
            self.knowledge_graph = Graph(
                name=       NEO4J_DEFAULT_DATABASE if neo4j_db_name is None else neo4j_db_name,
                password=   NEO4J_DEFAULT_PASSWORD if neo4j_db_password is None else neo4j_db_password
            )
        self.nlp = en_core_web_sm.load()

    def clear_graph(self):
        print("[+] Clearing graph data...")
        self.knowledge_graph.delete_all()
        print("[+] Clearing knowledge graph completed!")
        return True
    
    def create_knowledge_graph(self):
        print("[+] Start creating KG...")

        if self.prompt == None:
            print("[+] This object is not instantiated with a prompt! Please set a text prompt first.")
            return False
        elif self.nlp == None:
            print("[+] This object is not instantiated correctly! Please use default constructor so that NLP library can be initialized properly.")
            return False
        
        doc = self.nlp(self.prompt)
        article_node = Node("Article", text="Beyonce Article")
        self.knowledge_graph.create(article_node)

        entities = {}
        for ent in doc.ents:
            entities[ent.text] = Node(ent.label_, name=ent.text)

        for token in doc:
            if token.dep_ != "ROOT" and token.head.text in entities and token.text in entities:
                head_node = entities[token.head.text]
                dependent_node = entities[token.text]
                # Create relationship between nodes
                rel_entity_dependency = Relationship(head_node, token.dep_, dependent_node)
                self.knowledge_graph.create(rel_entity_dependency)

        # Create relationships between entities and the main article node
        for entity_node in entities.values():
            rel_article_entity = Relationship(article_node, "mentions", entity_node)
            self.knowledge_graph.create(rel_article_entity)

        print("[+] Finished creating KG!")
        return True