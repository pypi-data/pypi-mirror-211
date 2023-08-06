import lib_dzne_basetable.baseconv as _baseconv
import lib_dzne_basetable.table as _table
import lib_dzne_tsv as _tsv
import pandas as _pd


class BASEData(_tsv.TSVData):
    _ext = None
    @classmethod
    def basetype(cls):
        if cls._ext is None:
            return None
        if cls._ext.startswith("."):
            raise ValueError()
        if cls._ext.startswith("base"):
            raise ValueError()
        return cls._ext[1:-4]
    @classmethod
    def _load(cls, /, file, **kwargs):
        ans = super().load(file, **kwargs).dataFrame
        ans = _table.make(ans, basetype=cls.basetype())
        return ans
    def _save(self, /, file):
        data = _table.make(data, basetype=self.basetype())
        super().save(string, data)
    @classmethod
    def _default(cls):
        return _table.make(basetype=cls.basetype())
    @classmethod
    def from_file(cls, file, /):
        return super().from_file(file, ABASEData, CBASEData, DBASEData, MBASEData, YBASEData)
    @classmethod
    def clone_data(cls, data, /):
        data = super().clone_data(data)
        return _table.make(data, basetype=cls.basetype())
    @classmethod
    def concat(cls, *args):
        args = [cls(x).data for x in args]
        fulltable = _pd.concat(args, axis=0, ignore_index=True)
        return cls(fulltable)


class ABASEData(BASEData):
    _ext = ".abase"
    @property
    def dBASE(self):
        return DBASEData(_baseconv.a2d(self.data))
class CBASEData(BASEData):
    _ext = ".cbase"
class DBASEData(BASEData):
    _ext = ".dbase"
class MBASEData(BASEData):
    _ext = ".mbase"
class YBASEData(BASEData):
    _ext = ".ybase"
    @property
    def cBASE(self):
        return CBASEData(_baseconv.y2c(self.data))