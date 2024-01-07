from agents import RandomAgent
from environments import GameEnvironment, VisualGameEnvironment


def main():
    environment = VisualGameEnvironment(agent=RandomAgent())
    environment.game_loop()


if __name__ == "__main__":
    main()
