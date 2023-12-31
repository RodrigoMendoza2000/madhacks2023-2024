import cohere
import os
from dotenv import load_dotenv
load_dotenv()


class CohereAPI:
    def __init__(self):
        self.co = cohere.Client(os.environ.get("COHERE_APIKEY"))
        self.to_process = {}
    

    def get_topics(self, prompt):
        response = self.co.generate(
        model='command',
        prompt=f"""Within a given text, give me the top three topics of what the text is about. 
        These topics are going to be used later to generate custom TikTok video scripts. Return the data in a list enclosed by brackets.\n\nExample:\nAction: \'I 
        like to go Mexico city because there is an annual convention about pokemon cards.\nResponse: [Travel, Pokemon, Mexico city]\n\nAction: \'{prompt}\'\nResponse:""",
        max_tokens=300,
        temperature=0.9,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE')
        response_text = response.generations[0].text
        cleaned_string = response_text.strip("[] ").replace(" ", "")
        word_list = cleaned_string.split(",")
        return word_list
    
    def get_summary(self, prompt):
        response = self.co.summarize( 
        text=prompt,
        length='short',
        format='paragraph',
        model='command',
        additional_command='',
        temperature=0.3,
        ) 
        return response.summary


if __name__ == '__main__':
    cohereapi = CohereAPI()
    co = cohere.Client(os.environ.get("COHERE_APIKEY"))
    try:
        response = co.generate(
        model='command',
        prompt='Write a large TikTok script about the following topics: Pokemon, Videogames',
        max_tokens=900,
        temperature=0.9,
        k=0,
        stop_sequences=[],
        return_likelihoods='NONE')
        print( response[0])
    except Exception as e:
        print( {"message": f"{e}"})
    
    #text = "In what's our next move? This is bad on multiple fronts, wait a sec, so if you're here, then that means I'm aware, but something's not right you year."
    #print(cohereapi.get_summary(text))
    #print(cohereapi.get_topics(text))
    