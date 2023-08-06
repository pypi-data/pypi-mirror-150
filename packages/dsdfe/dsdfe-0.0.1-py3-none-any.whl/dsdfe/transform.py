import struct
import lzma
import pandas as pd


def transform(bi5: str, csv: str, precision: int = None):
    if not _validate_files(bi5, csv):
        raise ValueError("The names or extensions of files do not match")
    
    df = merge_files_into_df(bi5, csv)
    df.columns = ('timedelta', 'bid', 'ask', 'volume_bid', 'volume_ask', 'datetime')  
    df['datetime'] = df['datetime'] + pd.TimedeltaIndex(df['timedelta'], unit="ms")    
    df.drop(columns=['timedelta'], inplace=True)

    if precision:
        decimals = 10**precision
        df['bid'] = df['bid'] / decimals
        df['ask'] = df['ask'] / decimals

    return df


def merge_files_into_df(bi5: str, csv: str, format: str = ">3I2f") -> pd.DataFrame:
    result = []
    datetime_iterator = _get_dates(csv).itertuples()
    datetime = next(datetime_iterator)[1]
    chunk_size = struct.calcsize(format)
    previous_timedelta = 0
    with lzma.open(bi5) as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                unpacked = struct.unpack(format, chunk)
                if unpacked[0] < previous_timedelta:
                    datetime = next(datetime_iterator)[1]
                result.append([*unpacked, datetime])
                previous_timedelta = unpacked[0]
            else:
                break
    return pd.DataFrame(result)


def unpack_bi5(bi5: str, format=">3I2f") -> list[str]:
    result = []
    chunk_size = struct.calcsize(format)
    with lzma.open(bi5) as f:
        while True:
            chunk = f.read(chunk_size)
            if chunk:
                unpacked = struct.unpack(format, chunk)
                result.append(unpacked)
            else:
                break
    return result


def _get_dates(csv: str) -> pd.DataFrame:
    df = pd.read_csv(csv, header=None)
    df[0] = pd.to_datetime(df[0])
    return df


def _validate_files(bi5: str, csv: str) -> bool:
    bi5, bi5_ext = bi5.split('.')
    csv, csv_ext = csv.split('.')

    return bi5 == csv and bi5_ext == 'bi5' and csv_ext == 'csv'