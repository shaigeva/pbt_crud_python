# Server version 01: Incorrect id.
(See top-level README to understand the context of this README)

The bug in this version is that the server uses the title of the book as the id
for the book, instead of generating a unique id for each book.

See `src/app.py:_book_from_post_data()`.

The output of the of the test will end with something that looks like this
(the interesting parts are in ***bold italic***)

<!-- <style>
pre span{
    color:red;
    font-weight:bold;
}
</style> -->

<pre>
<b><i>
 &gt;       assert len(book_list_from_server) == self.book_count
 E       AssertionError: assert 1 == 2</i></b>

E        +  where 1 = len([{'author': 'a', 'id': 'a', 'read': False, 'title': 'a'}])
E        +  and   2 = MySrvTestHttp({}).book_count
tests/test_srv.py:77: AssertionError
-------------------------------------- Hypothesis ---------------------------------------
Falsifying example:
state = MySrvTestHttp()
state.init_test()

 <b><i>state.new_book(book_data=BookData(title='a', author='a'))
 state.new_book(book_data=BookData(title='a', author='a'))
 state.list_books()</i></b>

state.teardown()
================================ short test summary info ================================
FAILED tests/test_srv.py::TestMySrvTest::runTest - AssertionError: assert 1 == 2
================================== 1 failed in 11.70s ===================================
</pre>

The top emphasized part, with the assertion, means that the book_list_from_server contained 1 book (length 1), while we expected 2 books (book_count).

The bottom emphasized part is the sequence of actions that reproduces the bug.<br>
It is a good idea to see how this reproduces using the UI:
- Start with an empty list.
- Create a new book with author='a' and title='a'.
- Make sure you see the book.
- Create another new book with exactly the same parameters.
- Make sure that the list has not changed.
- Meaning - we expected that there will be a new book in the list, but instead the list remained with length 1 because the new book has overriden the old book.
