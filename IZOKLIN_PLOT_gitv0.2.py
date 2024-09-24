import numpy as np
import matplotlib.pyplot as plt

# Define the differential equation
def slope_field(x, y):
    return (y-x)/(y**2+1)

# Set up the grid for x and y values
x_vals = np.linspace(-4, 4, 40)
y_vals = np.linspace(-4, 4, 40)

X, Y = np.meshgrid(x_vals, y_vals)

# Calculate the slopes at each point
U = 1
V = slope_field(X, Y)

# Normalize the direction for plotting
N = np.sqrt(U**2 + V**2)
U2, V2 = U / N, V / N

# Calculate the angle of each vector for coloring
angles = np.arctan2(V2, U2)

# Normalize angles to [0, 1]
angles_normalized = (angles + np.pi) / (2 * np.pi)

# Parameters for customization
num_isoclines = 5  # Number of non-main isoclines
hue_shift = 0.2    # Amount of hue shift (0 to 1)

# Apply hue shift
angles_shifted = (angles_normalized + hue_shift) % 1  # Shift hue

# Create the plot
plt.figure(figsize=(8, 8))

# Use a colormap
cmap = plt.get_cmap('hsv')

# Plot the direction field with color representing the slope (angle)
quiver = plt.quiver(X, Y, U2, V2, angles_shifted, angles="xy", scale=None, cmap=cmap)

# Add color bar for the angle coloring
plt.colorbar(quiver, label="Direction (angle in radians)")

# Add isoclines for horizontal (slope = 0) and vertical (slope -> infinity)
Z = V2 / U2  # Calculate the slope at each point

# Manually add levels for horizontal and vertical directions
levels = np.linspace(Z.min(), Z.max(), num_isoclines)

# Add level for horizontal direction (slope = 0) and sort levels
if 0 not in levels:
    levels = np.append(levels, 0)
levels = np.sort(levels)

# Plot contour lines including the manually added levels
contours = plt.contour(X, Y, Z, levels=levels, colors='black')
plt.clabel(contours, inline=True, fontsize=8)

plt.title("Slope Field with Customizable Isoclines")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()
