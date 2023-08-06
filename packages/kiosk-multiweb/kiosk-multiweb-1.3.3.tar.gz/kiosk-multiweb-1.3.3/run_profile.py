

import faulthandler
from memory_profiler import profile
from multiweb.runnode import run_node


@profile
def run_profile():
    run_node()


if __name__ == '__main__':
    print("Starting faulthandler")
    faulthandler.enable()

    print("Running for memory profiling")
    run_profile()
