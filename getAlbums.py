#coding:utf-8
import requests, sys

def getAlbums(artist_name):

    suggestion_api = 'http://openapi.baidu.com/public/2.0/mp3/info/suggestion?format=json&word=%s'
    album_api =  'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.artist.getAlbumList&format=json&tinguid=%s&limits=1000&limit&order=2&from=mixapp'

    print 'Searching artist information...'    
    r = requests.get(suggestion_api % artist_name)
    if len(r.json()['artist']) <> 0:
  
        artist_id = r.json()['artist'][0]['artistid']
        r = requests.get(album_api % artist_id)
        for song in r.json()['albumlist']:
            sys.stdout.softspace = 0
            print song['title'].encode('utf-8') + '$',
    else:
        print u'没有找到歌手'
