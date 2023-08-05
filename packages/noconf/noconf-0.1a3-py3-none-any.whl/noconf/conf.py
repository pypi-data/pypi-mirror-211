from copy import deepcopy
import functools
from functools import cache
from functools import wraps
from importlib import import_module
from logging.config import dictConfig
import os
import sys
from threading import RLock


DEFAULT_CONFIG_FILE_LOCATIONS = (
    'noconf-config.py',
    os.path.join('etc', 'noconf-config.py'),
    )


def synchronized(func):
    lock = RLock()
    @wraps(func)
    def wrapper(*args, **kwargs):
        with lock:
            return func(*args, **kwargs)
    if hasattr(func, 'cache_clear'):
        wrapper.cache_clear = func.cache_clear
    return wrapper


def partial(func, *args, **kwargs):
    return functools.partial(func, *args, **kwargs)


def resolve_dotted_name(dotted_name):
    if ':' in dotted_name:
        module, name = dotted_name.split(':')
    elif '.' in dotted_name:
        module, name = dotted_name.rsplit('.', 1)
    else:
        module, name = dotted_name, None

    attr = import_module(module)
    if name:
        for name in name.split('.'):
            attr = getattr(attr, name)

    return attr


class Config(dict):
    """A dictionary that represents the app's configuration.

    Tries to send a more user friendly message in case of KeyError.
    """
    initialized = False

    def __getitem__(self, name):
        try:
            return super(Config, self).__getitem__(name)
        except KeyError:
            raise KeyError(
                f"The required key '{name}' was not found in your "
                "configuration."
            )


class ComponentHandler:
    key = '!'

    def __init__(self, config):
        self.config = config
        self.components = []

    def __call__(self, name, props):
        specification = props.copy()
        factory_dotted_name = specification.pop(self.key)
        factory = resolve_dotted_name(factory_dotted_name)
        component = factory(**specification)
        try:
            component.__noconf_key__ = name
        except (AttributeError, ValueError):
            pass
        self.components.append(component)
        return component

    def finish(self):
        for component in self.components:
            if hasattr(component, 'initialize_component'):
                component.initialize_component(self.config)


class CopyHandler:
    key = '__copy__'

    def __init__(self, configs):
        self.configs = configs

    @staticmethod
    def _resolve(configs, dotted_path):
        for config in configs[::-1]:
            value = config
            for part in dotted_path.split('.'):
                try:
                    value = value[part]
                except KeyError:
                    break
            else:
                return value
        else:
            raise KeyError(dotted_path)

    def __call__(self, name, props):
        dotted_path = props[self.key]
        try:
            value = self._resolve(self.configs[-1:], dotted_path)
            self_reference = value is props
        except KeyError:
            self_reference = False

        if self_reference:
            value = self._resolve(self.configs[:-1], dotted_path)
        else:
            try:
                value = self._resolve(self.configs, dotted_path)
            except KeyError:
                if '__default__' in props:
                    return props['__default__']
                else:
                    raise

        value = deepcopy(value)
        nonmagicprops = [
            prop for prop in props
            if not (prop.startswith('__') and prop.endswith('__'))
            ]
        if nonmagicprops:
            recursive_copy = self.key in value
            value.update(props)
            if not recursive_copy:
                del value[self.key]
        return value


class PythonHandler:
    key = '__python__'

    def __init__(self, config):
        self.config = config

    def __call__(self, name, props):
        statements = props.pop(self.key)
        exec(
            statements,
            globals(),
            {key: self.config for key in ['C', 'cfg', 'config']},
            )
        return props


def rewrite_handler(key_from, key_to):
    class RewriteHandler:
        key = key_from
        target = key_to

        def __init__(self, config):
            pass

        def __call__(self, name, props):
            props[self.target] = props.pop(self.key)
            return props
    return RewriteHandler


def _handlers_phase0(configs):
    return {
        Handler.key: Handler(configs) for Handler in [
            rewrite_handler('__factory__', '!'),
            CopyHandler,
            ]
        }


def _handlers_phase1(config):
    return {
        Handler.key: Handler(config) for Handler in [
            PythonHandler,
            ]
        }


def _handlers_phase2(config):
    return {
        Handler.key: Handler(config) for Handler in [
            ComponentHandler,
            ]
        }


def _run_config_handlers_recursive(props, handlers):
    if isinstance(props, dict):
        for key, value in tuple(props.items()):
            if isinstance(value, dict):
                _run_config_handlers_recursive(value, handlers)
                for name, handler in handlers.items():
                    if name in value:
                        value = props[key] = handler(key, value)
            elif isinstance(value, (list, tuple)):
                _run_config_handlers_recursive(value, handlers)
    elif isinstance(props, (list, tuple)):
        for i, item in enumerate(props):
            if isinstance(item, dict):
                _run_config_handlers_recursive(item, handlers)
                for name, handler in handlers.items():
                    if name in item:
                        item = props[i] = handler(str(i), item)
            elif isinstance(item, (list, tuple)):
                _run_config_handlers_recursive(item, handlers)


def _run_config_handlers(config, handlers):
    wrapped_config = {'root': config}
    _run_config_handlers_recursive(wrapped_config, handlers)
    for handler in handlers.values():
        if hasattr(handler, 'finish'):
            handler.finish()
    return wrapped_config['root']


def _initialize_logging(config):
    if 'logging' in config:
        dictConfig(config['logging'])


def process_configs(
    *configs,
    handlers0=_handlers_phase0,
    handlers1=_handlers_phase1,
    handlers2=_handlers_phase2
):
    config_final = {}

    for config in configs:
        config_org = deepcopy(config_final)
        config_final.update(config)
        _run_config_handlers(
            config_final, handlers0([config_org, config]))
        _run_config_handlers(
            config_final, handlers0([config_final, {}]))

    _run_config_handlers(config_final, handlers1(config_final))
    _run_config_handlers(config_final, handlers2(config_final))
    _initialize_logging(config_final)
    return config_final


@synchronized
@cache
def load(
    fnames=None,
    **extra,
):
    if fnames is None:
        for fname in DEFAULT_CONFIG_FILE_LOCATIONS:
            if os.path.exists(fname):  # pragma: no cover
                fnames = fname
                print("Using configuration at {}".format(fname))
                break
        else:
            if extra is None:
                raise RuntimeError(
                    "Could not determine configuration file to read from."
                )
            else:
                fnames = []
    configs = []
    if isinstance(fnames, str):
        fnames = [fname.strip() for fname in fnames.split(',')]
    for fname in fnames:
        sys.path.insert(0, os.path.dirname(fname))
        with open(fname) as f:
            config = eval(f.read(), {
                'environ': os.environ,
                'here': os.path.abspath(os.path.dirname(fname)),
                })
        configs.append(config)
    return process_configs(*(configs + [extra]))
