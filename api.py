import json
import sys
from collections import namedtuple
from datetime import datetime
from flask import Flask, request, jsonify
from atol import Atol
from command_cycle import cmd_atol
from enum import AtolCmdStatus

flaskApp = Flask(__name__)
SERVER_PORT = 16732
ATOL_URL_BASE = '/api/v2/requests'

def flaskRoutes(queue):
    @flaskApp.route('/')
    def default():
        atol = Atol()

        try:
            resInit = atol.init()

            if resInit:
                res = atol.info()
                model = atol.getModel()

                return (f'<div>Atol Web Server started</div>'
                        f'<div>version: {res.version}</div>'
                        f'<div>opened: {res.isOpened}</div>'
                        f'<div><p>{res.settings}</p></div>'
                        '</br>'
                        f'<div>model KKT: {model.name}</div>'
                        )
            else:
                return 'No Atol connection'
        except Exception:
            return f'Error {Exception}'
        finally:
            atol.close()

    # Protocol Атол HTTP server
    @flaskApp.route(ATOL_URL_BASE, methods=['POST'])
    def v2_requests():
        # Получаем параметры из тела запроса
        res = request.get_json()
        uuid = res.get("uuid")
        dat = res.get("request")
        print(f"Receive command {uuid}")
        print(dat)

        if not dat:
            return jsonify({"error": "Отсутствуют данные в теле запроса"}), 400

        cmd_atol.put(CommandAtol(uuid=uuid, json_cmd = dat[0], status=AtolCmdStatus.WAITING, date_create=datetime.now()))
        return jsonify(uuid), 200

    @flaskApp.route(f'{ATOL_URL_BASE}/<uuid>', methods=['GET'])
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

CommandAtol = namedtuple('CommandAtol', ['uuid','json_cmd', 'status', 'date_create'])
CommandResponsesAtol = namedtuple('CommandResponsesAtol', ['data', 'date_create'])
FormatResponseAtol = namedtuple('FormatResponseAtol', ['result', 'status', 'error'])
