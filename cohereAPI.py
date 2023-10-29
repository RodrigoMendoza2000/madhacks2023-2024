import cohere
import os
from dotenv import load_dotenv
load_dotenv()


class CohereAPI:
    def __init__(self):
        self.co = cohere.Client(os.environ.get("COHERE_APIKEY"))
    

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
        text='prompt',
        length='short',
        format='paragraph',
        model='command',
        additional_command='',
        temperature=0.3,
        ) 
        return response.summary


if __name__ == '__main__':
    cohereapi = CohereAPI()
    text = "Bro. This is a pokemon. This is another instance of and filter please do not use it. I. Tell you right now there is kids on this app and also like come on it could have been anything you'll pick a pokemon bro. What is wrong with you you're weird I shouldn't be saying you all but you know the all that made these filters people. Will say oh you make these filters you make these filters no, I, do not and why would I make something like this brawl this? Is just this is too much for the people that are new and somehow don't know what a 777 filter is by. This point pretty much what it is it. Shows a normal picture of that character and pretty much what you do is you tap the screen and if phases into an image of that character but you shouldn't be seen on tiktok but, in this case you shouldn't be seeing it at all because, why do people want to see of pokemon like that I'm burning the image out of my memory just don't use."
    print(cohereapi.get_topics(text))