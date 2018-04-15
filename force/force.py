
from flask import Flask, Markup, render_template, request
import tweepy
from tweepy.api import API
import sqlite3 
import sys
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import forceatlas2
import random 
import forceatlas2
import matplotlib.image as mpimg
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import d3py
import json
from networkx.readwrite import json_graph
import json
import flask
import networkx as nx
from networkx.readwrite import json_graph

conn = sqlite3.connect('tablet12.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS tweets(text VARCHAR, created_at DATETIME, id Number, retweeted BOOLEAN, retweet_count Number, reply_count Number, quote_count integer, in_reply_to_user_id_str VARCHAR, truncated BOOLEAN, source VARCHAR, user_id integer, retweeted_id integer)")

conn = sqlite3.connect('tablet12.db')
x = conn.cursor()
consumer_key="******************"
consumer_secret="**************"
access_token="***************"
access_token_secret="***********************"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

class CustomStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.n = 0
        self.m = 10
        super(tweepy.StreamListener, self).__init__()
       
        plt.figure(figsize=(15,10))
        #p = 0
    def on_status(self, status):


        if hasattr(status, 'retweeted_status'):

         x.execute("""INSERT INTO tweets (text,created_at,id,retweeted,retweet_count,reply_count,quote_count,in_reply_to_user_id_str,truncated,source,user_id,retweeted_id)
                                            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
          (status.text, status.created_at, status.id, status.retweeted, status.retweet_count, status.reply_count,status.quote_count,status.in_reply_to_user_id_str,status.truncated,status.source,status.user.id,status.retweeted_status.user.id))
         conn.commit()
        
          #p.show()  
        
          #pos = { i : (random.randint(1, 5), random.randint(1, 5)) for i in G.nodes()} # Optionally specify positions as a dictionary
          #l = forceatlas2.forceatlas2_networkx_layout(G)# Optionally specify iteration count     
          #nx.draw_networkx(G,pos=l,node_size=25,font_size=5,arrows=True, with_labels=False)
          #nx.write_gexf(G, "graph.gexf", version="1.2draft")
          #nx.draw(G,with_labels=True)
         return True

        else:

         self.n = self.n+1
         if self.n < self.m: 
          df = pd.read_sql_query("SELECT * from tweets", conn)
          print(df)
          G=nx.from_pandas_dataframe(df,'retweeted_id','user_id')#,create_using=nx.DiGraph()
          l = forceatlas2.forceatlas2_networkx_layout(G)# Optionally specify iteration count 
          nx.draw_networkx(G,pos=l,node_size=25,font_size=5,arrows=True, with_labels=True)
          print 'tweets = '+str(self.n)
          d = json_graph.node_link_data(G)  # node-link format to serialize
          # write json
          json.dump(d, open('force/force.json', 'w'))
          print('Wrote node-link JSON data to force/force.json')
          #plt.show() 
          return False
          #img=mpimg.imread("outputwithoutFA.png")
          #self.output.close()
          #imgplot = plt.imshow(img)
          #plt.axis('off')
          #plt.savefig("out.png", transparent = False)
        

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True


#sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))#uncomment line 100 and 101 when not using default flask route '/' 
#sapi.filter(track=['trump'])

# this d3 example uses the name attribute for the mouse-hover value,
# so add a name to each node
# write json formatted data

# Serve the file over http to allow for cross origin requests
app = flask.Flask(__name__, static_folder="force")
@app.route('/')
def tweet():
   return render_template('enter_tweet.html')

@app.route('/gettweet', methods = ['POST', 'GET'])
def gettweet():
   if request.method == 'POST':
        nm = request.form['nm']
        sapi = tweepy.streaming.Stream(auth, CustomStreamListener(api))
        sapi.filter(track=[nm])
        return render_template('force.html')

'''@app.route('/<path:path>')
def static_proxy(path):
    return app.send_static_file(path)'''

print('\nGo to http://localhost:8000/force.html to see the example\n')

if __name__ == "__main__":

  app.run(debug=True)
