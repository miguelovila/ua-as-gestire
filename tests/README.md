# Reading tests results

The tests are run by `tester.py` script. According to the script's logic, the tests should pass if the database is not initialized. If the database is initialized, some tests should fail.

## If DB is not initialized:

All tests should pass.

## If DB is initialized:

You should see 2 failed tests:

```bash
........FF.
======================================================================
FAIL: test_reserve_equipment (__main__.APITests.test_reserve_equipment)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../tests/tester.py", line 106, in test_reserve_equipment
    self.assertEqual(response.status_code, 200)
AssertionError: 400 != 200

======================================================================
FAIL: test_reserve_room (__main__.APITests.test_reserve_room)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".../tests/tester.py", line 75, in test_reserve_room
    self.assertEqual(response.status_code, 200)
AssertionError: 400 != 200

----------------------------------------------------------------------
Ran 11 tests in 4.635s

FAILED (failures=2)
```
