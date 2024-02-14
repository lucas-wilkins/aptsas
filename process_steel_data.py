from loadpos import PosData
from assignment import Assigner

data = PosData("data/R5083_23208-v01-roi_tempered.pos")

print(data)

# data.show_sample()

assigner = Assigner("data/S390_steel.rrng")

print(assigner)