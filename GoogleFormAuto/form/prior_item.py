import random

from utils.answer_type import AnswerType
from utils.short_inivt_type import ShortInvitType


class PriorItem:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PriorItem, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if PriorItem._initialized:
            return  # 이미 초기화된 경우, 바로 리턴
        # 전체 리스트 저장
        # 타입 / 콤보 리스트
        self.prior_list = []

        # 타입 / 응답 리스트
        self.prior_result = []

        self.etc = ""
        PriorItem._initialized = True

    def add_prior_list(self, item_list):
        self.prior_list.append(item_list)

    def del_prior_list(self, index):
        del self.prior_list[index]

    def print_prior_list(self):
        print(self.prior_list)

    def print_prior_result(self):
        print(self.prior_result)

    def get_prior_list_length(self):
        return len(self.prior_list)

    def get_prior_list_idx(self, idx):
        return self.prior_list[idx]

    def get_prior_result_idx(self, idx):
        return self.prior_result[idx]

    def get_prior_result(self):
        for item in self.prior_list:
            if item[0] == AnswerType.RADIO:
                self.get_prior_result_radio(item)
            if item[0] == AnswerType.RADIO2:
                self.get_prior_result_radio2(item)
            if item[0] == AnswerType.GRID_RADIO:
                self.get_prior_result_grid(item)
            if item[0] == AnswerType.SHORT_INVIT:
                self.get_prior_result_short_inv(item)

    def get_prior_result_radio(self, item):
        result = [idx for idx, rank in enumerate(item[1]) for _ in range(int(rank))]
        self.prior_result.append([AnswerType.RADIO, random.choice(result)])

    def get_prior_result_radio2(self, item):
        result = []
        for idx, rank in enumerate(item[1]):
            for i in range(0, rank):
                result.append(idx)
        self.prior_result.append([AnswerType.RADIO, result, item[2]])

    def get_prior_result_short_inv(self, item):
        if item[1] == ShortInvitType.MIN_MAX:
            min_val = item[2][0]
            max_val = item[2][1]
            value = random.randint(min_val, max_val)
            self.prior_result.append([AnswerType.RADIO, value])
        else:
            value = item[2]
            self.prior_result.append([AnswerType.RADIO, value])

    def get_prior_result_grid(self, item):
        result = []
        for x in item[1]:
            tmp_list = [idx for idx, rank in enumerate(x) for _ in range(int(rank))]
            result.append(random.choice(tmp_list))
        self.prior_result.append([AnswerType.GRID_RADIO, result])

    def get_prior_result_list(self):
        return self.prior_result

    def init_prior_items(self):
        # self.prior_list.clear()
        self.prior_result = []


