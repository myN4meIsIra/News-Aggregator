# main
'''
    entry point of news aggregator
'''
import news_parser
from cust_logging.logger import Log
Log = Log("main.py")


def main():

    # instantiate gui
    from gui import main_gui
    gui = main_gui.Gui()
    gui.main_page()


if __name__ == "__main__":
    main()

