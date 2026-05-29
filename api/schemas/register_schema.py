REGISTER_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["msg"],
    "properties": {
        "msg": {"type": "string"}
    }
}
REGISTER_4XX_SCHEMA = {
    "type": "object",
    "required": ["msg","fields"],
    "properties": {
        "msg": {"type": "string"},
        "fields": {"type": "object"}
    }
}