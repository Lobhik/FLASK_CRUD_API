
from flask import Flask, make_response, request, jsonify
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import pymongo



# from api constants import mongodb_password



connection_url = 'mongodb+srv://test:test@cluster0.9yqld.mongodb.net/?retryWrites=true&w=majority'
app = Flask(__name__)
client = pymongo.MongoClient(connection_url)

# Database
Database = client.get_database('CRUD')
# database_name = "CRUD"

# DB_URI = "mongodb+srv://test:test@cluster0.9yqld.mongodb.net/?retryWrites=true&w=majority"
# #app.config["MONGODB_HOST"]= DB_URI
app.config["MONGO_URI"] = "mongodb+srv://test:test@cluster0.9yqld.mongodb.net/?retryWrites=true&w=majority"
db = MongoEngine()
db.init_app(app)




class Book(db.Document):
    book_id= db.IntField()
    name = db.StringField()
    author = db.StringField()
    def to_json(self):
        return {
            "book_id": self.book_id,
            "name": self.name,
            "author": self.author
            }

#converts this document to JSON

    

#

@app.route('/api/db_populate', methods=['POST']) 
def db_populate():

    book1 = Book (book_id=1, name="A Game of Thrones", author="George RR Martin")

    book2 = Book(book_id=2, name="Lord of the Rings", author="JRR Tolkien")

    book1.save()

    book2.save()

    return make_response("", 201)


#


@app.route('/api/books', methods=['GET', 'POST']) 
def api_books():
    if request.method == "GET":
        print(request.method)
        books = []
        for book in Book.objects:
            books.append(book)
            return make_response(jsonify(books), 200)
    elif request.method =="POST":
        content = request.json
        book = Book (book_id=content['book_id'],
        name=content['name'],author=content['author'])
        book.save()
        return make_response("",201)
	
#



@app.route('/api/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_book(book_id):
    if request.method =="GET":
        book_obj = Book.objects(book_id=book_id).first()
        if book_obj:
            return make_response(jsonify(book_obj.to_json()), 200)
        else:
            return make_response("", 404)
		
		
		
    elif request.method == "PUT":
        content = request.json
        book_obj = Book.objects(book_id=book_id). first()
        book_obj.update (author=content['author'], name=content['name'])
        return make_response("", 204)
    
    elif request.method == "DELETE":
        book_obj = Book.objects(book_id=book_id).first()
        book_obj.delete()
        return make_response(" ", 204)
	
	



if __name__ == "__main__":
    app.run(debug=True)
