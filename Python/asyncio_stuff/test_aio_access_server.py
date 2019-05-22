from os import W_OK, X_OK, access, remove
from os.path import join

from aiohttp import web


class Foo:
    def __init__(self):
        self.save_file_path = '/srv/files'
        self.exists_path = '/tmp/'
        self.root_path = '/tmp/root'

    def hello(self, request):
        return web.json_response({"message": "hi"})

    async def health(self, request):
        return web.json_response(
            data={"checks": {
                "foo": {"success": await self.foo()},
                "goo": {"success": await self.goo()},
                "bar": {"success": await self.bar()},
                "do_it": {"success": await self.do_it()},
                "bar_tmp": {"success": await self.bar_tmp()},
                "do_it_tmp": {"success": await self.do_it_tmp()},
                "bar_root": {"success": await self.bar_root()},
                "do_it_root": {"success": await self.do_it_root()},
            }}
        )

    @staticmethod
    async def foo():
        return True

    @staticmethod
    async def goo():
        return False

    async def bar(self):
        return access(self.save_file_path, mode=W_OK|X_OK)

    async def do_it(self):
        filename = 'perms_check.tmp'
        test_file = join(self.save_file_path, filename)
        try:
            with open(test_file, 'w') as fout:
                fout.write('gibberish')
            remove(test_file)
            return True
        except Exception as e:
            print(e)
            return False

    async def bar_tmp(self):
        return access(self.exists_path, mode=W_OK|X_OK)

    async def do_it_tmp(self):
        filename = 'perms_check.tmp'
        test_file = join(self.exists_path, filename)
        try:
            with open(test_file, 'w') as fout:
                fout.write('gibberish')
            remove(test_file)
            return True
        except Exception as e:
            print(e)
            return False

    async def bar_root(self):
        return access(self.root_path, mode=W_OK|X_OK)

    async def do_it_root(self):
        filename = 'perms_check.tmp'
        test_file = join(self.root_path, filename)
        try:
            with open(test_file, 'w') as fout:
                fout.write('gibberish')
            remove(test_file)
            return True
        except Exception as e:
            print(e)
            return False


app = web.Application()
foo = Foo()
app.router.add_get('/health', foo.health)
app.router.add_get('/', foo.hello)
web.run_app(app)
