import os
import logging
import urllib.request as urllib
import csv as csvlib
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm


def extract(symbol: str, datetime_range: list[datetime], max_workers: int = None, path: str = 'out') -> None:
    """
    Extract multiple bi5 from the datafeed and write it in a single bi5 file with a datetime helper csv. \n
    The feed stores datetime information in its name only, this is lost if we want to store the data in a single bi5 file, hence the csv.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f'The path - {path} does not exist.')

    filename = _create_filename(symbol, datetime_range)
    bi5 = f"{path}/{filename}.bi5"
    csv = f"{path}/{filename}.csv"
    log = f"{path}/{filename}.log"

    if os.path.exists(bi5) or os.path.exists(csv):
        raise FileExistsError(f'A file with the name - {filename} already exists.')

    args = ((symbol, datetime, log) for datetime in datetime_range)

    with ThreadPoolExecutor(max_workers=max_workers) as executor, tqdm(
        total=len(datetime_range), desc="Extract"
    ) as pbar:
        results = executor.map(lambda f: _extract_one(*f), args)        
        for result in results:
            pbar.update(1)
            if result is None:
                continue
            with open(bi5, "ab") as bi5_writer:
                bi5_writer.write(result[1])
            with open(csv, "a", newline="") as file:
                writer = csvlib.writer(file)
                writer.writerow([result[0]])


def _extract_one(symbol: str, datetime: datetime, log: str) -> tuple[datetime, bytes] | None:
    endpoint = _create_endpoint(symbol, datetime)
    try:
        data = urllib.urlopen(endpoint).read()
        if data:
            print(type(data))
            return (datetime, data)
    except Exception as e:
        logging.basicConfig(
            filename=log,
            filemode="a",
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logging.warning(f"Extracting from {endpoint} - {symbol} - {datetime} failed with the exception {e}")


def _create_endpoint(symbol: str, datetime: datetime) -> str:
    """
    Create datafeed endpoint \n
    format: https://www.dukascopy.com/datafeed/{SYMBOL}/{YEAR}/{MONTH}/{DAY}/{HOUR}h_ticks.bi5 \n
    example: https://www.dukascopy.com/datafeed/EURUSD/2020/01/01/1h_ticks.bi5
    """
    year = datetime.year
    month = f"{datetime.month-1:02}"
    day = f"{datetime.day:02}"
    hour = f"{datetime.hour:02}"
    uri = f"{symbol.upper()}/{year}/{month}/{day}/{hour}h_ticks.bi5"
    return f"https://www.dukascopy.com/datafeed/{uri}"


def _create_filename(symbol: str, datetime_range: list[datetime]) -> str:
    """
    Create filename \n
    example: EURCAD_20200101_20200131
    """
    start = datetime_range[0].strftime("%Y%m%d")
    end = datetime_range[-1].strftime("%Y%m%d")
    return f"{symbol.upper()}_{start}_{end}"

