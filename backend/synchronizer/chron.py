from datetime import datetime, timedelta
from typing import Callable

from sqlalchemy.orm import Session

class Chron:
    """
    Chron
    Dedicated class to schedule the run of each data-type synchrinisation.

    constructor
        initializes the chron so jobs can be pushed

        :param campus_id int the campus ID that will be used to fetch all data
        :param cursus_id int the cursus ID that will be used to fetch all data
        :param default_last_run datetime date that will be used by default
    """
    def __init__(self, campus_id: int, cursus_id: int, default_last_run: datetime) -> None:
        self.campus_id: int = campus_id
        self.cursus_id: int = cursus_id
        self.default_last_run: datetime = default_last_run
        self.jobs: dict = {}

    def clear_run_history(self) -> None:
        """
        clear_run_history

        erases all run history, useful when data could be lost
        and refetch is needed
        """
        for job_properties in self.jobs.values():
            job_properties["last_run"] = self.default_last_run

    def add_job(self,
            job: Callable,
            days: int = 0,
            hours: int = 0,
            minutes: int = 0,
            seconds: int = 0,
            primary_object: bool = False
        ) -> None:
        """
        add_job

        builds a job that will be used on the #execute method,
        requires an interval, and needs to know if is primary_object

        The interval is added, 1 day and 1 minute means 86460 seconds

        A primary_object is a job that is not dependant and requires
        to know the campus_id and cursus_id associated with them

        :param days int interval of days
        :param hours int interval of hours
        :param minutes int interval of minutes
        :param seconds int interval of seconds
        :param primary_object bool callable have cursus_id and campus_id
        """
        interval = days * 86400 + hours * 3600 + minutes * 60 + seconds
        self.jobs[job] = {
            "interval": interval,
            "primary_object": primary_object,
            "last_run": datetime(1970, 1, 1) if primary_object else self.default_last_run
        }

    def execute(self, session: Session) -> datetime:
        """
        execute

        iterates through all jobs and runs the ones that passed
        their specified interval

        redefines each of them "last_run" property giving them
        a time error margin of the execution time span

        :param session session session to use for the database
        :return datetime elapsed span of time the task took
        """
        execute_begin = datetime.utcnow()
        for call, props in self.jobs.items():
            if props["last_run"] + timedelta(seconds=props["interval"]) > execute_begin:
                continue
            print(f"[synchronizer] Executing '{call.__name__}' on {execute_begin}")
            if props["primary_object"]:
                call(session, props["last_run"], self.cursus_id, self.campus_id)
            else:
                call(session, props["last_run"])
            session.commit()
            print(f"[synchronizer] Finished '{call.__name__}' on {execute_begin}\n")
            props["last_run"] = execute_begin - (execute_begin - datetime.utcnow())
        return execute_begin - datetime.utcnow()
