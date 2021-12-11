# Server version 02: Fixed incorrect id
(See top-level README to understand the context of this README)

This version fixes the bug found in the version server_01_incorrect_id.

The tests are the same as in server_01_incorrect_id - so they should pass.<br/>
This version exists just to show the process that we fixed the bug and with the
existing tests we don't find any more bugs.

Note: There are hidden bugs in the implementation, but they are not found by the
CURRENT tests. In the later versions, we make the tests stronger and they find
the bugs.

The output of the of the test will end with something that looks like this

<pre>
.                                                                                 [100%]
================================== 1 passed in 11.12s ===================================
</pre>
