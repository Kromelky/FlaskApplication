from flask import Flask
from flask import request
from OpenSSL import SSL
import logging
import threading
import time
import os

app = Flask(__name__)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)
service_name = 'AwesomeZooService'
dev_name = 'Gusarov Artem'
dev_repo = 'https://github.com/Kromelky'
animal_key = 'animal'
sound_key = 'sound'
count_key = 'count'


def get_MainMessage(animal_name, animal_sound, animal_count):
    if animal_count < 0:
        animal_count = abs(animal_count)
    if animal_count > 100000:
        return f"Error: too much values requested"
    return_list = [f"{animal_name} says {animal_sound}" for _ in range(round(animal_count))]
    return_list.append(get_AuthorMessage(service_name, dev_name))
    return "\n".join(return_list)


def get_AuthorMessage(ser_name, name):
    return f"Made with {ser_name} by {name}"


def processRequest(req):
    print(request.environ.get('SERVER_PROTOCOL'))
    if req.method == 'POST':
        if req.is_json:
            data = req.get_json(force=True)
            attrs = dict(data)
        else:
            attrs = req.form
    if req.method == 'GET':
        attrs = req.args
    if attrs is None:
        return "Error: missing attribute collection"
    if not (animal_key in attrs.keys() and sound_key in attrs.keys() and count_key in attrs.keys()):
        return "Error: missing required attributes"
    try:
        animal_count = int(attrs[count_key])
    except ValueError:
        return "ValueError: count couldn't convert to int"
    animal_name = attrs[animal_key]
    animal_sound = attrs[sound_key]

    response = get_MainMessage(animal_name, animal_sound, animal_count)
    return response


@app.route("/", methods=['GET', 'POST'])
def httpRoot():
    return processRequest(request)


def runHttps():
    print("Running https")
    cert_ditr = os.getcwd() + os.path.sep + "cert"
    priv_key = cert_ditr + os.path.sep + "key.pem"
    cert = cert_ditr + os.path.sep + "cert.pem"
    print(f"Cert path: {cert}");
    print(f"Cert path: {priv_key}");
    app.run(host="0.0.0.0", port=433, ssl_context=(cert, priv_key), threaded=True)


def runHttp():
    print("Running http")
    app.run(host="0.0.0.0", port=80, threaded=True)


if __name__ == '__main__':

    httpThread = threading.Thread(target=runHttp)
    httpThread.start()
    time.sleep(2)
    httpsThread = threading.Thread(target=runHttps)
    httpsThread.start()
