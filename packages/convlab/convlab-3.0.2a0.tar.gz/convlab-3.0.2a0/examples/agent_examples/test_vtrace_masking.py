
from convlab.dst.rule.multiwoz import RuleDST
from convlab.policy.vtrace_rnn_action_embedding import VTRACE_RNN
from convlab.policy.rule.multiwoz import RulePolicy
from convlab.dialog_agent import PipelineAgent
from convlab.util.analysis_tool.analyzer import Analyzer
import random
import numpy as np
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser


def set_seed(r_seed):
    random.seed(r_seed)
    np.random.seed(r_seed)


def test_end2end(seed=20200202, n_dialogues=1000):

    # Dialogue System
    sys_nlu = None
    sys_dst = RuleDST()
    sys_policy = VTRACE_RNN(use_masking=True)
    #sys_policy.load('convlab/policy/vtrace_rnn_action_embedding/vtrace_RL_trained/save/vtrace_rnn')
    sys_policy.load('convlab/policy/vtrace_rnn_action_embedding/unshrinked_RNN_supervised')
    sys_nlg = None
    sys_agent = PipelineAgent(sys_nlu, sys_dst, sys_policy, sys_nlg, name='sys')

    # User Simulator
    user_nlu = None
    user_dst = None
    user_policy = RulePolicy(character='usr')
    user_nlg = None
    user_agent = PipelineAgent(user_nlu, user_dst, user_policy, user_nlg, name='user')

    analyzer = Analyzer(user_agent=user_agent, dataset='multiwoz')

    set_seed(seed)
    name=f'VtraceRNN_supervised_masked'
    analyzer.comprehensive_analyze(sys_agent=sys_agent, model_name=name, total_dialog=n_dialogues)


if __name__ == '__main__':
    # Get arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('--seed', help='Seed', default=20200202, type=int)
    parser.add_argument('--n_dialogues', help='Number of eval dialogues', default=50, type=int)
    args = parser.parse_args()

    test_end2end(seed=args.seed, n_dialogues=args.n_dialogues)
