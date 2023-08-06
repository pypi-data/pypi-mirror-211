import logging
import time
from orchestration.task import Task


class Orchestrator:
    def __init__(self):
        self.tasks = []

    def add_task(self, cron_expression, script_type):
        task = Task(cron_expression, script_type)
        self.tasks.append(task)
        return task

    def execute_tasks(self):
        for task in self.tasks:
            # Check if the task should be skipped
            if any(skip_condition for skip_condition in task.skips):
                logging.info(f"Skipping task execution...")
                time.sleep(task.interval)
                continue

            if task.should_execute():
                for script in task.scripts:
                    if isinstance(script, tuple) and len(script) == 2:
                        script_path, parameters_list = script
                        task.repeat(script_path, parameters_list)
                    else:
                        task.execute_script(script)
                    time.sleep(task.interval)
            else:
                time.sleep(task.interval)