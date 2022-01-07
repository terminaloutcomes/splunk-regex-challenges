# #splunk-regex-challenges


## Installing

```
python3 -m venv venv
source venv/bin/activate
python3 -m pip install --upgrade pip click
```

## Running it

```
$ ./regex_challenge.py challenge challenges/2021-10-12-pre-conf.json '\w+'
challenges/2021-10-12-pre-conf.json by @The_Tick
##################################################
Input:
##################################################
bob
sally
george
bob
george
bob
sally
diego
dianora
diego

oh look
at my
beatiful
beautiful
beauiful
beatiful
REGEX
IT'S REGEX TASTIC
REGEX
IS
BEATIFUL
##################################################
Expected Matches:
##################################################
['bob', 'sally', 'george', 'bob', 'george', 'bob', 'sally', 'diego', 'diego', 'beatiful', 'beatiful', 'REGEX', 'REGEX', 'BEATIFUL']
##################################################
Found matches:
['bob', 'sally', 'george', 'bob', 'george', 'bob', 'sally', 'diego', 'dianora', 'diego', 'oh', 'look', 'at', 'my', 'beatiful', 'beautiful', 'beauiful', 'beatiful', 'REGEX', 'IT', 'S', 'REGEX', 'TASTIC', 'REGEX', 'IS', 'BEATIFUL']
##################################################
Sorry, you didn't succeed.
```


## Writing challenge files

TBA
# splunk-regex-challenges
