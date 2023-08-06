from jobs.jobs \
    import Job


class Buffer:
    def __init__(self):
        self.buffer_queue: list = []

    def get_length(self) -> int:
        return len(
            self.buffer_queue
        )

    def get_buffer_queue(self) -> list:
        return self.buffer_queue

    def set_buffer_queue(
            self,
            value: list
    ) -> None:
        self.buffer_queue = value

    def insert_value(
            self,
            value: Job
    ):
        self.buffer_queue\
            .append(
                value
            )

    def get_value_by_index(
            self,
            value: int
    ) -> Job:
        return self.buffer_queue[
            value
        ]

    def delete_value_at_index(
            self,
            value: int
    ) -> bool:
        return_value = False

        # Out of range
        if self.get_length() < value:
            return return_value

        self.buffer_queue\
            .pop(value)

        # Successful
        return_value = not return_value
        return return_value
