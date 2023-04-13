import numpy as np
from .models import Processor
from .serializers import ProcessorSerializer


def get_k_objects(k: int, fields: list[str], algorithm: str, aggr_func: str) -> tuple[int, list[ProcessorSerializer]]:
    """"
    fieldsList = []
    for field in fields:
        fieldName, order = field.split('_')
        fieldName += '_normalized'
        orderSign = '' if order == 'asc' else '-'
        fieldList = list(Processor.objects.values_list('id', fieldName).order_by(orderSign + fieldName))
        fieldsList.append(fieldList)
    """
    rowsRead, ids = (0, [])
    match algorithm:
        case 'naive':
            rowsRead, ids = get_k_naive(k, fields, get_aggr_func(aggr_func))
    processors = []
    for processorId in ids:
        processors.append(ProcessorSerializer(Processor.objects.get(pk=processorId)).data)
    return rowsRead, processors

def get_k_naive(k: int, fields: list[str], aggr_func) -> tuple[int,list[int]]:
    processors = list(Processor.objects.values())
    processors_rank = []
    for processor in processors:
        fieldValues = []
        for field in fields:
            fieldName, order = field.split('_')
            fieldName += '_normalized'
            fieldValue = processor[fieldName] if order == 'desc' else abs(1 - processor[fieldName])
            fieldValues.append(fieldValue)
        processors_rank.append([processor['id'], aggr_func(fieldValues)])
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