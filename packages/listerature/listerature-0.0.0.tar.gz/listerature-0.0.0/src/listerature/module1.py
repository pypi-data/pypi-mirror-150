from scholarly import scholarly

def scholtest():
	search_query = scholarly.search_author('James Gregory')
	first_author_result = next(search_query)
	scholarly.pprint(first_author_result)
