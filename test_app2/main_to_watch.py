import time


def main() -> None:
    try:
        while True:
            print("You are doing something wrong in main_to_watch.py!!!")
            time.sleep(5)

    except KeyboardInterrupt:
        pass

    finally:
        print("Stopped doing something")

if __name__ == "__main__":
    main()
