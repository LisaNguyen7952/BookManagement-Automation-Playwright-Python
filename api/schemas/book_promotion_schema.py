GET_BOOK_PROMOTION_LIST_SCHEMA = {
    "type": "object",
    "required": ["list","pagination"],
    "properties": {
        "list": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id","code","name","description",
                             "type","value","startDate","endDate","isActive","createdAt","updatedAt","countBooks"],
                "properties": {
                    "id": {"type": "string"},
                    "code": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "type": {"type": "string"},
                    "value": {"type": "integer"},
                    "startDate": {"type": "string"},
                    "endDate": {"type": "string"},
                    "isActive": {"type": "boolean"},
                    "createdAt": {"type": "string"},
                    "updatedAt": {"type": "string"},
                    "countBooks": {"type": "integer"}
                }
            }
        },
        "pagination": {
            "type": "object",
            "required": ["total","totalPage","currentPage","lengthData"],
            "properties": {
                "total": {"type": "integer"},
                "totalPage": {"type": "integer"},
                "currentPage": {"type": "integer"},
                "lengthData": {"type": "integer"}
            }
        }
    }


}
GET_SPECIFIC_BOOK_PROMOTION_SCHEMA = {
    "type": "object",
    "required":["id","code","name","description","type","value","startDate","endDate","isActive","createdAt","updatedAt","books"],
    "properties": {
        "id": {"type": "string"},
        "code": {"type": "string"},
        "name": {"type": "string"},
        "description": {"type": "string"},
        "type": {"type": "string"},
        "value": {"type": "integer"},
        "startDate": {"type": "string"},
        "endDate": {"type": "string"},
        "isActive": {"type": "boolean"},
        "createdAt": {"type": "string"},
        "updatedAt": {"type": "string"},
        "books": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id","slug","name","description","viewCount","picture","auth"],
                "properties": {
                    "id": {"type": "string"},
                    "slug": {"type": "string"},
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "viewCount": {"type": "integer"},
                    "picture": {"type": "string"},
                    "auth": {
                        "type": "string",
                        "required":["email","name","avatarUrl"],
                        "properties": {
                            "email": {"type": "string"},
                            "name": {"type": "string"},
                            "avatarUrl": {"type": "string"}
                        }
                    }
                }
            }
                  }
    }

}
