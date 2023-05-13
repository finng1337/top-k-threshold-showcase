import operator
import numpy as np
import heapq
from .models import Processor

def get_k_threshold(k: int, data: list[Processor], fields: list[str], aggr_func: callable) -> tuple[int,list[Processor]]:
    fieldsList = []
    fieldsIndexes = {}
    for field in fields:
        fieldName, order = field.rsplit('_', 1)
        fieldsList.append((fieldName + '_normalized', order))
        fieldsIndexes[fieldName + '_normalized'] = get_field_index(fieldName, data, order)
    seenIds = set()
    processorRank = []
    readRows = 0
    heapq.heapify(processorRank)

    for i in range(len(fieldsIndexes[fieldsList[0][0]])):
        readRows += 1
        thresholdValues = []
        for field in fieldsList:
            processor = fieldsIndexes[field[0]][i]
            thresholdValues.append(getattr(processor, field[0]) if field[1] == 'desc' else abs(1 - getattr(processor, field[0])))
            if processor.id not in seenIds:
                seenIds.add(processor.id)
                heapq.heappush(processorRank, (get_proc_rank(processor, fieldsList, aggr_func), processor))
                if len(processorRank) > k:
                    heapq.heappop(processorRank)
        threshold = aggr_func(thresholdValues)
        if processorRank[0][0] >= threshold and len(processorRank) >= k:
            return readRows, np.array(heapq.nlargest(k, processorRank))[:, 1]
    return readRows, np.array(heapq.nlargest(k, processorRank))[:, 1]

def get_k_naive(k: int, processors: list[Processor], fields: list[str], aggr_func: callable) -> tuple[int,list[Processor]]:
    processorsRank = []
    fieldsList = []

    for field in fields:
        fieldName, order = field.rsplit('_', 1)
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

def get_field_index(field: str, data_set: list[Processor], order: str) -> list[Processor]:
    fieldName = field + '_normalized'
    reverse = True if order == 'desc' else False

    return sorted(data_set, key=operator.attrgetter(fieldName), reverse=reverse)

def get_aggr_func(aggr_func: str) -> callable:
    match aggr_func:
        case 'sum':
            return sum
        case 'max':
            return max
        case 'min':
            return min