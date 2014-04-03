import time
from flask import Flask, request
import requests

# importing models
from models.eutopia.eutopia import Eutopia
from models.eutopia.intervention import PriceIntervention, NewActivityIntervention

app = Flask(__name__)

@app.route("/", methods=['POST', 'GET'])
def hello():

    if request.method == 'POST':
        print "POST request received!"
        print request.form.keys()
        message_type = request.form['message_type']
        
        if message_type == 'add_intervention':
            
            scale = request.form['tax_value']
            product = request.form['activity']
            time = request.form['year']
            
            model.intervene(PriceIntervention(time, product, scale))
            print "Added a new intervention!"
        
        elif message_type == 'game_state':
            state = request.form['game_state']
            print state
            if state == 'play':
                print "Play the game!"
                play_game[0] = True
                time_runner()
                
            elif state == 'pause':
                print "Game paused!"
                play_game[0] = False
    else:
        print request
        return "Hello World!"

def time_runner(pause_length=1, iterations=20, year=0):
    print model.interventions #list of intervention objects

    print play_game[0]
    while(play_game[0]):
        time.sleep(pause_length)
        next(model) #just runs the iteration
        payload = model.log[year][1]
        print payload
        requests.post(model_listener, data = payload)
        year += 1
    
    
    
if __name__ == "__main__":
    model = Eutopia([]) #the [] becomes model.log
    play_game = [False] # hack to make it "global"
    model_listener = "http://localhost:9080"
    app.run()


