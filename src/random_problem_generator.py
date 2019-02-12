import random
from main import process
from os.path import join


def random_list(start, stop, length):
    return [random.randrange(start, stop + 1) for _ in range(0, length)]


def generate_random_problem(tasks_count, data_entities_count, final_states_count):
    s_0 = random_list(0, 1, data_entities_count)
    m_tc = [random_list(-1, 1, data_entities_count)
            for i in range(0, tasks_count)]
    m_te = [random_list(-1, 1, data_entities_count)
            for i in range(0, tasks_count)]
    m_st = [random_list(0, 1, data_entities_count)
            for i in range(0, final_states_count)]

    assert len(m_tc) == len(m_te)

    for row in m_tc:
        assert len(row) == len(s_0)
    for row in m_te:
        assert len(row) == len(s_0)
    for row in m_st:
        assert len(row) == len(s_0)

    return (s_0, m_tc, m_te, m_st)


def problem_as_text(s_0, m_tc, m_te, m_st, traces):
    return '\n'.join([
        '# s_0',
        ', '.join(map(str, s_0)),
        '# m_tc',
        '\n'.join([', '.join(map(str, row)) for row in m_tc]),
        '# m_te',
        '\n'.join([', '.join(map(str, row)) for row in m_te]),
        '# m_st',
        '\n'.join([', '.join(map(str, row)) for row in m_st])
        ])


if __name__ == "__main__":
    problems = []
    while len(problems) < 5:
        s_0, m_tc, m_te, m_st = generate_random_problem(4, 5, 2)
        traces = process(s_0, m_tc, m_te, m_st)
        if len(traces) > 0:
            problem = (s_0, m_tc, m_te, m_st, traces)
            problems.append(problem)
            # print(problem)

    for p in problems:
        problem_text = problem_as_text(*p)
        with open(join('problems', str(random.randint(100000000, 1000000000)) + '.txt'), 'w+') as file:
            file.write(problem_text)
