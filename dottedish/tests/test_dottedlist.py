import unittest
from dottedish import api, dottedlist

def container_factory(parent_key, item_key):
    return []

class TestAPI(unittest.TestCase):

    def test_set(self):
        # Test top-level
        l = [None]
        api.set(l, '0', 'foo')
        self.assertEqual(l, ['foo'])
        # Test nested.
        l = [[None]]
        api.set(l, '0.0', 'foo')
        self.assertEqual(l, [['foo']])
        # Test traversal key error.
        l = [[None]]
        api.set(l,'1.0','bar',container_factory=container_factory)
        self.assertEqual(l, [[None],['bar']])

    def test_get(self):
        self.assertEqual(api.get(['foo'], '0'), 'foo')
        self.assertEqual(api.get([['foo']], '0.0'), 'foo')
        self.assertRaises(KeyError, api.get, [], '0')

    def test_getdefault(self):
        self.assertEqual(api.get([], '0', 'foo'), 'foo')
        self.assertEqual(api.get([[]], '0.0', 'foo'), 'foo')
        self.assertEqual(api.get([[]], '1.0', 'foo'), 'foo')

    def test_wrap(self):
        l = []
        dl = api.dotted(l)
        self.assertIsInstance(dl, dottedlist.DottedList)

    def test_wrap_dotted(self):
        l = []
        dl = api.dotted(l)
        self.assertIsInstance(dl, dottedlist.DottedList)
        self.assertIs(dl, api.dotted(dl))


class TestDottedList(unittest.TestCase):

    def test_getitem(self):
        dl = api.dotted(['foo', 'bar'])
        self.assertEqual(dl['0'], 'foo')
        self.assertEqual(dl.get('0'), 'foo')
        self.assertRaises(KeyError, dl.__getitem__, '2')

    def test_setitem(self):
        l = ['foo', 'bar']
        api.dotted(l)['0'] = 'wee'
        self.assertEqual(l[0], 'wee')

    def test_setitem_unwrap(self):
        l = ['foo', 'bar']
        api.dotted(l)['0'] = api.dotted([])
        self.assertEqual(l[0], [])
        self.assertNotIsInstance(l[0], dottedlist.DottedList)

    def test_keys(self):
        self.assertEqual(api.dotted([]).keys(), [])
        self.assertEqual(api.dotted(['foo', 'bar']).keys(), ['0', '1'])
        self.assertEqual(api.dotted([['foo']]).keys(), ['0'])

    def test_items(self):
        self.assertEqual(api.dotted([]).items(), [])
        self.assertEqual(api.dotted(['foo', 'bar']).items(), [('0', 'foo'), ('1', 'bar')])
        self.assertIsInstance(api.dotted([['foo']]).items()[0][1], dottedlist.DottedList)

    def test_len(self):
        self.assertEqual(len(api.dotted([])), 0)
        self.assertEqual(len(api.dotted(['foo', 'bar'])), 2)

    def test_eq(self):
        one = ['foo', 'bar']
        two = ['foo', 'rab']
        self.assertTrue(api.dotted(one) == one)
        self.assertTrue(api.dotted(one) == api.dotted(one))
        self.assertFalse(api.dotted(one) == two)
        self.assertFalse(api.dotted(one) == api.dotted(two))

    def test_iter(self):
        values = ['foo', 'bar']
        for value in api.dotted(['foo', 'bar']):
            self.assertEqual(value, values.pop(0))

    def test_contains(self):
        dl = api.dotted(['foo', 'bar'])
        self.assertTrue('bar' in dl)
        self.assertFalse(1 in dl)

    def test_repr(self):
        dl = api.dotted(['foo', 'bar'])
        self.assertEqual(repr(dl), '''<DottedList "['foo', 'bar']">''')

