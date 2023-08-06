import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

pos1, rad1 = (250, 200), 100
pos2, rad2 = (250, 250), 80

surf1 = pygame.Surface((500, 500), pygame.SRCALPHA)
surf2 = pygame.Surface((500, 500), pygame.SRCALPHA)

pygame.draw.circle(surf1, (255, 0, 0, 255), pos1, rad1)
pygame.draw.circle(surf2, (255, 0, 0, 255), pos2, rad2)

surf1.blit(surf2, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
surf2.blit(surf1, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            print(pygame.key.name(event.key))

    window.fill((255, 255, 255))

    window.blit(surf2, (0, 0))
    pygame.draw.circle(window, (128, 128, 128), pos1, rad1 + 1, 3)
    # pygame.draw.circle(window, (128, 128, 128), pos2, rad2 + 1, 3)

    pygame.display.flip()