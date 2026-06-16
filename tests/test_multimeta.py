import pytest

from multimethod import MultiMeta, MultiMethod, MultiDict, HasAdd


def test_metaclass_is_used():
    assert isinstance(HasAdd, MultiMeta)


def test_add_is_multimethod_on_class():
    assert isinstance(HasAdd.__dict__["add"], MultiMethod)


def test_registered_signatures():
    mm = HasAdd.__dict__["add"]

    assert (int, int) in mm.dir
    assert (str, str) in mm.dir
    assert (float, float) in mm.dir

    # created because y has a default value
    assert (float,) in mm.dir


def test_dispatch_int():
    obj = HasAdd()
    assert obj.add(1, 2) == 3


def test_dispatch_str():
    obj = HasAdd()
    assert obj.add("a", "b") == "a__b"  # type: ignore[arg-type]


def test_dispatch_float():
    obj = HasAdd()
    assert obj.add(1.2, 3.4) == pytest.approx(4.6)  # type: ignore[arg-type]


def test_dispatch_float_default_argument():
    obj = HasAdd()
    assert obj.add(1.2) == pytest.approx(3.5)  # type: ignore[arg-type]


def test_unknown_signature_raises_keyerror():
    obj = HasAdd()

    with pytest.raises(KeyError):
        obj.add(1, "x")  # type: ignore[arg-type]


def test_descriptor_returns_bound_method():
    obj = HasAdd()

    method = obj.add

    assert callable(method)
    assert method(2, 3) == 5


def test_class_attribute_is_descriptor():
    mm = HasAdd.add

    assert isinstance(mm, MultiMethod)


def test_prepare_returns_multidict():
    ns = MultiMeta.__prepare__("Dummy", ())
    assert isinstance(ns, MultiDict)


def test_multidict_converts_redefinitions_to_multimethod():
    ns = MultiDict()

    def f(x: int):
        return x

    def g(x: str):
        return x

    ns["foo"] = f
    ns["foo"] = g

    assert isinstance(ns["foo"], MultiMethod)

    mm = ns["foo"]

    assert (int,) in mm.dir
    assert (str,) in mm.dir
