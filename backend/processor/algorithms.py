import numpy as np
from .models import Processor


def get_k_objects(k: int, fields: list[str], algorithm: str, aggr_func: str) -> tuple[int, list]:
    match algorithm:
        case 'naive':
            return get_k_naive(k, fields, get_aggr_func(aggr_func))

def get_k_naive(k: int, fields: list[str], aggr_func) -> tuple[int,list]:
    processors = list(Processor.objects.all())
    processors_rank = []

    for processor in processors:
        fieldValues = []
        for field in fields:
            fieldName, order = field.split('_')
            fieldName += '_normalized'
            fieldValue = getattr(processor, fieldName) if order == 'desc' else abs(1 - getattr(processor, fieldName))
            fieldValues.append(fieldValue)
        processors_rank.append([processor, aggr_func(fieldValues)])
    processors_rank.sort(key=lambda pair: pair[1], reverse=True)

    return len(processors), list(np.array(processors_rank[:k])[:, 0])

def get_aggr_func(aggr_func: str):
    match aggr_func:
        case 'sum':
            return sum
        case 'max':
            return max
        case 'min':
            return min
        #fixme: add avg option