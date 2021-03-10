import pygame

class fps_counter():
    clock = pygame.time.Clock()

    def get_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_text = pygame.font.SysFont("Arial", 18).render(fps, 1, pygame.Color("coral"))
        return fps_text