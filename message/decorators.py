from serilizer.base import BaseSerializer


def message_decorator(message_code: int, message_serializer: BaseSerializer):

    def wrapper(f):

        def inner_wrapper(args, kwargs):
            return f()

        return inner_wrapper

    return wrapper
