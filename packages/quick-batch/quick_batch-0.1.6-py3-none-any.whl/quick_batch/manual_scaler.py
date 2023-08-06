import sys
import fire
from utilities.manage_client import create_client
from utilities.manage_services import scaleup_processor_service


def main(num_processors=None):
    # check num_processors - used as script fire will not be used
    if not num_processors:
        num_processors = int(sys.argv[1])

    # check num_processors is an integer
    try:
        num_processors = int(num_processors)
    except ValueError:
        raise ValueError("FAILURE: num_processors must be an integer")

    # check basic value of num_processors
    if num_processors < 1:
        raise ValueError("FAILURE: pip num_processors must be greater than 0")

    # create client
    client = create_client()

    # print update
    print(f"INFO: manual default scale override --> " + # noqa
          "scaling processor service to {num_processors} instances...")

    # scale up processor service
    scaleup_processor_service(client, num_processors)

    # print update
    print("INFO: ...complete")


if __name__ == '__main__':
    fire.Fire(main)
