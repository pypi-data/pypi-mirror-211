import logging

from risingplugin import getCompletion

# logging.basicConfig(level=logging.INFO)


def demo():
    result = getCompletion("Where is the River Nile?", "gpt-3.5-turbo", "", True)
    print('result===============', result)


if __name__ == "__main__":
    demo()
