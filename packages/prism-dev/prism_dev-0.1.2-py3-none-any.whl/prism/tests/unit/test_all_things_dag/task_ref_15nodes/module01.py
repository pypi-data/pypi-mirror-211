from prism.task import PrismTask
import prism.target as PrismTarget

class Module01(prism.task.PrismTask):

    def run(self, tasks, hooks):
        return "This is module 01. "


# EOF