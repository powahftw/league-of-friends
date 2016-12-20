import argparse
import requests
import time
import winsound

p = argparse.ArgumentParser(description="Notify when Friends finish to play a game")
p.add_argument("txtpath", help="File Path of the list of Friends")
args = p.parse_args()

def api_from_file(path): #GET API KEY FROM TXT FILE
    with open(path, 'r') as f:
        return f.readline()

def nick_format(nick):
    return nick.lower().replace(" ","")

platformdict = {'euw': 'EUW1', 'na': 'NA1', 'eune': 'EUN1', 'br': 'BR1', 'kr': 'KR', 'oce': 'OC1', 'ru': 'RU', 'tr': 'TR', 'jp': 'JP1', 'lan': 'LA1', 'las': 'LA2', 'pbe': 'PBE1'}

API_BASE_URL = "https://{}.api.pvp.net"
APIKEY = api_from_file("api.txt")

class player:
    def __init__(self, nick, region):
        self.nick = nick_format(nick)
        self.id = 0
        self.region = region
        self.ingame = False

    def get_id(self):
        if not self.id:
            self.id = upd_id(self)
        return self.id


def upd_id(player): #UPDATE PLAYER ID
    nick = player.nick
    region = player.region
    nick_id_url = "{0}/api/lol/{1}/v1.4/summoner/by-name/{2}?api_key={3}"\
                   .format(API_BASE_URL.format(region), region, nick, APIKEY)
    try:
        r = requests.get(nick_id_url)
    except requests.exceptions.RequestException as e:
        print (e)
        quit()

    status = r.status_code
    if status == 200:
        return r.json()[player.nick]['id']
    elif status == 404:
        print("SUMMONER %s DON'T EXIST" %player.nick)
        quit()
    elif status == 429:
        print("Rate Limit Exceeded")
        time.sleep(10)
        upd_id(player)
    else:
        print("UNHANDLED response %d from SUMMONER: %s" %(status,player.nick))
        quit()


def player_game(player): #GET INFORMATION ABOUT PLAYER GAME
    id = player.get_id()
    plat = platformdict[player.region]
    game_url = "{0}/observer-mode/rest/consumer/getSpectatorGameInfo/{1}/{2}?api_key={3}"\
                .format(API_BASE_URL.format(player.region), plat, id, APIKEY)
    try:
        r = requests.get(game_url)
    except requests.exceptions.RequestException as e:
        print (e)
        quit()

    status = r.status_code
    if status == 200:
        return 1
    elif status == 404:
        return 0
    elif status == 429:
        print("Rate Limit Exceeded")
        time.sleep(10)
        player_game(player)
    else:
        print("Unspecified API response code")
        quit()

def player_from_f(path): #GET PLAYER FROM FILE
    try:
        d = {}
        with open(path) as f:
            for line in f:
                nick = line.rsplit(' ', 1)[0]
                d[nick] = line.rsplit(' ', 1)[1].rstrip()
        players = [player(key, d[key]) for key in d]
        return players
    except IOError:
        print("There is  problem with the file you provided")
        quit()

def print_lista(list): #PRINT LIST OF PLAYER
    for e in list:
        print("NICK:\t%s\nREGION\t%s\n" %(e.nick, e.region))

def alert(player):
    print("%s has finished a GAME" % player.nick.upper())
    winsound.Beep(2000, 1000)

def check_all(list):
    print ("\n\n~~~~~~\n\n")
    for e in list:
         print("---")
         if player_game(e):
            e.ingame = True
            print ("-%s is currently in game" %e.nick.upper())
         else:
            if e.ingame:
                alert(e)
            else:
                print ("-%s is not playing" %e.nick.upper())
    print("---")

if __name__ == '__main__':
    lista = player_from_f(args.txtpath)
    print_lista(lista)
    while True:
        check_all(lista)
        time.sleep(15)
