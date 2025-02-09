import json
import sys
from collections import namedtuple
from datetime import datetime
from xmlrpc.client import DateTime

from flask import Flask, request, jsonify
from atol import Atol
from named_tuple import msgConnect

flaskApp = Flask(__name__)
SERVER_PORT = 16732
SERVER_URL = 'http://127.0.0.1' + ':' + str(SERVER_PORT) + '/'

def flaskRoutes(queue):
    cmd_responses_atol = dict()

    @flaskApp.route('/')
    def default():
        atol = Atol()

        try:
            resInit = atol.init()

            if resInit:
                res = atol.info()
                model = atol.getModel()
                # fn_info = atol.getFnInfo()

                # queue.put([fn_info])
                return (f'<div>Atol Web Server started</div> '
                        f'<div>version: {res.version}</div>'
                        f'<div>opened: {res.isOpened}</div>'
                        f'<div><p>{res.settings}</p></div>'
                        '</br>'
                        f'<div><a href="{SERVER_URL}/init">init</a></div>'
                        f'<div>model KKT: {model.name}</div>'
                        # f'<div>fnInfo: {fn_info}</div>'
                        )
            else:
                return 'No Atol connection'
        except Exception:
            return f'Error {Exception}'
        finally:
            atol.close()

    # Инициализация драйвера, возвращает статус подключения к ККТ
    @flaskApp.route('/init')
    def init():
        try:
            atol = Atol()
            res = 'Ok' if atol.init() else 'Not connection'
            atol.close()
            return res
        except Exception:
            return f'Error {Exception}'

    # General protocol
    @flaskApp.route('/jsonCmd', methods=['POST'])
    def json_cmd():
        # Получаем параметры из тела запроса
        json_data = request.get_json()

        if not json_data:
            return jsonify({"error": "Отсутствуют данные в теле запроса"}), 400

        atol = Atol()
        try:
            resInit = atol.init()
            if resInit:
                result = atol.jsonCmd(json_data)
                return jsonify(result), 200
            else:
                return jsonify({"error": 'Ошибка'}), 200
        except Exception:
            return f'Error {Exception}'
        finally:
            atol.close()

    # Protocol Атол HTTP server
    @flaskApp.route('/api/v2/requests', methods=['POST'])
    def v2_requests():
        # Получаем параметры из тела запроса
        res = request.get_json()
        uuid = res.get("uuid")
        dat = res.get("request")
        print(f"Receive command {uuid}")
        print(dat)

        if not dat:
            return jsonify({"error": "Отсутствуют данные в теле запроса"}), 400

        atol = Atol()
        try:
            res_init = atol.init()
            if res_init:
                result = atol.jsonCmd(dat[0], uuid)
                print(f"Response for {uuid}")
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
                cmd_responses_atol[uuid] = CommandResponsesAtol(data=data, date_create=datetime.now())

                return jsonify(result.uuid), 200
            else:
                return jsonify({"data": None, "error": 'Ошибка подключения к ККТ'}), 200
        except Exception:
            return f'Error {Exception}'
        finally:
            atol.close()

    @flaskApp.route('/api/v2/requests/<uuid>', methods=['GET'])
    def v2_get_requests(uuid):
        print(f"Received request response {uuid}")
        response = cmd_responses_atol[uuid]

        if not response:
            return jsonify({"error": "Отсутствуют данные в теле запроса"}), 400

        del cmd_responses_atol[uuid]
        print(response.data)
        return jsonify(response.data), 200

def flask_start(queue):
    flaskRoutes(queue)

    # передадим в gui статус подключения ККТ
    atol = Atol()
    status = atol.init()
    atol.close()
    queue.put([msgConnect(status)])

    sys.exit(flaskApp.run(port=16732))


    #  * постановка команды в очередь ККТ и ожидание результата выполнения
	#  *
	#  * @param command - объект согласно документации ККТ по JSON формату команд
	#  * @example пример команды постановки в очередь ККТ запросом POST  /api/v2/requests
	#  {
	# 	uuid: '0ba40014-5fa5-11ea-b5e9-037d4786a49d',
	# 	request: [
	# 		{
	# 			type: 'closeShift',
	# 			operator: {
	# 				name: 'Иванов',
	# 				vatin: '123654789507',
	# 			},
	# 		},
	# 	],
	# };
	#  * @example ответ на GET  запрос /api/v2/requests/{uuid} о поставленной в очередь команды к ККТ
	#  {
	# 	"results": [
	# 		{
	# 			"error": {
	# 				"code": 0,
	# 				"description": "Ошибок нет"
	# 			},
	# 			"status": "ready",
	# 			"result": {
	# 				"deviceInfo": {
	# 					"configurationVersion": "3.0.7942",
	# 					"ffdVersion": "1.05",
	# 					"firmwareVersion": "3.0.1245",
	# 					"fnFfdVersion": "1.0",
	# 					"model": 57,
	# 					"modelName": "АТОЛ 25Ф",
	# 					"receiptLineLength": 48,
	# 					"receiptLineLengthPix": 576,
	# 					"serial": "00105707756920"
	# 				}
	# 			}
	# 		}
	# 	]
	# }
	#  Описание полей
	#  status:
	#  	ready - задание выполнено без ошибок
	#  	inProgress - выполняется в данный момент
	#  	wait - ожидает выполнения
	#  	error - ошибка выполнения, все следующие за ней в очереди задания будут иметь статус 'interrupted'
	#  	interrupted -  выполнение прервано по причине ошибки одного из заданий до текущего
	#   	blocked - означает, что результат фискальной операции неизвестен(например, потеряна связь с ККТ), веб сервер в режиме восстановления,
	#  	коды ошибок при этом в полях error.Code и error.Description.
	#  result:  зависит от типа отправленной команды ККТ

CommandResponsesAtol = namedtuple('CommandResponsesAtol', ['data', 'date_create'])
FormatResponseAtol = namedtuple('FormatResponseAtol', ['result', 'status', 'error'])
