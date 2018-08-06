
from flask import Flask, Response
from kafka import KafkaConsumer
import json, ast

consumer = KafkaConsumer('vts', group_id='view', bootstrap_servers=['0.0.0.0:9092'])
app = Flask(__name__)

@app.route('/')
def index():
    try:
        print("HELLO")
        data = kafkastream()
        for i in data:
            i_decoded = i.decode('utf-8').replace("'", '"')
            c = json.loads(i_decoded)
            coordinates = ast.literal_eval(c)
        
        #return Response(stream_template('test.html', coordinates=data))
        return Response(data, mimetype='application/json')
        #return render_template(devicelocation.html, coordinates=coordinates)
    except:
        print("Something went wrong")

def stream_template(template_name, **context):
    app.update_template_context(context)
    t = app.jinja_env.get_template(template_name)
    rv = t.stream(context)
    rv.enable_buffering(5)
    return rv


def kafkastream():
    print("So what's up")
    for msg in consumer:
        #print(msg)
        #print(msg.value)
        #print(type(msg.value))
        yield(msg.value)

if __name__ == '__main__':
    app.run(host='192.168.2.3', debug=True)