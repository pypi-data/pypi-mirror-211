from abc \
    import \
    ABC, \
    abstractmethod


class Job (ABC):
    def __init__(self):
        pass

    def __del__(self):
        pass

    @abstractmethod
    def execute_action(self):
        pass

    @abstractmethod
    def help_action(self):
        pass
