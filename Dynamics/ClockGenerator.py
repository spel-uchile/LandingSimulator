

class ClockGenerator(object):
    def __init__(self, subsystems, systems_names):
        self.timer_count = 0
        self.subsystems = subsystems
        self.systems_names = systems_names

    def remove_component(self, subsystem, components):
        return

    def tick_to_components(self):
        for subsysname in self.systems_names:
            subsystem = self.subsystems[subsysname]
            if subsystem is not None:
                subsystem.tick(self.timer_count)
        self.timer_count += 1
