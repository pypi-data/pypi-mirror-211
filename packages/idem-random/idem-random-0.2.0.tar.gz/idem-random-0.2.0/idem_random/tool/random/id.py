import base64
import random


def generate_random_string(hub, length: int, prefix: str = None):
    """
    generate random string

    Args:
        length(Integer): The number of random bytes to produce a number in base64 format.
        prefix(Text, optional): Arbitrary string to prefix the output value with. This string is supplied as-is, meaning
            it is not guaranteed to be URL-safe or base64 encoded.
    Returns:
        The generated random ID presented in base64 with added prefix.
    """

    limit = pow(256, length) - 1
    number = random.randint(0, limit - 1)

    # Convert random number to base64 format
    num_base64 = base64.b64encode(bytes(str(number), "ascii"))
    num_base64 = str(num_base64)[2:-1]
    if prefix:
        random_id = prefix + str(num_base64)
    else:
        random_id = str(num_base64)

    return random_id
