from flask import Flask, render_template
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_scrape_db


@app.route("/")
def index():
    # get all the mars info from the mars database
    mars_data = db.mars_data.find()

    # render an index.html template and pass it the mars data
    return render_template("index.html", mars_data=mars_data)


@app.route("/scrape")
def scrape():
    # remove data currently in mars database
    db.mars_data.drop()
    mars_web_data = scrape_mars.scrape()

    db.mars_data.insert_one(mars_web_data)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)






