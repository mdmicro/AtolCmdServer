import json
from datetime import datetime, time
from multiprocessing import Queue
from flask import jsonify
from api import CommandResponsesAtol
from atol import Atol

cmd_atol = Queue()
cmd_responses_atol = dict()

def cmd_cycle(self):
    while True:
        try:
            data = cmd_atol.get(block=True, timeout=10)

            atol = Atol()
            try:
                res_init = atol.init()
                if res_init:
                    result = atol.jsonCmd(data.json_cmd, data.uuid)
                    print(f"Response for {data.uuid}")
                    print(result.data)

                    data = {"results":
                        [
                            {
                                "status": "ready",
                                "error": {"code": 0},
                                "result": json.loads(result.data)
                            }
                        ]
                    }
                    cmd_responses_atol[data.uuid] = CommandResponsesAtol(data=data, date_create=datetime.now())

                    return jsonify(result.uuid), 200
                else:
                    return jsonify({"data": None, "error": 'Ошибка подключения к ККТ'}), 200
            except Exception:
                return f'Error {Exception}'
            finally:
                atol.close()
                time.sleep(1)

        except cmd_atol.Empty:
            continue
