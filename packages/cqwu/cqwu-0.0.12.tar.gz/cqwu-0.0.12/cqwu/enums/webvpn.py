from enum import Enum


class ExamRound(str, Enum):
    Supplementation = "1"
    """ 开学补缓考 """
    Scattered = "2"
    """ 分散考试 """
    Concentration = "3"
    """ 集中考试 """
