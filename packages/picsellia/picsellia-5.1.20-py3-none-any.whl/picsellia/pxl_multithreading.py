import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, List, Union

import tqdm

try:
    download_bar_mode = os.environ["PICSELLIA_SDK_DOWNLOAD_BAR_MODE"]
    ascii_bar = True
except KeyError:
    download_bar_mode = "1"
    ascii_bar = False

def do_mlt_function(items: List[Any], f: Callable, h: Callable = lambda _: _, max_workers: Union[int, None] = None) -> dict:
    if max_workers == None or max_workers <= 0:
        max_workers = os.cpu_count() + 4

    with tqdm.tqdm(total=len(items), ncols=50, colour='green', ascii=ascii_bar) as pbar:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(f, item): h(item) for item in items}
            results = {}
            for future in as_completed(futures):
                arg = futures[future]
                try:
                    results[arg] = future.result()
                except Exception:
                    results[arg] = None
                pbar.update(1)
    return results

