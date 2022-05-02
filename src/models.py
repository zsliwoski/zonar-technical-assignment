import json
from flask_sqlalchemy import SQLAlchemy, DeclarativeMeta

db = SQLAlchemy()


# Converts a model to its dictionary representation
def to_dict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

# Represents a user
class UserModel(db.Model):
    __tablename__ = "user"
 
    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
 
    def __init__(self, first_name, last_name, email, password_hash):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = password_hash

    def __repr__(self):
        return '{"id":' + str(self.id) + ',"first_name":"' + self.first_name + '", "last_name" : "' + self.last_name + '", "email" : "' + self.email + '"}'
    
    def obj(self):
        return {
            "id" : self.id,
            "first_name" :  self.first_name, 
            "last_name" : self.last_name , 
            "email" :  self.email
        }
# Represents a book
class BookModel(db.Model):
    __tablename__ = "book"
 
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(), nullable=False)
    author = db.Column(db.String(), nullable=False)
    isbn = db.Column(db.String(), nullable=False)
    publish_date = db.Column(db.Date(), nullable=False)
 
    def __init__(self, title, author, isbn, publish_date):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publish_date = publish_date

    def __repr__(self):
        return '{"id":' + str(self.id) + ',"publish_date":"' + str(self.publish_date) + '", "title" : "' + str(self.title) + '", "author" : "' + self.author + '", "isbn" : "' + self.isbn + '"}'
    
    def obj(self):
        return {
            "id" : self.id,
            "title" :  self.title , 
            "author" : self.author , 
            "isbn" :  self.isbn ,
            "publish_date" : str(self.publish_date)
        }

# Represents an overarching wishlist
class WishlistModel(db.Model):
    __tablename__ = "wishlist"
 
    id = db.Column(db.Integer, primary_key=True)
    
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    name = db.Column(db.String())

    owner = db.relationship('UserModel', backref='wishlists', lazy=True)
    entries = db.relationship('WishlistEntryModel', backref='wishlist', lazy=True)

    def __init__(self, name, owner_id):
        self.owner_id = owner_id
        self.name = name

    def __repr__(self):
        return '{"id":' + str(self.id) + ',"owner":' + repr(self.owner) + ', "name" : "' + self.name + '"}'

    def obj(self):
        entry_list = []
        owner_obj = None
        
        if (self.owner):
            owner_obj = self.owner.obj()
        
        if (self.entries):
            for entry in self.entries:
                entry_list.append(entry.obj())
        
        return {
            "id" : self.id,
            "name" :  self.name , 
            "owner" : owner_obj, 
            "entries" :  entry_list ,
        } 
           
# Represents an individual entry on a wishlist
class WishlistEntryModel(db.Model):
    __tablename__ = "wishlist_entry"
 
    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('wishlist.id', ondelete='cascade'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='cascade'), nullable=False)
 
    book = db.relationship('BookModel', backref='wished_for', lazy=True)

    def __init__(self, list_id, book_id):
        self.list_id = list_id
        self.book_id = book_id
 
    def __repr__(self):
        return '{"id":' + str(self.id) + ', "book" : ' + repr(self.book) + ', "wishlist" : ' + repr(self.wishlist) + '}'
    
    def obj(self):
        book_obj = None
        if (self.book):
            book_obj = self.book.obj()
        return {
            "id" : self.id, 
            "book" : book_obj,
        } 