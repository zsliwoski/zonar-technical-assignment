import json
from flask import Flask, abort, request, jsonify, make_response
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///wishlists.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

''' Creating database tables '''
@app.before_first_request
def create_table():
    db.create_all()

''' API friendly error handler '''
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

''' Adds a new wishlist entry for "book_id" to list with "list_id" '''
@app.route('/data/wishlist/add', methods = ["POST"])
def add_wishlist_entry():
    if not request.json or not 'book_id' in request.json or not 'list_id' in request.json:
        abort(400)

    print (json.dumps(request.json))
    
    newListEntry = WishlistEntryModel(list_id = request.json['list_id'], book_id = request.json['book_id'])
    
    db.session.add(newListEntry)
    db.session.commit()
    db.session.flush()
    
    db.session.refresh(newListEntry)

    obj = {"data": newListEntry.obj()}

    return obj

''' List all entries for wishlist "list_id" '''
@app.route('/data/wishlist/get/<int:list_id>', methods = ["GET"])
def get_wishlist_entries(list_id):
    query = db.session.query(WishlistModel)
    query.join(WishlistEntryModel, WishlistEntryModel.list_id == WishlistModel.id)
    query.join(BookModel, WishlistEntryModel.book_id == BookModel.id)
    
    wishlist = query.filter(WishlistModel.id == list_id).one()
    
    obj = {"data":wishlist.obj()}

    return obj

''' Gets all wishlists with their entries'''
@app.route('/data/wishlist/get', methods = ["GET"])
def get_all_wishlists():
    query = db.session.query(WishlistModel)
    query.join(WishlistEntryModel, WishlistEntryModel.list_id == WishlistModel.id)
    query.join(BookModel, WishlistEntryModel.book_id == BookModel.id)

    all_wishlists = query.all()

    output = []
    for row in all_wishlists:
        output.append(row.obj())
    obj = {"data":output}

    return obj

''' Updates the book for an existing wishlist entry with "id" '''
@app.route('/data/wishlist/update/<int:entry_id>', methods = ["PUT"])
def update_entry(entry_id):
    if not request.json or not 'book_id' in request.json:
        abort(400)

    query = db.session.query(WishlistEntryModel).filter(WishlistEntryModel.id == entry_id)
    entry = query.first()
    entry.book_id = request.json['book_id']    
    
    db.session.commit()
    
    obj = {"data": entry.obj()}

    return obj

'' 'Deletes an existing wishlist entry at "list_id" with "entry_id" '''
@app.route('/data/wishlist/delete/<int:entry_id>', methods = ["DELETE"])
def delete_entry(entry_id):
    entry = db.session.query(WishlistEntryModel).filter(WishlistEntryModel.id == entry_id).first()
    
    db.session.delete(entry)
    db.session.commit()
    
    obj = {"data": {"deleted_entry_id" : entry_id}}
    
    return obj


if __name__ == '__main__':
    app.run(debug=True)