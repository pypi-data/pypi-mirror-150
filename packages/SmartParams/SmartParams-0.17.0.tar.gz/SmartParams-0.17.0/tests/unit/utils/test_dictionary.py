import smartparams.utils.dictionary as dictutil
from tests.unit import UnitCase


class TestFindNested(UnitCase):
    def setUp(self) -> None:
        self.dict = dict(arg1='arg1', arg2=['arg2'], arg3={'arg31': 'a31', 'arg32': 'a32'})

    def test(self) -> None:
        key = 'arg3.arg31'

        dictionary, last_key = dictutil.find_nested(dictionary=self.dict, key=key)

        self.assertEqual('arg31', last_key)
        self.assertTupleEqual((('arg31', 'a31'), ('arg32', 'a32')), tuple(dictionary.items()))

    def test__not_in_dictionary__non_required(self) -> None:
        key = 'missing.any'

        dictionary, last_key = dictutil.find_nested(dictionary=self.dict, key=key, required=False)

        self.assertEqual({}, dictionary)
        self.assertEqual('any', last_key)

    def test__not_in_dictionary__required(self) -> None:
        key = 'missing.any'

        self.assertRaises(
            KeyError,
            dictutil.find_nested,
            dictionary=self.dict,
            key=key,
            required=True,
        )

    def test__required_true(self) -> None:
        key = 'arg3.missing'

        self.assertRaises(
            KeyError,
            dictutil.find_nested,
            dictionary=self.dict,
            key=key,
            required=True,
        )

    def test__is_not_dictionary(self) -> None:
        key = 'arg3.arg31.a31'

        self.assertRaises(KeyError, dictutil.find_nested, dictionary=self.dict, key=key)

    def test__create_mode(self) -> None:
        key = 'arg3.missing.key'

        dictionary, last_key = dictutil.find_nested(
            dictionary=self.dict,
            key=key,
            create_mode=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('key', last_key)

    def test__set_mode(self) -> None:
        key = 'arg3.arg31.a31'

        dictionary, last_key = dictutil.find_nested(
            dictionary=self.dict,
            key=key,
            set_mode=True,
        )

        self.assertIsInstance(dictionary, dict)
        self.assertFalse(bool(dictionary))
        self.assertEqual('a31', last_key)


class TestNormalize(UnitCase):
    def test(self) -> None:
        data = {'a.b': 10, 'a.c': 15, 'd': 20, 'e': {1: {'a.b.c': 10}}}
        expected = {'a': {'b': 10, 'c': 15}, 'd': 20, 'e': {1: {'a.b.c': 10}}}

        actual = dictutil.normalize(data)

        self.assertEqual(expected, actual)

    def test__error(self) -> None:
        data = {'a.b': 10, 'a': {'b': 15}}

        self.assertRaises(ValueError, dictutil.normalize, data)

    def test__diff(self) -> None:
        data = {'a.b': {'c': {'e': 10}}, 'a': {'b': {'c': {'d': 5}}}}
        expected = {'a': {'b': {'c': {'e': 10, 'd': 5}}}}

        actual = dictutil.normalize(data)

        self.assertEqual(expected, actual)

    def test__diff__error(self) -> None:
        data = {'a.b': 10, 'a': {'b': {'c': {'d': 5}}}}

        self.assertRaises(ValueError, dictutil.normalize, data)

    def test__merge(self) -> None:
        data = {'a.b.x': 10, 'a.c': 15, 'd': 20}
        expected = {'a': {'b': {'x': 10}, 'c': 15}, 'd': 20}

        actual = dictutil.normalize(data)

        self.assertEqual(expected, actual)

    def test__merge_inv(self) -> None:
        data = {'a.b': 10, 'a.c.x': 15, 'd': 20}
        expected = {'a': {'b': 10, 'c': {'x': 15}}, 'd': 20}

        actual = dictutil.normalize(data)

        self.assertEqual(expected, actual)

    def test__merge__error(self) -> None:
        data = {'a.b.c.d': 10, 'a.b': 15}

        self.assertRaises(ValueError, dictutil.normalize, data)

    def test__merge_inv__error(self) -> None:
        data = {'a.b': 15, 'a.b.c.d': 10}

        self.assertRaises(ValueError, dictutil.normalize, data)


class TestMerge(UnitCase):
    def test(self) -> None:
        a = {'a': {'b': 10}, 'd': 20}
        b = {'a': {'c': 15}}
        expected = {'a': {'b': 10, 'c': 15}, 'd': 20}

        actual = dictutil.merge(a, b)

        self.assertEqual(expected, actual)

    def test__error__overridden(self) -> None:
        a = {'a': {'b': 10}, 'd': 20}
        b = {'a': {'c': 15}, 'd': 20}

        self.assertRaises(ValueError, dictutil.merge, a, b)

    def test__error__non_string(self) -> None:
        a = {'a': {'b': 10}, 1: {'d': 11}}
        b = {'a': {'c': 15}, 1: {'e': 22}}

        self.assertRaises(KeyError, dictutil.merge, a, b)
