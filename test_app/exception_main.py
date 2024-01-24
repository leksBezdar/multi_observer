import time


def main() -> None:
    try:
        while True:
            print("You are doing something wrong in exception_main.py!!!")
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    
    finally:
        print("Stopped doing something")
        
if __name__ == "__main__":
    main()
