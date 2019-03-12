import requests
from flask import Flask
from flask_restful import Resource, Api, reqparse, abort



app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('url')
parser.add_argument('palavra')
parser.add_argument('ignorecase')
	
def count_words_in(url, word, ignore_case):
	try:
		r = requests.get(url)
		data = str(r.text)
		if (str(ignore_case).lower() == 'true'):
			return data.lower().count(word.lower())
		else:
			return data.count(word)
	except Exception as e:
		raise e
		
def validate_url(url):
	if not(url.startswith('http')):
		url = 'http://' + url
	return url
	

class UrlCrawlerAPI(Resource):
	def get(self):
		try:
			args = parser.parse_args()
			valid_url = validate_url(args['url'])
			return { valid_url : { args['palavra'] : count_words_in(valid_url, args['palavra'], args['ignorecase']) }}
		except AttributeError:
			return { 'message' : 'Informe uma URL e uma PALAVRA a ser pesquisada' }
		except Exception as e:
			return { 'message' : 'Indefinido: ' + str(e) }

		
api.add_resource(UrlCrawlerAPI, "/")

if __name__ == '__main__':
	app.run(debug=True)