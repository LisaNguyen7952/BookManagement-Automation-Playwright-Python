LOGIN_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["msg", "accessToken","exo"],
    "properties": {
        "msg": {"type": "string"},
        "accessToken": {"type": "string"},
        "exo": {"type": "string"}
        
    }
}
LOGIN_FAIL_SCHEMA = {
    "type": "object",
    "required": ["msg", "fields"],
    "properties": {
        "msg": {"type": "string"},
        "fields": {"type": "array"}
    }
}