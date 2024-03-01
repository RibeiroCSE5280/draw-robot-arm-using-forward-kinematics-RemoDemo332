from vedo import Box, Sphere, Plotter
import numpy as np

def create_segment(length=1, height=0.2, width=0.2, color='gray'):
    """Creates a single rectangular prism segment and stores its dimensions."""
    segment = Box(size=(length, height, width), c=color)
    segment.dimensions = (length, height, width)  # Manually attach dimensions
    return segment

def create_hinge(radius=0.15, color='red'):
    """Creates a single sphere acting as a hinge with a slightly larger radius."""
    return Sphere(r=radius, c=color)

def position_components(segments, hinges):
    """Positions segments and hinges in a line with hinges directly connecting segments."""
    x_offset = 0
    for i, segment in enumerate(segments):
        segment_length = segment.dimensions[0]
        segment.pos(x_offset + segment_length / 2, 0, 0)
        x_offset += segment_length
        if i < len(hinges):
            hinges[i].pos(x_offset, 0, 0)
            x_offset += 0.15

joint_angles = [0, 0, 0]  # Initial angles for the 3 hinges

def update_joint_angles():
    """Updates the joint angles to simulate bending."""
    for i in range(len(joint_angles)):
        joint_angles[i] += 2  # Increment each angle

def apply_forward_kinematics():
    """Applies forward kinematics to position segments based on joint angles."""
    cumulative_angle = 0
    for i, angle in enumerate(joint_angles):
        cumulative_angle += angle
        if i < len(segments) - 1:
            segments[i + 1].rotate(angle=cumulative_angle+5, axis=(0, 0, 1))

def update_hinge_positions():
    for i, hinge in enumerate(hinges):
        if i < len(segments) - 1:
            # Calculate the new position for the hinge based on the segment's length
            segment_length = segments[i].dimensions[0]
            # Assuming segments are initially placed along the x-axis and then rotated.
            end_pos = segments[i].pos() + np.array([segment_length/2, 0, 0])
            # Update hinge position to the calculated end position of the segment
            hinges[i].pos(end_pos)
            
def animate(event):
    print("animate!")
    update_joint_angles()
    apply_forward_kinematics()
    update_hinge_positions()
    plotter.render()

segments = [create_segment(length=1 + i*0.2, color='grey') for i in range(4)]
hinges = [create_hinge(color='orange') for _ in range(3)]
position_components(segments, hinges)

plotter = Plotter()
[plotter.add(obj) for obj in segments + hinges]
plotter.add_callback("Enter", animate)
#plotter.timer_callback("create", dt=50)
plotter.show(interactive=True)
