import hypothesis.strategies as some
import requests
from hypothesis import settings
from hypothesis.stateful import Bundle, RuleBasedStateMachine, initialize, rule

URL = "http://localhost:5001"

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

    # This is a Hypothesis "Bundle".
    # It is a tool that helps manage data that needs to be created by some
    # action and used by others.
    # This specific usage maintains the id-s of books that have been created
    # by the new_book action (@rule).
    created_books = Bundle("books")

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

    @rule(book_data=some_book_data, target=created_books)
    def new_book(self, book_data):
        # Execute action
        res = requests.post(f"{URL}/books", json=book_data)
        created_book = res.json()["book"]

        # State transition
        self.book_count += 1

        # Save the created book id into the Bundle.
        # The mechanism is that because we declared (in the decorator above)
        # that the "target" is created_books - the return value will be placed
        # into the created_books Bundle.
        return created_book["id"]

    @rule()
    def list_books(self):
        # Execute action
        res = requests.get(f"{URL}/books")
        book_list_from_server = res.json()["books"]

        # Post-condition
        assert len(book_list_from_server) == self.book_count
    
    # The rule here states that the parameter created_book should be taken
    # from the Bundle "created_books".
    @rule(created_book_id=created_books)
    def delete_book(self, created_book_id):
        # Execute action
        requests.delete(f"{URL}/books/{created_book_id}")

        # State transition
        self.book_count -= 1

MySrvTestHttp.TestCase.settings = settings(
    max_examples=50,
    stateful_step_count=100,
    deadline=None,
)

TestMySrvTest = MySrvTestHttp.TestCase
