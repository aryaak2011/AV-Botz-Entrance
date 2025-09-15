import cv2
import numpy as np
import math

image = cv2.imread(r"C:\Users\manju\Coding Projects\Extras\AV Botz\torpBoard2.png")

# Convert to HSV for white detection
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower_white = np.array([0, 0, 200])
upper_white = np.array([180, 50, 255])
white_mask = cv2.inRange(hsv, lower_white, upper_white)

# Clean up mask
kernel = np.ones((5, 5), np.uint8)
white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_CLOSE, kernel)

# Find contours
contours, _ = cv2.findContours(white_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key=cv2.contourArea, reverse=True)

# Find 4-corner white contour
board_vertices = []
for contour in contours:
    area = cv2.contourArea(contour)
    if area < 1000:
        continue
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)
    if len(approx) == 4:
        board_vertices = [tuple(map(int, pt[0])) for pt in approx]
        break

print(board_vertices)
cx = int(sum(x for x, y in board_vertices) / 4)
cy = int(sum(y for x, y in board_vertices) / 4)

p1 = board_vertices[0]
p2 = board_vertices[1]
p3 = board_vertices[2]
p4 = board_vertices[3]

def slope(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    if x2 == x1:
        return None  # Vertical line: infinite slope
    return (y2 - y1) / (x2 - x1)

m1 = slope(p1, p2)
m2 = slope(p3, p4)

# Handle vertical lines
if m1 is None and m2 is None:
    print("None")  # both vertical → angle 0
elif m1 is None:
    angle_rad = math.atan(abs(1 / m2))
elif m2 is None:
    angle_rad = math.atan(abs(1 / m1))
else:
    tan_theta = abs((m2 - m1) / (1 + m1 * m2))
    angle_rad = math.atan(tan_theta)

angle_deg = math.degrees(angle_rad)

print(cx,cy, angle_deg)