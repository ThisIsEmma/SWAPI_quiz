from flask import Flask, request, render_template
from pprint import PrettyPrinter
import json
import requests

app = Flask(__name__)

pp = PrettyPrinter(indent=4)

@app.route('/', methods = ['GET'])
def swapi_result():
    # Get  Character info:
    id = request.args.get('id')
    response = requests.get(f'https://swapi.py4e.com/api/people/{id}')
    result = json.loads(response.content)
    #pp.pprint(result)

    # Get character homeworld and films info:
    if 'detail' in result:
        result['homeworld'] = ''
        homeworld_results = ''
        result['films'] = ''
        film_title_list = []
    else:
        # Homeworld
        homeworld_url = result['homeworld']
        homeworld_response = requests.get(homeworld_url)
        homeworld_results = json.loads(homeworld_response.content)
        #pp.pprint(homeworld_results)

        # list of films: 
        list_of_film = result['films']
        film_title_list = [] # to store all the film titles that we will receive from API request
        for url in list_of_film:
                film_results = json.loads((requests.get(url)).content)
                film_title = film_results['title']
                film_title_list.append(film_title)

    context = {
        'id' : id,
        'character' : result,
        'homeworld' : homeworld_results,
        'films' : film_title_list,
    }
    return render_template('index.html', **context)


if __name__ == "__main__":
    app.run(debug=True, port=3000)
