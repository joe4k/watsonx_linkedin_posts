import streamlit as st
import streamlit_scrollable_textbox as stx

import arxiv
from ibm_watsonx_ai import APIClient

from searchPapers import *
from watsonx_llm_deployments import *

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'search' not in st.session_state:
    st.session_state["search"] = None

if 'searchResults' not in st.session_state:
    st.session_state["searchResults"] = None

if 'paper' not in st.session_state:
    st.session_state["paper"] = None

if 'watsonx_creds' not in st.session_state:
    watsonxCreds = getCredentials()
    st.session_state["watsonx_creds"] = watsonxCreds

if 'watsonx_client' not in st.session_state:
    credentials = {
        "url": watsonxCreds["url"],
        "apikey": watsonxCreds["api_key"]
    }
    client = APIClient(credentials)
    st.session_state["watsonx_client"] = client

if 'addendum' not in st.session_state:
    st.session_state["addendum"] = """
        Thank you to arXiv for use of its open access interoperability.
        This post was generated with assistance from watsonx LLMs """

if 'analyzeButton' not in st.session_state:
    st.session_state["analyzeButton"] = False

def markdown_progress(x: int) -> str:
    '''
    Returns a bar from a number between 0 and 100. 
    '''
    return(f"""![](https://geps.dev/progress/{x})""")

def ascii_progress(x: float, solid: bool = False) -> str:
    '''
    Returns an ascii bar from a number between 0 and 1. 
    The bar has lenght 10
    '''
    nbars = int(min(max(x, 0.0), min(x, 1.0), x) * 10)
    bar = ((("\u2593","\u2588")[solid])*nbars).ljust(10,"\u2591")
    return(bar)

# Main function for the application
def main():
    st.set_page_config(
    page_title='Brand Assistant App',
    layout='wide',
    page_icon=':rocket:'
    )
    
    if 'analyzeButton' in st.session_state:
        st.session_state["analyzeButton"] = False
    
    colx, coly = st.columns([1,20])
    with colx:
        st.image('watsonx_logo.png', width=30)
    with coly:
        st.markdown("##### ***watsonx*** Personal Brand Assistant")

    #    st.title("Personal Brand Assistant")

    ####st.markdown(ascii_progress(0.8))

    with st.sidebar:
        st.markdown("***Search***")
        searchTerm = st.text_input(label="term",help="enter terms to search",placeholder="large language models")
        #st.text_input()
        nResults = st.number_input('number of search results', min_value=1, max_value=10, value=5, step=1)
        if st.button("Search"): 
            searchResults = searchArxiv(searchTerm,nResults)
            if searchResults != None and len(searchResults) > 0:
                st.session_state["searchResults"] = searchResults
    
    cola, colb = st.columns([9,1],gap="small", vertical_alignment="bottom")
    with cola:
        if st.session_state["searchResults"] != None:
            paper_selection = st.selectbox("Select paper for details",options=st.session_state["searchResults"])
            st.session_state["paper"] = paper_selection
    with colb:
        if st.session_state["searchResults"] != None:
            if st.button("Go"):
                st.session_state["analyzeButton"] = True


    if st.session_state["paper"] is not None:
        print("button pressed: ", st.session_state["analyzeButton"])
        if st.session_state["analyzeButton"] == True:
            st.write("Title: ", st.session_state["paper"].title)
            st.write("Link: ", st.session_state["paper"].pdf_url)
            abstract = st.session_state["paper"].summary
            abstract = abstract.replace("\n"," ")
            creds = st.session_state["watsonx_creds"]
            space_id = creds["space_id"]
            deployment_id = creds["deployment_id"]
            eval_id = creds["eval_deployment_id"]
            with st.spinner("Generating post"):
                linkedin_post = generateLinkedInPost(watsonxClient=st.session_state["watsonx_client"],space_id=space_id,deployment_id=deployment_id,input_text=abstract)
                linkedin_post = linkedin_post + st.session_state["addendum"]
            
                col1, col2, col3 = st.columns([4,4,2],vertical_alignment="top")
                with col1:
                    st.write("Original Abstract")
                    stx.scrollableTextbox(abstract,height = 350,fontFamily='Calibri')
                with col2:
                    st.write("Generated LinkedIn Post")
                    stx.scrollableTextbox(linkedin_post,height = 350,fontFamily='Calibri')
                evalResult = evalLLM(watsonxClient=st.session_state["watsonx_client"],space_id=space_id,eval_id=eval_id,org_text=abstract,gen_text=linkedin_post)
                #print("eval Result: ", evalResult)
                evalResult = evalResult.replace("`","").strip()
                #print("mod eval result: ", evalResult)
                with col3:
                    st.markdown("*Faithfulness*",help="faithfulness metric measures how well the generated text correlates with original text")
                    plotval = 10*int(evalResult)
                    ###st.markdown(ascii_progress(plotval))
                    
                    #plotval = float(evalResult)
                    if plotval >= 0 and plotval <= 100:
                    #    print("plot val: ", plotval)
                        st.markdown(markdown_progress(plotval))
                    #    #st.bar_chart({"":[90],"":[10]},horizontal=True,color=["#00ff00","#000000"],x_label=None,y_label=None)
                    #    st.markdown(ascii_progress(plotval))
                    else:
                        print("Error plotval: ", plotval, " eval result: ", evalResult)
              


    


if __name__ == "__main__":
    main()