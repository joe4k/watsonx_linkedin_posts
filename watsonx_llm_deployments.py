import os
from dotenv import load_dotenv

#
def getCredentials():
    load_dotenv()
    creds = {
        "api_key": os.getenv("api_key",None),
        "url": os.getenv("url","https://us-south.ml.cloud.ibm.com"),
        "space_id": os.getenv("space_id",None),
        "deployment_id": os.getenv("deployment_id",None),
        "eval_deployment_id": os.getenv("eval_deployment_id",None)
    }
    return creds


# This function takes as input text and generates as output a Linked In post
# highlighting key information in the text
# One use case is to share key highlights from a research paper abstract
def generateLinkedInPost(watsonxClient,space_id,deployment_id,input_text):

    watsonxClient.set.default_space(space_id)

    generated_response = watsonxClient.deployments.generate_text(deployment_id,params={"prompt_variables": {"abstract": input_text}})

    return generated_response


# This function takes as input original text and generated text
# and sends both to an LLM-as-a-judge evaluation to provide a measure
# of how well is the generated text supported by the original text
def evalLLM(watsonxClient,space_id,eval_id,org_text,gen_text):
    watsonxClient.set.default_space(space_id)

    eval_result = watsonxClient.deployments.generate_text(eval_id,params={"prompt_variables": {"context": org_text,"gentext": gen_text}})

    return eval_result

