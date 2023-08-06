from importlib.resources import files

eop_historical = files("naif_eop_historical").joinpath("earth_720101_070426.bpc").as_posix()
_eop_historical_md5 = files("naif_eop_historical").joinpath("earth_720101_070426.md5").as_posix()
