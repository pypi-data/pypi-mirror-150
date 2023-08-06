from censius import ModelType
from censius import DatasetType

register_model_schema = {
    "type": "object",
    "properties": {
        "dataset_id": {
            "type": "integer"
        },
        "model_id": {
            "type": "string"
        },
        "model_name": {
            "type": "string"
        },
        "model_version": {
            "type": "string"
        },
        "project_id": {
            "type": "integer"
        },
        "type": {
            "type": "string",
            "enum": [ModelType.BINARY_CLASSIFICATION,ModelType.REGRESSION]
        },
        "targets": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "features": {
            "type": "array",
            "items": {
                "type": "string"
            }
        },
        "window_size": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer"
                },
                "unit": {
                    "type": "string",
                    "enum": ["day", "week", "hour"]
                }
            },
            "required": ["number", "unit"]
        },
        "window_start_time": {
            "type": "integer"
        }
    },
    "required": ["dataset_id", "model_id", "model_name", "model_version", "project_id", "type","targets","features"]
}
register_dataset_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "project_id": {
            "type": "integer"
        },
        "features": {
            "type": "array",
            "properties": {
                "name": {
                    "type": "string"
                },
                "type": {
                    "type": "string",
                    "enum": [DatasetType.DECIMAL,DatasetType.INT]
                }
            },
            "required": ["name", "type"]
        },
        "raw_values":{
            "type": "object",
            "properties": {
                "name": {
                    "type": "string"
                },
                "type": {
                    "type": "string",
                    "enum": [DatasetType.DECIMAL,DatasetType.INT,DatasetType.STRING,DatasetType.BOOLEAN]
                }
            },
            "required": ["name", "type"]
        },
        "type": {
            "type": "string",
            "enum":[DatasetType.TRAINING_TYPE,DatasetType.VALIDATION_TYPE]
        },
        "version": {
            "type": "string"
        },
        "timestamp_col": {
            "type": "string"
        },
        "timestamp_type": {
            "type": "string"
        },
        "unix_interval":{
            "type":"string",
            "enum": [DatasetType.UNIX_MS,DatasetType.UNIX_NS,DatasetType.UNIX_S]
        }
        

    },
    "required": ["name", "project_id", "features","type","version"]

}


process_model_schema = {
    "type": "object",
    "properties": {
        "dataset_id": {
            "type": "integer"
        },
        "model_id": {
            "type": "integer"
        },
        "values": {
            "type": "array",
            "properties": {
                "target": {
                    "type": "string"
                },
                "perdiction": {
                    "type": "string"
                }
            },
            "required": ["target"]
        },
        "window_start_time":{
            "type":"integer"
        },
        "window_size": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer"
                },
                "unit": {
                    "type": "string",
                    "enum": ["day", "week", "hour"]
                }
            },
            "required": ["number", "unit"]
        }
    },
    "required": ["dataset_id", "model_id", "values"]
}

revise_model_schema = {
    "type": "object",
    "properties": {
        "model_id": {
            "type": "string"
        },
        "model_version": {
            "type": "string"
        },
        "is_rolling_window_enabled": {
            "type": "boolean"
        },
        "window_size": {
            "type": "object",
            "properties": {
                "number": {
                    "type": "integer"
                },
                "unit": {
                    "type": "string",
                    "enum": ["day", "week", "hour"]
                }
            },
            "required": ["number", "unit"]
        }
    },
    "if": {
        "properties": {
            "is_rolling_window_enabled": {
                "const": True
            }
        }
    },
    "then": {
        "required": ["window_size"]
    },
    "required": ["model_id", "model_version", "is_rolling_window_enabled"]
}

update_actual_schema = {
    "type": "object",
    "properties": {
        "prediction_id": {
            "type": "string"
        },
        "actual": {
            "type": "object"
        },
        "model_version": {
            "type": "string"
        },
        "model_id": {
            "type": "string"
        }
    },
    "required": ["model_id", "model_version", "actual", "prediction_id"]
}

individual_log_schema = {
    "type": "object",
    "properties": {
        "prediction_id": {
            "type": "string"
        },
        "model_version": {
            "type": "string"
        },
        "model_id": {
            "type": "string"
        },
        "features": {
            "type": "object"
        },
        "prediction": {
            "type": "object",
            "patternProperties": {
                ".*": {
                    "type": "object",
                    "label": "integer",
                    "confidence": "integer",
                    "required": ["label", "confidence"]
                }
            }
        },
        "timestamp": {
            "type": "integer"
        },
        "raw_values": {
            "type": "object"
        },
        "actual": {
            "type": "object"
        }
    },
    "required": ["prediction_id", "model_version", "model_id", "features", "prediction", "timestamp"]
}

batch_log_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "prediction_id": {
                "type": "string"
            },
            "model_version": {
                "type": "string"
            },
            "model_id": {
                "type": "string"
            },
            "features": {
                "type": "object"
            },
            "prediction": {
                "type": "object",
                "patternProperties": {
                    ".*": {
                        "type": "object",
                        "label": "integer",
                        "confidence": "integer",
                        "required": ["label", "confidence"]
                    }
                }
            },
            "timestamp": {
                "type": "integer"
            },
            "raw_values": {
                "type": "object"
            },
            "actual": {
                "type": "object"
            }
        },
        "required": ["prediction_id", "model_version", "model_id", "features", "prediction", "timestamp"]
    }
}



register_project_schema={
    "type": "object",
    "properties": {
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string"
        },
        "key": {
            "type": "string"
        },
        "icon": {
            "type": "string"
        }
    },
    "required": ["name"]

}