from globals.constants \
    import \
    zero,\
    one


class Counter:
    def __init__(self):
        self.value: int = zero()

    def increment(self):
        self.increase(
            one()
        )

    def decrement(self):
        self.decrease(
            one()
        )

    def reset(self):
        self.set_value(
            zero()
        )

    def increase(
            self,
            by_value: int
    ):
        self.set_value(
            self.get_value() + by_value
        )

    def decrease(
            self,
            by_value: int
    ):
        self.set_value(
            self.get_value() - by_value
        )

    def get_value_as_string(self) -> str:
        return str(
            self.get_value()
        )

    def get_value(self) -> int:
        return self.value

    def set_value(
            self,
            value: int
    ) -> None:
        self.value = value
