class Pipeline:
    def __init__(self):
        self._steps = []

    def add_step(self, step):
        self._steps.append(step)
        return self # so add_step() can be chained

    def run(self, initial_data:str):
        current_data = initial_data
        for step in self._steps:
            current_data = step.execute(current_data)
        return current_data

    def __add__(self, other):
        if isinstance(other, Pipeline):
            self._steps += other._steps
            return self
        raise Warning(f"cannot add {type(self)} and {type(other)}")