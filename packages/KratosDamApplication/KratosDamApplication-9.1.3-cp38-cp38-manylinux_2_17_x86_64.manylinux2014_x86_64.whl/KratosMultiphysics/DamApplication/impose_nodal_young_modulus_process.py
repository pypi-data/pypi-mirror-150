from KratosMultiphysics import *
from KratosMultiphysics.DamApplication import *

## In this case, the scalar value is automatically fixed.

def Factory(settings, Model):
    if not isinstance(settings, Parameters):
        raise Exception("expected input shall be a Parameters object, encapsulating a json string")
    return ImposeNodalYoungModulusProcess(Model, settings["Parameters"])

class ImposeNodalYoungModulusProcess(Process):

    def __init__(self, Model, settings ):

        Process.__init__(self)
        model_part = Model[settings["model_part_name"].GetString()]
        settings.AddEmptyValue("is_fixed").SetBool(True)

        self.process = DamNodalYoungModulusProcess(model_part, settings)


    def ExecuteInitialize(self):

        self.process.ExecuteInitialize()

    def ExecuteInitializeSolutionStep(self):

        self.process.ExecuteInitializeSolutionStep()
