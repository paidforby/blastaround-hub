import os
from flask import Flask, render_template
import time
import datetime
#from wheels import NeoPixelStrip
#from neopixel import *
from multiprocessing import Process, Value, Pool, Manager

app = Flask(__name__)
manager = Manager()
selected_scooter = 0 
selected_mode = manager.Value('i', 0) 

# Create a dictionary of scooters:
# TODO dynamically fill this, or at least, detect if online
scooters = { 
	0 : {'name': 'ReinDog1', 'mode': 0, 'online': True}, 
	1 : {'name': 'ReinDog2', 'mode': 0, 'online': True}, 
	2 : {'name': 'Dinosaur', 'mode': 0, 'online': True},
	3 : {'name': 'Kangaroo', 'mode': 0, 'online': False},
	4 : {'name': 'Elephant', 'mode': 0, 'online': True}
	}

# Create a dictionary of possible modes:
modes = { 
	0 : {'name': 'STANDBY'}, 
	1 : {'name': 'RIDING'}, 
	2 : {'name': 'RIDE_OVER'}
	}

@app.route('/')
def main():
	templateData = {
		'scooters' : scooters,
		'modes' : modes
	}
	return render_template('main.html', **templateData)


# The function below is executed when someone requests a URL with the pin number and action in it:
@app.route("/<set_scooter>/<set_mode>")
def action(set_scooter, set_mode):
        selected_scooter = int(set_scooter)
	selected_mode.value = int(set_mode)
        scooters[selected_scooter]['mode'] = selected_mode.value
	templateData = {
		'scooters' : scooters,
                'selected_scooter': set_scooter,
		'modes' : modes,
		'selected_mode' : selected_mode.value
	}
	return render_template('main.html', **templateData)


def start_lights(state):
	while True:
		wheels.run()
		wheels.update_mode(state.value)
		if state.value == 0:
			wheels.update_speed(.5)
		elif state.value == 1:
			wheels.update_speed(.001)
		elif state.value == 2:
			wheels.update_speed(.3)

def start_server(state):
	app.run(debug=True, use_reloader=False, host='0.0.0.0')


if __name__ == '__main__':
	app.run(debug=True, use_reloader=False, host='0.0.0.0')
	# SCOOTER_COLOR = Color(0, 255, 0)
	# wheels = NeoPixelStrip(4, 24, SCOOTER_COLOR)
	# start_time = time.time()

	# script = Process(target=start_lights, args=(current_mode,))
	# script.start()  
	# server = Process(target=start_server, args=(current_mode,))
	# server.start()
	# script.join()

