import inspect
import types
from pydoc import locate

from core.constants import *


def get_type(item):
    item_type = str(type(item))
    return item_type[8:len(item_type) - 2]


class Serializer:

    def serialize(self, obj):
        if isinstance(obj, (int, float, complex, bool, str, type(None))):
            return self.serialize_single_var(obj)
        elif isinstance(obj, (list, tuple, set, bytes)):
            return self.serialize_collection(obj)
        elif isinstance(obj, dict):
            return self.serialize_dict(obj)
        elif inspect.isfunction(obj):
            return self.serialize_function(obj)
        elif inspect.isclass(obj):
            return self.serialize_class(obj)
        elif inspect.iscode(obj):
            return self.serialize_code(obj)
        elif inspect.ismodule(obj):
            return self.serialize_module(obj)
        elif inspect.ismethoddescriptor(obj) or inspect.isbuiltin(obj):
            return self.serialize_instance(obj)
        elif inspect.isgetsetdescriptor(obj) or inspect.ismemberdescriptor(obj):
            return self.serialize_instance(obj)
        elif isinstance(obj, type(type.__dict__)):
            return self.serialize_instance(obj)
        else:
            return self.serialize_object(obj)

    def serialize_single_var(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: item}

        return serialized_dict

    def serialize_collection(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: [self.serialize(obj) for obj in item]}

        return serialized_dict

    def serialize_dict(self, item):
        serialized_dict = {TYPE: get_type(item), VALUE: [[self.serialize(key), self.serialize(item[key])] for key in item]}

        return serialized_dict

    def serialize_function(self, item):
        members = inspect.getmembers(item)
        serialized = dict()
        serialized['type'] = str(type(item))[8:-2]
        value = dict()

        for tmp in members:
            if tmp[0] in ['__code__', '__name__', '__defaults__']:
                value[tmp[0]] = (tmp[1])
            if tmp[0] == '__code__':
                co_names = tmp[1].__getattribute__('co_names')
                globs = item.__getattribute__('__globals__')
                value['__globals__'] = dict()

                for tmp_co_names in co_names:
                    if tmp_co_names == item.__name__:
                        value['__globals__'][tmp_co_names] = item.__name__
                    elif not inspect.ismodule(tmp_co_names) \
                            and tmp_co_names in globs:
                        # and tmp_co_names not in __builtins__:
                        value['__globals__'][tmp_co_names] = globs[tmp_co_names]

        serialized['value'] = self.serialize(value)

        return serialized

    def serialize_class(self, item):
        serialized_dict = {TYPE: CLASS}
        value = {NAME: item.__name__}
        members = inspect.getmembers(item)
        for obj in members:
            if not (obj[0] in NOT_CLASS_ATTRIBUTES):
                value[obj[0]] = obj[1]
        serialized_dict[VALUE] = self.serialize(value)

        return serialized_dict

    def serialize_code(self, item):
        if get_type(item) is None:
            return None

        members = inspect.getmembers(item)
        serialized_dict = {TYPE: get_type(item),
                           VALUE: self.serialize({obj[0]: obj[1] for obj in members if not callable(obj[1])})}

        return serialized_dict

    def serialize_module(self, item):
        temp_item = str(item)
        serialized_dict = {TYPE: get_type(item), VALUE: temp_item[9:len(temp_item) - 13]}

        return serialized_dict

    def serialize_instance(self, item):
        members = inspect.getmembers(item)
        serialized_dict = {TYPE: get_type(item),
                           VALUE: self.serialize({obj[0]: obj[1] for obj in members if not callable(obj[1])})}

        return serialized_dict

    def serialize_object(self, item):
        serialized_dict = {TYPE: OBJECT, VALUE: self.serialize({OBJECT_TYPE: type(item), FIELDS: item.__dict__})}

        return serialized_dict

    def deserialize(self, item):
        if item[TYPE] in [INT, FLOAT, BOOL, STRING, COMPLEX, NONE_TYPE]:
            return self.deserialize_single_var(item)
        elif item[TYPE] in [LIST, TUPLE, SET, BYTES]:
            return self.deserialize_collection(item)
        elif item[TYPE] == DICT:
            return self.deserialize_dict(item)
        elif item[TYPE] == FUNCTION:
            return self.deserialize_function(item)
        elif item[TYPE] == CLASS:
            return self.deserialize_class(item)
        elif item[TYPE] == MODULE:
            return self.deserialize_module(item)
        elif item[TYPE] == OBJECT:
            return self.deserialize_object(item)

    def deserialize_single_var(self, item):
        if item[TYPE] == NONE_TYPE:
            return None
        elif item[TYPE] == BOOL and isinstance(item[VALUE], str):
            return item[VALUE] == TRUE
        else:
            return locate(item[TYPE])(item[VALUE])

    def deserialize_collection(self, item):
        if item[TYPE] == LIST:
            return list(self.deserialize(obj) for obj in item[VALUE])
        elif item[TYPE] == TUPLE:
            return tuple(self.deserialize(obj) for obj in item[VALUE])
        elif item[TYPE] == SET:
            return set(self.deserialize(obj) for obj in item[VALUE])
        elif item[TYPE] == BYTES:
            return bytes(self.deserialize(obj) for obj in item[VALUE])

    def deserialize_dict(self, item):
        return {self.deserialize(obj[0]): self.deserialize(obj[1]) for obj in item[VALUE]}

    def deserialize_function(self, item):
        res_dict = self.deserialize(item['value'])

        res_dict['code'] = self.deserialize_code(item)
        res_dict.pop('__code__')

        res_dict['globals'] = res_dict['__globals__']
        res_dict.pop('__globals__')

        res_dict['name'] = res_dict['__name__']
        res_dict.pop('__name__')

        res_dict['argdefs'] = res_dict['__defaults__']
        res_dict.pop('__defaults__')

        res = types.FunctionType(**res_dict)
        if res.__name__ in res.__getattribute__('__globals__'):
            res.__getattribute__('__globals__')[res.__name__] = res

        return res

    def deserialize_code(self, item):
        items = item['value']['value']

        for tmp in items:
            if tmp[0]['value'] == '__code__':
                args = self.deserialize(tmp[1]['value'])
                code_dict = dict()
                for arg in args:
                    arg_val = args[arg]
                    if arg != '__doc__':
                        code_dict[arg] = arg_val
                code_list = [0] * 16

                for name in code_dict:
                    if name == 'co_lnotab':
                        continue
                    code_list[CODE_ARGS.index(name)] = code_dict[name]

                return types.CodeType(*code_list)

    def deserialize_class(self, item):
        class_dict = self.deserialize(item[VALUE])
        name = class_dict[NAME]
        del class_dict[NAME]

        return type(name, (object,), class_dict)

    def deserialize_module(self, item):
        return __import__(item[VALUE])

    def deserialize_object(self, item):
        value = self.deserialize(item[VALUE])
        result = value[OBJECT_TYPE](**value[FIELDS])

        for key, value in value[FIELDS].items():
            result.key = value

        return result
