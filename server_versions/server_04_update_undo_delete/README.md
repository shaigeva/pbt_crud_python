# Server version 04: update_book undoes delete_book
(See top-level README to understand the context of this README)

This version fixes the faulty test from version 03, and the tests now find a new bug.<br/>
The bug in this version is that update_book "brings back to life" a book that
has been deleted by delete_book.

Changes to the test:
- We now also track the books that have already been deleted (there's a new
  class member in the test)
- delete_book checks if the book that it's looking at has already been deleted
  and behaves accordingly.
- update_book has been defined (it overrides one of the existing books with new
  data)


The output of the of the test will end with something that looks like this
(the interesting parts are in ***bold italic***)

<pre>
<b><i>
 &gt;       assert len(book_list_from_server) == self.book_count
 E       AssertionError: assert 1 == 0
</i></b>
E        +  where 1 = len([{'author': 'a', 'id': 'ee4f4e733dc54646bd81768579aa40c4', 'read': False, 'title': 'a'}])
E        +  and   0 = MySrvTestHttp({'books': [VarReference(name='v1')]}).book_count

tests/test_srv.py:88: AssertionError
-------------------------------------- Hypothesis ---------------------------------------
Falsifying example:
state = MySrvTestHttp()
state.init_test()
<b><i>
 v1 = state.new_book(book_data=BookData(title='a', author='a'))
 state.delete_book(created_book_id=v1)
 state.update_book(created_book_id=v1, override_book_data=BookData(title='a', author='a'))
 state.list_books()
</i></b>
state.teardown()
================================ short test summary info ================================
FAILED tests/test_srv.py::TestMySrvTest::runTest - AssertionError: assert 1 == 0
================================== 1 failed in 16.66s ===================================
</pre>
