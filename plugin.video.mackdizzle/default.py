import sys
import urllib
import urlparse
import xbmcgui
import xbmcplugin
import nanscrapers
import urlresolver9 as urlresolver
import urllib2


###############################
#######BEGIN ADDON DIRECTORY###
addon_handle = int(sys.argv[1])
###############################
xbmcplugin.setContent(addon_handle, 'movies')

player      = xbmc.Player()
base_url    = sys.argv[0]
args        = urlparse.parse_qs(sys.argv[2][1:])
mode        = args.get('mode', None)
seth        = 'http://txt.newfierocket.com/seth.jpg'
clare       = 'http://txt.newfierocket.com/clare.jpg'
seraya      = 'http://txt.newfierocket.com/seraya.jpg'
kid_pic     = 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTAxNDYxMjg0MjNeQTJeQWpwZ15BbWU3MDcyNTk2OTM@._V1_UX182_CR0,0,182,268_AL_.jpg'
adult_pic   = 'https://images-na.ssl-images-amazon.com/images/M/MV5BMTkxMTA5OTAzMl5BMl5BanBnXkFtZTgwNjA5MDc3NjE@._V1_UX182_CR0,0,182,268_AL_.jpg'
url1        = 'http://www.txt.newfierocket.com/movie_list.txt'
url2        = 'http://www.txt.newfierocket.com/adult_list.txt'
seth_list   = 'http://www.txt.newfierocket.com/seth.txt'

###put this in as it wouldn't split at the colon
###so sent it to this function
def cleanColon(item):
        clean = item.split('"')
        return clean

def getList(url):
    webfile = urllib.urlopen(url)
    # movie_list = {}
    file_contents = webfile.readlines()
    file_contents = map(str.strip, file_contents)
    movie_list = {}
    
    for item in file_contents:
        clean = cleanColon(item)
        movie_list[clean[0]] = clean[-1]

    return movie_list

###cleans title from sys.argv to movie and year
###to be sent to NaN
def cleanTitle():
    movie = str(args['foldername'][0])
    seperate = movie.split('(')
    title = seperate[0]
    #title = title.replace(' ', '&')
    #xbmc.log(str(title))
    year = seperate[1]
    year = year.strip('()')
    url = scrape(title, year)
    play(url, title, year)

def scrape(movie, year):
    ###Got this sort function from Midraal#####
    if movie is not "" and year is not "":
        def sort_function(item):
            xbmc.log(str(item))
            quality = item[1][0]["quality"]
            if quality == "1080": quality = "HDa"
            if quality == "720": quality = "HDb"
            if quality == "560": quality = "HDc"
            if quality == "HD": quality = "HDd"
            if quality == "480": quality = "SDa"
            if quality == "360": quality = "SDb"
            if quality == "SD": quality = "SDc"
            #xbmc.log(quality)
            return quality

    resolved_url = None
    link = nanscrapers.scrape_movie_with_dialog(movie, year, '', timeout=600, sort_function=sort_function)
    if link:    
        url = link['url']
    try:
        resolved_url = urlresolver.resolve(url)
    except:
        pass
        sys.exit()
    if resolved_url:
        url = resolved_url
        
    return url

def play(url, movie, year):
    listitem = xbmcgui.ListItem (movie)
    player.play(url, listitem)


def build_url(query):
    built_url = base_url + '?' + urllib.urlencode(query)
    xbmc.log(str(built_url))
    return built_url
    
def addFolder(name, icon):
    url = build_url({'mode': name, 'foldername': name})
    li = xbmcgui.ListItem(name, iconImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=True)

def addMovie(movie, icon):
    url = build_url({'mode': 'playmovie', 'foldername': movie})
    li = xbmcgui.ListItem(movie, iconImage=icon)
    xbmcplugin.addDirectoryItem(handle=addon_handle, url=url,
                                listitem=li, isFolder=False)


if mode is None:
    addFolder('For the Kids', kid_pic)
    addFolder('Not for Kids', adult_pic)
    #addFolder('Seraya', seraya)
    #addFolder('Clare', clare)
    #addFolder('Seth', seth)

elif mode[0] == 'For the Kids':
    macks_movies = getList(url1)
    for movie, icon in macks_movies.items():
        movie = movie.replace('&', ' ' )
        addMovie(movie, icon)

elif mode[0] == 'Not for Kids': 
    chris_movies = getList(url2)
    for movie, icon in chris_movies.items():
        movie = movie.replace('&', ' ' )
        addMovie(movie, icon)

elif mode[0] == 'Seraya':
    macks_movies = getList(url1)
    for movie, icon in macks_movies.items():
        movie = movie.replace('&', ' ' )
        addMovie(movie, icon)

elif mode[0] == 'Clare':
    macks_movies = getList(url1)
    for movie, icon in macks_movies.items():
        movie = movie.replace('&', ' ' )
        addMovie(movie, icon)

elif mode[0] == 'Seth':
    seth_movies = getList(seth_list)
    for movie, icon in seth_movies.items():
        movie = movie.replace('&', ' ' )
        addMovie(movie, icon)


elif mode[0] == 'playmovie':
    cleanTitle()
    

    
#######################################
xbmcplugin.endOfDirectory(addon_handle)
#######################################
