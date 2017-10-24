from flask import Flask, render_template, request
import requests
import json

from flask import Flask, request, make_response
app = Flask(__name__)
app.debug = True 

from wtforms import Form, StringField, validators, SubmitField

class ActorForm(Form):
    actor = StringField('Enter Actor:')
    submit = SubmitField('Submit')

@app.route('/')
def artist_form():
	form = ActorForm()
	return render_template('actor.html', form=form)

@app.route('/tvshow', methods = ['POST'])
def show_form():
	if request.method == 'POST':
		term = request.form.get('actor')
		d ={'media': 'movie'}
		resp = requests.get('https://itunes.apple.com/search?term='+term+'&limit=', params=d)
		data = json.loads(resp.text)
		print (data)
		return render_template('seasons.html', results=data['results'])

@app.route('/description/<movie_title>', methods = ['GET', 'POST'])
def movie(movie_title):
	d ={'media': 'movie'}
	resp = requests.get('https://itunes.apple.com/search?term='+movie_title+'&limit=', params=d)
	data = json.loads(resp.text)
	print (data['results'][0]['longDescription'])
	return render_template('movieinfo.html', title=movie_title, des=data['results'][0]['longDescription'])

@app.route('/list', methods = ['GET'])
def movie_list():
	response = make_response('My favorite movie list would go here')
	response.set_cookie('x', 'y')
	return response

@app.errorhandler(404)
def error_1(x):
    return render_template('404.html'), 404

@app.errorhandler(405)
def error_2(y):
	return render_template('405.html'), 405

if __name__ == '__main__':
    app.run(debug=True)