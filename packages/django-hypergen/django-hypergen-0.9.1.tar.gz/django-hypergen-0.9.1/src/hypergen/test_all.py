# coding=utf-8
from __future__ import (absolute_import, division, unicode_literals)

import pytest
from hypergen.incubation import SessionVar, pickle_dumps

d = dict
import re, sys
from datetime import date, datetime

from contextlib import ContextDecorator
from django.test.client import RequestFactory
from pyrsistent import pmap
from pytest import raises

from hypergen.core import *
from hypergen.core import context as c, context_middleware, ContextMiddleware, hypergen_context, join_html, dumps
from hypergen.core import callback as cb
from hypergen.contrib import *

import django

class User(object):
    pk = 1
    id = 1

class Request(object):
    user = User()
    session = {}

    def is_ajax(self):
        return False

class HttpResponse(object):
    pass

def mock_hypergen_callback(f):
    f.reverse = lambda *a, **k: "/path/to/cb/"
    return f

def test_context():
    context.replace(request=Request(), user=User())
    assert context.request.user.id == 1
    assert "request" in context

def test_context_cm():
    def inc(ctx):
        return ctx.set("i", ctx.get("i", 0) + 1)

    with context(inc):
        assert context["i"] == 1

        with context(inc, foo=9):
            assert context["foo"] == 9
            assert context["i"] == 2
            with context(bar=42):
                assert context["i"] == 2
                assert context["bar"] == 42
            assert context["i"] == 2

        assert context["i"] == 1
        assert "foo" not in context

def test_context_immutable():
    with context(my_appname=pmap({"title": "foo", "items": [1, 2, 3]})):
        assert context.my_appname["title"] == "foo"
        assert context.my_appname["items"] == [1, 2, 3]
        assert context["my_appname"]["title"] == "foo"
        assert context["my_appname"]["items"] == [1, 2, 3]
        with context(at="my_appname", items=[4, 5]):
            assert context.my_appname["title"] == "foo"
            assert context.my_appname["title"] == "foo"
            assert context["my_appname"]["title"] == "foo"
            assert context["my_appname"]["items"] == [4, 5]

        assert context.my_appname["title"] == "foo"
        assert context.my_appname["items"] == [1, 2, 3]
        assert context["my_appname"]["title"] == "foo"
        assert context["my_appname"]["items"] == [1, 2, 3]

def test_context_mutable_update_should_fail():
    with context(my_appname={"title": "foo", "items": [1, 2, 3]}):
        assert context.my_appname["title"] == "foo"
        assert context.my_appname["items"] == [1, 2, 3]
        assert context["my_appname"]["title"] == "foo"
        assert context["my_appname"]["items"] == [1, 2, 3]
        with pytest.raises(Exception):
            with context(at="my_appname", items=[4, 5]):
                # No updating of mutable data.
                pass

def test_context_at_creation():
    with context(at="my_appname", title="foo", items=[1, 2, 3]):
        assert context.my_appname["title"] == "foo"
        assert context.my_appname["items"] == [1, 2, 3]
        assert context["my_appname"]["title"] == "foo"
        assert context["my_appname"]["items"] == [1, 2, 3]
        with context(at="my_appname", items=[4, 5]):
            assert context.my_appname is not None
            assert context.my_appname["title"] == "foo"
            assert context.my_appname["title"] == "foo"
            assert context["my_appname"]["title"] == "foo"
            assert context["my_appname"]["items"] == [4, 5]

        # Oh now, this is now not correct. Right now it's up to the user to use a pmap for fancy stuff.
        assert context.my_appname["title"] == "foo"
        assert context.my_appname["items"] == [1, 2, 3]
        assert context["my_appname"]["title"] == "foo"
        assert context["my_appname"]["items"] == [1, 2, 3]

def test_context_middleware():
    def view(request):
        assert context.user.pk == 1
        assert context["request"].user.pk == 1
        return HttpResponse()

    get_response = lambda request: view(request)
    context_middleware(get_response)(Request())

def test_context_middleware_old():
    if int(django.get_version()[0]) > 3:
        return
    middleware = ContextMiddleware()
    middleware.process_request(Request())
    assert context.request.user.pk == 1

def setup():
    import os
    DIR = os.path.realpath(os.path.dirname(__file__))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_settings")
    sys.path.append(DIR)
    import django
    django.setup()
    context.replace(request=Request(), user=User())

def render_hypergen(func):
    return hypergen(func).content

def e(s):
    h = HTMLParser()
    return h.unescape(s)

def f():
    return re.sub(r'[0-9]{5,}', '1234', join_html(c.hypergen.into))

def test_element():
    with context(hypergen=hypergen_context()):
        div("hello world!")
        assert str(join_html(c.hypergen.into)) == '<div>hello world!</div>'
    with context(hypergen=hypergen_context()):
        with div("a", class_="foo"):
            div("b", x_foo=42)
        assert f() == '<div class="foo">a<div x-foo="42">b</div></div>'
    with context(hypergen=hypergen_context()):

        @div("a", class_="foo")
        def f1():
            div("b", x_foo=42)

        f1()
        assert f() == '<div class="foo">a<div x-foo="42">b</div></div>'
    with context(hypergen=hypergen_context()):
        div("a", None, div("b", x_foo=42), class_="foo")
        assert f() == '<div class="foo">a<div x-foo="42">b</div></div>'

    with context(hypergen=hypergen_context()):
        div(None, [1, 2], sep="-")
        assert f() == '<div>1-2</div>'

    with context(hypergen=hypergen_context()):
        ul([li([li(y) for y in range(3, 4)]) for x in range(1, 2)])
        assert f() == "<ul><li><li>3</li></li></ul>"

    with context(hypergen=hypergen_context()):
        ul(li(li(y) for y in range(3, 4)) for x in range(1, 2))
        assert f() == "<ul><li><li>3</li></li></ul>"

    with context(hypergen=hypergen_context()):
        div([1, 2], div(1, 2, div(1, None, 2, ul(list(li(x) for x in range(1, 3))))))
        assert f() == '<div>12<div>12<div>12<ul><li>1</li><li>2</li></ul></div></div></div>'
    with context(hypergen=hypergen_context()):
        ul(None, [li(None, (li(li(z) for z in range(1, 2)) for y in range(3, 4)), None) for x in range(5, 6)], None)
        assert f() == "<ul><li><li><li>1</li></li></li></ul>"

def test_live_element():
    setup()

    with context(is_test=True):

        @mock_hypergen_callback
        def my_callback():
            pass

        with context(is_test=True, hypergen=hypergen_context()):
            div("hello world!", onclick=cb("my_url", 42), id_="i1")
            assert f() == """<div onclick="e(event,'i1__onclick')" id="i1">hello world!</div>"""

        return
        with context(is_test=True, hypergen=hypergen_context()):
            div("hello world!", onclick=cb(my_callback, [42]))
            assert f() == """<div id="A" onclick="e(event,'__main__',1234)">hello world!</div>"""

        with context(is_test=True, hypergen=hypergen_context()):
            a = input_(name="a")
            input_(name="b", onclick=cb(my_callback, a))
            assert f() == """<input name="a"/><input id="A" name="b" onclick="e(event,'__main__',1234)"/>"""

        with context(is_test=True, hypergen=hypergen_context()):
            el = textarea(placeholder="myplace")
            with div(class_="message"):
                with div(class_="action-left"):
                    span("Annullér", class_="clickable")
                with div(class_="action-right"):
                    span("Send", class_="clickable", onclick=cb(my_callback, el))
                div(el, class_="form form-write")

            assert f(
            ) == """<div class="message"><div class="action-left"><span class="clickable">Annull\xe9r</span></div><div class="action-right"><span class="clickable" onclick="e(event,'__main__',1234)" id="A">Send</span></div><div class="form form-write"><textarea placeholder="myplace"></textarea></div></div>"""

        with context(is_test=True, hypergen=hypergen_context()):
            input_(autofocus=True)
            assert join_html(c.hypergen.into) == '<input autofocus/>'

def test_live_element2():
    setup()

    with context(is_test=True):

        @mock_hypergen_callback
        def my_callback():
            pass

        with context(is_test=True, hypergen=hypergen_context()):
            el1 = input_(id_="id_new_password", placeholder="Adgangskode", oninput=cb(my_callback, THIS, ""))
            el2 = input_(id_="el2", placeholder="Gentag Adgangskode", oninput=cb(my_callback, THIS, el1))

            h2("Skift Adgangskode")
            p("Rules:")
            with div(class_="form"):
                with div():
                    with ul(id_="password_verification_smartassness"):
                        div("TODO")
                    with div(class_="form"):
                        div(el1, class_="form-field")
                        div(el2, class_="form-field")
                        div("Skift adgangskode", class_="button disabled")

            assert f(
            ) == """<h2>Skift Adgangskode</h2><p>Rules:</p><div class="form"><div><ul id="password_verification_smartassness"><div>TODO</div></ul><div class="form"><div class="form-field"><input id="id_new_password" placeholder="Adgangskode" oninput="e(event,'id_new_password__oninput')"/></div><div class="form-field"><input id="el2" placeholder="Gentag Adgangskode" oninput="e(event,'el2__oninput')"/></div><div class="button disabled">Skift adgangskode</div></div></div></div>"""

def test_callback():
    setup()
    with context(is_test=True, hypergen=hypergen_context()):

        @mock_hypergen_callback
        def f1(foo, punk=300):
            pass

        element = input_(oninput=cb(f1, THIS, 200, debounce=500), id_="testcb")
        assert type(cb("foo", 42, debounce=42)(element, "oninput", 92)) is list

def test_components():
    def f1():
        div("a")

    @component
    def f2():
        div("a")

    with context(is_test=True, hypergen=hypergen_context()):
        div(1, f1(), 2)
        assert f() == "<div>a</div><div>12</div>"

    with context(is_test=True, hypergen=hypergen_context()):
        div(1, f2(), 2)
        assert f() == "<div>1<div>a</div>2</div>"

def test_components2():
    @component
    def comp1():
        @component
        def comp2():
            input_(value="a")

        comp2()

    with context(is_test=True, hypergen=hypergen_context()):
        with tr():
            td(comp1())
        assert f() == '<tr><td><input value="a"/></td></tr>'

    with context(is_test=True, hypergen=hypergen_context()):
        with tr():
            with td():
                comp1()
        assert f() == '<tr><td><input value="a"/></td></tr>'

def test_js_value_func():
    with context(is_test=True, hypergen=hypergen_context()):
        i = input_(type_="hidden", value=200, collect_name="pk", js_value_func="hypergen.v.i",
            id_="cch{}".format(200))

    assert i.js_value_func == "hypergen.v.i"

def test_eventhandler_cache():
    with context(is_test=True, hypergen=hypergen_context()):

        @mock_hypergen_callback
        def f1():
            pass

        input_(onclick=cb(f1, THIS), id_="tec")

        ehc = {i: v for i, v in enumerate(context.hypergen.event_handler_callbacks.values())}

        assert dumps(
            ehc
        ) == '{"0":["hypergen.callback","/path/to/cb/",[["_","element_value",["hypergen.read.value",null,"tec"]]],{"debounce":0,"confirm_":false,"blocks":false,"uploadFiles":false,"clear":false,"elementId":"tec","debug":false,"meta":{}}]}'

def test_call_js():
    with context(is_test=True, hypergen=hypergen_context()):

        @mock_hypergen_callback
        def f1():
            pass

        a(onclick=call_js("hypergen.xyz", THIS), id_="tcj")
        assert dumps(list(context.hypergen.event_handler_callbacks.values())
                    ) == '[["hypergen.xyz",["_","element_value",["hypergen.read.value",null,"tcj"]]]]'

def test_string_with_meta():
    assert "a" + str(StringWithMeta("b", None)) + "c" == "abc"
    assert StringWithMeta("a", None) + "b" == "ab"
    s = StringWithMeta("a", None)
    s += "b"
    assert s == "ab"

    with raises(TypeError):
        "a" + StringWithMeta("b", None)

def test_repr():
    with context(is_test=True, hypergen=hypergen_context()):
        el1 = input_(id_="el1")
        el2 = input_(onclick=cb("alert", el1), id_="el2")
        assert repr(el2) == 'input_(onclick=callback("alert", input_(id_="el1")), id_="el2")'

def test_serialization():
    x = {
        "string": "hi",
        "int": 42,
        "float": 9.9,
        "list": [1, 2, 3],
        "range": range(1, 10, 2),
        # Pythons json.dumps force converts tuples to list.
        # "tuple": (1, 2, 3),
        "dict": {"key": "value"},
        "set": {1, 2, 3},
        "frozenset": frozenset({1, 2, 3}),
        "date": date(2022, 1, 1),
        "datetime": datetime(2022, 1, 1, 10, 11, 23),}

    assert loads(dumps(x)) == x

def test_incubation_session_var():
    context.replace(request=Request(), user=User())
    x = SessionVar("foo", 92)
    assert x.get() == 92
    x.set(99)
    assert x.get() == 99
    assert c.request.session == {"hypergen_request_var__foo": pickle_dumps(99)}
