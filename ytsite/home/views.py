from django.shortcuts import render, HttpResponse, Http404
from django.views import generic
import bs4 as bs
import urllib.request
from pytube import YouTube
import os


class IndexView(generic.View):

    def get(self, request):
        return render(request, 'home/index.htm', {})
    def post(self, request):
        # BEAUTIFUL SOUP WORKSPACE FOR REQUESTING VIDEOS FROM YOUTUBE
        #'https://www.youtube.com/results?search_query='
        choice = request.POST['choice_selected']
        print(f'The Choice choosen was {choice}')
        song_name = request.POST['song_name']
        print(f'Searching For {song_name}')
        song_name = song_name.replace(' ', '+')

        url_to_request = 'https://www.youtube.com/results?search_query=' + song_name
        print(f'Url we gonna request is {url_to_request}')

        req = urllib.request.Request(url_to_request, headers={'User-Agent': 'Mozilla/5.0'})
        source = urllib.request.urlopen(req).read()

        soup = bs.BeautifulSoup(source,'html.parser')

        related_url_list = []

        for url in soup.find_all('a'):
            if url.get('href')[:7] == '/watch?':
                related_url_list.append(url.get('href'))

        # PYTUBE WORKSPACE FOR GETTING DOWNLOADED THE RELATED YT VIDEOS
        yt = YouTube('https://www.youtube.com' + related_url_list[0])
        print(f'Element to download is {related_url_list[0]}')
        print(f'Downloading {song_name}...')
        stream = yt.streams.first()
        print('1')
        video_downloaded = False
        print('2')
        try:
            stream.download('/home/sandaru/Downloads/')
            video_downloaded = True
        except:
            video_downloaded = False
        finally:
            pass
        
        if video_downloaded:
            return HttpResponse('Success')
        else:
            raise Http404()