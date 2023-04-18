import numpy as np
import heapq
from .models import Processor

def get_k_treshold(k: int, fields_indexes: dict[str, list], fields: list[str], aggr_func: callable) -> tuple[int,list]:
    fieldsList = []
    for field in fields:
        fieldName, order = field.split('_', 1)
        fieldsList.append((fieldName + '_normalized', order))
    seenIds = set()
    processorRank = []
    readRows = 0
    heapq.heapify(processorRank)

    for i in range(len(fields_indexes[fieldsList[0][0]])):
        readRows += 1
        tresholdValues = []
        for field in fieldsList:
            processor = fields_indexes[field[0]][i]
            tresholdValues.append(getattr(processor, field[0]) if field[1] == 'desc' else abs(1 - getattr(processor, field[0])))
            if processor.id not in seenIds:
                seenIds.add(processor.id)
                heapq.heappush(processorRank, (get_proc_rank(processor, fieldsList, aggr_func), processor))
                if len(processorRank) > k:
                    heapq.heappop(processorRank)
        treshold = aggr_func(tresholdValues)
        if processorRank[0][0] >= treshold and len(processorRank) >= k:
            return readRows, np.array(heapq.nlargest(k, processorRank))[:, 1]
    return 0, []

def get_k_naive(k: int, processors: list, fields: list[str], aggr_func: callable) -> tuple[int,list]:
    processorsRank = []
    fieldsList = []

    for field in fields:
        fieldName, order = field.split('_', 1)
        fieldsList.append((fieldName + '_normalized', order))

    for processor in processors:
        processorsRank.append((get_proc_rank(processor, fieldsList, aggr_func), processor))
    processorsRank.sort(reverse=True)

    return len(processors), list(np.array(processorsRank[:k])[:, 1])

def get_proc_rank(processor: Processor, fields: list[tuple[str, str]], aggr_func: callable):
    fieldValues = []
    for field in fields:
        fieldValue = getattr(processor, field[0]) if field[1] == 'desc' else abs(1 - getattr(processor, field[0]))
        fieldValues.append(fieldValue)
    return aggr_func(fieldValues)

def get_field_index(field: str, order: str) -> list:
    fieldName = field + '_normalized'
    orderBy = fieldName if order == 'asc' else '-' + fieldName

    match field:
        case 'cores':
            return list(Processor.objects.all().order_by(orderBy))
        case 'threads':
            return list(Processor.objects.all().order_by(orderBy))
        case 'frequency':
            return list(Processor.objects.all().order_by(orderBy))
        case 'boost_frequency':
            return list(Processor.objects.all().order_by(orderBy))
        case 'cache':
            return list(Processor.objects.all().order_by(orderBy))
        case 'lithography':
            return list(Processor.objects.all().order_by(orderBy))
        case 'tdp':
            return list(Processor.objects.all().order_by(orderBy))

def get_aggr_func(aggr_func: str) -> callable:
    match aggr_func:
        case 'sum':
            return sum
        case 'max':
            return max
        case 'min':
            return min
        #fixme: add avg option