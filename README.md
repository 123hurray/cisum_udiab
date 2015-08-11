cisum_udiab
===========

A tool written in Python to batch download Baidu music

## Dependencies

* requests
* eyed3

## Usage

* Check that you have installed all dependent libs
* Create config.txt in the root path
* Run main.py
* When download finish, you should find all mp3 file in the music folder

## TODO

* Select bitrate based on the configuration file
* Formatting ID3 information


## Demo of config.txt

```
林俊杰   1   *
金莎   1   星月神话$不可思议$空气$换季
梁静茹   2   La La La La$直觉
```

## Configuration file format

* A recorder should be "Singer   DownloadType   DownloadList" format. Remember that there are three spaces between two fields.
* Download type: 1 means album title, 2 means song's name
* Download list: Album titles or songs' names depends on download type. * means all songs
* Download list should be split by $

## Copyright

Only for **learning** and **testing** and SHALL NOT be used for commercial purposes. All copyright of MP3 files belong to Baidu Inc. and their original authors.
