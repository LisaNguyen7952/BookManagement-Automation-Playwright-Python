GET_400_ERROR_SCHEMA = {
    "type": "object",
    "required": ["error","msg"],
    "properties": {
        "error":{"type": "string"},
        "msg":{"type": "string"},
    }

}
GET_422_ERROR_SCHEMA = {
    "type": "object",
    "required": ["fields","msg"],
    "properties": {
        "fields":{"type": "string"},
        "msg":{"type": "string"},
    }
}
NORMAL_RESPONSE_SCHEMA = {
    "type": "object",
    "required": ["msg"],
    "properties": {
        "msg":{"type": "string"},
    }
}