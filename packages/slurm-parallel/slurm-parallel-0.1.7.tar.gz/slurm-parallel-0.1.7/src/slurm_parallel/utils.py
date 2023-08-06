import importlib
import os
import sys

def to_cmd_options(**kwargs):
    options = []

    for k, v in kwargs.items():
        k = k.replace('_', '-')
        k = f'--{k}' if len(k) > 1 else f'-{k}'

        if isinstance(v, bool) and not v:
            continue
        
        options.append(k)
        
        if isinstance(v, bool):
            continue
        elif isinstance(v, (list, tuple)):
            options += [str(vi) for vi in v]
        else:
            options.append(str(v))

    return options

def import_from_file_path(path):
    """Performs a module import given the filename. This code is copied from 
    https://github.com/google/python-fire/blob/master/fire/__main__.py

    Args:
    path (str): the path to the file to be imported.

    Raises:
    IOError: if the given file does not exist or importlib fails to load it.

    Returns:
    Tuple[ModuleType, str]: returns the imported module and the module name,
      usually extracted from the path itself.
    """

    if not os.path.exists(path):
        raise IOError('Given file path does not exist.')

    module_name = os.path.basename(path)

    if sys.version_info.major == 3 and sys.version_info.minor < 5:
        loader = importlib.machinery.SourceFileLoader(  # pylint: disable=no-member
            fullname=module_name,
            path=path,
        )

        module = loader.load_module(module_name)  # pylint: disable=deprecated-method

    elif sys.version_info.major == 3:
        from importlib import util  # pylint: disable=g-import-not-at-top,import-outside-toplevel,no-name-in-module
        spec = util.spec_from_file_location(module_name, path)

        if spec is None:
            raise IOError('Unable to load module from specified path.')

        module = util.module_from_spec(spec)  # pylint: disable=no-member
        spec.loader.exec_module(module)  # pytype: disable=attribute-error

    else:
        import imp  # pylint: disable=g-import-not-at-top,import-outside-toplevel,deprecated-module
        module = imp.load_source(module_name, path)

    return module, module_name
