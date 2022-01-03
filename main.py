import serilizer


class CommandEvent(serilizer.BaseSerializer):

    code: int = serilizer.Int32()
    balance: float = serilizer.Float32()
    status: int = serilizer.Int32()
    name: str = serilizer.String(length=10)
    flag: bool = serilizer.Bool()


class Account(serilizer.BaseSerializer):

    account: int = serilizer.UInt32()
    balance: float = serilizer.Float32()


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
