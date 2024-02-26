from SPARQLWrapper import SPARQLWrapper, JSON

# Global variables and configurations for SPARQL requests
baseURL = "http://dbpedia.org"
baseURL_Secure = "https://dbpedia.org/"

sparql = SPARQLWrapper(baseURL_Secure + "sparql/")
sparql.setReturnFormat(JSON)


# Handle SPARQL requests, catch and print possible errors
def handleSPARQLResponse():
    try:
        return sparql.queryAndConvert()
    except Exception as e:
        print(e)
        return None


# Returns facades of a given object.
# Example: if facadeName = "Apple Inc", result will include URIs for website, author, company etc.
# TODO: NEEDS TO BE GENERALIZED
def getDBPediaFacades(facadeName):
    facadeQuery = """
      select distinct ?prop where {{
        ?apple a <http://dbpedia.org/ontology/Company> . 
        ?apple rdfs:label ?name.
        filter(regex(?name, "{}")).
        {{?x ?prop ?apple}} union {{?apple ?prop ?y}}
      }}
    """.format(facadeName)
    
    sparql.setQuery(facadeQuery)
    result = handleSPARQLResponse()
    
    if result is None:
        print("Following SPARQL query failed: {}".format(facadeQuery))
    else:
        for r in result["results"]["bindings"]:
            if r["prop"]["value"].startswith(baseURL) or r["prop"]["value"].startswith(baseURL_Secure):
                print(r)


# Perform a search in DBPedia
# TODO: ALLOW SEARCH FILTERS AND GET MORE INFO
def searchInDBPedia(objectName):
    query = """
        SELECT *
        WHERE
        {{ ?searchObject rdfs:label "{}"@en }}
    """.format(objectName)

    sparql.setQuery(query)
    result = handleSPARQLResponse()
    
    if result is None:
        print("Following SPARQL query failed: {}".format(query))
    else:
        for r in result["results"]["bindings"]:
            if r["searchObject"]["value"].startswith(baseURL) or r["searchObject"]["value"].startswith(baseURL_Secure):
                print(r)

getDBPediaFacades("Apple Inc")
searchInDBPedia("Apple Inc")
