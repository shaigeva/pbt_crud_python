# Server version 03: Negative book count
(See top-level README to understand the context of this README)

In this version, the test failure is caused by a bug in the test (as opposed to a bug in the code under test).

The version exists to show what kind of problems we might face when trying to
write a non-trivial test.

The tests in this version attempt to increase the code coverage by also
defining the delete_book action. In order for delete_book to have the id of the
book (which it needs in order to tell the server what to delete), we create a
Hypothesis "Bundle", and put the id-s of created books into it.

However, we do not handle the case that delete_book is called twice for the
same book. This causes the test to fail because we get an empty list, but we
expect the book count to be -1.


The output of the of the test will end with something that looks like this
(the interesting parts are in ***bold italic***)

<pre>
<b><i>
 &gt;       assert len(book_list_from_server) == self.book_count
 E       AssertionError: assert 0 == -1
</i></b>
E        +  where 0 = len([])
E        +  and   -1 = MySrvTestHttp({'books': [VarReference(name='v1')]}).book_count

tests/test_srv.py:87: AssertionError
-------------------------------------- Hypothesis ---------------------------------------
Falsifying example:
state = MySrvTestHttp()
state.init_test()
<b><i>
 v1 = state.new_book(book_data=BookData(title='a', author='a'))
 state.delete_book(created_book_id=v1)
 state.delete_book(created_book_id=v1)
 state.list_books()
</i></b>
state.teardown()
================================ short test summary info ================================
FAILED tests/test_srv.py::TestMySrvTest::runTest - AssertionError: assert 0 == -1
================================== 1 failed in 11.39s ===================================
</pre>
