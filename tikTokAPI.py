import requests
# from dotenv import load_dotenv
import os
import urllib.request
import re
from dotenv import load_dotenv
import json


load_dotenv()


class TikTok:
    def __init__(self):
        self.headers = {
            "X-RapidAPI-Key": os.environ.get("APIKEY"),
            "X-RapidAPI-Host": os.environ.get("APIHOST")
        }
        self.video_dictionary = {}
        self.next_video_id = None
        self.number_video = 0
        self.total_number = 0
        self.to_process = 0
        self.current_cursor = 0

    def remove_emojis(self, data):
        emoj = re.compile("["
                          u"\U0001F600-\U0001F64F"  # emoticons
                          u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                          u"\U0001F680-\U0001F6FF"  # transport & map symbols
                          u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                          u"\U00002500-\U00002BEF"  # chinese char
                          u"\U00002702-\U000027B0"
                          u"\U00002702-\U000027B0"
                          u"\U000024C2-\U0001F251"
                          u"\U0001f926-\U0001f937"
                          u"\U00010000-\U0010ffff"
                          u"\u2640-\u2642"
                          u"\u2600-\u2B55"
                          u"\u200d"
                          u"\u23cf"
                          u"\u23e9"
                          u"\u231a"
                          u"\ufe0f"  # dingbats
                          u"\u3030"
                          "]+", re.UNICODE)
        return re.sub(emoj, '', data)

    def search(self, keyword, count=30, offset=0, sort_type=0, publish_time=30):
        self.video_dictionary = {}
        self.number_video = 0
        self.total_number = 0
        self.next_video_id = None
        print("Searching TikTok videos...")
        url = "https://tokapi-mobile-version.p.rapidapi.com/v1/search/post"
        querystring = {"keyword": keyword, "count": count, "sort_type": sort_type,
                       "publish_time": publish_time, "offset": offset}
        response = requests.get(url, headers=self.headers, params=querystring)
        print("got response")
        response_json = response.json()
        response_videos = response_json["aweme_list"]
        for response_video in response_videos:
            
            added_sound_music_info = {}
            added_sound_music_info_tags = ['author', 'duration', 'title', 'audition_duration', 'id']
            for tag in added_sound_music_info_tags:
                added_sound_music_info[tag] = response_video["added_sound_music_info"][tag]

            author = {}
            author_tags = ['follower_count', 'nickname', 'search_user_name', 'following_count', 'uid']

            for tag in author_tags:
                author[tag] = response_video["author"][tag]

            create_time = response_video["create_time"]
            desc = response_video["desc"]
            desc_language = response_video["desc_language"]


            share_info = {}
            share_info_tags = ['share_url']
            for tag in share_info_tags:
                share_info[tag] = response_video['share_info'][tag]


            statistics = {}
            statistics_tags = ['collect_count', 'comment_count', 
                               'digg_count', 'download_count', 'forward_count', 'play_count', 
                               'share_count', 'whatsapp_share_count']
            
            for tag in statistics_tags:
                statistics[tag] = response_video['statistics'][tag]

            links_json = []
            video = {}
            video_tags = ['download_addr', 'duration']
            for tag in video_tags:
                if tag == 'download_addr':
                    if response_video['video'][tag]['url_list'] is not None:
                        for link in response_video['video'][tag]['url_list']:
                            links_json.append({'url': link})
                else:
                    video[tag] = response_video['video'][tag]

            text_extra = []
            if response_video['text_extra']  is not None:
                for hashtag in response_video['text_extra']:
                    text_extra.append({'hashtag_id': hashtag['hashtag_id'], 'hashtag_name': hashtag['hashtag_name']})
            
            # text_extra = response_video['text_extra']
            aweme_id = response_video['aweme_id']

            print(aweme_id)

            
            self.video_dictionary[aweme_id] = {'added_sound_music_info': [added_sound_music_info], 'author': [author],
                                               'create_time': create_time, 'desc': desc, 'desc_language': desc_language,
                                               'share_info': [share_info], 'statistics': [statistics],
                                               'video': [video], 'text_extra': text_extra, 'aweme_id': aweme_id, 'download_addr': links_json}
            print("added to dic")
            
        with open("response.json", "w") as outfile:
            json.dump(self.video_dictionary, outfile, indent=4)
        self.total_number = len(self.video_dictionary)


    def increase_number_video(self):
        self.number_video = self.total_number - len(self.video_dictionary)
        try:
            self.next_video_id = list(self.video_dictionary.keys())[0]
        except Exception as e:
            self.next_video_id = None
            print(e)

    def get_next_dictionary(self):
        if self.next_video_id and len(self.video_dictionary) > 0:
            return self.video_dictionary[self.next_video_id]

    def delete_next_video(self):
        if self.next_video_id is not None and len(self.video_dictionary) > 0:
            self.video_dictionary.pop(self.next_video_id)

    def get_total_number_of_videos(self):
        return len(self.video_dictionary)

    def get_video_dictionary(self):
        return self.video_dictionary

    def reset(self):
        self.next_video_id = None
        self.number_video = 0
        self.total_number = 0
        self.to_process = 0
        self.current_cursor = 0
        self.video_dictionary = {}


if __name__ == '__main__':
    tiktok = TikTok()
    tiktok.search('wine', count=2)
