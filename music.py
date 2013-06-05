#coding:utf-8
import requests
import os, sys
from urllib import urlretrieve
from os.path import getsize
import socket
import re


timeout = 60
socket.setdefaulttimeout(timeout)
def cbk(a, b, c):  
    per = 100.0 * a * b / c  
    if per > 100:  
        per = 100  
    print '%.2f%%\r' % per,  
def download(item):
    artist_name = item['artist']
    d_list = item.get('list','')
    download_type = item['type']
    is_download_all = item['all']
    suggestion_api = 'http://openapi.baidu.com/public/2.0/mp3/info/suggestion?format=json&word=%s'
    songlist_api = 'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.artist.getSongList&format=json&tinguid=%s&limits=1000&limit&order=2&from=mixapp'
    album_api =  'http://tingapi.ting.baidu.com/v1/restserver/ting?method=baidu.ting.artist.getAlbumList&format=json&tinguid=%s&limits=1000&limit&order=2&from=mixapp'
    song_api = 'http://ting.baidu.com/data/music/links?songIds=%s&rate=128'
    
    base_dir = u'music'
    
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)
    print 'Searching artist information...'    
    r = requests.get(suggestion_api % artist_name)
    
    if len(r.json()['artist']) <> 0:
        
        if not os.path.exists(base_dir + '/' + artist_name):
            os.mkdir(base_dir + '/' + artist_name)
    
        artist_id = r.json()['artist'][0]['artistid']
 
        print 'Fetching song list...'
        r = requests.get(songlist_api % artist_id)
        reg = re.compile(ur'[\/\\\:\*\?\"<>|]', re.IGNORECASE)
        for song in r.json()['songlist']: 
            song_id = song['song_id']
            album_title = song['album_title']
            
            album_title = reg.sub(' ', album_title, 1)
            
            if album_title == '':
                album_title = u'未分类'
            title = song['title']
            if not is_download_all and (download_type == '1' and not album_title in d_list):
                continue;
            if not is_download_all and (download_type == '2' and not title in d_list) :
                continue;

            song_dir = base_dir + '/' + artist_name + '/' + album_title
            
            if not os.path.exists(song_dir):
                try: 
                    os.mkdir(song_dir)
                except:
                    song_dir = base_dir + '/' + artist_name + u'/专辑名无法创建'
                    if not os.path.exists(song_dir):
                        os.mkdir(song_dir)
            
            title = reg.sub(' ', title)
            music_name = song_dir + '/' + artist_name + ' - ' + title
            if os.path.exists(music_name + '.mp3') and os.path.exists(music_name + '.lrc'):
            	continue
            r = requests.get(song_api % song_id)
            # resourceType 不为零表示不在百度音乐服务器，此时若下载则无法得到正确歌曲
            if int(r.json()['data']['songList'][0]['resourceType']) <> 0:
                continue
            song_link = r.json()['data']['songList'][0]['showLink']
            lrc_link = 'http://music.baidu.com' + r.json()['data']['songList'][0]['lrcLink'] 
            size = int(r.json()['data']['songList'][0]['size'])
            for i in range(3):
                print 'Downloading ' , album_title, title 
                sys.stdout.flush()
                try:
                    if not os.path.exists(music_name + '.mp3'):
                        urlretrieve(song_link, music_name + '.mp3', cbk)
                        if getsize(music_name + '.mp3') <> size:
                        	raise IOError
                    if not os.path.exists(music_name + '.lrc'):
                        urlretrieve(lrc_link, music_name + '.lrc', cbk)
                except IOError:
                    print 'Fail               '
                    if os.path.exists(music_name + '.mp3'):
                        os.remove(music_name + '.mp3')
                    if os.path.exists(music_name + '.lrc'):
                        os.remove(music_name + '.lrc')
                else:
                    print 'OK                 '
                    break
            
    
    else:
        print u'没有找到歌手'
