import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, images):
        super().__init__()
        self.images = images
        self.image = images['p1_jump']
        self.rect = self.image.get_rect()
        self.rect.center = pos
        # index 0 represents dx, index 1 represents dy
        self.xy_speed = pygame.math.Vector2(0, 0)
        self.facing = "R"
        self.jump_speed = -14
        self.world_y = 0
        self.progress = 0

    def update(self, platforms):
        screen_info = pygame.display.Info()
        self.image = self.images['p1_jump']
        if self.facing == "L":
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.right < 0:
            self.rect.left = screen_info.current_w
        if self.rect.left > screen_info.current_w:
            self.rect.right = 0
        self.rect.move_ip(self.xy_speed)
        if self.rect.top < 100:
            self.rect.top = 100
            for platforms in platforms.sprites():
                platforms.scroll(-1 * self.xy_speed[1])
        elif self.rect.top > screen_info.current_h - 80:
            self.rect.top = screen_info.current_h - 80
            for platforms in platforms.sprites():
              if platforms.rect.bottom > 0:
                  platforms.scroll(-1 * self.xy_speed[1])
              else:
                platforms.kill()
            return True
        hitlist = pygame.sprite.spritecollide(self, platforms, False)
        for platforms in hitlist:
            if self.xy_speed[1] > 0 and abs(self.rect.bottom - platforms.rect.top) <= self.xy_speed[1]:
                self.rect.bottom = platforms.rect.top
                self.xy_speed[1] = self.jump_speed
        self.xy_speed[0] = 0
        self.xy_speed[1] += .5

    def left(self):
        self.facing = 'L'
        self.xy_speed[0] = -10

    def right(self):
        self.facing = "R"
        self.xy_speed[0] = 10
