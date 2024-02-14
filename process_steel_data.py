from loadpos import PosData
from assignment import Assigner

# data = PosData("data/R5083_23208-v01-roi_tempered.pos")
data = PosData("data/R5083_22972-v01_austenited.pos")

print(data)

data.show_sample()

assigner = Assigner("data/S390_steel.rrng")

print(assigner)

assignment = assigner.assign(data)

print(assignment)

# assignment.ion_plot("Fe")
assignment.ion_plots()