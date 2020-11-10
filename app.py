from flask import Flask, render_template
import Scrape 

app = Flask(__name__)

@app.route("/") 
def home():

    return render_template("index.html")
@app.route("/gantt.html") 
def gantt():
    return render_template("gantt.html")
@app.route("/radial.html") 
def radial():
    return render_template("radial.html")    

@app.route("/bar.html") 
def bar():

    return render_template("bar.html")


@app.route("/scrape") 
def scrape():
    
    data = Scrape.scrapping() #activates the scrapping function

    return render_template("scrape.html", xyz = data )
    

if __name__ == "__main__":
    app.run()





  
