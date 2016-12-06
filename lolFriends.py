import argparse
import requests
import time
import winsound
import os.path

p = argparse.ArgumentParser(description="Notify when Friends finish to play a game")
p.add_argument("txtpath", help="File Path of the list of Friends")
args = p.parse_args()

def api_from_file(path):
    print("THIS HAS TO CHANGE DONT EXPOSE API. ALSO TO ADD OTHER REGION AND CHANGE API BASE URL BASED ON THAT\n"
          "ADD CHECK TO SEE IF API REQUEST WAS EXCEEDED MAKING THE CHECK TIMER BASED ON CURRENT USER "
          "ADD SOME TRY TO PREVENT PROBLEM SUCH AS NO CONNECTION")
    with open(path, 'r') as f:
        return f.readline()

def nick_format(nick):
    return nick.lower().replace(" ","")

platformdict = {'euw': 'EUW1', 'na': 'NA1', 'eune': 'EUN1', 'br': 'BR1', 'jp': 'JP1', 'kr': 'KR', 'oce': 'OC1', 'ru': 'RU', 'tr': 'TR'}

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


def upd_id(player):
    nick = player.nick
    region = player.region
    nick_id_url = "{0}/api/lol/{1}/v1.4/summoner/by-name/{2}?api_key={3}"\
                   .format(API_BASE_URL.format(region), region, nick, APIKEY)
    r = requests.get(nick_id_url)
    if r.status_code == 200:
        return r.json()[player.nick]['id']
    elif r.status_code == 404:
        print("SUMMONER %s DON'T EXIST" %player.nick)
        quit()
    elif r.status_code == 429:
        print("Rate Limit Exceeded")
        time.sleep(10)
        upd_id(player)
    else:
        print("UNKNOW ERROR WITH SUMMONER %s" %player.nick)
        quit()


def player_game(player):
    id = player.get_id()
    plat = platformdict[player.region]
    game_url = "{0}/observer-mode/rest/consumer/getSpectatorGameInfo/{1}/{2}?api_key={3}"\
                .format(API_BASE_URL.format(player.region), plat, id, APIKEY)
    r = requests.get(game_url)
    if r.status_code == 200:
        return 1
    elif r.status_code == 404:
        return 0
    elif r.status_code == 429:
        print("Rate Limit Exceeded")
        time.sleep(10)
        player_game(player)
    else:
        print("Unspecified API response code")
        quit()

def player_from_f(path):
    try:
        d = {}
        with open(path) as f:
            for line in f:
                a, b = str(line).split() #CARE NOT TO PROVIDE NICKNAME WITH SPACES
                d[a] = b
        players = [player(key, d[key]) for key in d]
        return players
    except IOError:
        print("There is  problem with the file you provided")
        quit()

def print_lista(list):
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

def print_data(player):
    print("\nAPI:\t%s\nNICK:\t%s\nREGION:\t%s\nID:\t\t%s\n" %(APIKEY[0:9] + "...", player.nick, player.region, player.id))

if __name__ == '__main__':
    lista = player_from_f(args.txtpath)
    print_lista(lista)
    while True:
        check_all(lista)
        time.sleep(15)
