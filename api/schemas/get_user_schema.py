GET_USER_INFOR_SUCCESS_SCHEMA = {
    "type": "object",
    "required": ["id","email","name","avatarUrl","phone","address"],
    "properties": {
        "id":{"type": "string"},
        "email":{"type": "string"},
        "name":{"type": "string"},
        "avatarUrl":{"type": "string"},
        "phone":{"type": "string"},
        "address":{"type": "string"},
  }
}
GET_USER_LIST_SUCCESS_SCHEMA = {
    "type": "object",
    "required":["list","pagination"],
    "properties":{
        "list":{
            "type": "array",
            "items":{
                "type": "object",
                "required":["id","email","name","avatarUrl","phone","address","isActive","createdAt","updatedAt"],
                "properties":{
                    "id":{"type": "string"},
                    "email":{"type": "string"},
                    "name":{"type": "string"},
                    "avatarUrl":{"type": "string"},
                    "phone":{"type": "string"},
                    "address":{"type": "string"},
                    "isActive":{"type": "boolean"},
                    "createdAt":{"type": "string"},
                    "updatedAt":{"type": "string"},
                }
            }
        },
        "pagination":{
            "type":"object",
            "required":["total","totalPage","currentPage","lengthData"],
            "properties":{
                "total":{"type": "integer"},
                "totalPage":{"type": "integer"},
                "currentPage":{"type": "integer"},
                "lengthData":{"type": "integer"},
            }


        }

    }
}
DELETE_USER_SUCCESS_SCHEMA = {
    "type": "object",
    "required":["msg"],
    "properties":{
        "msg":{"type": "string"},
    }
}