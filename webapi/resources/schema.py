DATASET_SCHEMA = {
    "is_public": {"type": "boolean"},
    "meta":{
        "title": {
            "type": "string",
                "minLength":1,
                "maxLength":128
        },
        "description": {
            "type": "string",
            "maxLength": 4096
        },
        "category": {
            "type": "string",
            "maxLength": 64
        },
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength":64
            },
            "uniqueItems": True
        }
    },
}

MODEL_SCHEMA = {
    "is_public": {"type": "boolean"},
    "meta":{
        "title": {
            "type": "string",
            "minLength": 1,
            "maxLength": 128
        },
        "description": {
            "type": "string",
            "maxLength": 4096
        },
        "category": {
            "type": "string",
            "maxLength": 64
        },
        "labels": {
            "type": "array",
            "items": {
                "type": "string",
                "maxLength": 64
            },
            "uniqueItems": True
        },
        "architecture": {
            "type": "string",
            "maxLength": 128
        },
        "dataset": {
            "type": "string",
            "maxLength": 128
        }
    }
}

