import os,sys,hashlib
movie_exts=["avi","mp4","mkv","mpg","mpeg","mov","rm","vob","wmv","flv","3gp"]
if len(sys.argv)==1:
      folder='H:/Movies/'
else:
      folder=sys.argv[1]
try:
      import urllib.request, urllib.parse
      pythonVer = 3
except ImportError:
      
      import urllib2
      pythonVer = 2

def check(file):
      extension=file.split('.')[-1]
      file=file.replace(extension,"srt")
      if os.path.exists(file):
            return True
      else:
            return False

      
def getFiles(path):
      files=os.listdir(path)
      returnList=[]
      for file in files:
            extension=file.split('.')[-1]
            
            if  extension in movie_exts:
                  returnList.append(path+file)
      return returnList
            
def getHash(name):
        readsize = 64 * 1024
        with open(name, 'rb') as f:
            size = os.path.getsize(name)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)
        return hashlib.md5(data).hexdigest()

def getSubtitle(key):
      try:
            headers = { 'User-Agent' : 'SubDB/1.0 (Movie Subtitle Downloader/1.0; http://github.com/geekpradd/subtitle-downloader)' }
            url = "http://api.thesubdb.com/?action=download&hash="+key+"&language=en"
            if pythonVer == 3:
                  request = urllib.request.Request(url, None, headers)
                  response = urllib.request.urlopen(request).read()
            else:
                  request = urllib2.Request(url, '', headers)
                  response = urllib2.urlopen(request).read()
            if len(response)<20:
                  return False,False
            else:
                  return response,True
      except:
            return False,False
def writeSubtitle(data,path):
      ext=path.split('.')[-1]
      path=path.replace(ext,"srt")
      
      print ("Writing Subtiles... Opening and Creating {0}\n\n".format(path))
      with open(path,'wb') as file:
            file.write(data)
      return True
      
def main():
      failed=0
      success=0
      files=getFiles(folder)
      
      print ("Welcome To The Subtitle Downloader By Pradd \n\n")
      for file in files:
            print ("Opening {0} ...".format(file))
            hashKey=getHash(file)
            exists=check(file)
            if exists:
                  print ("Subtitles already downloaded for {0}... Skipping \n\n".format(file))
            else:
                  subtitle,status=getSubtitle(hashKey)
                  if not status:
                        print ("No subtitle found for File {0}.. Skipping It \n\n".format(file))
                        failed+=1
                  else:
                        writeSubtitle(subtitle,file)
                        
                        success+=1

      print ("\nDownloaded {0} subtitles out of {1} Media files. Failed to download for {2} files.".format(success,len(files),failed))


if __name__=='__main__':
      main()
