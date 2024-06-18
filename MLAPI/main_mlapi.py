import base64
import datetime

import requests
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS, cross_origin

import Stable_diff

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy   dog'
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/txttoimg": {"origins": "http://localhost:8080"}})


@app.route('/txttoimg', methods=['POST'])
@cross_origin(origin='http://localhost:8080', headers=['Content-Type', 'Authorization'])
def txttoimg():
    data = request.get_json()

    url = "http://127.0.0.1:7860"

    payload = {
        "prompt": Stable_diff.getEnhancedPrompt(data["prompt"]),
        "negative_prompt": "blurry, grainy, bad anatomy, easynegative, bad proportions, worst quality, ugly, difformed, day, sun, man, multiple people",
        "steps": 50
    }

    # Send said payload to said URL through the API.
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    r = response.json()

    # Decode and save the image.
    now = datetime.datetime.now()
    with open("..\\MLFRONT\\src\\assets\\generated\\" + f'{now:20%y%m%d_%H%M%S}' + "_Generated.png", 'wb') as f:
        f.write(base64.b64decode(r['images'][0]))

    response = {"status": "success", "filename": f'{now:20%y%m%d_%H%M%S}' + "_Generated.png"}
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
