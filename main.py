from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

class Item():
    def __init__(self, name,amount):
        self.name=name
        self.amount=amount
        
def toggleFavoriteStatusHandler(meetup):
    meetupData = {
            "title": meetup.title,
            "address": meetup.address,
            "images": meetup.images,
            "description": meetup.description,
            "averageRating": meetup.averageRating,
            "reviews": meetup.reviews,
            "owner": meetup.owner,
            "isFavorite": not(meetup.isFavorite),
            "category": meetup.category,
            };
    requests.put("https://meetup-getup-python.bscebeci.de/api/meetups/${meetup.id}", meetupData)
    
def submitHandler(meetupData):
    requests.post("https://meetup-getup-python.bscebeci.de/api/meetups", meetupData)

@app.route('/')
def hello():
    items=[
        Item("Apfel",5),
        Item("Birne",1),
        Item("Banane",4)
        ]
    
    person=("Bkr", "Tkr")
    
# items=[{"name":"Apfel", "amount":5},{"name":"Birne", "amount":5},{"name":"Banane", "amount":5}]

    return render_template("start.html", person=person, items=items)

@app.route('/test')
def test():
    name = request.args.get("name")
    age = request.args.get("age")
    return render_template("test.html", name=name, age=age)

# if name and age have no data, what should done in html written.

@app.route('/currency')
def currency():
    currency = request.args.get("currency", "EUR")
    amount = float(request.args.get("amount", 1))
    rate = float(request.args.get("rate", 1))
    excurrency = request.args.get("excurrency", "EUR")
    
    examount = round(amount * rate, 2)
    
    return render_template("currency.html", currency=currency, rate=rate, amount=amount, excurrency=excurrency, examount=examount)

@app.route('/exchangetable')
def exchangetable():
    currency1 = request.args.get("currency1", "EUR")
    rate = float(request.args.get("rate", 1))
    currency2 = request.args.get("currency2", "EUR")
    
    table1=[]
    table2=[]
    
    for x in range (1,50):
        table1.append((x, round(x*rate, 2)))
        
    for x in range (1,50):
        table2.append((x, round(x/rate,2)))
    
    
    return render_template("exchangetable.html", currency1=currency1, rate=rate, currency2=currency2, table1=table1, table2=table2)

@app.route('/books', methods=['GET'])
def books():
    req= requests.get("https://apis-for-beginner.bscebeci.de/api/books")
    data=req.content
    books=json.loads(data)
    
    return render_template("books.html", books=books)

@app.route('/allmeetups', methods=['GET','PUT'])
def allmeetups():
    req= requests.get("https://meetup-getup-python.bscebeci.de/api/meetups")
    data=req.content
    meetups=json.loads(data)
    
    return render_template("allmeetups.html", meetups=meetups, toggleFavoriteStatusHandler=toggleFavoriteStatusHandler)

@app.route('/favorites', methods=['GET','PUT'])
def favorites():
    req= requests.get("https://meetup-getup-python.bscebeci.de/api/meetups")
    data=req.content
    meetups=json.loads(data)
    
    return render_template("favorites.html", meetups=meetups, toggleFavoriteStatusHandler=toggleFavoriteStatusHandler)

@app.route('/newmeetup', methods=['POST'])
def newmeetup():
    title = request.args.get("title", "Enter title hier")
    image = request.args.get("image", "https://picsum.photos/520/460")
    address = request.args.get("address", "Asd Str. 16, 546372, Oklohama")
    category = request.args.get("category", "Meetup")
    description=request.args.get("description", "This is a meetup...")
    
    meetupData = {
            "title": title,
            "address": address,
            "images": image,
            "description": description,
            "category": category,
            };
    
    return render_template("newmeetup.html", title=title,image=image, address=address, category=category, description=description, submitHandler=submitHandler)

  
if __name__ == '__main__':
    app.run()