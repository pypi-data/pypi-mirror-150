import pygame

pygame.init()
screen = pygame.display.set_mode((600, 800))
clock = pygame.time.Clock()

# draw some aweful shapes onto a surface
surf = pygame.Surface((400, 380))
surf.fill(pygame.Color('blue'))
pygame.draw.polygon(surf, pygame.Color('red'),
                    [(20, 20), (60, 90), (20, 120),
                     (90, 120), (130, 200), (160, 120),
                     (240, 120), (140, 80), (180, 20),
                     (100, 80)])
pygame.draw.polygon(surf, pygame.Color('yellow'),
                    [(120, 340), (230, 180), (300, 340)])

# make masks with color threshold
mask_red = pygame.mask.from_threshold(surf, pygame.Color('red'),
                                      (1, 1, 1, 255))
mask_yellow = pygame.mask.from_threshold(surf, pygame.Color('yellow'),
                                         (1, 1, 1, 255))

# create a second surface for the masks
surf2 = pygame.Surface((400, 380))
surf2.fill(pygame.Color('black'))

# draw the masks
pygame.draw.polygon(surf2, (pygame.Color('red')),
                    mask_red.outline(), 0)
pygame.draw.polygon(surf2, (pygame.Color('yellow')),
                    mask_yellow.outline(), 0)

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('black'))
    screen.blit(surf, (100, 20))
    screen.blit(surf2, (100, 420))

    pygame.display.update()
    clock.tick()

pygame.quit()