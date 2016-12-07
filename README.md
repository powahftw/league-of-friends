# league-of-friends

Python script that given a list of league of legends player track if they are in game and in that case notify you when they finish

### Prerequisites

You will need an API key to use the script. Paste it in the api.txt

The script makes uses of requests for the API calls.

Prepare the friendsnick.txt with a list of firends you'd like to track. Please remember that since you have limited API calls rate you should limit yourself with few friends at time.


Please avoid blank spaces in nickname. Few regions are missing, feel free to add those :)
Check Final Notes on the why 

```
nickname server
nickname server
nickname server
```


### Usage

You can use it by launching like

```
python lolfriends.py <inputpath>
```

###Example 


```
python lolfriends.py friendsnick.txt
```


### Final notes

I hacked togheter this script as a way to utilize [Riot Api](https://developer.riotgames.com) and to quickly remind me when my friends finished a game.

I decided to share this little project in case anyone found it useful but this is the technical equivalent of chewing gum and duct tape.
There is almost zero error handling and some region are not supported, use it with care. 
I'll try to fix most of the things in future iteration of this utility.

