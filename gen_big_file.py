import random
import string


def gen(num_strings: int, max_length: int, filename='big_file.txt'):
    with open(filename, 'w') as fout:
        for _ in range(num_strings):
            cur_str = ''.join(
                [
                    random.choice(string.ascii_letters)
                    for _ in range(random.randint(1, max_length))
                ],
            )
            print(cur_str, file=fout)


if __name__ == '__main__':
    gen(int(1e5), 1000)
