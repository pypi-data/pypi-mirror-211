from typing import Any

class Extend:
    def __init__(self, cls, method):
        # Gets the name of the method
        method_name = method.__name__

        # Gets the previous method of the cls
        self._previous_method = getattr(cls, method_name, False)

        # Sets the method to the cls
        setattr(cls, method_name, method)
        
        # Sets the cls and method name as attrs
        self._cls = cls
        self._method_name = method_name

    def __call__(self, *args, **kwargs) -> Any:
        """Triggered when the object is called.

        Returns:
            Any: Any object of any class that was inputed to the Extension.
        """
        return self._cls(*args, **kwargs)

    def __enter__(self) -> Any:
        """Triggered when the object is entered. As in with statement.

        Returns:
            Any: Any object of any class that was inputed to the Extension.
        """
        return self._cls

    def __exit__(self, type, value, traceback) -> None:
        """called when exiting the with statement.
            When exiting the with statement, a overwritten method is returned to the original state.
            And an added method is removed.
        """
        if self._previous_method:
            setattr(self._cls, self._method_name, self._previous_method)
        else:
            delattr(self._cls, self._method_name)

if __name__ == "__main__":
    class C:
        def __init__(self, a) -> None:
            self._a = a

        def test(self):
            return "TEST"

    def test(self):
        return "TEST" + str(self._a)

    c = C(6)
    with Extend(C, test):
        print(c.test()) # TEST6
