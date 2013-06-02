#coding:utf-8
import codecs
from music import download
print 'Analysing config file...' 
with codecs.open('config.txt', encoding='utf-8') as f:
    download_list = []
    for line in f:
        line = line.strip().split('   ')
        item = {}
        item['artist'] = line[0]
        item['type'] = line[1]
        item['all'] = line[2] == '*' and True or False
        if item['all'] == False:
            item['list'] = line[2].split('$')
        download_list.append(item)

for item in download_list:
    download(item)
