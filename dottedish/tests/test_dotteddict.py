import unittest
from dottedish import api, dotteddict

def container_factory(parent_key, item_key):
    return {}

class TestAPI(unittest.TestCase):

    def test_set(self):
        # Test top-level.
        d = {}
        api.set(d, 'foo', 'bar')
        self.assertEqual(d, {'foo': 'bar'})
        # Test nested.
        d = {'foo': {}}
        api.set(d, 'foo.bar', 'rab')
        self.assertEqual(d, {'foo': {'bar': 'rab'}})
        # Test traversal key error.
        d = {'foo': {}}
        api.set(d, 'oof.bar','rab', container_factory=container_factory)
        self.assertEqual(d, {'foo': {},'oof': {'bar':'rab'}})

    def test_get(self):
        self.assertEqual(api.get({'foo': 'bar'}, 'foo'), 'bar')
        self.assertEqual(api.get({'foo': {'bar': 'rab'}}, 'foo.bar'), 'rab')
        self.assertRaises(KeyError, api.get, {}, 'foo')
        self.assertRaises(KeyError, api.get, {'foo': 'bar'}, 'oof.bar')

    def test_get_default(self):
        self.assertEqual(api.get({}, 'foo', 'bar'), 'bar')
        self.assertEqual(api.get({'foo': {}}, 'foo.bar', 'rab'), 'rab')
        self.assertEqual(api.get({'foo': 'bar'}, 'oof.bar', None), None)

    def test_wrap(self):
        d = {}
        dd = api.dotted(d)
        self.assertIsInstance(dd, dotteddict.DottedDict)

    def test_wrap_dotted(self):
        d = {}
        dd = api.dotted(d)
        self.assertIsInstance(dd, dotteddict.DottedDict)
        self.assertIs(dd, api.dotted(dd))


class TestDottedDict(unittest.TestCase):

    def test_getitem(self):
        d = {'foo': 'bar'}
        dd = api.dotted(d)
        self.assertEqual(dd['foo'], 'bar')
        self.assertEqual(dd.get('foo'), 'bar')

    def test_getitem_missing(self):
        self.assertRaises(KeyError, api.dotted({}).__getitem__, 'foo')

    def test_setitem(self):
        d = {}
        api.dotted(d)['foo'] = 'bar'
        self.assertEqual(d['foo'], 'bar')

    def test_setitem_unwrap(self):
        d = {}
        api.dotted(d)['foo'] = api.dotted({})
        self.assertEqual(d['foo'], {})
        self.assertNotIsInstance(d['foo'], dotteddict.DottedDict)

    def test_keys(self):
        self.assertEqual(api.dotted({}).keys(), [])
        self.assertCountEqual(api.dotted({'foo': 0, 'bar': 1}).keys(), ['foo', 'bar'])
        self.assertCountEqual(api.dotted({'foo': {'bar': 1}}).keys(), ['foo'])

    def test_items(self):
        self.assertEqual(api.dotted({}).keys(), [])
        self.assertCountEqual(api.dotted({'foo': 0, 'bar': 1}).items(), [('foo', 0), ('bar', 1)])
        self.assertIsInstance(api.dotted({'foo': {'bar': 1}}).items()[0][1], dotteddict.DottedDict)

    def test_len(self):
        self.assertEqual(len(api.dotted({})), 0)
        self.assertEqual(len(api.dotted({'foo': 0, 'bar': 1})), 2)
        self.assertEqual(len(api.dotted({'foo': {'bar': 1}})), 1)

    def test_eq(self):
        one = {'foo': 0, 'bar': 1}
        two = {'foo': {'bar': 1}}
        self.assertTrue(api.dotted(one) == one)
        self.assertTrue(api.dotted(one) == api.dotted(one))
        self.assertFalse(api.dotted(one) == two)
        self.assertFalse(api.dotted(one) == api.dotted(two))

    def test_iter(self):
        keys = ['foo', 'bar']
        for key in api.dotted({'foo': 0, 'bar': 1}):
            self.assertIn(key, keys)
            keys.remove(key)

