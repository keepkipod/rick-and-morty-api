from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_characters(url):
    characters = []
    while url:
        response = requests.get(url)
        data = response.json()
        characters.extend(data['results'])
        url = data['info']['next']
    return characters

def filter_characters(characters):
    return [
        {
            'name': char['name'],
            'location': char['location']['name'],
            'image': char['image']
        }
        for char in characters
        if char['species'] == 'Human' and 
           char['status'] == 'Alive' and 
           char['origin']['name'].startswith('Earth')
    ]

@app.route('/healthcheck')
def healthcheck():
    return jsonify({"status": "healthy"}), 200

@app.route('/characters')
def get_filtered_characters():
    base_url = 'https://rickandmortyapi.com/api/character'
    all_characters = get_characters(base_url)
    filtered_characters = filter_characters(all_characters)
    return jsonify(filtered_characters)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)