GET_FILES_SCHEMA = {
    "type": "object",
    "required":["list"],
    "properties":{
        "list":{
        "type":"array",
        "items":{
            "type":"object",
            "required":["name","path","isFile","size","type","modified","created"],
            "properties":{
                "name":{"type":"string"},
                "path":{"type":"string"},
                "isFile":{"type":"boolean"},
                "size":{"type":"integer"},
                "type":{"type":"string"},
                "modified":{"type":"string"},
                "created":{"type":"string"},
            }
        }
        }
    }

}