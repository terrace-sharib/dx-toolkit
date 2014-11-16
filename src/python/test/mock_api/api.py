#!/usr/bin/env python3

from __future__ import print_function, unicode_literals

import os, sys, random, hashlib, argparse, io
from flask import Flask, request, jsonify

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("-p", "--port", help="TCP port to serve on", type=int)
args = parser.parse_args()

app = Flask(__name__)
#random.seed(1)

file_desc = {
    "id": "file-0123456789ABCDEF01234567",
    "class": "file",
    "name": "test",
    "state": "closed"
}

@app.route("/system/setPayload", methods=["POST"])
def set_payload():
    payload = io.BytesIO()
    for i in range(4):
        r = random.getrandbits(1024*1024*1024)
        payload.write(r.to_bytes((r.bit_length() // 8) + 1, 'little'))
    app.payload = payload.getvalue()
    file_desc["md5"] = hashlib.md5(app.payload).hexdigest()
    file_desc["size"] = len(app.payload)
    return jsonify(dict())

@app.route("/system/findDataObjects", methods=["POST"])
def find_data_objects():
    results=[]
    results.append(dict(project=request.json["scope"]["project"],
                        id=file_desc["id"],
                        describe=file_desc))
    return jsonify(dict(results=results, next=None))

@app.route("/<resource>/listFolder", methods=["POST"])
def list_folder(resource):
    folders=[]
    objects=[]
    return jsonify(dict(folders=folders, objects=objects))

@app.route("/<resource>/describe", methods=["POST"])
def describe(resource):
    if resource.startswith("project-") or resource.startswith("container-"):
        return jsonify(dict(folders=[]))
    elif resource.startswith("file-"):
        return jsonify(file_desc)
    elif resource.startswith("job-"):
        return jsonify(dict(app="app-0123456789ABCDEF01234567"))
    else:
        return jsonify(dict())

@app.route("/file-<id>/download", methods=["POST"])
def download(id):
    url = request.url_root + "F/D"
    return jsonify(dict(url=url))

@app.route("/F/D", methods=["GET"])
def serve_download():
    start, stop = (int(x) for x in request.headers["range"].split("=")[1].split("-"))
    #print("SERVING", request.url, start, stop, request.headers)
    return app.payload[start:stop+1]

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, port=args.port)
