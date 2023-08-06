import pickle as pkl
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch

from smartparams import Smart
from smartparams.exceptions import (
    ArgumentTypeError,
    CannotParseEvalName,
    Misconfiguration,
    MissingArgument,
    MissingArgumentValue,
    MissingDumpPath,
    ParamsFileNotExists,
    UnexpectedArgument,
)
from smartparams.utils.enums import Option
from tests.custom_classes import (
    Class,
    ClassChild,
    ClassComposition,
    Iter,
    RaiseClass,
    some_function,
)
from tests.integration import IntegrationCase


class TestSerialization(IntegrationCase):
    def setUp(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        class_child_name = f"{ClassChild.__module__}.{ClassChild.__qualname__}"
        self.smart = Smart(
            ClassComposition,
            **{
                'vanilla_cls': {'arg1': 'argument1', 'arg2': 15, 'class': class_name},
                'smart': {'class': 'Smart'},
                'smart_cls': {'arg1': 'str???', 'arg2': 75, 'class': f'{class_name}:Smart'},
                'unknown': some_function,
                'smart_cls_with_default': {
                    'arg1': 'argument1',
                    'arg2': 5,
                    'class': f'{class_child_name}:Smart',
                },
            },
        )

    def test__pickle(self) -> None:
        pickled = pkl.dumps(self.smart)
        smart = pkl.loads(pickled)

        self.assertIsInstance(smart, Smart)
        self.assertEqual(str(self.smart), str(smart))
        self.assertIs(smart.type(), ClassComposition)
        self.assertEqual(self.smart.dict(), smart.dict())


class TestSmartRunCase(IntegrationCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg2=10)
        self.smart.debug = True

    def tearDown(self) -> None:
        Smart.strict = False

    @patch('smartparams.utils.cli.sys', Mock(argv='script.py --dump --merge-params'.split()))
    def test_run__dump(self) -> None:
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml') as file:
            self.smart.run(function=Mock(), path=Path(file.name))

            self.assertEqual("arg2: 10\narg1: str???\n", file.read())

    @patch('smartparams.utils.cli.sys', Mock(argv='script.py --dump'.split()))
    def test_run__dump_no_path(self) -> None:
        self.assertRaises(MissingDumpPath, self.smart.run, function=Mock(), path=None)

    @patch('smartparams.utils.cli.sys', Mock(argv='script.py'.split()))
    def test_run__mode(self) -> None:
        self.smart._callable = Mock()
        with tempfile.TemporaryDirectory() as name:
            temp_dir = Path(name)
            path = temp_dir.joinpath('params.yaml')
            path.write_text('a: 1\nb: 2\nc.a: 11\nc.b: 22')
            temp_dir.joinpath('params.dev.yaml').write_text('b: -2\nc.b: -22\nc.c: -33')
            temp_dir.joinpath('data').mkdir()
            temp_dir.joinpath('models', 'baselines').mkdir(parents=True)
            temp_dir.joinpath('data', 'params.d1.yaml').write_text('d: foo\ne: buu')
            temp_dir.joinpath('models', 'baselines', 'params.m1.yaml').write_text('e: boo\nc.b: 0')

            self.smart.run(
                path=path,
                mode='dev,data/d1,models/baselines/m1',
            )

        self.smart._callable.assert_called_once_with(
            arg2=10,
            a=1,
            b=-2,
            c={'a': 11, 'b': 0, 'c': -33},
            d='foo',
            e='boo',
        )

    @patch('smartparams.utils.cli.sys', Mock(argv='script.py --print params'.split()))
    @patch('smartparams.utils.io.print')
    def test_run__print_params(self, print_mock: Mock) -> None:
        self.smart.run(function=Mock())

        print_mock.assert_called_with("arg1: str???\narg2: 5\n")

    @patch('smartparams.utils.cli.sys', Mock(argv='script.py --print dict'.split()))
    @patch('smartparams.utils.io.print')
    def test_run__print_dict(self, print_mock: Mock) -> None:
        self.smart.run(function=Mock())

        print_mock.assert_called_with("arg2: 10\n")

    @patch('smartparams.utils.cli.sys', Mock(argv='script.py --print keys'.split()))
    @patch('smartparams.utils.io.print')
    def test_run__print_keys(self, print_mock: Mock) -> None:
        self.smart.run(function=Mock())

        print_mock.assert_called_with("- arg2\n")

    @patch('smartparams.utils.cli.sys', Mock(argv='script.py --strict arg1=10'.split()))
    def test_run__strict(self) -> None:
        self.assertRaises(ArgumentTypeError, self.smart.run, function=lambda x: x())

    def test_run__function__no_file(self) -> None:
        self.assertRaises(ParamsFileNotExists, self.smart.run, path=Path('/does_not_exist.yaml'))

    @patch('smartparams.smart.load_data', Mock(return_value={'arg1': 'string'}))
    def test_run__function(self) -> None:
        function = Mock()
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.yaml') as file:
            file.write("arg1: string\n")
            file.seek(0)

            self.smart.run(function=function, path=Path(file.name))

            function.assert_called_once_with(self.smart)

    def test_run__without_function(self) -> None:
        function = Mock()
        self.smart._callable = function

        self.smart.run()

        function.assert_called_once_with(arg2=10)

    def test_run__parser_error(self) -> None:
        function = Mock(side_effect=MissingArgument('name', 'message'))
        self.smart.debug = False

        self.assertRaises(SystemExit, self.smart.run, function=function)

    def test_eval__function_a(self) -> None:
        expected = 'Hello, function_a!'

        actual = self.smart.eval(
            name='tests.script_example:Params:function_a',
            params=dict(
                param='Hello, ',
            ),
        )

        self.assertEqual(expected, actual)

    def test_eval__function_b(self) -> None:
        expected = 'Hello, function_b!'

        actual = self.smart.eval(
            name='tests.script_example:function_b',
            params=dict(
                param='Hello, ',
            ),
        )

        self.assertEqual(expected, actual)

    def test_eval__function_c__with_path(self) -> None:
        path = Path(__file__).parent.parent.joinpath('params.yaml')
        expected = 'Hello, function_c!'

        actual = self.smart.eval(
            name='tests.script_example::function_c',
            path=path,
        )

        self.assertEqual(expected, actual)

    def test_eval__no_module(self) -> None:
        self.assertRaises(CannotParseEvalName, self.smart.eval, name='unknown')

    def test_eval__mode_without_path(self) -> None:
        name = 'tests.script_example:Params:function_a'

        self.assertRaises(Misconfiguration, self.smart.eval, name=name, mode='mode')


class TestSmartRepresentationCase(IntegrationCase):
    def setUp(self) -> None:
        self.smart: Smart = Smart()

    def tearDown(self) -> None:
        self.smart.register.reset()

    def test_representation(self) -> None:
        actual = self.smart.representation()

        self.assertEqual({}, actual)

    def test_object_representation__iter(self) -> None:
        expected = {
            'di': {},
            'li': [],
            'li_o': [],
            'se': [],
            'tu': [],
            'tu_d': [0, 1],
        }
        actual = self.smart._object_representation(Iter, skip_default=False)

        self.assertEqual(expected, actual)

    def test_object_representation__with_defaults(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        expected = {
            'class_type': {'class': f'{class_name}:Type'},
            'vanilla_cls': {'class': class_name, 'arg1': 'str???', 'arg2': 5},
            'smart_cls': {'class': f'{class_name}:Smart', 'arg1': 'str???', 'arg2': 5},
            'smart': {'class': 'Smart'},
            'unknown': '???',
        }

        actual = self.smart._object_representation(ClassComposition, skip_default=False)

        self.assertEqual(expected, actual)

    def test_object_representation__without_defaults(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        expected = {
            'class_type': {'class': f'{class_name}:Type'},
            'vanilla_cls': {'class': class_name, 'arg1': 'str???'},
            'smart_cls': {'class': f'{class_name}:Smart', 'arg1': 'str???'},
            'smart': {'class': 'Smart'},
            'unknown': '???',
        }

        actual = self.smart._object_representation(ClassComposition, skip_default=True)

        self.assertEqual(expected, actual)

    def test_object_representation__with_aliases(self) -> None:
        class_name = f"{Class.__module__}.{Class.__qualname__}"
        class_name_smart = f"{class_name}:{Option.SMART.value}"
        class_child_name = f"{ClassChild.__module__}.{ClassChild.__qualname__}"
        self.smart.allow_only_registered_classes = True
        self.smart.register(
            (class_name, 'Parent'),
            (class_child_name, 'Child'),
            (class_name_smart, 'SmartParent'),
        )
        expected = {
            'class_type': {'class': 'Parent:Type'},
            'vanilla_cls': {'class': 'Parent', 'arg1': 'str???', 'arg2': 5},
            'smart_cls': {'class': 'SmartParent', 'arg1': 'str???', 'arg2': 5},
            'smart': {'class': 'Smart'},
            'unknown': '???',
        }

        actual = self.smart._object_representation(ClassComposition, skip_default=False)

        self.assertEqual(expected, actual)


class TestCheckCase(IntegrationCase):
    def setUp(self) -> None:
        self.smart = Smart(Class, arg1='str???', arg2=15)
        self.smart.strict = True

    def test_init_class__check_false(self) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = False
        self.smart.check_typings = False

        obj = self.smart(arg2='88')

        self.assertIsInstance(obj, Class)
        self.assertEqual('88', obj.arg2)

    def test_init_class__check_missings_true(self) -> None:
        self.smart.check_missings = True
        self.smart.check_overrides = False
        self.smart.check_typings = False

        self.assertRaises(MissingArgumentValue, self.smart, arg2='88')

    @patch('smartparams.utils.typing.warnings')
    def test_init_class__check_missings_warning(self, warnings: Mock) -> None:
        self.smart.strict = False

        self.smart.check_missings = True
        self.smart.check_overrides = False
        self.smart.check_typings = False

        obj = self.smart(arg2='88')

        self.assertEqual('88', obj.arg2)
        warnings.warn.assert_called()

    def test_init_class__check_overrides_true(self) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = True
        self.smart.check_typings = False

        self.assertRaises(UnexpectedArgument, self.smart, arg2='88')

    @patch('smartparams.utils.typing.warnings')
    def test_init_class__check_overrides_warning(self, warnings: Mock) -> None:
        self.smart.strict = False

        self.smart.check_missings = False
        self.smart.check_overrides = True
        self.smart.check_typings = False

        obj = self.smart(arg2='88')

        self.assertEqual('88', obj.arg2)
        warnings.warn.assert_called()

    def test_init_class__check_typings_true(self) -> None:
        self.smart.check_missings = False
        self.smart.check_overrides = False
        self.smart.check_typings = True

        self.assertRaises(ArgumentTypeError, self.smart, arg2='88')

    @patch('smartparams.utils.typing.warnings')
    def test_init_class__check_typings_warning(self, warnings: Mock) -> None:
        self.smart.strict = False

        self.smart.check_missings = False
        self.smart.check_overrides = False
        self.smart.check_typings = True

        obj = self.smart(arg2='88')

        self.assertEqual('88', obj.arg2)
        warnings.warn.assert_called()

    def test_init_class__trace(self) -> None:
        smart = Smart(Smart, nested=[{'class': 'Smart'}])
        smart._trace = 'trace'

        obj = smart()

        self.assertIsInstance(obj, Smart)
        self.assertEqual('trace.nested.0', obj.get('nested')[0]._trace)

    def test_init_class__raise(self) -> None:
        smart = Smart(RaiseClass)

        self.assertRaises(Exception, smart)
