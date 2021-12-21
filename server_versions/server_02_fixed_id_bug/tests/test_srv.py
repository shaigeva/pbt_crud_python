import hypothesis.strategies as some
import requests
from hypothesis import settings
from hypothesis.stateful import Bundle, RuleBasedStateMachine, initialize, rule

URL = "http://localhost:5000"

####################################################################################
# hypothesis strategies:

lower_case_ascii = some.characters(min_codepoint=0, max_codepoint=100, whitelist_categories=('Ll',))
names = some.text(lower_case_ascii, min_size=1, max_size=4)
non_empty_names = names\
    .map(lambda s: s.strip())\
    .filter(lambda s: len(s) > 0)
some_book_data = some.tuples(non_empty_names, non_empty_names)\
    .map(lambda tup: { "title": tup[0], "author": tup[1], "read": False })

####################################################################################
# Test model
class MySrvTestHttp(RuleBasedStateMachine):
    """
    A stateful test (also rule-based state machine or model-based test).
    """
    def __init__(self):
        super(MySrvTestHttp, self).__init__()

        self.book_count = 0

    @initialize()
    def init_test(self):
        self._clear()

    def teardown(self):
        self._clear()

    def _clear(self):
        requests.get(f"{URL}/clear")

    @rule(book_data=some_book_data)
    def new_book(self, book_data):
        # Execute action
        res = requests.post(f"{URL}/books", json=book_data)

        # State transition
        self.book_count += 1

    @rule()
    def list_books(self):
        # Execute action
        res = requests.get(f"{URL}/books")
        book_list_from_server = res.json()["books"]

        # Post-condition
        assert len(book_list_from_server) == self.book_count


MySrvTestHttp.TestCase.settings = settings(
    max_examples=50,
    stateful_step_count=100,
    deadline=None,
)

TestMySrvTest = MySrvTestHttp.TestCase
