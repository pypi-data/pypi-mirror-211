from cleo.application import Application 
from src.deeputilities.client.commands.config_maker_command import ConfigMaker
from src.deeputilities.client.commands.demo_command import DemoCommand
import sys

deeputils_app = Application()
deeputils_app.add(DemoCommand())

def main() -> int:
    return deeputils_app.run()


if __name__ == "__main__":
    sys.exit(main())
