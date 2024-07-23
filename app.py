from flask import Flask, request, jsonify
import pandas as pd
import requests

app = Flask(__name__)

# Function to get coordinates from OpenCage Geocoding API
def get_coordinates(place, api_key):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={place}&key={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['results']:
            coordinates = data['results'][0]['geometry']
            return coordinates['lat'], coordinates['lng']
    return None, None

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file:
        df = pd.read_csv(file)
        api_key = 'YOUR_OPENCAGE_API_KEY'
        df['Latitude'], df['Longitude'] = zip(*df['Place'].apply(lambda x: get_coordinates(x, api_key)))
        result = df.to_dict(orient='records')
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
