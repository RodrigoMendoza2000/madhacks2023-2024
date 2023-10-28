import cohere
from bertopic.representation import Cohere
from bertopic import BERTopic
import os
from dotenv import load_dotenv
load_dotenv()


co = cohere.Client(os.environ.get("COHERE_APIKEY"))
representation_model = Cohere(co)
topic_model = BERTopic(representation_model=representation_model)

def cohere_promt(prompt):
    try:
        response = co.generate(
            prompt=prompt
        )
        return response[0]
    except Exception as e:
        return {"message": f"{e}"}

print(cohere_promt('what is 1+1'))