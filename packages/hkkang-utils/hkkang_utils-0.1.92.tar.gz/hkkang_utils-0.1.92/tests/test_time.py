import unittest

import time as time_module
import src.hkkang_utils.time as time_utils

TEST_TIME = 2


class Test_time_utils(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test_time_utils, self).__init__(*args, **kwargs)

    def test_timer_measure(self):
        timer = time_utils.Timer()
        timer.start()
        time_module.sleep(TEST_TIME)
        timer.stop()
        assert (
            timer.elapsed_time > TEST_TIME and timer.elapsed_time < TEST_TIME + 1
        ), f"Timer is not working properly: {timer.elapsed_time} sec is measured."

    def test_timer_measure_using_with(self):
        timer = time_utils.Timer()
        with timer.measure():
            time_module.sleep(TEST_TIME)
        assert (
            timer.elapsed_time > TEST_TIME and timer.elapsed_time < TEST_TIME + 1
        ), f"Timer is not working properly: {timer.elapsed_time} sec is measured."

    def test_timer_singleton_by_name1(self):
        def test_func():
            timer = time_utils.Timer()
            with timer.measure():
                time_module.sleep(TEST_TIME)

        test_func()
        timer = time_utils.Timer(
            class_name="Test_time_utils",
            func_name="test_timer_singleton_by_name1.test_func",
        )
        assert (
            timer.elapsed_time > TEST_TIME and timer.elapsed_time < TEST_TIME + 1
        ), f"Timer is not working properly: {timer.elapsed_time} sec is measured."

    def test_timer_singleton_by_name2(self):
        timer = time_utils.Timer()
        with timer.measure():
            time_module.sleep(TEST_TIME)

        timer = time_utils.Timer(
            class_name="Test_time_utils",
            func_name="test_timer_singleton_by_name2",
        )
        assert (
            timer.elapsed_time > TEST_TIME and timer.elapsed_time < TEST_TIME + 1
        ), f"Timer is not working properly: {timer.elapsed_time} sec is measured."

    def test_timer_decorator(self):
        @time_utils.measure_time
        def test_func():
            time_module.sleep(TEST_TIME)

        test_func()
        timer = time_utils.Timer(
            class_name="Test_time_utils", func_name="test_timer_decorator.test_func"
        )
        assert (
            timer.elapsed_time > TEST_TIME and timer.elapsed_time < TEST_TIME + 1
        ), f"Timer is not working properly: {timer.elapsed_time} sec is measured."

    def test_timer_measure_total_elapsed_time(self):
        timer = time_utils.Timer()
        with timer.measure():
            time_module.sleep(TEST_TIME)
        with timer.measure():
            time_module.sleep(TEST_TIME)
        assert (
            timer.elapsed_time > TEST_TIME and timer.elapsed_time < TEST_TIME + 1
        ), f"Timer is not working properly: {timer.elapsed_time} sec is measured."
        assert timer.total_elapsed_time > TEST_TIME * 2 and timer.total_elapsed_time < (
            TEST_TIME * 2 + 1
        ), f"Timer is not working properly: {timer.total_elapsed_time} sec is measured."
        timer.show_total_elapsed_time()

    def test_timer_measure_avg_elapsed_time(self):
        timer = time_utils.Timer()
        with timer.measure():
            time_module.sleep(TEST_TIME)
        with timer.measure():
            time_module.sleep(TEST_TIME)
        assert (
            timer.elapsed_time > TEST_TIME and timer.elapsed_time < TEST_TIME + 1
        ), f"Timer is not working properly: {timer.elapsed_time} sec is measured."
        assert timer.avg_elapsed_time > TEST_TIME and timer.avg_elapsed_time < (
            TEST_TIME + 1
        ), f"Timer is not working properly: {timer.avg_elapsed_time} sec is measured."
        timer.show_avg_elapsed_time()


if __name__ == "__main__":
    unittest.main()
