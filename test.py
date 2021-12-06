def a_coder(address):
    """
    :param address: address excluding @ from A_instruction
    :return: binary representation in string
    """
    # convert address to integer then to binary
    return f'{int(address):016b}'

print(a_coder(6))