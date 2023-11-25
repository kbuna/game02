import pygame
import os
import random

def lerp(a, b, t):
    return a + t * (b - a)

class TitleScene:
    # 既存のコード...

class MainGame:
    def __init__(self, screen):
        self.screen = screen
        self.camera_x, self.camera_y = 0, 0
        self.camera_speed = 0.02
        self.isometric_size = int(TILESIZE * 1.5)
        self.isometric_tiles = {}

        for key, color in colours.items():
            tile_surf = pygame.Surface((TILESIZE, TILESIZE), pygame.SRCALPHA)
            tile_surf.fill(color)
            tile_surf = pygame.transform.rotate(tile_surf, 45)
            tile_surf = pygame.transform.scale(tile_surf, (self.isometric_size, self.isometric_size // 2))
            self.isometric_tiles[key] = tile_surf

        self.npc_images = {
            'npc_type_1': {
                'up': [
                    pygame.image.load('npc_up_0.png'),
                    pygame.image.load('npc_up_1.png'),
                    pygame.image.load('npc_up_2.png')
                ],
                'down': [
                    pygame.image.load('npc_down_0.png'),
                    pygame.image.load('npc_down_1.png'),
                    pygame.image.load('npc_down_2.png')
                ],
                'left': [
                    pygame.image.load('npc_left_0.png'),
                    pygame.image.load('npc_left_1.png'),
                    pygame.image.load('npc_left_2.png')
                ],
                'right': [
                    pygame.image.load('npc_right_0.png'),
                    pygame.image.load('npc_right_1.png'),
                    pygame.image.load('npc_right_2.png')
                ]
            },
            # 他のNPCタイプも追加
        }

        self.move_frames = 30
        self.frame_count = 0
        self.animation_frames = 10
        self.animation_counter = 0
        self.clock = pygame.time.Clock()

    def update(self, events):
        self.frame_count += 1

        for npc in npcs:
            if self.frame_count % self.move_frames == 0:
                direction = random.choice(['up', 'down', 'left', 'right'])
                if direction == 'up' and npc['position'][1] > 0:
                    npc['position'][1] -= 1
                elif direction == 'down' and npc['position'][1] < MAPHEIGHT - 1:
                    npc['position'][1] += 1
                elif direction == 'left' and npc['position'][0] > 0:
                    npc['position'][0] -= 1
                elif direction == 'right' and npc['position'][0] < MAPWIDTH - 1:
                    npc['position'][0] += 1
                npc['direction'] = direction
                npc['animation_counter'] = 0

        self.screen.fill((0, 0, 0))

        for column in range(MAPWIDTH):
            for row in range(MAPHEIGHT):
                tile_surf = self.isometric_tiles[tilemap[row][column]]
                x = (column + (MAPHEIGHT - row)) * self.isometric_size // 2 - self.camera_x
                y = 20 + (column + row) * self.isometric_size // 4 - self.camera_y
                self.screen.blit(tile_surf, (x, y))

        for npc in npcs:
            x = (npc['position'][0] + (MAPHEIGHT - npc['position'][1])) * self.isometric_size // 2 - self.camera_x
            y = 20 + (npc['position'][0] + npc['position'][1]) * self.isometric_size // 4 - self.camera_y

            animation_list = self.npc_images[npc['type']][npc['direction']]
            animation_counter = npc['animation_counter'] // (self.animation_frames // len(animation_list))
            npc_image = animation_list[animation_counter % len(animation_list)]

            self.screen.blit(npc_image, (x, y))
            npc['animation_counter'] = (npc['animation_counter'] + 1) % self.animation_frames

        pygame.display.update()
        self.clock.tick(60)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.camera_x = lerp(self.camera_x, mouse_x, self.camera_speed)
        self.camera_y = lerp(self.camera_y, mouse_y, self.camera_speed)

# ゲームのメイン処理
def main():
    pygame.init()
    pygame.display.set_caption("nv")
    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()

    title_scene = TitleScene(screen)
    main_game = MainGame(screen)
    current_scene = title_scene

    while True:
        events = pygame.event.get()

        current_scene.handle_events(events)
        current_scene.update(events)

        if isinstance(current_scene, TitleScene) and current_scene.idx == 1:
            current_scene = MainGame(screen)
        elif isinstance(current_scene, MainGame) and current_scene.idx == 0:
            current_scene = title_scene

if __name__ == "__main__":
    main()
