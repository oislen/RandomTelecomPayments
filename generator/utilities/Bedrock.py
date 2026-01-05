import json
import boto3
from beartype import beartype

class Bedrock():
    """
    Bedrock AWS API client wrapper for invoking language models.
    This class provides a simplified interface to interact with AWS Bedrock runtime,
    enabling prompt-based interactions with language models like Llama 3.
    
    Parameters
    ----------
    session : boto3.Session
        A Boto3 session object configured with appropriate AWS credentials.
    model_region: str
        The AWS region where the Bedrock model is hosted.
    model_id: str
        The identifier of the Bedrock model to use.
    
    Attributes
    ----------
    client: boto3.Session.client
        Boto3 Bedrock runtime client for model invocation.
    model_id: str
        The identifier of the Bedrock model to use.
    
    References
    ----------
    https://docs.aws.amazon.com/general/latest/gr/bedrock.html
    """
    @beartype
    def __init__(
        self,
        session:boto3.Session,
        model_region="us-east-1",
        model_id:str="meta.llama3-8b-instruct-v1:0",
        ):
        self.client = session.client("bedrock-runtime", region_name=model_region)
        self.model_id = model_id
    
    @beartype
    def prompt(
        self,
        user_prompt:str,
        system_prompt:str="",
        top_p:float=0.5,
        temperature:float=0.5,
        max_gen_len:int=512,
        ) -> str:
        """
        Invoke the Bedrock model with the provided prompts and generation parameters.
        
        Formats the user and system prompts according to the Llama 2 chat template,
        sends a request to the configured Bedrock model, and returns the generated response.
        
        Parameters
        ----------
        user_prompt : str
            The main prompt or query to send to the model.
        system_prompt : str, optional
            System-level instructions for the model behavior. Defaults to "".
        top_p : float, optional
            Nucleus sampling parameter controlling diversity. Defaults to 0.5.
        temperature : float, optional
            Temperature parameter controlling randomness. Defaults to 0.5.
        max_gen_len : int, optional
            Maximum length of the generated response. Defaults to 512.
        
        Returns
        -------
        str:
            The generated text response from the Bedrock model.
        
        Raises
        ------
            Exception: If the model invocation fails.
        
        Examples
        --------
        ```
        bedrockModel = Bedrock(session=boto3.Session(...), model_region="us-east-1")
        bedrockModel.prompt(user_prompt="Who was the first president of the United States?", system_prompt="You are a helpful assistant.", max_gen_len=100)
        ```
        """
        # generate bedrock request payload
        formatted_prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>{system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>{user_prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
        native_request = {"prompt": formatted_prompt, "max_gen_len": max_gen_len, "temperature": temperature, "top_p":top_p}
        request = json.dumps(native_request)
        # call bedrock model
        try:
            # Invoke the model with the request.
            response = self.client.invoke_model(modelId=self.model_id, body=request)
        except Exception as e:
            raise Exception(f"ERROR: Can't invoke '{self.model_id}'. Reason: {e}")
        # Decode and extract the response
        model_response = json.loads(response["body"].read())
        response_text = model_response["generation"]
        return response_text

system_prompt = """# Task

You are a name generator for people from different countries in Europe. Your task is to generate an arbitrary N number of distinct and varied first names and last names for people from a given European country of origin.

# Requirements

- Generate typical names for both male and female people.
- The names do not need to be traditional to the target European country.
- Do not repeat any first names or last names more than once. Each individual first name must be unique and each individual last name must be unique.
- You should return the first names and last names using a valid JSON object tagged as <answer></answer>.
- The valid JSON object should be of the following structure; {"firstnames":["first name 1","first name 2",...,"first name N"], "lastnames":["last name 1","last name 2",...,"last name N"]}

# Examples

- Generate 2 first names and 2 last names for people from the country "Germany" -> <answer>{"firstnames":["Max","Hannah"], "lastnames":["Müller","Schmidt"]}</answer>
- Generate 4 first names and 4 last names for people from the country "United Kingdom" -> <answer>{"firstnames":["George","Richard","Katie","Mary"], "lastnames":["Smith","Taylor","Jones","Brown"]}</answer>
- Generate 3 first names and 3 last names for people from the country "France" -> <answer>{"firstnames":["Lola","Mathieu","Léa"], "lastnames":["Benoît","Pierre","Lefort"]}</answer>
- Generate 5 first names and 5 last names for people from the country "Spain" -> <answer>{"firstnames":["Juan","Cristina","Javier","Julia","Isabel"], "lastnames":["Garcia","Martinez","Rodriguez","Lopez","Gomez"]}</answer>
- Generate 6 first names and 6 last names for people from the country "Sweden" -> <answer>{"firstnames":["Tova","Alva","Casper","Märta","Axel","Elsa"], "lastnames":["Andersson","Johansson","Lundberg","Svensson","Pettersson","Nilsson"]}</answer>"""

prompt = 'Generate {n_user_names} first names and {n_user_names} last names for people from the country "{country}"'