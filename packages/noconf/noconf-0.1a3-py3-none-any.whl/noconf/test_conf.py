from contextlib import contextmanager
from copy import deepcopy
import os
import threading
import time
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def load_cache_clear():
    from noconf import load
    load.cache_clear()


class MyDummyComponent:
    def __init__(self, arg1, arg2='blargh', subcomponent=None):
        self.arg1 = arg1
        self.arg2 = arg2
        self.subcomponent = subcomponent
        self.initialize_component_arg = None

    def initialize_component(self, config):
        self.initialize_component_arg = config

    def __eq__(self, other):
        return all([
            self.arg1 == other.arg1,
            self.arg2 == other.arg2,
            self.subcomponent == other.subcomponent,
            self.initialize_component_arg == other.initialize_component_arg,
            ])


class BlockingDummy:
    def __init__(self):
        time.sleep(0.1)


@contextmanager
def cwd(path):
    before = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(before)


def test_config_class_keyerror():
    from noconf.conf import Config
    with pytest.raises(KeyError) as e:
        Config({})['invalid']
    assert "The required key 'invalid' was not found" in str(e.value)


class TestLoad:
    @pytest.fixture
    def load(self):
        from noconf.conf import load
        return load

    @pytest.fixture
    def config1_fname(self, tmpdir):
        path = tmpdir.join('noconf-config.py')
        path.write("""{
            'env': environ['ENV1'],
            'here': here,
            'blocking': {
                '!': 'noconf.test_conf.BlockingDummy',
            }
        }""")
        return str(path)

    @pytest.fixture
    def config2_fname(self, tmpdir):
        path = tmpdir.join('config2.py')
        path.write("{'env': environ['ENV2']}")
        return str(path)

    def test_extras(self, load):
        assert load(foo='bar')['foo'] == 'bar'

    def test_default_config(self, load, config1_fname, monkeypatch):
        here = os.path.dirname(config1_fname)
        monkeypatch.setitem(os.environ, 'ENV1', 'one')
        with cwd(here):
            config = load()
        assert config['here'] == here

    def test_variables(self, load, config1_fname, monkeypatch):
        monkeypatch.setitem(os.environ, 'ENV1', 'one')
        config = load(config1_fname)
        assert config['env'] == 'one'
        assert config['here'] == os.path.dirname(config1_fname)

    def test_multiple_files(self, load, config1_fname, config2_fname,
                            monkeypatch):
        monkeypatch.setitem(os.environ, 'ENV1', 'one')
        monkeypatch.setitem(os.environ, 'ENV2', 'two')
        config = load((config1_fname, config2_fname))
        assert config['env'] == 'two'
        assert config['here'] == os.path.dirname(config1_fname)

    def test_multithreaded(self, load, config1_fname, monkeypatch):
        monkeypatch.setitem(os.environ, 'ENV1', 'one')

        cfgs = {}
        def load_me_config():
            cfgs[threading.get_ident()] = load(config1_fname).copy()

        threads = [threading.Thread(target=load_me_config) for i in range(20)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        cfg_values = list(cfgs.values())
        for cfg in cfg_values[1:]:
            assert cfg == cfg_values[0]

    def test_noconf_key(self, load, config1_fname, monkeypatch):
        monkeypatch.setitem(os.environ, 'ENV1', 'one')
        config = load(config1_fname)
        assert config['blocking'].__noconf_key__ == 'blocking'


class TestProcessConfig:
    @pytest.fixture
    def process_configs(self):
        from noconf.conf import process_configs
        return process_configs

    @pytest.fixture
    def config1(self):
        dummy = 'noconf.test_conf.MyDummyComponent'
        return {
            'mycomponent': {
                '!': dummy,
                'arg1': 3,
                'arg2': {'no': 'factory'},
                'subcomponent': {
                    '!': dummy,
                    'arg1': {
                        'subsubcomponent': {
                            '!':
                            dummy,
                            'arg1': 'wobwob',
                            'arg2': 9,
                            },
                        },
                    'arg2': 6,
                    },
                },
            'mylistofcomponents': [{
                '!': dummy,
                'arg1': 'wobwob',
                },
                'somethingelse',
                ],
            'mynestedlistofcomponents': [[{
                '!': dummy,
                'arg1': 'feep',
                'arg2': {
                    '__factory__': dummy,  # alternative to '!'
                    'arg1': 6,
                },
            }]],
            'myconstant': 42,

            'mycopiedconstant': {
                '__copy__': 'mycomponent.arg1',
                },

            'mydict': {
                'arg1': 1,
                'mycopiedcomponent': {
                    '__copy__': 'mycomponent',
                    'arg2': None,
                    },
                },

            '__python__': """
C['mynestedlistofcomponents'][0][0]['arg2']['!'] = 'builtins:dict'
C['myotherconstant'] = 13
""",
            }

    @pytest.fixture
    def config2(self):
        return {
            'mydict': {
                '__copy__': 'mydict',
                'arg1': 3,
                'arg2': None,
                },
            'mynewdict': {
                '__copy__': 'mydict',
                'arg2': 2,
                },
            'mysupernewdict': {
                '__copy__': 'mynewdict',
                },
            'mycopiedconstant': {
                '__copy__': 'mycopiedconstant',
                '__default__': 42,
                },
            'mycopywithdefault': {
                '__copy__': 'nonexistant',
                '__default__': 42,
                },
            }

    def test_config1(self, process_configs, config1):
        config = process_configs(config1)

        assert config['myconstant'] == 42

        mycomponent = config['mycomponent']
        assert isinstance(mycomponent, MyDummyComponent)
        assert mycomponent.arg1 == 3
        assert mycomponent.arg2 == {'no': 'factory'}
        assert mycomponent.initialize_component_arg is config

        subcomponent = mycomponent.subcomponent
        assert isinstance(subcomponent, MyDummyComponent)
        assert subcomponent.arg2 == 6
        assert subcomponent.initialize_component_arg is config

        subsubcomponent = subcomponent.arg1['subsubcomponent']
        assert isinstance(subsubcomponent, MyDummyComponent)
        assert subsubcomponent.arg1 == 'wobwob'
        assert subsubcomponent.arg2 == 9
        assert subsubcomponent.initialize_component_arg is config

        mylistofcomponents = config['mylistofcomponents']
        assert len(mylistofcomponents) == 2
        assert isinstance(mylistofcomponents[0], MyDummyComponent)
        assert mylistofcomponents[0].arg1 == 'wobwob'
        assert mylistofcomponents[1] == 'somethingelse'

        mnl = config['mynestedlistofcomponents']
        assert isinstance(mnl[0][0], MyDummyComponent)
        assert mnl[0][0].arg1 == 'feep'

        assert config['mycopiedconstant'] == 3

        mcc = config['mydict']['mycopiedcomponent']
        assert mcc.arg2 is None
        assert mcc.arg1 == mycomponent.arg1
        assert mcc.subcomponent == mycomponent.subcomponent
        assert mcc.subcomponent is not mycomponent.subcomponent

        assert isinstance(mnl[0][0].arg2, dict)
        assert config['myotherconstant'] == 13

    def test_config1_and_2(self, process_configs, config1, config2):
        config = process_configs(config1, config2)

        assert config['mydict']['arg1'] == 3

        mycomponent = config['mycomponent']
        mcc = config['mydict']['mycopiedcomponent']
        assert mcc.arg2 is None
        assert mcc.arg1 == mycomponent.arg1
        assert mcc.subcomponent == mycomponent.subcomponent
        assert mcc.subcomponent is not mycomponent.subcomponent

        assert config['mynewdict']['arg1'] == config['mydict']['arg1']
        assert config['mynewdict']['arg2'] == 2
        assert isinstance(
            config['mynewdict']['mycopiedcomponent'], MyDummyComponent)
        assert isinstance(
            config['mysupernewdict']['mycopiedcomponent'], MyDummyComponent)

        assert config['mycopiedconstant'] == 3
        assert config['mycopywithdefault'] == 42

    @pytest.fixture
    def config3(self):
        return {
            'first': 5,
            'second': {
                '__copy__': 'first',
                '__default__': 6,
                },
            }

    def test_copy_source_exists_with_default(self, process_configs, config3):
        expected = deepcopy(config3)
        expected['second'] = expected['first']
        got = process_configs(config3)
        assert got == expected

    def test_copy_source_exists_no_default(self, process_configs, config3):
        expected = deepcopy(config3)
        expected['second'] = expected['first']
        del config3['second']['__default__']
        got = process_configs(config3)
        assert got == expected

    def test_copy_source_missing_with_default(self, process_configs, config3):
        expected = deepcopy(config3)
        expected['second'] = expected['second']['__default__']
        del expected['first']
        del config3['first']
        got = process_configs(config3)
        assert got == expected

    def test_copy_source_missing_no_default(self, process_configs, config3):
        del config3['first']
        del config3['second']['__default__']
        with pytest.raises(KeyError):
            process_configs(config3)

    def test_initialize_config_logging(self, process_configs):
        with patch('noconf.conf.dictConfig') as dictConfig:
            process_configs({'logging': 'yes, please'})
            dictConfig.assert_called_with('yes, please')
