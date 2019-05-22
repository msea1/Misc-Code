from aiohttp import web


class Foo:
    def test_resp(self, request):
        return web.json_response({"message": "hello"})

    def test_exc(self, request):
        raise Exception("oh no! here is a custom error")

    def test_exc2(self, request):
        raise web.HTTPBadRequest(reason="oh no! bad request!")

    def hello(self, request):
        return web.json_response({"message": "hi"})


app = web.Application()
foo = Foo()
app.router.add_get('/hello', foo.test_resp)
app.router.add_get('/exc', foo.test_exc)
app.router.add_get('/exc_new', foo.test_exc2)
app.router.add_get('/', foo.hello)
web.run_app(app)
