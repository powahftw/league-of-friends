# league-of-friends

Python script that given a list of league of legends player track if they are in game and in that case notify you when they finish

### Prerequisites

You will need an API key to use the script. Paste it in the api.txt

The script makes uses of requests for the API calls.

Prepare the friendsnick.txt with a list of firends you'd like to track. Please remember that since you have limited API calls rate you should limit yourself with few friends at time.


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

I decided to share this little project in case anyone found it useful to know when their friends finish a game, so you can bug them to play with you!
There might be some missing error handling, use it with care.
I'll try to fix most of the things in future iteration of this utility such as a better API request limiter.



