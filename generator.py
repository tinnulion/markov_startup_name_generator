import random
from markov_model import MarkovChain

def dream_smart_way(init_seq, model_1, model_2, model_3, model_4):
    result = init_seq
    if len(result) == 0:
        result = model_1.get_random_symbol()
    while result[-1] != '#':
        if len(result) >= 32:
            break
        coin = random.uniform(0, 1)
        if coin > 0.2:
            new_char = model_4.dream_one_char(result)
            if not (new_char is None):
                result += new_char
                continue
        if coin > 0.1:
            new_char = model_3.dream_one_char(result)
            if not (new_char is None):
                result += new_char
                continue
        if coin > 0.05:
            new_char = model_2.dream_one_char(result)
            if not (new_char is None):
                result += new_char
                continue
        new_char = model_1.dream_one_char(result)
        if not (new_char is None):
            result += new_char
            continue
        result += model_1.get_random_symbol()
    return result

if __name__ == '__main__':
    model_1 = MarkovChain.load('model_1.dat')
    model_2 = MarkovChain.load('model_2.dat')
    model_3 = MarkovChain.load('model_3.dat')
    model_4 = MarkovChain.load('model_4.dat')

    while True:
        init_seq = input('Init sequence (type EXIT to exit): ')
        if init_seq == 'EXIT':
            break
        for i in range(20):
            result = dream_smart_way(init_seq, model_1, model_2, model_3, model_4)
            if result != init_seq + '#':
                print('  My dream: ' + result)


