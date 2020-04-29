import os
from typing import Optional, Dict
import codecs
import logging
import _easyice
from enum import IntEnum

logger = logging.getLogger(__name__)


def process_ts(*, filename: str) -> Optional[Dict[str, str]]:
    """ analyze the ts file and return a dict of json str
    {
        "ffprobe":"",
        "mediainfo":"",
        "pids":"",
        "programinfo":"",
        "psi":"",
        "tr101290":""
    }
    """
    full_path = os.path.abspath(filename)
    mrl = "file://" + full_path
    try:
        _easyice.easyice_process(mrl=mrl)
    except Exception as e:
        logger.exception("process ts(%s) failed", mrl, exc_info=e)
        return None

    data = dict()

    def load_data(typename: str):
        json_path = full_path + "." + typename + ".json"
        with codecs.open(json_path, encoding="utf-8") as fin:
            json = fin.read()
            data[typename] = json

    load_data("ffprobe")
    load_data("mediainfo")
    load_data("pids")
    load_data("programinfo")
    load_data("psi")
    load_data("tr101290")

    return data


class UdpliveCallbackType(IntEnum):
    MEDIAFINO = 0  # 只调用一次
    FFPROBE = 1  # 只调用一次
    PIDS = 2  #
    PSI = 3  # 只调用一次
    TR101290 = 4
    PCR = 5
    RATE = 6
    PROGRAM_INFO_BRIEF = 7
    UNKNOW = 8

    @classmethod
    def value_of(cls, value: int):
        for m in cls:
            if m == value:
                return m
        return cls.UNKNOW
