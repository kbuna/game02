import pygame

class BaseGame:
    def __init__(self, width, height, title="My Game"):
        pygame.init()
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.is_running = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            # 他のイベントのハンドリングも追加可能

    def update(self):
        # ゲームオブジェクトの状態更新
        pass

    def draw(self):
        # ゲームオブジェクトの描画
        pass

    def run(self):
        self.is_running = True
        while self.is_running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def main():
        pass
    
if __name__ == "__main__":
    BaseGame.main()