from flask import Flask, render_template
from flask import request
import argparse
import threading
import time
import os

from emojiParser import Parser

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
    emoj = ps.getEmogi(animal_name)
    return_list = [f"{emoj} says {animal_sound}" for _ in range(round(animal_count))]
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
    if attrs is None or len(attrs) == 0:
        ip_address = req.remote_addr
        proto = req.scheme
        return render_template("form.html", ip_address=ip_address, proto=proto, port=args.port)
    elif not (animal_key in attrs.keys() and sound_key in attrs.keys() and count_key in attrs.keys()):
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
    print(f"Current working directory {os.getcwd()}")
    print(f"Cert path: {args.sslcert}")
    print(f"Key path: {args.sslkey}")
    app.debug = True
    app.run(host=args.host, port=args.port, ssl_context=(args.sslcert, args.sslkey), threaded=True, debug=False)


def runHttp():
    print("Running http")
    app.run(host=args.host, port=args.port, threaded=True, debug=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="AwesomeZoo Flask Application")
    parser.add_argument('-s', '--source', help=' Change emogipedia data source. ', type=str, default='https://emojipedia.org/nature/')
    parser.add_argument('-H', '--host', help=' Change application host ', type=str, default='0.0.0.0')
    parser.add_argument('-p', '--port', help=' Change listening post', type=int,
                        default=80)
    parser.add_argument('-ssl', '--usessl', help=' Using ssl on selected port', type=bool,
                        default=False)
    parser.add_argument('-sk', '--sslkey', help=' Determinate relative path to SSl Key ', type=str,
                        default="cert/key.pem")
    parser.add_argument('-sc', '--sslcert', help=' Determinate relative path to SSl Certificate ', type=str,
                        default='cert/cert.pem')
    args = parser.parse_args()
    ps = Parser('https://emojipedia.org/nature/')
    ps.parseDatabase()
    if args.usessl:
        runHttps()
    else:
        runHttp()


