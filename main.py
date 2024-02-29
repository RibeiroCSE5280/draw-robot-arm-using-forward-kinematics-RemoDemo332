from vedo import Box, Sphere, Plotter, show
import numpy as np

class RoboticArmSegment:
    def __init__(self, length=1.0, height=0.1, width=0.1, color='gray', initial_pos=(0, 0, 0)):
        self.length = length
        self.width = width
        self.height = height
        self.color = color
        self.segment_body = Box(pos=initial_pos, size=(length, width, height)).color(color)
        self.rotation_matrix = np.eye(3)  # Initialize rotation matrix as identity matrix

    def get_end_pos(self):
        # Calculate the end position of the segment based on its current position and length
        return self.segment_body.pos() + np.dot(self.rotation_matrix, np.array([self.length/2, 0, 0]))

# Function to create rotation matrix for the z-axis
def rotation_matrix_z(angle):
    cos_angle, sin_angle = np.cos(angle), np.sin(angle)
    return np.array([[cos_angle, -sin_angle, 0],
                     [sin_angle, cos_angle, 0],
                     [0, 0, 1]])

# Animation function using forward kinematics
def animate_arm(segments, joint_angles, joint_spheres):
    prev_rotation_matrix = np.eye(3)  # Initialize previous rotation matrix as identity matrix
    for i, (segment, joint_sphere) in enumerate(zip(segments, joint_spheres)):
        # Calculate the transformation matrix for each segment based on joint angle
        rotation_matrix = rotation_matrix_z(joint_angles[i])
        segment.rotation_matrix = np.dot(prev_rotation_matrix, rotation_matrix)

        # Update segment position relative to the joint sphere
        translation = np.dot(segment.rotation_matrix, np.array([segment.length, 0, 0]))
        new_pos = joint_sphere.pos() + translation

        # Update segment position
        segment.segment_body.pos(new_pos)

        # Update joint sphere position
        if i < len(joint_spheres) - 1:
            joint_spheres[i + 1].pos((joint_sphere.pos() + segments[i + 1].segment_body.pos()) / 2)
        
        prev_rotation_matrix = segment.rotation_matrix

# Initialize segments with different colors and positions
colors = ['red', 'green', 'blue', 'yellow']
initial_positions = [(0, 0, 0), (1.0, 0, 0), (2.0, 0, 0), (3.0, 0, 0)]
segments = [RoboticArmSegment(length=1, height=0.2, width=0.2, color=colors[i], initial_pos=initial_positions[i]) for i in range(4)]

# Create joint spheres
joint_spheres = [Sphere(pos=segments[i].segment_body.pos() - np.dot(segments[i].rotation_matrix, np.array([segments[i].length/2, 0, 0])), r=0.15, c='red') for i in range(len(segments))]

# Initialize joint angles
joint_angles = [0 for _ in segments]

# Create base and set its position
base = Box(pos=(-0.65, 0, 0), size=(0.1, 0.5, 0.5), c='white')

# Create Plotter object and add the base and segments
plotter = Plotter()
plotter += base
for segment, sphere in zip(segments, joint_spheres):
    plotter += segment.segment_body
    plotter += sphere

# Animation loop
for angle in np.linspace(0, np.pi/8, 360):
    # Update joint angles for animation
    joint_angles = [angle for _ in joint_angles]
    
    # Animate the arm
    animate_arm(segments, joint_angles, joint_spheres)

    # Render and pause to control animation speed
    plotter.show(interactive=False)
    plotter.clear()
    plotter += base
    for segment in segments:
        plotter += segment.segment_body
    plotter += joint_spheres

show(plotter, interactive=True)
