from impl.Neo4JKnowledgeGraphImpl import Neo4JKnowledgeGraphImpl as neo4jKG

TEXT_PROMPT = "Beyoncé Giselle Knowles-Carter (/bi:'jɒnseɪ/bee-YON-say) (born September 4, 1981) is an American singer, songwriter, record producer and actress. Born and raised in Houston, Texas, she performed in various singing and dancing competitions as a child, and rose to fame in the late 1990s as lead singer of R&B girl-group Destiny's Child. Managed by her father, Mathew Knowles, the group became one of the world's best-selling girl groups of all time. Their hiatus saw the release of Beyoncé's debut album, Dangerously in Love (2003), which established her as a solo artist worldwide, earned five Grammy Awards and featured the Billboard Hot 100 number-one singles \"Crazy in Love\" and \"Baby Boy\"."

if __name__ == '__main__':
    kg = neo4jKG(TEXT_PROMPT)
    kg.clear_graph()
    kg.create_knowledge_graph()
    