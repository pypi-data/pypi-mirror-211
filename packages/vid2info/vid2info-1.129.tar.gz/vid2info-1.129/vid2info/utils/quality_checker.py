from __future__ import annotations
import yaml
import os

class QualityChecker:
    def __init__(self, config_yaml: str):
        assert os.path.isfile(config_yaml), f"File {config_yaml} does not exist."

        with open(config_yaml, 'r') as f:
            config = yaml.load(f, Loader=yaml.FullLoader)

        self.config = self.__parse_config(config=config)


    def __parse_config(self, config: dict):
        """
        Takes a dictionary in the format {config_<i>: {apply_to: [list_of_class_names], <key_1>: <value_1>, ...}, ...}
        to the format: {<class_name_1>: {<key_1>: <value_1>, ...}, ...}

        NOTE: If a property is defined twice for the same class, the last definition is used. (As happens in CSS)

        :param config: dict. The config dictionary.
        :return: dict. The parsed config dictionary.
        """
        parsed_config = {}

        for config_key, config_values in config.items():
            # Extract class names
            class_names = config_values.pop('apply_to', [])
            # For each class, assign config values
            for class_name in class_names:
                if class_name not in parsed_config:
                    parsed_config[class_name] = {}
                parsed_config[class_name].update(config_values)
        return parsed_config

    def check(self, values: dict[str, float], class_name:str) -> tuple[bool | None, tuple]:
        if class_name not in self.config:
            return None, ()
        fails = []
        for key, value in self.config[class_name].items():
            min_value, max_value = value['min'], value['max']
            # If any is None, it means that there is no limit for that property
            if min_value is not None and values[key] < min_value or \
                max_value is not None and values[key] > max_value:
                fails.append(key)
        return len(fails) == 0, tuple(fails)






