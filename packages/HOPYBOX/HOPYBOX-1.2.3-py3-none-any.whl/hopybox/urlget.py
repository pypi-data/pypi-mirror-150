import os
import ssl
import time
import requests as visit
import webbrowser
from requests.exceptions import *
from .headers import headers_water
from rich import console,syntax
from .hopter import Error_ptb

Console = console.Console()
headers = headers_water()
ssl._create_default_https_context = ssl._create_unverified_context

def hoget(url):
  global headers
  res = 0
  start_time = time.time()
  try:
    print('Loading url …',end='\r')
    res = visit.get(url,headers=headers,stream=True)
    if res.status_code == 200:
      end_time = time.time()
      total_time = end_time - start_time
      print('\033[32mUrl-Url:'+res.url) 
      print('\033[32mUrl-Time:'+str(total_time)+'S')
      print('\033[32mUrl-Szie:'+str(len(res.text))+'B')
      print('\033[32mUrl-Cookies:\033[0m\033[35m')
      for name, value in visit.utils.dict_from_cookiejar(res.cookies).items():
        print('├ %s:%s ' % (name, value))
      if not visit.utils.dict_from_cookiejar(res.cookies):
        print(None)
      print('\033[32mUrl-Headers:\033[0m\033[35m')
      for name, value in res.headers.items():
        print('├ %s:%s ' % (name, value))
      print('\033[32mUrl-Requests-Headers:\033[0m\033[35m')
      for name, value in res.request.headers.items():
        print('├ %s:%s ' % (name, value))
      try:
        print('\033[32mUrl-Code-Coding:'+str(res.encoding).upper())
      except TypeError as url_error:
        print('\033[32mUrl-Code-Type:Other network')
        pass
      except AttributeError as url_error:
        print('\033[31mUrl-Code-AttributeError:'+str(url_error))
      else:
        print('\033[32mUrl-Code-Type:General network\033[0m')
        res.encoding = 'utf-8'
        print('Loaing …',end='\r')
        Console.print(syntax.Syntax(res.text,'html',theme="ansi_dark", line_numbers=True))
        while True:
          howsave = input('\033[32mDo you want to save the source code of this url?(Y/n)')
          if howsave == 'Y' or howsave == 'y':
            url_file = open('{}.html'.format(int(time.mktime(time.localtime(time.time())))),'wb')
            url_file.write(res.content)
            url_file = open('{}.txt'.format(int(time.mktime(time.localtime(time.time())))),'wb')
            url_file.write(res.content)
            break
          elif howsave == 'n':
            break
          else:
            Error_ptb(howsave)
  except HTTPError as res:
    print('\033[31mHOPYBOX:REQUEST:GET:URL:HTTPError:{}'.format(res))
  except SSLError as res:
    print('\033[31mHOPYBOX:REQUEST:GET:URL:SSLError:{}'.format(res))
  except ConnectionError as res:
    print('\033[31mHOPYBOX:REQUEST:GET:URL:ConnectionError:{}'.format(res))
  except RequestException as res:
    print('\033[31mHOPYBOX:REQUEST:GET:URL:RequestException:{}'.format(res))
 
def browse_get(url):
  webbrowser.open(url)
  print('\033[32mNone')  