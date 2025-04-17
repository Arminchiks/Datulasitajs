import pygame
import pygame3d
from pygame3d import Camera, Mesh, Scene, Cube

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set up camera
camera = Camera(fov=60, aspect_ratio=screen_width / screen_height)
camera.position = (0, 5, -10)

# Create a scene
scene = Scene(camera)

# Create a simple cube to represent a block
block = Cube(size=2)
block.position = (0, 0, 0)  # Place the block in the world

# Add block to the scene
scene.add_object(block)

# Set up the clock for FPS
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the scene (move camera, handle inputs, etc.)
    camera.rotate(0.01, 0.01)

    # Draw the scene
    screen.fill((0, 0, 0))  # Clear screen with black
    scene.render(screen)

    pygame.display.flip()

    clock.tick(60)  # Limit to 60 FPS

pygame.quit()
