from jobs.buffers \
    import Buffer


class Workflow:
    def __init__(self):
        self.buffer = Buffer()

    def get_buffer(self) -> Buffer:
        return self.buffer

    def set_buffer(
            self,
            value: Buffer
    ) -> None:
        self.buffer = value

    def size(self):
        return self.get_buffer() \
                   .get_length()
