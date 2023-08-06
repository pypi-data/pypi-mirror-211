__version__ = '0.1.2'

import requests, json
#Api provided by https://protondb.max-p.me/
class protonDB():
  def __init__(self,cache=True):
    self.api = "https://protondb.max-p.me/"
    self.cachingEnabled = cache
    if cache == True:
      self.cache = [[],{}] # 0 is the gamelist cache, 1 is the game reviews cache.
  def getGames(self):
    """
    Lists all the games we have discovered so far.
    Returns an array of JSON objects with these fields in it:
    appId
    title 
    """
    #Checks to see if caching is enabled, then either returns the populated cache, populates the cache and returns cache, or returns the response.
    if self.cachingEnabled == True:
      if self.cache[0] == []:
        response = requests.get(self.api+"games").text
        response = json.loads(response)
        self.cache[0] = response
        return response
      else:
        return self.cache[0]
    else:  
      response = requests.get(api+"games").text
      response = json.loads(response)
      return response
  def getReports(self,appId):
    if self.cachingEnabled == True:
      if self.cache[1] == {} or self.cache[1].has_key(str(appId)):
        response = requests.get(self.api+"games/"+str(appId)+"/reports/").text
        response = json.loads(response)
        self.cache[1][str(appId)] = response
        return response
      elif self.cache[1].has_key(str(appId)) == True:
        return self.cache[1][str(appId)]
    else:
      response = requests.get(self.api+"games/"+str(appId)+"/reports/").text
      response = json.loads(response)
      return response
        
  