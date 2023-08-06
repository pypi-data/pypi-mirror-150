import os
import ssl
import wget
import time
import requests as visit
from .headers import headers_water
from .hopter import Error_pta
from rich.progress import track

headers = headers_water()
ssl._create_default_https_context = ssl._create_unverified_context

def download(url):
  print('\033[92m',end='\r')
  try:
    res = visit.get(url,headers,stream=True)
  except Exception as e:
    Error_pta('DownloadError','Command',str(e),'download …')
  else:
    try:
      file_size = int(res.headers['content-length'])
      for i in track(range(100),description ='Download …'):
        pass
      print('Successfully downloaded this file')
    except Exception as e:
      Error_pta('DownloadError','Command',str(e),'download …')
      