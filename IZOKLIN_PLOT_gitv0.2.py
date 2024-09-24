import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


# Define the differential equation symbolically
def solve_implicit_ode(equation, x, y, dy):
    """
    Solves an implicit ODE of the form F(x, y, dy) = 0 for dy.

    Args:
    equation : sympy expression - The implicit ODE F(x, y, dy).
    x        : sympy symbol - The independent variable (usually x).
    y        : sympy symbol - The dependent variable (usually y).
    dy       : sympy symbol - The derivative of y w.r.t. x (dy/dx).

    Returns:
    sol : sympy expression - The solution for dy.
    """
    # Solve the equation for dy
    solution = sp.solve(equation, dy)

    # Return the first solution (or you can modify to handle multiple solutions)
    return solution[0] if solution else None


# Example: User inputs an implicit equation (dy + y - x = 0)
x, y, dy = sp.symbols('x y dy')
implicit_equation = y*(dy+x)-1 #(x - dy)**3 - dy - y #

# Solve it for dy (dy/dx)
solved_ode = solve_implicit_ode(implicit_equation, x, y, dy)
print(f"Explicit ODE: dy/dx = {solved_ode}")

# Convert symbolic solution to a numerical function
solved_ode_func = sp.lambdify((x, y), solved_ode, "numpy")

# Set up the grid for x and y values
x_vals = np.linspace(-4, 4, 40)
y_vals = np.linspace(-4, 4, 40)

X, Y = np.meshgrid(x_vals, y_vals)

# Calculate the slopes using the solved ODE
U = 1  # x-direction is always 1
V = solved_ode_func(X, Y)  # y-direction is determined by the ODE

# Normalize the direction for plotting
N = np.sqrt(U ** 2 + V ** 2)
U2, V2 = U / N, V / N

# Calculate the angle of each vector for coloring
angles = np.arctan2(V2, U2)

# Normalize angles to [0, 1]
angles_normalized = (angles + np.pi) / (2 * np.pi)

# Parameters for customization
num_isoclines = 5  # Number of non-main isoclines
hue_shift = 0.0  # Amount of hue shift (0 to 1)

# Apply hue shift
angles_shifted = (angles_normalized + hue_shift) % 1  # Shift hue

# Create the plot
fig, ax = plt.subplots(figsize=(10, 10))  # Set a large square figure

# Use a colormap
cmap = plt.get_cmap('hsv')

# Plot the direction field with color representing the slope (angle)
quiver = plt.quiver(X, Y, U2, V2, angles_shifted, angles="xy", scale=None, cmap=cmap)

# Add color bar for the angle coloring
plt.colorbar(quiver, label="Direction (normalized)")

# Add isoclines for horizontal (slope = 0) and vertical (slope -> infinity)
Z = V2 / U2  # Calculate the slope at each point

# Manually add levels for horizontal and vertical directions
levels = np.linspace(Z.min(), Z.max(), num_isoclines)

# Add level for horizontal direction (slope = 0) and sort levels
if 0 not in levels:
    levels = np.append(levels, 0)  # Add zero if not already included
levels = np.sort(levels)

# Plot contour lines including the manually added levels
contours = plt.contour(X, Y, Z, levels=levels, colors='black')
plt.clabel(contours, inline=True, fontsize=8)

# Set equal aspect ratio
ax.set_aspect('equal', adjustable='box')

# Tight layout to make the plot as large as possible
plt.tight_layout()

plt.title("Slope Field with Isoclines")
plt.xlabel("x")
plt.ylabel("y")
plt.grid(True)
plt.show()
