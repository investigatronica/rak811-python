import datetime
import dateutil.parser
carga={"app_id":"temperatura_1-prueba","dev_id":"rak811-esp32-upython-2","hardware_serial":"3530353079377A14","port":2,"counter":5,"payload_raw":"AXQ=","payload_fields":{"2":23.25},"metadata":{"time":"2019-04-22T12:19:28.204145582Z","frequency":903.9,"modulation":"LORA","data_rate":"SF10BW125","airtime":329728000,"coding_rate":"4/5","gateways":[{"gtw_id":"eui-b827ebfffec78bda","timestamp":1690698548,"time":"2019-04-22T12:19:28.011288Z","channel":0,"rssi":-109,"snr":-12.8,"rf_chain":0,"latitude":-27.485186,"longitude":-55.11077,"altitude":40,"location_source":"registry"}]}}
print(carga["payload_fields"]["2"])
print(carga["metadata"]["time"])
#print(datetime.datetime.strptime(carga["metadata"]["time"], "%Y-%m-%dT%H:%M:%S.%s%fZ"))
#print(datetime.datetime.strptime(carga["metadata"]["time"].translate(None, ':-'), "%Y%m%dT%H%M%S.%fZ"))
#print(fromisoformat(carga["metadata"]["time"]))
print(dateutil.parser.parse(carga["metadata"]["time"]))
