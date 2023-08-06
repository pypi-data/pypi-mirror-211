#!/usr/bin/env python

# python standard libraries
import pathlib
import json
import typing
import time

# third party
from structlog import get_logger
from dask import dataframe as dd

# internal
from kurve.util import check_is_unix_timestamp
from kurve.enums import FileProvider


# in order to support composite types we'll need something more expansive
PK_TYPES = ['int', 'string']
DATE_TYPES = ['timestamp', 'date', 'datetime']


logger = get_logger(__name__)


class Entity:
    def __init__(self,
            source,
            identifier : str,
            columns : typing.Optional[typing.List[str]] = [],
            column_type_map : typing.Optional[dict] = {},
            column_df = None,
            pk : str = None
            ) -> None:
        """
Constructor for an `Entity` object
        """
        self.source = source
        self.identifier = identifier
        self.columns = columns
        self.column_type_map = column_type_map

        # primary key candidates
        self._pk_candidates = []
        # elected primary key
        self.pk = pk
        # date keys
        self.dks = []
        self.row_count = None
        self._sample = None


    def __repr__(self):
        return f'<Entity (identifier={self.identifier}, source={self.source.__repr__()})>'


    def __str__(self):
        return f'<Entity (identifier={self.identifier}, source={self.source.__repr__()})>'


    def get_pk(self):
        if not self.pk:
            self.elect_pk()
        return self.pk


    def extract_dt_candidates(self):
        dt_candidates = []
        for c, t in self.get_type_map().items():
            if sum([t in dt or t.startswith(dt) for dt in DATE_TYPE]):
                dt_candidates.append( c )
        return dt_candidates


    def elect_pk (self):
        try:
            start = time.time()
            if not self.pk:
                pk_candidates = self.extract_pk_candidates()
                self.pk = self.designate_pk(pk_candidates)
                end = time.time()
                logger.info(f"elect_pk ran for identity: {self.identifier} in {end-start} seconds") 
            else:
                logger.info(f"already had pk for identity: {self.identifier}")
        except Exception as e:
            logger.error(e)


    def extract_pk_candidates (
            self,
            ) -> str:
        pk_candidates = []
        for c, t in self.get_type_map().items():
            if c.lower() == 'id':
                return [c]
            # type check
            if sum([t in pkt or t.startswith(pkt) for pkt in PK_TYPES]):
                pk_candidates.append( c )
        return pk_candidates


    def designate_pk (
            self,
            pk_candidates: list = [],
            sample_max : int = 100,
            # a common winner name
            prior_winner : str = None
            ):
        # num rows to get
        samp = self.get_sample(n=sample_max)
        N = len(samp)
        finals = []
        for pkc in pk_candidates:
            if pkc.lower().endswith('_id') or pkc.lower() == 'id':
                finals.append(pkc)
            elif check_is_unix_timestamp(samp, pkc):
                continue
            # if we've made it here there is no identifier indication
            # in the naming of the column, the data doesn't appear to
            # be a timestamp, and we've now got to check if the uniqueness
            # aspects apply
            elif len(samp[pkc].unique()) / N == 1:
                finals.append(pkc)

        logger.debug(f"got {len(finals)} pk candidates for {self.identifier}")
        if len(finals) == 1:
            return finals[0]
        else:
            # hacky, but avoids circular import errors
            if self.source.__class__.__name__ in ['PostgresSource', 'MySQLSource', 'SnowflakeSource']:
                if len(samp) < sample_max:
                    return None
            # check for identifier colname
            # # this is brittle
            for c in finals:
                if c.lower().endswith('_id'):
                    return c
            # this should be a top level parameter of the algorithm eventually
            if sample_max < 1000:
                return self.designate_pk(pk_candidates=finals, sample_max=sample_max*10)
            else:
                logger.debug(f"tried {sample_max} samples and no primary keys have been found for: {self.identifier}")
                return None


    def elect_dk(self):
        """
Elects a column to the date 
key with which to orient in the data
        """
        pass


    def get_columns(self) -> list:
        if len(self.columns):
            return list(self.columns)
        else:
            self.columns = self.source.get_columns(self)
        return self.columns


    def load_type_map(self):
        if not self.column_type_map:
            self.column_type_map = self.source.get_column_type_map(self)


    def get_type_map(self) -> dict:
        self.load_type_map()
        return self.column_type_map


    def get_dask_dataframe(self) -> dd.core.DataFrame:
        """
Get a dask dataframe
        """
        if self.source.provider == FileProvider.local:
            path = self.identifier
        elif self.source.provider in [FileProvider.s3, FileProvider.gcs, FileProvider.azure]:
            path = f"{self.source.provider.value}{self.identifier}"

        return getattr(dd, f"read_{self.source.storage_format.value}")(path)


    def get_sample(self, n=100):
        """
Gets a sample of `n` records of this entity instance's underlying data by
leveraging the associated source
        """
        if isinstance(self._sample, None.__class__):
            sample = self.source.get_sample(self, n=n)
            self._sample = sample
        elif len(self._sample) < n:
            sample = self.source.get_sample(self, n=n)
            self._sample = sample
        return self._sample


    def extract_date_keys(self):
        """
Extracts the date keys for this instance
        """
        raise NotImplementedError("`extract_date_keys` not yet implemented")
