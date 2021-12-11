from dataclasses import dataclass
import requests


from hypothesis import settings
from hypothesis import settings, Phase
import hypothesis.strategies as some
from hypothesis import settings
import hypothesis.strategies as some
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize


####################################################################################
# hypothesis strategies:

lower_case_ascii = some.characters(min_codepoint=0, max_codepoint=100, whitelist_categories=('Ll',))
names = some.text(lower_case_ascii, min_size=1, max_size=4)
non_empty_names = names\
    .map(lambda s: s.strip())\
    .filter(lambda s: len(s) > 0)
some_book_data = some.tuples(non_empty_names, non_empty_names)\
    .map(lambda tup: BookData(title=tup[0], author=tup[1]))


####################################################################################
# Helper data classes:
@dataclass
class BookData(object):
    title: str
    author: str


####################################################################################
# Test model
class MySrvTestHttp(RuleBasedStateMachine):
    """
    A stateful test (also rule-based state machine or model-based test).
    """
    def __init__(self):
        super(MySrvTestHttp, self).__init__()
        self.host = "http://localhost:5000"

        self.book_count = 0

    @initialize()
    def init_test(self):
        self._clear()

    def teardown(self):
        self._clear()

    def _clear(self):
        requests.get(f"http://localhost:5000/clear")

    @rule(book_data=some_book_data)
    def new_book(self, book_data: BookData):
        # Execute action
        requests.post(
            f"http://localhost:5000/books",
            json={
                "title": book_data.title,
                "author": book_data.author,
                "read": False
            },
        )

        # State transition
        self.book_count += 1

    @rule()
    def list_books(self):
        # Execute action
        res = requests.get(f"http://localhost:5000/books")
        book_list_from_server = res.json()["books"]

        # Post-condition
        assert len(book_list_from_server) == self.book_count


MySrvTestHttp.TestCase.settings = settings(
    max_examples=50,
    stateful_step_count=100,
    deadline=None,
)

TestMySrvTest = MySrvTestHttp.TestCase
