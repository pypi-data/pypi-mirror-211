from prism.task import PrismTask
import prism.target as PrismTarget

class Module06(prism.task.PrismTask):

    def run(self, tasks, hooks):
        return tasks.ref('module05.py') + "This is module 06. "


# EOF