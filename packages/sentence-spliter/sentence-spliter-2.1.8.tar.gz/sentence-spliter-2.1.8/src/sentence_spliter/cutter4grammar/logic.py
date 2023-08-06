# -*- coding:utf-8 -*-
# CREATED BY: jiangbohuai
# CREATED ON: 2021/11/16 10:18 AM
# LAST MODIFIED ON:
# AIM:
from sentence_spliter.architect.graph_component import Graph
import sentence_spliter.cutter4grammar.condition as cond
import sentence_spliter.cutter4grammar.operation as opt
from sentence_spliter.cutter4grammar.long_handler import LongHandler, Operation


class SimpleLogic(Graph):
    def __init__(self, name: str = 'SimpleLogic'):
        super(SimpleLogic, self).__init__(name)

    def init_conditions(self):
        self.is_end_state = cond.IsEndState()
        self.is_end_symbol = cond.IsEndSymbol()
        self.is_bracket_close = cond.IsBracketClose()
        self.is_quota_close = cond.IsQuotaClose().add_and(cond.IsSingleQuotaClose())
        self.not_in_white_list = cond.TokenInWhiteList(reverse=True)
        self.next_start_with_capital_or_Num = cond.NextStartWithCapital(name='NextStartWithCapitalOrNum').add_or(
            cond.NextStartWithNum())
        self.not_number_dot = cond.IsNumberDot(name='NotNumberDot', reverse=True)
        self.is_next_quota_and_symbol = cond.IsNextQuotaAndSymbol()

    def init_operations(self):
        self.init_state = opt.Indolent()
        self.end_state = opt.EndState()
        self.proceed_state = opt.Proceed()
        self.cut_state = opt.Cut()

    def build_logic(self) -> 'Operation':
        self.init_state \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.cut_state, [self.is_next_quota_and_symbol], args=all) \
            .add_child(self.cut_state,
                       [self.is_bracket_close, self.next_start_with_capital_or_Num,
                        self.not_in_white_list, self.is_end_symbol, self.not_number_dot],
                       args=all) \
            .add_child(self.proceed_state)

        self.proceed_state \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.init_state)

        self.cut_state \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.init_state)
        return self.init_state


class LongShortLogic(Graph):
    def __init__(self, name: str = 'LongShortLogic', max_len: int = 40, min_len: int = 6, hard_max: int = -1):
        self.max_len = max_len
        self.min_len = min_len
        self.hard_max = hard_max
        super(LongShortLogic, self).__init__(name)

    def init_conditions(self):
        is_right_before_left_quota = cond.IsRightBeforeLeftQuota().add_and(cond.RightQuotaAfterEnd())

        self.is_end_state = cond.IsEndState()
        self.is_end_symbol = cond.IsEndSymbol().add_or(is_right_before_left_quota)
        self.is_bracket_close = cond.IsBracketClose()
        self.is_quota_close = cond.IsQuotaClose().add_and(cond.IsSingleQuotaClose())
        self.not_in_white_list = cond.TokenInWhiteList(name='NotInWhiteList', reverse=True)
        self.next_start_with_capital_or_num = cond.NextStartWithCapital(name='NextStartWithCapitalOrNum') \
            .add_or(cond.NextStartWithNum()) \
            .add_or(is_right_before_left_quota) \
            .add_or(cond.IsNearestLeftQuota())
        self.not_short_sentence = cond.IsShortSentence(name='NotShortSentence', reverse=True)
        self.is_long_sentence = cond.IsLongSentence(max_length=self.max_len)
        # if self.hard_max < 0:+
        self.is_max_long = cond.IsLongSentence(max_length=self.hard_max,
                                               name='harmax') if self.hard_max > 0 else self.is_long_sentence
        self.not_number_dot = cond.IsNumberDot(name='NotNumberDot', reverse=True)
        self.is_blank = cond.IsBlank()

    def init_operations(self):
        self.init_state = opt.Indolent()
        self.reset_num_words = opt.ResetNumWords()
        self.end_state = opt.EndState(min_length=self.min_len)
        self.proceed_state = opt.Proceed()
        self.cut_state = opt.Cut()
        self.long_state = LongHandler(max_len=self.max_len, min_len=self.min_len)

    def build_logic(self) -> Operation:
        self.init_state \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.cut_state,
                       [self.is_quota_close, self.is_bracket_close, self.next_start_with_capital_or_num,
                        self.not_in_white_list, self.not_short_sentence,
                        self.is_end_symbol, self.not_number_dot],
                       args=all) \
            .add_child(self.proceed_state, self.is_blank) \
            .add_child(self.long_state, self.is_long_sentence) \
            .add_child(self.proceed_state)

        self.proceed_state \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.init_state)

        self.cut_state \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.init_state)

        self.long_state \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.cut_state, self.is_max_long) \
            .add_child(self.reset_num_words, self.is_long_sentence) \
            .add_child(self.init_state)

        self.reset_num_words \
            .add_child(self.end_state, self.is_end_state) \
            .add_child(self.init_state)

        return self.init_state
