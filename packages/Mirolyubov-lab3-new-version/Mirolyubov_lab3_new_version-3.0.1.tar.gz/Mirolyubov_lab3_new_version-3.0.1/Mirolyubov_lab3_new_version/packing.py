import inspect
import builtins
import types
from Mirolyubov_lab3_new_version.CONSTANTS import PRIMITIVE_TYPES
from types import FunctionType, BuiltinFunctionType, LambdaType, CodeType, GetSetDescriptorType, MappingProxyType, \
    MethodDescriptorType, WrapperDescriptorType


def is_generator(obj):
    return inspect.isgenerator(obj)


def is_function(obj):
    return inspect.isfunction(obj) or inspect.ismethod(obj) or isinstance(obj, LambdaType)


def is_iterable(obj):
    return getattr(obj, "__iter__", None) is not None


def convert(obj):
    if isinstance(obj, PRIMITIVE_TYPES):
        return obj

    elif isinstance(obj, (list, tuple, set, dict)):
        return obj

    elif is_function(obj):
        return pack_function(obj)

    elif inspect.iscode(obj):
        return pack_inner_func(obj)

    elif inspect.isclass(obj):
        return pack_class(obj)

    elif is_generator(obj):
        return pack_generator(obj)

    elif is_iterable(obj):
        return pack_iterable(obj)

    else:
        return pack_object(obj)


def pack_generator(obj, cls=None):
    result = {"__type__": "generator"}
    result["__name__"] = obj.__name__
    lst = []

    for i in obj:
        lst.append(i)
    result["__values__"] = lst

    return result

def unpack_generator(obj, cls=None):
    for i in obj["__values__"]:
        yield i

def pack_function(obj, cls=None):
    result = {"__type__": "function"}

    if inspect.ismethod(obj):
        obj = obj.__func__

    obj.__name__ = obj.__name__.replace('>', '')
    result["__name__"] = obj.__name__.replace('<', '')

    globs = get_global_vars(obj, cls)
    result["__globals__"] = pack_iterable(globs)

    arguments = {}

    for (key, value) in inspect.getmembers(obj.__code__):
        if key.startswith("co_"):
            if key == "co_lines":
                continue
            if isinstance(value, bytes):
                value = list(value)

            if is_iterable(value) and not isinstance(value, str):
                converted_vals = []

                for val in value:
                    if val is not None:
                        converted_vals.append(convert(val))

                    else:
                        converted_vals.append(None)

                arguments[key] = converted_vals

                continue

            arguments[key] = value

    result["__args__"] = arguments

    return result


def get_global_vars(func, cls):
    globs = {}

    for global_var in func.__code__.co_names:
        if global_var in func.__globals__:
            if isinstance(func.__globals__[global_var], types.ModuleType):
                globs[global_var] = func.__globals__[global_var].__name__

            elif inspect.isclass(func.__globals__[global_var]):
                if cls and func.__globals__[global_var] != cls:
                    globs[global_var] = func.__globals__[global_var]

            elif global_var != func.__code__.co_name:
                globs[global_var] = func.__globals__[global_var]

            else:
                globs[global_var] = func.__name__
    return globs


def pack_iterable(obj):
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        packed_iterable = []

        for value in obj:
            packed_iterable.append(convert(value))

        if isinstance(obj, tuple):
            return tuple(packed_iterable)

        if isinstance(obj, set):
            return set(packed_iterable)

        return packed_iterable

    elif isinstance(obj, dict):
        packed_dict = {}

        for key, value in obj.items():
            packed_dict[key] = convert(value)

        return packed_dict


def pack_inner_func(obj):   
    return pack_function(FunctionType(obj, {}))


def pack_class(obj):
    result = {'__type__': 'class', '__name__': obj.__name__}

    for attr in inspect.getmembers(obj):
        if attr[0] not in (
                "__mro__", "__base__", "__basicsize__",
                "__class__", "__dictoffset__", "__name__",
                "__qualname__", "__text_signature__", "__itemsize__",
                "__flags__", "__weakrefoffset__", "__objclass__"
        ) and type(attr[1]) not in (
                WrapperDescriptorType,
                MethodDescriptorType,
                BuiltinFunctionType,
                MappingProxyType,
                GetSetDescriptorType
        ):
            attr_value = getattr(obj, attr[0])

            if is_function(attr_value):
                result[attr[0]] = pack_function(attr_value, obj)

            else:
                result[attr[0]] = convert(attr_value)

    result["__bases__"] = [pack_class(base) for base in obj.__bases__ if base != object]

    return result


def unpack_class(obj):
    class_bases = tuple(unpack_class(base) for base in obj["__bases__"])
    class_methods = {}

    for attr, value in obj.items():
        class_methods[attr] = deconvert(value)

    result = type(obj["__name__"], class_bases, class_methods)

    for key, method in class_methods.items():
        if inspect.isfunction(method):
            method.__globals__.update({result.__name__: result})

    return result


def pack_object(obj):
    result = {"__type__": "object", "__class__": pack_class(obj.__class__), "attr": {}}

    for key, value in inspect.getmembers(obj):
        if not key.startswith("__") and not is_function(value):
            result["attr"][key] = convert(value)

    return result


def unpack_object(obj):
    obj_class = deconvert(obj["__class__"])
    attrs = {}

    for key, value in obj["attr"].items():
        attrs[key] = deconvert(value)

    result = object.__new__(obj_class)
    result.__dict__ = attrs

    return result


def deconvert(src):
    if isinstance(src, PRIMITIVE_TYPES):
        return src

    elif isinstance(src, dict):
        if "function" in src.values():
            return unpack_function(src)

        elif "object" in src.values():
            return unpack_object(src)

        elif "generator" in src.values():
            return unpack_generator(src)

        elif "class" in src.values():
            return unpack_class(src)

        else:
            return unpack_iterable(src)

    elif is_iterable(src):
        return unpack_iterable(src)

    else:
        raise Exception("Unknown type")


def unpack_function(src):
    arguments = src["__args__"]
    globs = src["__globals__"]
    globs["__builtins__"] = builtins

    for key in src["__globals__"]:
        if key in arguments["co_names"]:
            try:
                globs[key] = __import__(src["__globals__"][key])
            except:
                if globs[key] != src["__name__"]:
                    globs[key] = deconvert(src["__globals__"][key])

    coded = CodeType(arguments['co_argcount'],
                     arguments['co_posonlyargcount'],
                     arguments['co_kwonlyargcount'],
                     arguments['co_nlocals'],
                     arguments['co_stacksize'],
                     arguments['co_flags'],
                     bytes(arguments['co_code']),
                     tuple(arguments['co_consts']),
                     tuple(arguments['co_names']),
                     tuple(arguments['co_varnames']),
                     arguments['co_filename'],
                     arguments['co_name'],
                     arguments['co_firstlineno'],
                     bytes(arguments['co_lnotab']),
                     tuple(arguments['co_freevars']),
                     tuple(arguments['co_cellvars']))

    func_result = FunctionType(coded, globs)
    func_result.__globals__.update({func_result.__name__: func_result})

    return func_result


def unpack_iterable(obj):
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        unpacked_iterable = []

        for value in obj:
            unpacked_iterable.append(deconvert(value))

        if isinstance(obj, tuple):
            return tuple(unpacked_iterable)

        if isinstance(obj, set):
            return set(unpacked_iterable)

        return unpacked_iterable

    elif isinstance(obj, dict):
        unpacked_dict = {}

        for key, value in obj.items():
            unpacked_dict[key] = deconvert(value)

        return unpacked_dict


def turn_obj_into_dict(obj):
    if isinstance(obj, type(None)):

        return {
            "None": "None"
        }

    elif isinstance(obj, PRIMITIVE_TYPES):

        return {
            str(type(obj)): obj
        }

    elif isinstance(obj, (list, tuple, set)):
        result = []

        for item in obj:
            result.append(turn_obj_into_dict(item))

        return {
            str(type(obj)): result
        }

    elif isinstance(obj, dict):
        result = {}

        for key, value in obj.items():
            result[key] = turn_obj_into_dict(value)

        return result

    else:
        raise Exception("Unknown type")


def restore_object_from_dict(src):
    if type(src) is dict:

        if len(src.keys()) == 1:
            key, value = list(src.items())[0]

            if key == "None":
                return None

            elif isinstance(value, PRIMITIVE_TYPES):
                return value

            elif isinstance(value, list):
                result = []

                for obj in value:
                    result.append(restore_object_from_dict(obj))

                if key == "<class 'tuple'>":
                    result = tuple(result)

                elif key == "<class 'set'>":
                    result = set(result)

                return result

        result = {}

        for key, val in src.items():
            result[key] = restore_object_from_dict(val)

        return result

    else:
        raise Exception("Object type must be dict")
