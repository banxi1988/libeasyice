import os
from typing import Optional, Dict
import codecs
import logging
import _easyice

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
        json_path = full_path + typename + ".json"
        with codecs.open(path, mode="rt", encoding="utf-8") as fin:
            json = fin.read()
            data[typename] = json

    load_data("ffprobe")
    load_data("mediainfo")
    load_data("pids")
    load_data("programinfo")
    load_data("psi")
    load_data("tr101290")

    return data

