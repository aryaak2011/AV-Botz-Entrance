import math

# --- Placeholder Functions and Classes to simulate the submarine environment ---
# This class represents the state of the submarine and includes the mock functions
# provided in the mission details. In a real-world scenario, these would
# be replaced by actual hardware control and sensor reading functions.

class Submarine:
    def __init__(self):
        # Initial state of the sub: [x, y, z, yaw, pitch, roll]
        self.state = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # Coordinates of the mission objects for simulation purposes
        self.torpBoard_coords = (12.0, 2.0, -5.0)  # x, y, z
        self.hole1_coords = (12.0, 2.5, -4.5)     # x, y, z
        self.hole2_coords = (12.0, 1.5, -5.5)     # x, y, z

    def setForward(self, x):
        """Tells the sub to move forward x meters (negative x goes backwards)."""
        print(f"Setting forward movement by {x} meters...")
        self.state[0] += x * math.cos(math.radians(self.state[3]))
        self.state[1] += x * math.sin(math.radians(self.state[3]))

    def setHorizontal(self, y):
        """Tells the sub to move right y meters (negative y goes left)."""
        print(f"Setting horizontal movement by {y} meters...")
        self.state[0] += y * math.cos(math.radians(self.state[3] + 90))
        self.state[1] += y * math.sin(math.radians(self.state[3] + 90))

    def setAngle(self, a):
        """Tells the sub to yaw left or right (positive yaws right, negative yaws left)."""
        print(f"Setting yaw angle by {a} degrees...")
        self.state[3] += a

    def setDepth(self, z):
        """Sets the depth of the submarine to z meters deep."""
        print(f"Setting depth to {z} meters...")
        self.state[2] = z

    def getState(self):
        """Returns the state of the sub: [x, y, z, yaw, pitch, roll]."""
        return self.state

    def move(self, x, y, z, yaw, pitch, roll):
        """Tells the sub to move to the desired absolute coordinates."""
        print(f"Moving to absolute coordinates: x={x}, y={y}, z={z}, yaw={yaw}, pitch={pitch}, roll={roll}")
        self.state = [x, y, z, yaw, pitch, roll]

    def findDistance(self, obj_name, dim1, dim2):
        """
        Returns the 2D distance to the object.
        Dimensions must be 'x', 'y', or 'z'.
        Objects must be 'torpBoard', 'hole1', or 'hole2'.
        """
        current_coords = self.state[0:3]
        if obj_name == 'torpBoard':
            target_coords = self.torpBoard_coords
        elif obj_name == 'hole1':
            target_coords = self.hole1_coords
        elif obj_name == 'hole2':
            target_coords = self.hole2_coords
        else:
            return 9999.0 # Placeholder for invalid object

        dims = {'x': 0, 'y': 1, 'z': 2}
        dim1_index = dims.get(dim1.lower())
        dim2_index = dims.get(dim2.lower())

        if dim1_index is None or dim2_index is None:
            return 9999.0 # Invalid dimensions

        dx = target_coords[dim1_index] - current_coords[dim1_index]
        dy = target_coords[dim2_index] - current_coords[dim2_index]

        return math.sqrt(dx**2 + dy**2)

    def align_yaw(self, obj_name):
        """
        Returns the relative yaw angle (-90 to 90) to center the object
        horizontally in the camera feed. Returns -999 if not found.
        Includes a 20% inaccuracy margin.
        """
        print(f"Finding yaw angle to align with {obj_name}...")
        current_yaw = self.state[3]
        current_x, current_y, _ = self.state[0:3]
        
        if obj_name == 'torpBoard':
            target_x, target_y, _ = self.torpBoard_coords
        elif obj_name == 'hole1':
            target_x, target_y, _ = self.hole1_coords
        elif obj_name == 'hole2':
            target_x, target_y, _ = self.hole2_coords
        else:
            return -999.0

        delta_x = target_x - current_x
        delta_y = target_y - current_y

        # Calculate absolute angle to target
        angle_to_target = math.degrees(math.atan2(delta_y, delta_x))

        # Calculate relative yaw angle from current sub's orientation
        relative_yaw = angle_to_target - current_yaw
        
        # Normalize to -180 to 180 range
        if relative_yaw > 180:
            relative_yaw -= 360
        elif relative_yaw < -180:
            relative_yaw += 360

        # Simulate vision inaccuracy
        inaccuracy = relative_yaw * 0.2
        return relative_yaw + inaccuracy

    def align_pitch(self, obj_name):
        """
        Returns the relative pitch angle (-90 to 90) to center the object
        vertically in the camera feed. Returns -999 if not found.
        Includes a 20% inaccuracy margin.
        """
        print(f"Finding pitch angle to align with {obj_name}...")
        current_x, _, current_z = self.state[0:3]

        if obj_name == 'torpBoard':
            target_x, _, target_z = self.torpBoard_coords
        elif obj_name == 'hole1':
            target_x, _, target_z = self.hole1_coords
        elif obj_name == 'hole2':
            target_x, _, target_z = self.hole2_coords
        else:
            return -999.0

        delta_x = target_x - current_x
        delta_z = target_z - current_z
        
        # Calculate relative pitch angle
        relative_pitch = math.degrees(math.atan2(delta_z, delta_x))

        # Simulate vision inaccuracy
        inaccuracy = relative_pitch * 0.2
        return relative_pitch + inaccuracy

    def orientAtDistance(self, angle):
        """
        Orients the sub to the input angle while remaining at the same relative
        X distance from the torp board.
        """
        print(f"Orienting sub to {angle} degrees at current relative X distance...")
        current_x_rel = self.torpBoard_coords[0] - self.state[0]
        current_y_rel = self.torpBoard_coords[1] - self.state[1]

        # Calculate absolute distance to board
        distance_to_board = math.sqrt(current_x_rel**2 + current_y_rel**2)

        # Calculate new absolute coordinates based on the new yaw angle
        new_x = self.torpBoard_coords[0] - distance_to_board * math.cos(math.radians(angle))
        new_y = self.torpBoard_coords[1] - distance_to_board * math.sin(math.radians(angle))
        
        # Update the state
        self.state[0] = new_x
        self.state[1] = new_y
        self.state[3] = angle

    def shootTorpedo1(self):
        """Shoots the first torpedo."""
        print("Shooting torpedo 1!")
    
    def shootTorpedo2(self):
        """Shoots the second torpedo."""
        print("Shooting torpedo 2!")
    
    def offsetToTorpedoes(self):
        """Offsets the sub so that the torpedoes will be in front of the hole instead of the camera."""
        # This function would be calibrated to the physical offset of the torpedo tubes.
        # For simulation, we'll assume a small forward movement to clear the camera.
        print("Offsetting sub to align torpedo tubes...")
        self.setForward(0.2)
        
# --- Mission Code ---

def mission_script(sub):
    """
    Guides the sub to align with the torpedo board, find the holes,
    and shoot torpedoes through them.
    """
    
    # Define a small tolerance for alignment loops
    YAW_TOLERANCE = 0.5  # degrees
    PITCH_TOLERANCE = 0.5  # degrees
    DISTANCE_TOLERANCE = 0.5 # meters
    SHOOTING_DISTANCE = 2.0  # meters

    print("--- Beginning Mission: Torpedo Task ---")
    print(f"Initial State: {sub.getState()}")
    
    # --- Phase 1: Navigate to the Torpedo Board and become perpendicular ---
    
    # Find the current horizontal distance to the board
    current_xy_distance = sub.findDistance('torpBoard', 'x', 'y')
    print(f"Initial horizontal distance to torp board: {current_xy_distance} meters")
    
    # Get the required angle to become perpendicular with the torp board
    # My "Function from Part 1" logic: align with the board and then turn 90 degrees.
    # The orientAtDistance function handles this in one step by setting the new yaw.
    # We'll use the align_yaw function and then add 90 degrees to become perpendicular.
    
    # Calculate the angle to face the torp board
    yaw_to_align_with_board = sub.align_yaw('torpBoard')
    print(f"Calculated yaw to face torp board: {yaw_to_align_with_board} degrees")
    
    # Calculate the perpendicular angle (90 degrees to the right for this example)
    perpendicular_angle = sub.getState()[3] + yaw_to_align_with_board + 90
    
    # Orient the sub to be perpendicular with the torp board at the current distance
    print(f"Orienting perpendicular to the torp board at yaw {perpendicular_angle}...")
    sub.orientAtDistance(perpendicular_angle)
    
    # Re-align yaw multiple times for accuracy
    perpendicular_adjustment_yaw = sub.align_yaw('torpBoard')
    while abs(perpendicular_adjustment_yaw) > YAW_TOLERANCE:
        sub.setAngle(perpendicular_adjustment_yaw)
        perpendicular_adjustment_yaw = sub.align_yaw('torpBoard')
        
    print("Perpendicular alignment to torp board achieved.")
    
    # Move forward until within shooting distance of the board
    current_distance = sub.findDistance('torpBoard', 'x', 'y')
    while current_distance > SHOOTING_DISTANCE:
        forward_movement = (current_distance - SHOOTING_DISTANCE) * 0.5 # Move a fraction of the remaining distance
        sub.setForward(forward_movement)
        current_distance = sub.findDistance('torpBoard', 'x', 'y')
        # Re-check yaw and pitch during approach to maintain alignment
        yaw_adjustment = sub.align_yaw('torpBoard')
        if abs(yaw_adjustment) > YAW_TOLERANCE:
            sub.setAngle(yaw_adjustment)
            
    print(f"Sub is within shooting range at {current_distance} meters.")
    
    # Determine the correct depth for shooting
    print("Finding optimal shooting depth...")
    pitch_to_align_depth = sub.align_pitch('torpBoard')
    while abs(pitch_to_align_depth) > PITCH_TOLERANCE:
        # Using trigonometry: tan(pitch) = relative_z / relative_x
        current_x_rel = sub.torpBoard_coords[0] - sub.getState()[0]
        relative_z = current_x_rel * math.tan(math.radians(pitch_to_align_depth))
        
        # Set the new depth to the current depth plus the calculated relative Z
        new_depth = sub.getState()[2] + relative_z
        sub.setDepth(new_depth)
        
        pitch_to_align_depth = sub.align_pitch('torpBoard')
        
    print(f"Optimal depth of {sub.getState()[2]} meters achieved.")
    
    # --- Phase 2: Align with Hole 1 and shoot ---
    
    print("\n--- Aligning with Hole 1 ---")
    
    # Align yaw to Hole 1 with a loop for accuracy
    yaw_to_hole1 = sub.align_yaw('hole1')
    while abs(yaw_to_hole1) > YAW_TOLERANCE:
        sub.setAngle(yaw_to_hole1)
        yaw_to_hole1 = sub.align_yaw('hole1')
        
    # Align pitch to Hole 1 with a loop for accuracy
    pitch_to_hole1 = sub.align_pitch('hole1')
    while abs(pitch_to_hole1) > PITCH_TOLERANCE:
        current_x_rel = sub.torpBoard_coords[0] - sub.getState()[0]
        relative_z = current_x_rel * math.tan(math.radians(pitch_to_hole1))
        new_depth = sub.getState()[2] + relative_z
        sub.setDepth(new_depth)
        pitch_to_hole1 = sub.align_pitch('hole1')
        
    print("Hole 1 alignment complete.")
    
    # Offset and shoot
    sub.offsetToTorpedoes()
    sub.shootTorpedo1()
    
    # --- Phase 3: Align with Hole 2 and shoot ---
    
    print("\n--- Aligning with Hole 2 ---")
    
    # Align yaw to Hole 2 with a loop for accuracy
    yaw_to_hole2 = sub.align_yaw('hole2')
    while abs(yaw_to_hole2) > YAW_TOLERANCE:
        sub.setAngle(yaw_to_hole2)
        yaw_to_hole2 = sub.align_yaw('hole2')
        
    # Align pitch to Hole 2 with a loop for accuracy
    pitch_to_hole2 = sub.align_pitch('hole2')
    while abs(pitch_to_hole2) > PITCH_TOLERANCE:
        current_x_rel = sub.torpBoard_coords[0] - sub.getState()[0]
        relative_z = current_x_rel * math.tan(math.radians(pitch_to_hole2))
        new_depth = sub.getState()[2] + relative_z
        sub.setDepth(new_depth)
        pitch_to_hole2 = sub.align_pitch('hole2')
        
    print("Hole 2 alignment complete.")

    # Offset and shoot
    sub.offsetToTorpedoes()
    sub.shootTorpedo2()
    
    print("\n--- Mission Complete! ---")
    print(f"Final State: {sub.getState()}")

# Main execution block
if __name__ == "__main__":
    submarine = Submarine()
    mission_script(submarine)