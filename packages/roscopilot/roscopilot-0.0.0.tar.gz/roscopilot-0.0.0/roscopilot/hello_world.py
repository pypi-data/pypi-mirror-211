from typing import Callable


class HelloWorld(Callable):
    def __call__(self):
        print("Hello World!")
