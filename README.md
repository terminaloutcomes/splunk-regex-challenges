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

Each challenge is spec'd as a JSON-formatted file:

```json
{
    "input" : "hello world",
    "matches" : [
        "hello"
    ],
    "groups" : [
        "hello"
    ],
    "creator" : "@yaleman",
    "example_solution" : "(^\\w+)"
}
```

You can test them by running `./regex_challenge.py test <filename>`, eg:


```bash
$ ./regex_challenge.py test "./challenges/2022-01-07-hello-world.json"
2022-01-07 12:33:34.382 | INFO     | __main__:test:111 - # Testing ./challenges/2022-01-07-hello-world.json
2022-01-07 12:33:34.382 | DEBUG    | __main__:test:121 - Found example solution
2022-01-07 12:33:34.382 | INFO     | __main__:test:135 - ✅ ./challenges/2022-01-07-hello-world.json passes tests!

```