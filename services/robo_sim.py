from robodk.robolink import *
from robodk.robomath import *

# Any interaction with RoboDK must be done through RDK:
RDK = Robolink()

# Select a robot (popup is displayed if more than one robot is available)
robot = RDK.ItemUserPick('Select a robot', ITEM_TYPE_ROBOT)
if not robot.Valid():
    raise Exception('No robot selected or available')

# Get the current position of the TCP with respect to the reference frame:
# (4x4 matrix representing position and orientation)
target_ref = robot.Pose()
pos_ref = target_ref.Pos()
print("Drawing a square around the target: ")
print(Pose_2_TxyzRxyz(target_ref))

# Move the robot to the first point:
robot.MoveJ(target_ref)

# It is important to provide the reference frame and the tool frames when generating programs offline
robot.setPoseFrame(robot.PoseFrame())
robot.setPoseTool(robot.PoseTool())
robot.setRounding(10)  # Set the rounding parameter
robot.setSpeed(5)   # Set linear speed in mm/s

# Set the number of sides of the polygon (for a square, it's 4):
n_sides = 5
side_length = 500  # 3 cm in mm


def draw_box(edges):
    print("edges : ", edges)
    # RDK.Command("Trace","on")

    for edge in edges:
        target_i = Mat(target_ref)
        pos_i = target_i.Pos()
        # print("target_i", target_i)
        # print("pos_i before change :",pos_i)

        pos_i[0] = pos_i[0] + edge[0]
        pos_i[1] = pos_i[1] + edge[1]
        pos_i[2] = pos_i[2] - 200


        target_i.setPos(pos_i)
        # print("Moving to target %i: angle %.1f" % (i, ang * 180 / pi))
        # print(str(Pose_2_TxyzRxyz(target_i)))
        robot.MoveL(target_i)

    target_i = Mat(target_ref)
    pos_i = target_i.Pos()
    pos_i[0] = pos_i[0] + edges[0][0]
    pos_i[1] = pos_i[1] + edges[0][1]
    pos_i[2] = pos_i[2] -200
    target_i.setPos(pos_i)
    robot.MoveL(target_i)

    robot.MoveL(target_ref)
    # RDK.Command("Trace","off")



if __name__ == "__main__":
    edges = [
        [0,0],
        [250,0],
        [250,550],
        [0,550]
    ]
    draw_box(edges)
    # print('Done')
