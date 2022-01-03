import serializer


class CommandEvent(serializer.BaseSerializer):

    code: int = serializer.Int32()
    balance: float = serializer.Float32()
    status: int = serializer.Int32()
    name: str = serializer.String(length=10)
    flag: bool = serializer.Bool()


class Account(serializer.BaseSerializer):

    account: int = serializer.UInt32()
    balance: float = serializer.Float32()


def main():

    event = CommandEvent()
    event.name = "Hello"
    event.flag = True
    print(event.get_data())

    acc = Account()
    acc.account = 1233213
    acc.balance = 0.212
    print(acc.get_data())


if __name__ == '__main__':
    main()
