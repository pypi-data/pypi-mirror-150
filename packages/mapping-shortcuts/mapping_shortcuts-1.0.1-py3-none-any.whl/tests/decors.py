
from unittest import TestCase

from mapping_shortcuts.decors import create_collector


class DecorTestCase(TestCase):

    def test_ok(self):
        decor, collection = create_collector()

        @decor('1')
        def f1():
            ...

        @decor('2')
        def f2():
            ...

        self.assertEqual(len(collection), 2)
        self.assertIn('1', collection)
        self.assertIn('2', collection)
        self.assertEqual(collection['1'], f1)
        self.assertEqual(collection['2'], f2)

    def test_duplicate_raise(self):
        decor, collection = create_collector()

        @decor('1')
        def f1():
            ...

        try:
            @decor('1')
            def f2():
                ...
        except ValueError as ex:
            self.assertTrue(str(ex).startswith('Duplication for key'))
        else:
            self.assertTrue(False, 'expected exception here')

        self.assertEqual(len(collection), 1)
        self.assertIn('1', collection)
        self.assertEqual(collection['1'], f1)

    def test_duplicate_ok(self):
        decor, collection = create_collector(
            raise_on_duplicate=False,
        )

        @decor('1')
        def f1():
            ...

        @decor('1')
        def f2():
            ...

        self.assertEqual(len(collection), 1)
        self.assertIn('1', collection)
        self.assertEqual(collection['1'], f2)
