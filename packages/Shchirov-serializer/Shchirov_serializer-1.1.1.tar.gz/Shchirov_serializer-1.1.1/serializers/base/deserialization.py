from serializers.base.constants import (PRIMITIVES, COLLECTIONS, CODE_ATTRIBUTES,
                                          TYPE, VALUE, METHOD_DECORATORS, ITERATOR_TYPE)
from types import NoneType, FunctionType, CodeType, CellType, MethodType
import inspect
import builtins


class Deserializer:

    @staticmethod
    def unpack(obj: dict):
        """
        Method that converts dictionary that
        represents the object to object.

        Parameters:
        obj (Any): Dictionary.

        Returns:
        object.
        """

        if obj[TYPE] in tuple(map(lambda p: p.__name__, PRIMITIVES)):
            if obj[TYPE] == str(NoneType.__name__):
                return None
            else:
                return getattr(builtins, obj[TYPE])(obj[VALUE])

        if obj[TYPE] in tuple(map(lambda c: c.__name__, COLLECTIONS)):
            if obj[TYPE] == dict.__name__:
                return {Deserializer.unpack(item[0]): Deserializer.unpack(item[1])
                        for item in obj[VALUE]}
            else:
                return getattr(builtins, obj[TYPE])(Deserializer.unpack(item)
                                                    for item in obj[VALUE])

        if obj[TYPE] in [FunctionType.__name__, MethodType.__name__]:
            return Deserializer._unpack_function(obj[VALUE])

        if obj[TYPE] == CodeType.__name__:
            return Deserializer._unpack_code(obj[VALUE])

        if obj[TYPE] == CellType.__name__:
            return CellType(Deserializer.unpack(obj[VALUE]))

        if obj[TYPE] == "class":
            return Deserializer._unpack_class(obj[VALUE])

        if obj[TYPE] in tuple(map(lambda md: md.__name__, METHOD_DECORATORS)):
            return getattr(builtins, obj[TYPE])(Deserializer.unpack(obj[VALUE]))

        if obj[TYPE] == property.__name__:
            return property(fget=Deserializer.unpack(obj[VALUE]["fget"]),
                            fset=Deserializer.unpack(obj[VALUE]["fset"]),
                            fdel=Deserializer.unpack(obj[VALUE]["fdel"]))

        if obj[TYPE] == ITERATOR_TYPE:
            return iter(Deserializer.unpack(item) for item in obj[VALUE])

        return Deserializer._unpack_object(obj[VALUE])

    @staticmethod
    def _unpack_function(obj: dict):
        code = Deserializer._unpack_code(obj["__code__"])

        globs = Deserializer._unpack_globals(obj["__globals__"], obj)
        globs["builtins"] = __import__("builtins")

        closure = Deserializer.unpack(obj["__closure__"])
        closure = tuple(closure) if closure else tuple()

        unpacked = FunctionType(code=code, globals=globs, closure=closure)
        unpacked.__globals__.update({unpacked.__name__: unpacked})
        unpacked.__defaults__ = Deserializer.unpack(obj["__defaults__"])
        unpacked.__kwdefaults__ = Deserializer.unpack(obj["__kwdefaults__"])

        return unpacked

    @staticmethod
    def _unpack_globals(globs, func):
        unpacked = dict()

        for key, value in globs.items():
            if "module" in key:
                unpacked[value[VALUE]] = __import__(value[VALUE])

            elif value != func["__name__"]:
                unpacked[key] = Deserializer.unpack(value)

        return unpacked

    @staticmethod
    def _unpack_class(obj):

        attrs = {member: Deserializer.unpack(value)
                 for member, value in obj.items()}

        cls = type(Deserializer.unpack(obj["__name__"]),
                   Deserializer.unpack(obj["__bases__"]),
                   attrs)

        for value in attrs.values():
            if inspect.isfunction(value):
                value.__globals__.update({cls.__name__: cls})
            elif isinstance(value, (staticmethod, classmethod)):
                value.__func__.__globals__.update({cls.__name__: cls})

        return cls

    @staticmethod
    def _unpack_object(obj):

        unpacked = object.__new__(Deserializer.unpack(obj["__class__"]))
        unpacked.__dict__ = {key: Deserializer.unpack(value)
                             for key, value in obj["__vars__"].items()}

        return unpacked

    @staticmethod
    def _unpack_code(code):
        # return CodeType(*(Deserializer.unpack(code[ATTRIBUTE])
        #                   for ATTRIBUTE in CODE_ATTRIBUTES))

        return CodeType(Deserializer.unpack(code["co_argcount"]),
                        Deserializer.unpack(code["co_posonlyargcount"]),
                        Deserializer.unpack(code["co_kwonlyargcount"]),
                        Deserializer.unpack(code["co_nlocals"]),
                        Deserializer.unpack(code["co_stacksize"]),
                        Deserializer.unpack(code["co_flags"]),
                        Deserializer.unpack(code["co_code"]),
                        Deserializer.unpack(code["co_consts"]),
                        Deserializer.unpack(code["co_names"]),
                        Deserializer.unpack(code["co_varnames"]),
                        Deserializer.unpack(code["co_filename"]),
                        Deserializer.unpack(code["co_name"]),
                        #Deserializer.unpack(code["co_qualname"]),
                        Deserializer.unpack(code["co_firstlineno"]),
                        Deserializer.unpack(code["co_lnotab"]),
                        #Deserializer.unpack(code["co_exceptiontable"]),
                        Deserializer.unpack(code["co_freevars"]),
                        Deserializer.unpack(code["co_cellvars"]))