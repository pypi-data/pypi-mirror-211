#!/usr/bin/env python

import enum

class FileProvider(enum.Enum):
    local = '/'
    s3 = 's3://'
    gcs = 'gs://'
    azure = 'abfs://'

class StorageFormat(enum.Enum):
    parquet = 'parquet'
    csv = 'csv'
    pkl = 'pkl'
    tsv = 'tsv'
    txt = 'txt'


class GraphComputeLayer(enum.Enum):
    pandas = 'pandas'
    dask = 'dask'
    # these need middleware
    spark = 'spark'
    ray = 'ray'
