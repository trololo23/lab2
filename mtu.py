import argparse
import logging
import icmplib
import sys
import time


def validate_mtu(value):
    ivalue = int(value)
    if ivalue < 1 or ivalue > 100000000:
        raise argparse.ArgumentTypeError("Invalid MTU")
    return ivalue


def mtu_search(destination, min_mtu, max_mtu, interval):
    low = min_mtu
    high = max_mtu
    while low <= high:
        mid = (low + high) // 2

        ping_res = icmplib.ping(
            destination,
            interval=interval,
            payload_size=mid - 28,
        )

        if ping_res.is_alive:
            low = mid + 1
        else:
            high = mid - 1

        time.sleep(interval)
    return high


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--min', type=validate_mtu, required=True)
    parser.add_argument('--max', type=validate_mtu, required=True)
    parser.add_argument('--domain', type=str, required=True)
    parser.add_argument('--interval', type=float, default=0)
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format='[%(levelname)s] %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    if not icmplib.ping(args.domain).is_alive:
        logging.error("Address is not reachable")
        sys.exit(0)

    try:
        mtu = mtu_search(args.domain, args.min, args.max, args.interval)
        if mtu:
            logging.info(f"Min: {mtu}")
        else:
            logging.error("Not found")
    except Exception as e:
        logging.exception(f"Error occurred: {e}")
        sys.exit(0)