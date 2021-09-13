from flask import Blueprint 
blue_book = Blueprint("book", __name__, url_prefix="/book") 
@blue_book.route("/read") 
def read(): 
    return "this is read" 
@blue_book.route("/write") 
def write(): 
    return "this is write"

