import time


def main() -> None:
    try:
        while True:
            print("You are doing something wrong!!!")
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        print("Stopped doing something")
        
        
if __name__ == "__main__":
    main()
    
    