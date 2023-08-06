import pytest
import time
from chatstream import LoadTime  # 実際のモジュール名に置き換えてください


def long_running_function():
    # 5秒間の時間がかかる処理
    time.sleep(5)
    return 42


# 初回はプログレスが表示されない
def test_loadtime_output_for_long_running_function_when_first_try():
    output = []

    def print_to_list(str):
        output.append(str)

    timer = LoadTime(name="long_running_test", fn=long_running_function, fn_print=print_to_list)
    timer.clear_stored_data()  # いったん計測データをクリアする
    timer.start()  # 手動開始

    output_str = "".join(output)

    assert output[0].startswith('\r')

    assert output[0].replace('\r', '') \
           == 'Loading "long_running_test" ... 00:00'

    assert output[len(output) - 1].replace('\r', '') \
           == 'Loading "long_running_test" ... 00:04\n'

    assert "Loading \"long_running_test\" ..." in output_str


def test_loadtime_output_for_long_running_function_when_after_second_try():
    output = []

    def print_to_list(str):
        output.append(str)

    def print_to_nothing(str):
        print(str)
        pass

    # 1回目、計測データを記録するための実行
    timer = LoadTime(name="long_running_test", fn=long_running_function, fn_print=print_to_nothing)
    timer.clear_stored_data()  # いったん計測データをクリアする
    timer.start()

    # 2回目、プログレスバーつき出力を検証するための実行
    LoadTime(name="long_running_test", fn=long_running_function, fn_print=print_to_list)()

    output_str = "".join(output)

    assert output[0].startswith('\r')

    assert output[0].replace('\r', '') \
           == 'Loading "long_running_test" ... 00:00/00:04 [                    ] (0%)'

    assert output[len(output) - 1].replace('\r', '') \
           == 'Loading "long_running_test" ... 00:04/00:04 [████████████████████] (100%)\n'

    assert "Loading \"long_running_test\" ..." in output_str

    # プログレスバーが表示されていることを確認（進行状況に応じて変化）
    assert "[" in output_str and "]" in output_str


def func_to_time():
    time.sleep(2)
    return 42


def print_function(str):
    print(str, end='')


def test_loadtime_run():
    timer = LoadTime(name="test1", fn=func_to_time, fn_print=print_function)
    result = timer.start()
    assert result == 42


# fn_print を利用して、出力を検証するテスト
def test_loadtime_output():
    output = []

    def print_to_list(str):
        output.append(str)

    timer = LoadTime(name="test2", fn=func_to_time, fn_print=print_to_list)
    timer.start()

    # fn_print を介して出力された文字列をチェック
    assert "test" in "".join(output)


# fn が未指定の場合のテスト
def test_loadtime_no_fn():
    with pytest.raises(TypeError):  # fn が未指定なら TypeError が発生するはず
        timer = LoadTime(name="test3", fn=None)
        timer.start()


# fn_print が未指定の場合のテスト
def test_loadtime_no_fn_print():
    timer = LoadTime(name="test4", fn=func_to_time)
    result = timer.start()  # fn_print が未指定でもエラーにならないことを確認
    assert result == 42
