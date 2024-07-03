import arxiv


# Function to search arxiv
# https://arxiv.org/multi
def searchArxiv(search_term,num_results):
    # append double quotes around search term to search for that specific term
    term = f"\"{search_term}\""

    #search = arxiv.Search(query = "au:del_maestro AND ti:checkerboard")
    # return results where term appears in title or abstract
    # sort results by submitted date
    search_pointer = arxiv.Search(
        query = f"ti: {term} OR abs: {term}",
        max_results = num_results,
        sort_by = arxiv.SortCriterion.SubmittedDate
    )
    print("s: ", search_pointer)

    # Construct the default API client.
    client = arxiv.Client()
        
    search_results = client.results(search_pointer)
    all_results = list(search_results)


    return all_results