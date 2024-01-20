import time

def main() -> None:
    try:
        while True:
            print("Doing some useful stuff...")
            time.sleep(5)

    except KeyboardInterrupt:
        pass

    finally:
        print("Stopped doing something")

if __name__ == "__main__":
    main()
