import random
import pickle

ALPHABET = 'abcdefghijklmnopqrstuvwxyz01234567890'
STOP = '#'
INPUT = r'D:\Repositories\NameProposal\names_superclear.txt'

class MarkovChain:

    _prefix_size = 1
    _mapping = {}

    def __init__(self, prefix_size):
        self._prefix_size = prefix_size
        self._mapping = {}

    def _generate_n_grams(self, sample):
        result = []
        for i in range(len(sample) - self._prefix_size):
            prefix = sample[i:i+self._prefix_size]
            suffix = sample[i+self._prefix_size]
            result.append((prefix, suffix))
        prefix = sample[-self._prefix_size:]
        suffix = STOP
        result.append((prefix, suffix))
        return result

    def _train_by_sample(self, sample):
        data = self._generate_n_grams(sample)
        for item in data:
            prefix = item[0]
            suffix = item[1]
            if not (prefix in self._mapping):
                self._mapping[prefix] = {}
            suffix_dict = self._mapping[prefix]
            if suffix in suffix_dict:
                suffix_dict[suffix] += 1
            else:
                suffix_dict[suffix] = 1

    def train(self, filename):
        samples = None
        with open(filename) as f:
            samples = f.readlines()
        for sample in samples:
            sample = sample.strip('\n')
            self._train_by_sample(sample)

    def get_random_symbol(self):
        return random.choice(ALPHABET)

    def do_random_walk(self, prefix):
        if prefix in self._mapping:
            suffix_dict = self._mapping[prefix]
            sum = 0
            for key, value in suffix_dict.items():
                sum += value
            coin = random.randint(0, sum - 1)
            sum = 0
            for key, value in suffix_dict.items():
                sum += value
                if sum > coin:
                    return key
        else:
            return None

    def extend_step(self, init_str):
        if len(init_str) < self._prefix_size:
            raise Exception('Initial sequence too short!')
        prefix = init_str[-self._prefix_size:]
        suffix = self.do_random_walk(prefix)
        return suffix

    def dream_one_char(self, init_str):
        if len(init_str) < self._prefix_size:
            return None
        result = self.extend_step(init_str)
        return result

    def dream(self, init_str='', size=-1):
        if len(init_str) < self._prefix_size:
            raise Exception('Initial sequence too short!')
        result = init_str
        while len(result) < size:
            suffix = self.extend_step(result)
            if suffix is None:
                break
            result += suffix
            if suffix == STOP:
                break
        return result

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print('Saved to:', filename)

    @staticmethod
    def load(filename):
        model = None
        with open(filename, 'rb') as f:
            model = pickle.load(f)
        return model

if __name__ == '__main__':
    print('Train model 1...')
    model_1 = MarkovChain(1)
    model_1.train(INPUT)
    model_1.save('model_1.dat')

    print('Train model 2...')
    model_2 = MarkovChain(2)
    model_2.train(INPUT)
    model_2.save('model_2.dat')

    print('Train model 3...')
    model_3 = MarkovChain(3)
    model_3.train(INPUT)
    model_3.save('model_3.dat')

    print('Train model 4...')
    model_4 = MarkovChain(4)
    model_4.train(INPUT)
    model_4.save('model_4.dat')