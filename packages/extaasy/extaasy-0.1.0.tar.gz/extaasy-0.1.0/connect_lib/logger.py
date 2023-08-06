#
# This file is part of the Ingram Micro CloudBlue Connect EaaS Extension Library.
#
# Copyright (c) 2022 Ingram Micro. All Rights Reserved.
#

"""
This module implements the logger capabilities
"""

from copy import deepcopy
from logging import Logger, LoggerAdapter
from typing import Any, Dict, List, Tuple, Union

from . import consts

__masked_fields: Tuple[str]
__masked_params: Tuple[str]


def masked_fields(fields: Union[List[str], Tuple[str]]) -> None:
    global __masked_fields
    __masked_fields = tuple(fields)


def mask_fields(data: Union[Dict, List, Tuple, Any]) -> Union[Dict, List, Tuple, Any]:
    if isinstance(data, dict):
        return __mask_dict(data)
    elif isinstance(data, (list, tuple)):
        return [mask_fields(x) for x in data]
    else:
        return data


def __mask_dict(data: Dict) -> Dict:
    data = deepcopy(data)
    for k in data.keys():
        if k in __masked_fields:
            data[k] = '*' * len(str(data[k]))
    for k in data.keys():
        data[k] = mask_fields(data[k])
    return data


def masked_params(params: Union[List[str], Tuple[str]]) -> None:
    global __masked_params
    __masked_params = tuple(params)


def mask_params(data: Union[Dict, List, Tuple, Any]) -> Union[Dict, List, Tuple, Any]:
    if isinstance(data, dict):
        return __mask_params_dict(data)
    elif isinstance(data, (list, tuple)):
        return [mask_params(x) for x in data]
    else:
        return data


def __mask_params_dict(data: Dict) -> Dict:
    data = deepcopy(data)
    for k in data.keys():
        value = data[k]
        if k == consts.PARAMS and isinstance(value, list):
            data[k] = __mask_params_list(value)
        elif k == consts.PARAMETER and consts.VALUE in data:
            data[k] = __mask_config_param(data, value)
        elif isinstance(value, (dict, list, tuple)):
            data[k] = mask_params(value)
    for k in data.keys():
        data[k] = mask_params(data[k])
    return data


def __mask_params_list(params: List) -> List:
    return [__mask_param(p) for p in params]


def __mask_param(param: Any) -> Any:
    if isinstance(param, dict) and consts.ID in param and consts.VALUE in param:
        is_password = param[consts.TYPE] == consts.PASSWORD if consts.TYPE in param else False
        if is_password or str(param[consts.ID]) in __masked_params:
            param[consts.VALUE] = '*' * len(str(param[consts.VALUE]))
    return param


def __mask_config_param(parent: Dict, param: Any) -> Any:
    if isinstance(param, dict) and consts.ID in param:
        is_password = param[consts.TYPE] == consts.PASSWORD if consts.TYPE in param else False
        if is_password or str(param[consts.ID]) in __masked_params:
            if consts.VALUE in parent:
                parent[consts.VALUE] = '*' * len(str(parent[consts.VALUE]))
            if consts.VALUE in param:
                param[consts.VALUE] = '*' * len(str(param[consts.VALUE]))
    return param


class ExtensionLoggerAdapter(LoggerAdapter):
    """
    Wrapper around the EaaS logger
    Used to add extra fields to the message
    """

    def __init__(self, logger: Logger, extra: dict, request_id: str):
        self.request_id = request_id
        # mask header 'Authorization' and token value from an API response
        masked_fields([consts.AUTHORIZATION, consts.TOKEN])
        super().__init__(logger, extra)

    def process(self, msg, kwargs):
        task_id = ''
        if consts.TASK_ID in self.extra:
            task_id = f'[{self.extra[consts.TASK_ID]}] '

        request_id = ''
        if self.request_id:
            request_id = f'[{self.request_id}] '

        msg = f'{task_id}{request_id}{msg}'
        return super().process(msg, kwargs)
