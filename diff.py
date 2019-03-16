file_a_path = 'lib/browser.py'
file_b_path = 'Executable/lib/browser.py'

with open(file_a_path, 'rt', encoding='utf-8') as file_a:
    with open(file_b_path, 'rt', encoding='utf-8') as file_b:

        line = 0
        different_lines = []
        a_prev, b_prev = None, None
        print('Comparing {} with {}'.format(file_a_path, file_b_path))

        for a, b in zip(file_a, file_b):

            line += 1

            if a.strip() != b.strip():

                if a_prev == None:
                    different_lines.append(line)
                else:
                    if a != b_prev and b != a_prev:
                        different_lines.append(line)

            a_prev, b_prev = a, b

        print('Different Lines: {}'.format(different_lines))
