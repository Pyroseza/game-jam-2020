"""
Teeetris - based off Array Backed Grid example from Arcade website
https://arcade.academy/examples/array_backed_grid_buffered.html#array-backed-grid-buffered

Show how to use a two-dimensional list/array to back the display of a
grid on-screen.

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.array_backed_grid_buffered
"""
import arcade
import random
import math

# Set how many rows and columns we will have
ROW_COUNT = 3**3
COLUMN_COUNT = 3**3

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


SCREEN_TITLE = "Threee Flying Feeesh presents Teeetris"
GLOBE_RADIUS = (SCREEN_WIDTH * ( 1/3 ))
PARTICLE_RADIUS = 10
PARTICLE_COUNT = 100
SPEED = 0.1

PERSPECTIVE = SCREEN_WIDTH * 0.8 # The field of view of our 3D scene
PROJECTION_CENTER_X = SCREEN_WIDTH * 0.5 # x center of the canvas
PROJECTION_CENTER_Y = SCREEN_HEIGHT * 0.5 # y center of the canvas
particles = [] # Store every "particle" in this array

class Particle:
    def __init__(self, direction=1):
        self.x = 0
        self.y = 0
        self.z = 0
        self.theta = random.random() * 2 * math.pi
        self.phi = math.acos((random.random() * 2) - 1)
        self.x_projected = 0 # x coordinate on the 2D world
        self.y_projected = 0 # y coordinate on the 2D world
        self.scale_projected = 0 # Scale of the element on the 2D world (further = smaller)
        self.radius = (PARTICLE_RADIUS * random.random()) + 5
        self.direction = direction
        # pick a random colour
        p = range(128, 256)
        rc = random.choice
        self.colour = (rc(p), rc(p), rc(p))


    # Project our element from its 3D world to the 2D canvas
    def project(self):
        # Calculate the x, y, z coordinates in the 3D world
        self.x = GLOBE_RADIUS * math.sin(self.phi) * math.cos(self.theta);
        self.y = GLOBE_RADIUS * math.cos(self.phi);
        self.z = GLOBE_RADIUS * math.sin(self.phi) * math.sin(self.theta) + GLOBE_RADIUS;
        # Project the 3D coordinates to the 2D canvas
        self.scale_projected = PERSPECTIVE / (PERSPECTIVE + self.z);
        self.x_projected = (self.x * self.scale_projected) + PROJECTION_CENTER_X;
        self.y_projected = (self.y * self.scale_projected) + PROJECTION_CENTER_Y;


    # Update the location of each particle on the canvas
    def move(self):
        # self.theta = self.theta + math.pi * 2
        self.theta += (SPEED * self.direction * random.random())


    # Draw the particle on the canvas
    def draw(self):
        # We first calculate the projected values of our particle
        self.project();
        # We define the opacity of our element based on its distance
        self.alpha = abs(1 - self.z / SCREEN_WIDTH)
        # We draw a rectangle based on the projected coordinates and scale
        arcade.draw_rectangle_filled(self.x_projected - self.radius,
                                        self.y_projected - self.radius,
                                        self.radius * 2 * self.scale_projected,
                                        self.radius * 2 * self.scale_projected,
                                        self.colour)


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)
        self.direction = 1
        self.create_particles()


    def create_particles(self):
        self.particles_list = []
        self.direction *= -1
        # Create the particles
        for i in range(PARTICLE_COUNT):
            # Create a new particle and push it into the array
            self.particles_list.append(Particle(self.direction))


    def render_particles(self):
        arcade.set_background_color(arcade.color.BLACK)

        # sort sprites, this gives the 3D effect when they are drawn from "furtherest" away to "closest"
        self.particles_list = sorted(
            self.particles_list, key=lambda particle: particle.z,
            reverse=True
        )
        # draw all the particles
        for particle in self.particles_list:
            particle.draw()


    def on_draw(self):
        """
        Render the screen.
        """
        # This command has to happen before we start drawing
        arcade.start_render()
        # now draw out little particles
        self.render_particles()


    def on_update(self, delta_time):
        """ Movement and game logic """
        # update the movement of each particle
        for particle in self.particles_list:
            particle.move()


    def on_mouse_press(self, x, y, button, modifiers):
        self.create_particles()
    #     """
    #     Called when the user presses a mouse button.
    #     """

    #     # Change the x/y screen coordinates to grid coordinates
    #     column = int(x // (WIDTH + MARGIN))
    #     row = int(y // (HEIGHT + MARGIN))]

    #     print(f"Click coordinates: ({x}, {y}). Grid coordinates: ({row}, {column})")

    #     # Make sure we are on-grid. It is possible to click in the upper right
    #     # corner in the margin and go to a grid location that doesn't exist
    #     if row < ROW_COUNT and column < COLUMN_COUNT:

    #         # Flip the location between 1 and 0.
    #         if self.grid[row][column] == 0:
    #             self.grid[row][column] = 1
    #         else:
    #             self.grid[row][column] = 0

    #     self.recreate_grid()


def main():
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()
