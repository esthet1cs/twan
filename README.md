

### Twan is a shortcut for Twitter Analytics

The two scripts provided here are based on [Tweepy](https://tweepy.readthedocs.io). 

`analuese.py` contains several functions that should make it easier to compile data from twitter and save it to disk for later use.

The most interesting functions provided are probably these:

- authenticate with the Twitter API using your own application credentials
- search for tweets using keywords (and all the grammar the twitter search api has to offer)
- search for tweets and save them to file
- get all follower IDs for a given account
- get all friend IDs for a given account
- get both friend and follower IDs for a given account

The code is mostly well commented.

`analuese.py` is intended for use in an interactive IPython session. In order to use these functions, you need to provide the credentials in the format given in `credentials.example`. The script expects the credentials in `~/.twan/credentials`. 

Attention: There are no safeguards to prevent overwriting existing files. 


### Streaming content to file

`twitstream.py` is a command line script that allows to stream content directly to file. The data is saved in a file named `datafile.json`. Be careful: There is no mechanism that checks if a file or folder with this name is already there. Use at your own risk! 

A searchphrase has to be provided using `-s`, all other things are optional.
The location of a file with credentials in the format described above can be provided explicitly using the `-c` flag. The defaults is `~/.twan/credentials`.
The searchphrase using `-s` is mandatory. A directory for saving the datafile `datafile.json` can be provided using `--save_dir`. This usage information is also available via the command `python twitstream.py --help`.

twitstream can be used to permanently collect data, e.g. if you want to build a dataset about a hashtag. Just let the script run in the background on a server, e.g. using `screen`. 

Example usage: `python twitstream.py -s '#reallypopular' --save_dir 'datadir' -c 'mycredentials'`

Full usage information, also available via the `--help` option:

~~~
usage: twitstream.py [-h] [-s SEARCHPHRASE [SEARCHPHRASE ...]]
                     [--save_dir SAVE_DIR] [-c CREDENTIALS]

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCHPHRASE [SEARCHPHRASE ...], --searchphrase SEARCHPHRASE [SEARCHPHRASE ...]
                        You should provide a searchphrase, multiple
                        searhphrases are possible
  --save_dir SAVE_DIR   Specify the directory where your data should be saved.
  -c CREDENTIALS, --credentials CREDENTIALS
                        Specify the file that contains your Twitter app
                        credentials. See the README for the required format.
                        Specify the full path or the path relative to your
                        working directory. Defaults to ~/.twan/credentials.
~~~

## Installation

After installing the dependencies using `pipenv` or `pip`, e.g. `pip install -r requirements.txt`, the scripts can be used as-is.

`analuese.py` is just a file with some function and automated API authentication for convenient use in an IPython shell. `twitstream.py` is a script that can be used on any server console.


