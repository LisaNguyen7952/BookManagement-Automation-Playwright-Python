GET_BOOK_CATEGORY_LIST_SCHEMA = {
    "type":"object",
    "required":["list","pagination"],
    "properties":{
        "list":{
            "type":"array",
            "items":{
                "type":"object",
                "required":["name","bookCount"],
                "properties":{
                    "name":{"type":"string"},
                    "bookCount":{"type":"integer"},
                }
            }

        },
        "pagination":{
            "type":"object",
            "required":["total"],
            "properties":{
                "total":{"type":"integer"},
            }
        }
    }

}