from src.tasks import init_dht, init_led


def main():
    init_dht.apply_async()
    init_led.apply_async()

if __name__ == "__main__":
    main()

