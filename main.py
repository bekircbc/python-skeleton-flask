from flask import Flask, render_template, request
import requests
import json
app = Flask(__name__)

class Item():
    def __init__(self, name,amount):
        self.name=name
        self.amount=amount

@app.route('/')
def hello():
    items=[
        Item("Apfel",5),
        Item("Birne",1),
        Item("Banane",4)
        ]
    
    person=("Bkr", "Cbc")
    
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
    
    return render_template("allmeetups.html", meetups=meetups, toggleFavoriteStatusHandler=toggleFavoriteStatusHandler)
  
if __name__ == '__main__':
    app.run()