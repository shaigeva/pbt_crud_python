from dataclasses import dataclass

from hypothesis import given, settings
from hypothesis import given, example, settings, Phase
import hypothesis.strategies as some
from pytest import skip
from pytest import mark

import requests


from hypothesis import given, example, settings
import hypothesis.strategies as some
from hypothesis.stateful import Bundle, RuleBasedStateMachine, rule, invariant, initialize

from src.srv_class import SrvClass


def test_foo():
    srv = SrvClass()
    srv.new_user("foo", "bar@baz.com")
    assert srv.get_user_email_address("foo")["email_address"] == "bar@baz.com"

####################################################################################
# hypothesis strategies:


lower_case_ascii = some.characters(min_codepoint=0, max_codepoint=100, whitelist_categories=('Ll',))
names = some.text(lower_case_ascii, min_size=1, max_size=4)
non_empty_names = names\
    .map(lambda s: s.strip())\
    .filter(lambda s: len(s) > 0)
some_book_data = some.tuples(non_empty_names, non_empty_names)\
    .map(lambda tup: BookData(title=tup[0], author=tup[1]))


@dataclass
class BookData(object):
    title: str
    author: str


class MySrvTestHttp(RuleBasedStateMachine):
    """
    A stateful test (also rule-based state machine or model-based test).
    Verifies that when we add and remove subscribers in whatever sequence (order,
    number of times), the last subscription action (subscribe / unsubscribe) for
    a specific subscriber is the current state.
    """
    def __init__(self):
        super(MySrvTestHttp, self).__init__()
        self.book_count = 0

        self.host = "http://localhost:5000"


        self.existing_books = {}

    created_books = Bundle("books")

    @initialize()
    def init_test(self):
        self._clear()

    def teardown(self):
        self._clear()

    def _clear(self):
        requests.get(f"http://localhost:5000/clear")

    @rule(target=created_books, book_data=some_book_data)
    def new_book(self, book_data: BookData):
        res = requests.post(
            f"http://localhost:5000/books",
            json={
                "title": book_data.title,
                "author": book_data.author,
                "read": False
            },
        )

        self.book_count += 1

        added_book = res.json()["book"]
        self.existing_books[added_book["id"]] = added_book
        return added_book

    @rule(created_book=created_books)
    def update_book(self, created_book):
        created_book['author'] = created_book['author'] + "_updated"
        requests.put(
            f"http://localhost:5000/books/{created_book['id']}",
            json={
                "id": created_book['id'],
                "title": created_book['title'],
                "author": created_book['author'],
                "read": False
            },
        )

    @rule(created_book=created_books)
    def delete_book(self, created_book):
        requests.delete(
            f"http://localhost:5000/books/{created_book['id']}",
        )

        book_id = created_book["id"]
        if book_id in self.existing_books:
            self.existing_books.pop(book_id)
            self.book_count -= 1

    @rule()
    def get_all_books(self):
        res = requests.get(
            f"http://localhost:5000/books",
        )

        book_list_from_server = res.json()["books"]
        assert len(book_list_from_server) == self.book_count


# For performance sake, reduce the number of iterations.
# IIUC, max_examples defaults to 100 and stateful_step_count defaults to 50.

# MySrvTest.TestCase.settings = settings(
#     max_examples=50,
#     stateful_step_count=50,
# )


MySrvTestHttp.TestCase.settings = settings(
    max_examples=50,
    stateful_step_count=100,
    deadline=None,  # I got a warning from Hypothesis recommending this.
)

TestMySrvTest = MySrvTestHttp.TestCase
# TestMySrvTest = MySrvTest.TestCase

