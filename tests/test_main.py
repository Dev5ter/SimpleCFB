import builtins

from unittest import mock
from main import main as main_function

def test_basic_run_through():
    with mock.patch.object(builtins, "input", lambda _: ""):
        main_function()    