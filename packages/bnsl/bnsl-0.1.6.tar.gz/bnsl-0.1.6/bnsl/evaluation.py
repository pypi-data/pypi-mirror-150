from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

from .accessory import from_bnlearn

pandas2ri.activate()

base, bnlearn = importr('base'), importr('bnlearn')


# evaluation methods
def compare(target, current):
    '''

    :param target: true CPDAG
    :param current: learned CPDAG
    :return: a dictionary contains TP, FP, FN and f1
    '''

    compare_dict = {}
    tp = 0
    fp = 0
    fn = 0
    for key, value in target.items():
        for par in value['par']:
            if par in current[key]['par']:
                tp = tp + 1
            else:
                fn = fn + 1
        for nei in value['nei']:
            if nei in current[key]['nei']:
                tp = tp + 0.5
            else:
                fn = fn + 0.5
    for key, value in current.items():
        for par in value['par']:
            if par not in target[key]['par']:
                fp = fp + 1
        for nei in value['nei']:
            if nei not in target[key]['nei']:
                fp = fp + 0.5

    compare_dict['tp'] = tp
    compare_dict['fp'] = fp
    compare_dict['fn'] = fn
    compare_dict['f1'] = 2 * tp / (2 * tp + fp + fn)
    return compare_dict


def shd(target, current):
    '''
    :param target: true CPDAG
    :param current: learned CPDAG
    :return: the separate SHD score of learned graph
    '''
    target = from_bnlearn(bnlearn.cpdag(target))
    current = from_bnlearn(bnlearn.cpdag(current))
    add = 0
    remove = 0
    reorient = 0
    for key, value in target.items():
        for par in value['par']:
            if par not in current[key]['par']:
                if par not in current[key]['nei'] and key not in current[par]['par']:
                    add += 1
                else:
                    reorient += 1
        for nei in value['nei']:
            if nei not in current[key]['nei']:
                if nei not in current[key]['par'] and key not in current[nei]['par']:
                    add += 0.5
                else:
                    reorient += 0.5
    for key, value in current.items():
        for par in value['par']:
            if (par not in target[key]['par']) and (par not in target[key]['nei']) and (key not in target[par]['par']):
                remove += 1
        for nei in value['nei']:
            if (nei not in target[key]['nei']) and (nei not in target[key]['par']) and (key not in target[nei]['par']):
                remove += 0.5
    return int(add + remove + reorient)


# compute the F1 score of a learned graph given true graph
def f1(dag_true, dag_learned):
    '''
    :param dag_true: true DAG
    :param dag_learned: learned DAG
    :return: the F1 score of learned DAG
    '''
    compare = bnlearn.compare(bnlearn.cpdag(dag_true), bnlearn.cpdag(dag_learned))
    return compare[0][0] * 2 / (compare[0][0] * 2 + compare[1][0] + compare[2][0])


# compute the precision of a learned graph given true graph
def precision(dag_true, dag_learned):
    '''
    :param dag_true: true DAG
    :param dag_learned: learned DAG
    :return: the F1 score of learned DAG
    '''
    compare = bnlearn.compare(bnlearn.cpdag(dag_true), bnlearn.cpdag(dag_learned))
    return compare[0][0] / (compare[0][0] + compare[1][0])


# compute the recall of a learned graph given true graph
def recall(dag_true, dag_learned):
    '''
    :param dag_true: true DAG
    :param dag_learned: learned DAG
    :return: the F1 score of learned DAG
    '''
    compare = bnlearn.compare(bnlearn.cpdag(dag_true), bnlearn.cpdag(dag_learned))
    return compare[0][0] / (compare[0][0] + compare[2][0])