from aspen.hooks import Hooks
from aspen.testing import attach_teardown


def test_hooks_is_barely_instantiable():
    actual = Hooks().__class__
    assert actual == Hooks, actual

def test_hooks_can_Be_run():
    hooks = Hooks()
    thing = object()
    hooks.yeah_hook = [lambda thing: thing]
    actual = hooks.run('yeah_hook', thing)
    assert actual is thing, actual


attach_teardown(globals())
