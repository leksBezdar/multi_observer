import time


def main() -> None:
    try:
        while True:
            print("Doing not so useful stuff...")
            time.sleep(5)

    except KeyboardInterrupt:
        pass

    finally:
        print("Stopped doing something.....")
        
if __name__ == "__main__":
    print(1) 
    
    main()
