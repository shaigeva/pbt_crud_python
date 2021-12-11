import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

BOOKS_DEFAULT_LIST = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]

BOOKS = {}

# configuration
# DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        added_book = _add_book(post_data)
        response_object['message'] = 'Book added!'
        print(f"returning book: {added_book}")
        response_object['book'] = added_book
    else:
        response_object['books'] = list(BOOKS.values())
    return jsonify(response_object)


@app.route('/clear', methods=['GET'])
def clear():
    response_object = {'status': 'success'}
    BOOKS.clear()
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        print("book_id:" + book_id)
        post_data = request.get_json()
        _remove_book(book_id)
        _add_book(post_data, book_id)
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        _remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


def _remove_book(book_id):
    if book_id not in BOOKS:
        return False
    else:
        BOOKS.pop(book_id)
        return True


def _add_book(post_data, _id=None):
    book = _book_from_post_data(post_data, _id)
    BOOKS[book['id']] = book
    return book
    # BOOKS.append()


def _book_from_post_data(post_data, _id=None):
    if not _id:
        _id = uuid.uuid4().hex
    return _mk_book(
        _id=_id,
        title=post_data.get('title'),
        author=post_data.get('author'),
        read=post_data.get('read'),
    )


def _mk_book(_id, title, author, read):
    return {
        'id': _id,
        'title': title,
        'author': author,
        'read': read,
    }


def run():
    app.run()


if __name__ == '__main__':
    app.run()
