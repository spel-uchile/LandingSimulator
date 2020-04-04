
from ..Abstract.ComponentBase import ComponentBase
from Interface.SpacecraftInOut.SCIDriver import SCIDriver


class OBC(ComponentBase):
    def __init__(self, port_id, properties):
        ComponentBase.__init__(self, 1)
        self.port_id = port_id
        self.properties = properties

    def get_current(self):
        if self.isOn:
            return 0.1
        return 0.0


