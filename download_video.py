from requests import *
import re
import urllib.request


class DownLoad_from_Inst:
    def __init__(self, url, user_name, video=False):
        self.url = url
        self.name_file = f'{user_name}.{["mp4" if video else "png"][0]}'
        self.video_url = ''
        self.image_url = ''
        self.dw_url = ''

    def get_url_video(self):
        r = get(self.url)
        self.video_url = re.search(r'\"(http[s]://*/.*mp.+\w)\"', r.text)
        if self.video_url:
            self.video_url = self.video_url.group(1)
            self.dw_url = self.video_url
            return 'Ready'
        else:
            return "Content is not find"

    def get_url_image(self):
        r = get(self.url)
        self.image_url = re.search(r'\"(http[s]://*/.*png.+\w)\"', r.text)
        if self.image_url:
            self.image_url = self.image_url.group(1)
            self.dw_url = self.image_url
            return 'Ready'
        else:
            return "Content is not find"

    def download(self):
        urllib.request.urlretrieve(self.dw_url, self.name_file)
