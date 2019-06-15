# Safari Reading List to Pocket Import

This script will import your Safari Reading List to Pocket.

Offered without support, warranty, etc.

Uses bplist from CCL Forensics; thanks!

I was not able to figure out how to check if a Reading List item was already read, so instead you can define a "stop" item and it will import as far as that and no further. Set this to some unique string in the title of your oldest unread item.

No attempt is made to dedupe items being added to Pocket (not sure if they do that for you themselves.) 

## API Access

You will need to create an application in their [developer portal](https://getpocket.com/developer/), and then use the consumer key from that to get yourself an access token.

The process is something like:

```
http POST https://getpocket.com/v3/oauth/request consumer_key=$CONSUMER_KEY redirect_uri=hello
```

Not that the `redirect_uri` should just be a string, the value doesn't matter. This will give you a `code` which you should keep a copy of for later in this process.

Then in your browser go to: `https://getpocket.com/auth/authorize?request_token=YOUR_REQUEST_TOKEN&redirect_uri=YOUR_REDIRECT_URI`. The value of `YOUR_REQUEST_TOKEN` is the code from the previous step, and the `YOUR_REDIRECT_URI` is the value you used. You should log in to Pocket and authorise the application.

Pocket will then try to redirect you to the redirect URI, which will fail. This is fine.

Now you need to do this:

```
http POST https://getpocket.com/v3/oauth/authorize consumer_key=$CONSUME_KEY code=$YOUR_REQUEST_TOKEN
```

This uses the consumer key for your app, and the code you obtained in step 1. The output of this is an access token you can use with the script.

## Safari bookmarks file

Copy your Safari bookmarks file to the same directory as this script. It's `~/Library/Safari/Bookmarks.plist`. You may need to authorise your terminal or other app to access it.

## Write configuration

Create a file called `.env` and in it put:

```
ACCESS_TOKEN=...
CONSUMER_KEY=...
STOP_TITLE=some-unique-substring-to-stop-processing
```

If you do not need to stop processing before the end of the file, define `STOP_TITLE` without a value.

## Run the script

You'll need pipenv (`pip3 install --user pipenv`), and Python 3 is preferred. (In fact, Python 2 is untested.)

```
pipenv install
pipenv run import.py
```
