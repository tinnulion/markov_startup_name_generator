INPUT = r'D:\Repositories\NameProposal\names_clear_57k.txt'
OUTPUT = r'names_superclear.txt'

def destroy_sign(c):
    if c.isalpha() or c.isdigit():
        return c
    else:
        return ' '

def destroy_signs(line):
    norm_line = [destroy_sign(c) for c in line]
    norm_line = ''.join(norm_line)
    norm_line = norm_line.strip()
    return norm_line

def normalize(line):
    line = line.lower()
    line = destroy_signs(line)
    return line

def is_nice_name(name, freq):
    if len(name) < 4:
        return False
    if freq > 1:
        return False
    return True

if __name__ == '__main__':
    histogram = {}
    with open(INPUT, 'r') as f:
        for line in f:
            norm_line = normalize(line)
            items = norm_line.split(' ')
            for item in items:
                if item in histogram:
                    histogram[item] += 1
                else:
                    histogram[item] = 1

    result = []
    keys = sorted(histogram.keys())
    for startup_name in keys:
        freq = histogram[startup_name]
        if is_nice_name(startup_name, freq):
            result.append(startup_name)

    with open(OUTPUT, 'w') as f:
        for item in result:
            f.write(item + '\n')