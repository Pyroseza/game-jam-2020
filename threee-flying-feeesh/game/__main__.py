"""
Threee Deee Whack-a-Dot!
"""
import arcade
import math
import random
import timeit

# Set how many rows and columns we will have
ROW_COUNT = 3**3
COLUMN_COUNT = 3**3

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600


SCREEN_TITLE = "Threee Flying Feeesh presents Teeetris"
GLOBE_RADIUS = (SCREEN_WIDTH * ( 1/3 ))
PARTICLE_RADIUS = 10
PARTICLE_COUNT = 100
SPEED = 0.1

PERSPECTIVE = SCREEN_WIDTH * 0.8 # The field of view of our 3D scene
PROJECTION_CENTER_X = SCREEN_WIDTH * 0.5 # x center of the canvas
PROJECTION_CENTER_Y = SCREEN_HEIGHT * 0.5 # y center of the canvas


class Shape:
    """ Generic base shape class """
    def __init__(self, x, y, width, height, angle, delta_x, delta_y,
                 delta_angle, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.angle = angle
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.delta_angle = delta_angle
        self.color = color
        self.shape_list = None

    def move(self):
        self.x += self.delta_x
        self.y += self.delta_y
        self.angle += self.delta_angle
        if self.x < 0 and self.delta_x < 0:
            self.delta_x *= -1
        if self.y < 0 and self.delta_y < 0:
            self.delta_y *= -1
        if self.x > SCREEN_WIDTH and self.delta_x > 0:
            self.delta_x *= -1
        if self.y > SCREEN_HEIGHT and self.delta_y > 0:
            self.delta_y *= -1

    def draw(self):
        self.shape_list.center_x = self.x
        self.shape_list.center_y = self.y
        # self.shape_list.angle = self.angle
        self.shape_list.draw()


class Particle(Shape):
    def __init__(self,
                x=0,
                y=0,
                width=0,
                height=0,
                angle=0,
                delta_x=0,
                delta_y=0,
                delta_angle=0,
                color=arcade.color.WHITE):
        super().__init__(x, y, width, height, angle, delta_x, delta_y,
                    delta_angle, color)
        shape = arcade.create_ellipse_filled(0, 0,
                                             self.width, self.height,
                                             self.color, self.angle,
                                             num_segments=60)
        #shape = arcade.create_ellipse_filled(0, 0,
        #                                     self.width, self.height,
        #                                     self.color, self.angle,
        #                                     num_segments=60)
        self.shape_list = arcade.ShapeElementList()
        self.shape_list.append(shape)
        # enough of the generic stuff let's get freaky
        self.z = 0
        self.theta = random.random() * 2 * math.pi
        self.phi = math.acos((random.random() * 2) - 1)
        self.x_projected = 0 # x coordinate on the 2D world
        self.y_projected = 0 # y coordinate on the 2D world
        self.scale_projected = 0 # Scale of the element on the 2D world (further = smaller)
        self.radius = (PARTICLE_RADIUS * random.random()) + 5
        self.direction = 1
        # pick a random colour
        p = range(128, 256)
        rc = random.choice
        self.colour = (rc(p), rc(p), rc(p))


    def change_direction(self):
        self.direction *= -1

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
        # We first calculate the projected values of our particle
        self.project();
        # We define the opacity of our element based on its distance
        self.alpha = abs(1 - self.z / SCREEN_WIDTH)
        # We draw a the particle based on the projected coordinates and scale


    def draw_particle(self, x, y, w, h, c, a):
        #shine = (3**5, 3**5, 3**5, self.alpha)
        self.shape = arcade.draw_ellipse_filled(x, y, w, h, c, a, num_segments=60)


    # Draw the particle on the canvas
    def draw(self):
        # We first calculate the projected values of our particle
        self.project();
        # We define the opacity of our element based on its distance
        self.alpha = abs(1 - self.z / SCREEN_WIDTH)
        # We draw a rectangle based on the projected coordinates and scale
        self.draw_particle(self.x_projected - self.radius,
                           self.y_projected - self.radius,
                           self.radius * 2 * self.scale_projected,
                           self.radius * 2 * self.scale_projected,
                           self.colour, 45)


class MyGame(arcade.Window):
    """
    Main application class.
    """


    def __init__(self, width, height, title):
        """
        Set up the application.
        """
        super().__init__(width, height, title)
        self.particles_list = None
        # some interesting debugging stuff
        self.processing_time = 0
        self.draw_time = 0
        self.frame_count = 0
        self.fps_start_timer = None
        self.fps = None


    def setup(self):
        self.create_particles()


    def create_particles(self):
        self.particles_list = []
        # Create the particles
        for i in range(PARTICLE_COUNT):
            # Create a new particle, they are self aware of where they are in the world
            #  and push it into the array
            self.particles_list.append(Particle())


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


    def change_particle_direction(self):
        for particle in self.particles_list:
            particle.change_direction()


    def on_update(self, delta_time):
        """ Movement and game logic """
        start_time = timeit.default_timer()
        if self.frame_count % 60 == 0:
            if self.fps_start_timer is not None:
                total_time = timeit.default_timer() - self.fps_start_timer
                self.fps = 60 / total_time
            self.fps_start_timer = timeit.default_timer()
        self.frame_count += 1
        # update the movement of each particle
        for particle in self.particles_list:
            particle.move()
        self.processing_time = timeit.default_timer() - start_time


    def on_draw(self):
        """
        Render the screen.
        """
        # Start timing how long this takes
        draw_start_time = timeit.default_timer()
        # This command has to happen before we start drawing
        arcade.start_render()
        c1 = (0, 255, 0)
        c2 = (0, 0, 0)
        self.shape = arcade.create_ellipse_filled_with_colors(PROJECTION_CENTER_X,
                        PROJECTION_CENTER_Y,
                        PERSPECTIVE / 3,
                        PERSPECTIVE / 3,
                        inside_color=c1, outside_color=c2,
                        tilt_angle=45, num_segments=60)
        self.shape.draw()
        # now draw out little particles
        self.render_particles()
        # Display timings
        output = f"Processing time: {self.processing_time:.3f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 20, arcade.color.WHITE, 16)

        output = f"Drawing time: {self.draw_time:.3f}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 40, arcade.color.WHITE, 16)

        if self.fps is not None:
            output = f"FPS: {self.fps:.0f}"
            arcade.draw_text(output, 20, SCREEN_HEIGHT - 60, arcade.color.WHITE, 16)
        output = f"Particle count: {PARTICLE_COUNT}"
        arcade.draw_text(output, 20, SCREEN_HEIGHT - 80, arcade.color.WHITE, 16)

        self.draw_time = timeit.default_timer() - draw_start_time


    def on_mouse_press(self, x, y, button, modifiers):
        self.change_particle_direction()
        # self.create_particles()

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
    try:
        window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        window.setup()
        arcade.run()
    except KeyboardInterrupt:
        print("quitting")


if __name__ == "__main__":
    main()
