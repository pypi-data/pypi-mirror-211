"""
    QuaO Project json_parser_util.py Copyright © CITYNOW Co. Ltd. All rights reserved.
"""
import numpy as np


class JsonParserUtils:

    @staticmethod
    def parse(unparsed_input: dict) -> dict:
        data_holder = {}

        for key, value in unparsed_input.items():
            if isinstance(value, dict):
                data_holder[key] = JsonParserUtils.parse(unparsed_input[key])
            elif isinstance(value, (list, tuple, str, int, float, bool,)) or value is None:
                data_holder[key] = value
            elif isinstance(value, np.ndarray):
                data_holder[key] = value.tolist()
            else:
                data_holder[key] = JsonParserUtils.parse(value.__dict__)

        return data_holder