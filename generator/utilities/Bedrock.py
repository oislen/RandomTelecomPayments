import json
from typing import Dict, List
from beartype import beartype

class Bedrock():
    """
    Bedrock AWS API client wrapper for invoking language models.
    This class provides a simplified interface to interact with AWS Bedrock runtime,
    enabling prompt-based interactions with language models like Llama 3.
    
    Parameters
    ----------
    bedrock_runtime : boto3.Session
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
        bedrock_runtime,
        ):
        self.bedrock_runtime = bedrock_runtime

    @beartype
    def prompt(
        self,
        model_id:str,
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
            response = self.bedrock_runtime.invoke_model(modelId=model_id, body=request)
        except Exception as e:
            raise Exception(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        # Decode and extract the response
        model_response = json.loads(response["body"].read())
        response_text = model_response["generation"]
        return response_text
    
    @beartype
    def converse(
        self,
        modelId:str,
        messages:List,
        system:List,
        inference_config:Dict={"maxTokens":512, "temperature":0.5, "topP":0.5,},
        tools_config:Dict=None
        ):
        """
        Invoke the Bedrock model with the provided messages and configurations.

        Parameters
        ----------
        messages : Dict
            A list of message objects representing the conversation history.
        system : Dict
            A system message object providing context or instructions for the model.
        inference_config : Dict
            Configuration settings for inference parameters.
        tools_config : Dict
            Configuration settings for any tools to be used during inference.

        Returns
        -------
        Dict:
            The response from the Bedrock Claude model.
        
        References
        ----------
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/bedrock-runtime/client/converse.html
        """
        payload = {"modelId": modelId, "messages": messages, "system": system}
        if inference_config:
            payload["inferenceConfig"] = inference_config
        if tools_config:
            payload["toolsConfig"] = tools_config
        # call converse api
        response = self.bedrock_runtime.converse(**payload)
        return response
