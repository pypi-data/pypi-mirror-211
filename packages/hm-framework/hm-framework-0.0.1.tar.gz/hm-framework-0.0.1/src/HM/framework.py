from setup.configuration.variables \
    import \
    setup_of_default_variables, \
    clean

from jobs.workflows \
    import Workflow

from jobs.jobs \
    import Job


class AutomationFramework:
    def __init__(self):
        setup_of_default_variables()
        self.workflow = Workflow()

    def __del__(self):
        self.finish()
        clean()

    def setup(self):
        pass

    def execute(self):
        pass

    def finish(self):
        pass

    def append_job(
            self,
            job: Job
    ) -> None:
        self.workflow           \
            .buffer             \
            .insert_value(
                job
            )

    def get_job(
            self,
            value: int
    ) -> Job | int | None:
        return self.workflow\
                   .buffer\
                   .get_value_by_index(
                        value
                   )

    def delete_job(
            self,
            value: int
    ) -> bool:
        return self.workflow\
                   .buffer\
                   .delete_value_at_index(
                        value
                   )
