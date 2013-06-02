#coding:utf-8
import requests
import os, sys
from urllib import urlretrieve
import socket

timeout = 60
socket.setdefaulttimeout(timeout)

def download_song(song_name):
    suggestion_api = 'http://openapi.baidu.com/public/2.0/mp3/info/suggestion?format=json&word=%s'
    songlist_api = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.artist.getSongList&format=json&tinguid=%s&limits=1000&limit&order=2&from=mixapp'
    song_api = 'http://ting.baidu.com/data/music/links?songIds=%s&rate=128'
    
    base_dir = 'music_tmp'
    
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
        
    r = requests.get(suggestion_api % song_name)
    
    if len(r.json()['song']) <> 0:
        for index, song_item in enumerate(r.json()['song']):
            if song_item['songname'].encode('utf-8') == song_name:
                print index, song_item['artistname']
        n = int(raw_input())
        artist_name = r.json()['song'][n]['artistname'].encode('utf-8') 
        if not os.path.exists(base_dir + '/' + artist_name):
            os.mkdir(base_dir + '/' + artist_name)    
        song_id = r.json()['song'][n]['songid']
           
        r = requests.get(song_api % song_id)
            
        song_link = r.json()['data']['songList'][0]['showLink']
        lrc_link = 'http://music.baidu.com' + r.json()['data']['songList'][0]['lrcLink'] 
        album_title = r.json()['data']['songList'][0]['albumName'].encode('utf-8') 
        
        song_dir = base_dir + '/' + artist_name + '/' + album_title
            
        if not os.path.exists(song_dir):
            os.mkdir(song_dir)
 
       
        music_name = song_dir + '/' + artist_name + ' - ' + song_name
        for i in range(3):
            print 'Downloading ' , album_title, song_name ,'....', 
            sys.stdout.flush()
            try:
                if not os.path.exists(music_name + '.mp3'):
                    urlretrieve(song_link, music_name + '.mp3')
                if not os.path.exists(music_name + '.lrc'):
                     urlretrieve(lrc_link, music_name + '.lrc')
            except IOError:
                  print 'fail'
            else:
                print 'OK'
                break
