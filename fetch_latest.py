from fetch_helpers import fetch_latest
import sys

def print_help_and_exit():
    print("Usage:")
    print("python fetch_latest [OPTIONS]")
    print("")
    print("OPTIONS:")
    print("--from-web")
    print("--from-cache")

    sys.exit(1)

if __name__ == "__main__":

    if len(sys.argv) != 2:
        print_help_and_exit()

    opt_src = sys.argv[1]
    if opt_src == "--from-web":
        from_cache = False
    elif opt_src == "--from-cache":
        from_cache = True
    else:
        print_help_and_exit()

    # Run
    fetch_latest(from_cache)