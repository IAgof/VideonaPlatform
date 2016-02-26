import os
from flask import Flask


app = Flask(__name__)
app.config.from_object('videona_platform.default_settings')

app.logger.debug('Flask instance path is %s' % app.instance_path)

@app.route('/')
def hello_world():
    return '#VideonaTime!'