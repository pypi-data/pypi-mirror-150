from cleo import Application
#from commands.commands import DeepDanceRun

import sys

from deep_dance.client.commands.commands import DeepDanceDemoRun

dance_app = Application()
dance_app.add(DeepDanceDemoRun())

def main() -> int:
    return dance_app.run()

if __name__ == '__main__':
    sys.exit(main())
