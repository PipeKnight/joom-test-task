import heapq
import os
import shutil
import tempfile
import time
from typing import List

import gen_big_file

BUFFER = 32_000


def run_sort(input_filename):
    with tempfile.TemporaryDirectory() as tmp_dir_path:
        print(f'Created temp dir: {tmp_dir_path}')
        file_paths = split(input_filename, tmp_dir_path)
        result_path = merge_all(file_paths, tmp_dir_path, input_filename)
        print(f'Sorted result is in: {result_path}')


def split(input_filename: str, tmp_dir_path: str) -> List[str]:
    cur_data: List[str] = []
    file_paths: List[str] = []
    file_path = os.path.join(tmp_dir_path, f'{BUFFER}-{len(file_paths)}.txt')

    with open(input_filename) as f:
        for index, line in enumerate(f):
            cur_data.append(line)
            if index % BUFFER == BUFFER - 1:
                write_data(file_path, sorted(cur_data))
                file_paths.append(file_path)
                file_path = os.path.join(
                    tmp_dir_path, f'{BUFFER}-{len(file_paths)}.txt',
                )
                cur_data = []
    if cur_data:
        write_data(file_path, sorted(cur_data))
        file_paths.append(file_path)

    return file_paths


def merge_all(
        file_paths: List[str], tmp_dir_path: str, input_filename: str,
) -> str:
    cnt = 0
    while len(file_paths) >= 2:
        t0 = time.time()

        file_path1 = file_paths.pop()
        file_path2 = file_paths.pop()
        target_path = os.path.join(tmp_dir_path, f'heapsort-{cnt}.txt')
        cnt += 1

        merge_files(file_path1, file_path2, target_path)
        file_paths.append(target_path)
        os.remove(file_path1)
        os.remove(file_path2)

        t1 = time.time()

        print(
            f'Merged two files in {t1 - t0:0.2f}s. Remaining: {len(file_paths)}',
        )

    result_path = 'sorted_' + input_filename
    shutil.move(file_paths[0], result_path)
    return result_path


def write_data(file_path, data):
    with open(file_path, 'w') as fout:
        for line in data:
            fout.write(line)


def merge_files(file_path1: str, file_path2: str, outpath: str) -> int:
    with open(outpath, 'w') as fout, open(file_path1) as f1, open(
            file_path2,
    ) as f2:
        for line in heapq.merge(f1, f2):
            fout.write(line)


if __name__ == '__main__':
    gen_big_file.gen(100000, 100, 'some_file.txt')
    run_sort('some_file.txt')
