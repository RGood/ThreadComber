# oauth PRAW template by /u/The1RGood #
#==================================================Config stuff====================================================
import time, praw, prawcore
import webbrowser
from flask import Flask, request

#==================================================End Config======================================================
#==================================================OAUTH APPROVAL==================================================
app = Flask(__name__)

CLIENT_ID = 'IIgSuhQ2_91vmg' #SET THIS TO THE ID UNDER PREFERENCES/APPS
CLIENT_SECRET = 'eIYckpM8ty_AZefhNALotWJw3qY' #SET THIS TO THE SECRET UNDER PREFERENCES/APPS
scope = 'identity read privatemessages' #SET THIS. SEE http://praw.readthedocs.org/en/latest/pages/oauth.html#oauth-scopes FOR DETAILS.

REDIRECT_URI = 'http://127.0.0.1:65010/authorize_callback'

#Kill function, to stop server once auth is granted
def kill():
	func = request.environ.get('werkzeug.server.shutdown')
	if func is None:
		raise RuntimeError('Not running with the Werkzeug Server')
	func()
	return "Shutting down..."

#Callback function to receive auth code
@app.route('/authorize_callback')
def authorized():
    global REFRESH_TOKEN
    code = request.args.get('code','')
    try:
        REFRESH_TOKEN = r.auth.authorize(code)
    except:
        traceback.print_exc(file=sys.stdout)
    text = 'Bot started on /u/' + r.user.me().name
    kill()
    return text
	
r = praw.Reddit(
	client_id=CLIENT_ID,
	client_secret=CLIENT_SECRET,
	redirect_uri=REDIRECT_URI,
	user_agent='Threadcomber Example')
print(r.auth.url(scope.split(' '),'UniqueKey'))
app.run(debug=False, port=65010)

def list_in_title(list, title):
	for word in list:
		if(not mentions_word(title,word)):
			return False
	return True

def mentions_word(body,sub):
	result = (sub in body)
	if(result):
		result &= ((body.find(sub) + len(sub) == len(body)) or not (body[body.find(sub) + len(sub)].isalnum() or body[body.find(sub) + len(sub)]=='_'))
	if(result):
		result &= ((body.find(sub)==0) or not (body[body.find(sub)-1].isalnum() or body[body.find(sub) - 1]=='_'))
	return result

#==================================================END OAUTH APPROVAL-=============================================

running = True

words = [
  ['word1', 'word2'],
  ['word1', 'word3'],
  ['word1', 'word4'],
  ['word1']
]

whitelist_subreddit = [
	'subreddit1',
	'subreddit2',
	'subreddit3'
]

subreddit = r.subreddit('+'.join(whitelist_subreddit))

target = r.redditor('<username>')

while(running):
	try:
		for post in subreddit.stream.submissions():
			for wordlist in words:
				if(list_in_title(wordlist, post.title.lower())):
					target.message('Post found with keywords ' + ' '.join(wordlist), post.permalink)

					print('===========')
					print('Keywords Found: ' + ' '.join(wordlist))
					print(post.title)
					print(post.permalink)
	except prawcore.exceptions.ServerError:
		print('Server Error. Restarting...')
		pass
	except KeyboardInterrupt:
		running = False