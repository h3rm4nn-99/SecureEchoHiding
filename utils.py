from bitarray import bitarray

def next_key_chunk(current_key_chunk, a_key) -> int:
    return (a_key * current_key_chunk + 2 * a_key)

def gen_r_sequence(length, seed, a_key) -> bitarray:
    R_sequence = bitarray(length)
    current_key_chunk = seed
    for i in range(length):
        current_key_chunk = next_key_chunk(current_key_chunk, a_key)
        if current_key_chunk % 6 > 2:
            R_sequence[i] = True
        elif current_key_chunk % 6 <= 2:
            R_sequence[i] = False
    return R_sequence