import sys
import os
import threading
import subprocess
from time import sleep

CUR_DIR = os.path.dirname(__file__)
sys.path.append(os.path.join(CUR_DIR, "build/lib.linux-x86_64-3.7-pydebug"))


def run_udplive(filepath: str = None):
    path = filepath or "/home/codetalks/bili.mp4"
    cmd = f" ffmpeg -re -i {path} -c copy -f mpegts 'udp://127.0.0.1:1234'"
    subprocess.check_call(cmd, shell=True)


if __name__ == "__main__":
    import json
    import _easyice
    from easyice import UdpliveCallbackType

    mrl = "udp://127.0.0.1:1234"
    cb_update_interval = 1000000  # 1s
    calctsrate_interval_ms = 1000  # 1s

    datas = []

    def handle_udplive_db(type: int, json_str: str):
        if type == UdpliveCallbackType.TR101290:
            # ignore error msg
            return
        type_m = UdpliveCallbackType.value_of(type)
        json_obj = json.loads(json_str)
        datas.append({"type": type_m.name, "json": json_obj})

    _easyice.process_udplive(
        mrl=mrl,
        callback=handle_udplive_db,
        cb_update_interval=cb_update_interval,
        calctsrate_interval_ms=calctsrate_interval_ms,
    )
    sleep(20)
    print("DONE!")
    import json

    with open("udp.json", mode="wt", encoding="utf-8") as fout:
        json.dump(datas, fout, ensure_ascii=False)
