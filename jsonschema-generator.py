# -*-coding:utf-8 -*-
import json
import traceback

import jsonschema


def get_jsonschema(json_object):
    jsonschema = {
        "$id": "http://example.com/example.json",
        "type": "object",
        "definitions": {},
        "$schema": "http://json-schema.org/draft-07/schema#"
    }
    try:
        jsonschema["properties"] = prase_jsonschema_prop(json_object)
    except:
        print "get jsonschema failed! %s" % traceback.format_exc()

    return jsonschema


# 根据json对象生成jsonschema
def prase_jsonschema_prop(json_object):
    properties = {}
    if isinstance(json_object, dict):
        for n1 in json_object:
            value = json_object[n1]
            if isinstance(value, dict):
                properties[n1] = {
                    "type": "object",
                    "properties": prase_jsonschema_prop(value)
                }

            # 处理list
            elif isinstance(value, list):
                properties[n1] = {
                    "type": "array",
                }
                # list元素是dict or list
                if isinstance(value[0], (dict, list)):
                    properties[n1]["items"] = {
                        "type": "object",
                        "properties": prase_jsonschema_prop(value[0])
                    }
                elif isinstance(value[0], basestring):
                    properties[n1]["items"] = {"type": "string"}
                elif isinstance(value[0], float):
                    properties[n1]["items"] = {"type": "number"}
                elif isinstance(value[0], bool):
                    properties[n1]["items"] = {"type": "boolean"}
                elif isinstance(value[0], int):
                    properties[n1]["items"] = {"type": "integer"}
                else:
                    properties[n1]["items"] = {"type": "string"}

            elif isinstance(value, basestring):
                properties[n1] = {
                    "type": "string"
                }
            elif isinstance(value, float):
                properties[n1] = {
                    "type": "number"
                }
            elif isinstance(value, bool):
                properties[n1] = {
                    "type": "boolean"
                }
            elif isinstance(value, int):
                properties[n1] = {
                    "type": "integer"
                }
            else:
                properties[n1] = {
                    "type": "string"
                }
    # elif isinstance(json_object, list):
    #     print "list"
    #     properties = {
    #         "type": "array"
    #     }
    # elif isinstance(json_object, basestring):
    #     print "str"
    #     properties = {
    #         "type": "string"
    #     }
    #
    # elif isinstance(json_object, int):
    #     print "int"
    #     properties = {
    #         "type": "integer"
    #     }
    else:
        print "%s 数据类型未知!" % json_object
        properties = {
            "type": "string"
        }
    return properties


if __name__ == "__main__":
    json_object = {
        "DTOList": [
            {
                "DTOSublist": [
                    {
                        "DTOLastlist": [
                            {
                                "id": 1, "name": "lastlist1"
                            }
                        ],
                        "updateTime": "2018-06-01 10:00:00",
                    }
                ],
                "updateTime": "2018-06-01 10:01:00",
            }
        ],
        "updateTime": "2018-06-01 10:00:00",
        "message": {
            "code": 1,
            "data": [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
        }}
    schema = get_jsonschema(json_object)
    print "json schema is : \n%s" % json.dumps(schema)
    try:
        jsonschema.validate(json_object, schema)
        print "validate success."
    except:
        print "validate failed! %s" % traceback.format_exc()
