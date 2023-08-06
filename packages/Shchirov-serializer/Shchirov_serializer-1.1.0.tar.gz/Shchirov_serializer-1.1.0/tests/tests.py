import unittest
from serializers.json_serializer.JsonSerializer import _JsonSerializer
from tests.constants_for_testing import (circle_area, square_area, generator, bts, bts_arr, sum_func,
                        generator_expression, closure, factorial, Profile,
                        sum_args, sum_kwargs, sum_args_kwargs, subgenerator,
                        lambda_pow, C, E, Human, func1, func2, func3, it)



class BaseJsonTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.serializer = _JsonSerializer()
        self.alias = lambda x: self.serializer.loads(self.serializer.dumps(x))


class PrimitivesTestCase(BaseJsonTestCase):
    def test_int(self):
        self.assertEqual(10, self.alias(10))
        self.assertEqual(0, 0)
        self.assertEqual(-10, self.alias(-10))

    def test_float(self):
        self.assertEqual(10.1, self.alias(10.1))
        self.assertEqual(-10.1, self.alias(-10.1))

    def test_bool(self):
        self.assertEqual(True, self.alias(True))
        self.assertEqual(False, self.alias(False))

    def test_str(self):
        self.assertEqual("", self.alias(""))
        self.assertEqual("Hello world!", self.alias("Hello world!"))

    def test_none(self):
        self.assertEqual(None, self.alias(None))

    def test_complex(self):
        self.assertEqual(5 + 3j, self.alias(5 + 3j))
        self.assertEqual(5 + 0j, self.alias(5 + 0j))
        self.assertEqual(3j, self.alias(3j))
        self.assertEqual(0j, self.alias(0j))


class CollectionsTestCase(BaseJsonTestCase):
    def test_list(self):
        self.assertEqual([], self.alias([]))
        self.assertEqual([1, 2, 3], self.alias([1, 2, 3]))

    def test_tuple(self):
        self.assertEqual((), self.alias(()))
        self.assertEqual((1, 2, 3), self.alias((1, 2, 3)))

    def test_set(self):
        self.assertEqual({}, self.alias({}))
        self.assertEqual({1, 2, 3}, self.alias({1, 2, 3}))

    def test_dict(self):
        self.assertEqual({'a1': 'b2'}, self.alias({'a1': 'b2'}))
        self.assertEqual({'a1': 'b2', 'c3': 'd4'}, self.alias({'a1': 'b2', 'c3': 'd4'}))

    def test_big_collection(self):
        collection = [1, 2, [3, 4], 5, (6, 7), {8, 9}, [], 10, (), {}, {11: '12', '13': 14}]
        collection.append(collection[::])
        self.assertEqual(collection, self.alias(collection))

    def test_bytes(self):
        deserialized = self.alias(bts)
        self.assertEqual(bts, deserialized)
        self.assertEqual(bts.decode(), deserialized.decode())

    def test_bytearray(self):
        deserialized = self.alias(bts_arr)
        self.assertEqual(bts_arr, deserialized)
        self.assertEqual(bts_arr.decode(), deserialized.decode())


class FunctionsTestCase(BaseJsonTestCase):
    def test_using_modules(self):
        deserialized = self.alias(circle_area)
        self.assertEqual(circle_area(10), deserialized(10))

    def test_decorator(self):
        self.assertEqual(square_area(10), self.alias(square_area)(10))

        deserialized = self.alias(sum_func)
        self.assertEqual(sum_func(1, 2, 3, 4, 5), deserialized(1, 2, 3, 4, 5))
        try:
            deserialized(1, 2, 3, 4, 5, 6)
        except Exception as e:
            self.assertEqual(True, isinstance(e, ValueError))

    def test_closure(self):
        deserialized = self.alias(closure)
        self.assertEqual(type(closure), type(deserialized))
        self.assertEqual(closure(1, 2, 3)(), deserialized(1, 2, 3)())

    def test_lambda(self):
        deserialized = self.alias(lambda_pow)
        self.assertEqual(type(lambda_pow), type(deserialized))
        self.assertEqual(lambda_pow(36.6), deserialized(36.6))

    def test_recursion(self):
        deserialized = self.alias(factorial)
        self.assertEqual(type(factorial), type(deserialized))
        self.assertEqual(factorial(15), deserialized(15))

    def test_args_kwargs(self):
        self.assertEqual(sum_args(10, 20, 30), self.alias(sum_args(10, 20, 30)))

        self.assertEqual(sum_kwargs(a=10, b=20, c=30), self.alias(sum_kwargs(a=10, b=20, c=30)))

        self.assertEqual(sum_args_kwargs(1, 2, 3, a=1, b=2, c=3),
                         self.alias(sum_args_kwargs(1, 2, 3, a=1, b=2, c=3)))


class IterableTestCase(BaseJsonTestCase):
    def test_generator(self):
        deserialized = self.alias(generator())
        self.assertEqual(type(generator()), type(deserialized))
        self.assertEqual(sum(generator()), sum(deserialized))

    def test_generator_function(self):
        deserialized = self.alias(generator)
        self.assertEqual(type(generator()), type(deserialized()))
        self.assertEqual(sum(generator()), sum(deserialized()))

    def test_subgenerator(self):
        deserialized = self.alias(subgenerator())
        self.assertEqual(type(subgenerator()), type(deserialized))
        self.assertEqual(list(subgenerator()), list(deserialized))

    def test_generator_expression(self):
        deserialized = self.alias(generator_expression)
        self.assertEqual(type(generator_expression), type(deserialized))
        self.assertEqual(45, sum(deserialized))

    def test_iterator(self):
        deserialized = self.alias(it)
        self.assertEqual(45, sum(deserialized))


class ClassesTestCase(BaseJsonTestCase):
    def test_multiple_inheritance(self):
        deserialized = self.alias(C())
        self.assertEqual(str(type(C())), str(type(deserialized)))
        self.assertEqual(C().info_c(), deserialized.info_c())

    def test_long_inheritance(self):
        deserialized = self.alias(E())
        self.assertEqual(str(type(E())), str(type(deserialized)))
        self.assertEqual(E().info_e(), deserialized.info_e())

    def test_mro(self):
        self.assertEqual(str(C.__mro__), str(self.alias(C).__mro__))
        self.assertEqual(str(E.__mro__), str(self.alias(E).__mro__))

    def test_class_method(self):
        deserialized = self.alias(Human)
        #self.assertEqual(str(Human.get_const), str(deserialized.get_const))
        self.assertEqual(Human.get_const(), deserialized.get_const())

    def test_static_method(self):
        deserialized = self.alias(Human)
        self.assertEqual(type(Human.static), type(deserialized.static))
        self.assertEqual(Human.static(), deserialized.static())

    def test_property(self):
        deserialized = self.alias(Human)

        h1 = Human(18, 'Denis')
        h2 = deserialized(18, 'Denis')
        self.assertEqual(h1.age, h2.age)

        h1.age = 100
        h2.age = 100
        self.assertEqual(h1.age, h2.age)

        del h2.age
        self.assertEqual('name after age deletion', h2._name)
        self.assertEqual(False, hasattr(h2, 'age'))


class ObjectTestCase(BaseJsonTestCase):
    def test_class_object(self):
        attrs = {'age': 18,
                 'name': 'Pavel',
                 'email': 'qwe@asd.ru',
                 'phone': 123456}

        deserialized = self.alias(Profile(**attrs))
        self.assertEqual(str(Profile(**attrs)), str(deserialized))

    def test_property(self):

        human = Human(18, 'Denis')
        deserialized = self.alias(Human(18, 'Denis'))
        self.assertEqual(human.age, deserialized.age)

        human.age = 100
        deserialized.age = 100
        self.assertEqual(human.age, deserialized.age)

        del deserialized.age
        self.assertEqual('name after age deletion', deserialized._name)
        self.assertEqual(False, hasattr(deserialized, 'age'))


class ScopesTestCase(BaseJsonTestCase):
    def test_global(self):
        deserialized = self.alias(func1)
        self.assertEqual(10, deserialized())

    def test_nonlocal(self):
        deserialized = self.alias(func2)
        self.assertEqual(func2(), deserialized())

    def test_built_in(self):
        deserialized = self.alias(func3)
        self.assertEqual(func3([1, 2, 3]), deserialized([1, 2, 3]))

if __name__ == "__main__":
    unittest.main()