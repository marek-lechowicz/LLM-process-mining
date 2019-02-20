import random
from os.path import join
from workflow.generator import get_workflow_log


def random_list(start, stop, length):
    return [random.randrange(start, stop + 1) for _ in range(0, length)]


def generate_random_problem(tasks_count, data_entities_count, final_states_count):
    while True:
        s_0 = random_list(0, 1, data_entities_count)
        m_tc = [random_list(-1, 1, data_entities_count)
                for i in range(0, tasks_count)]
        m_te = [random_list(-1, 1, data_entities_count)
                for i in range(0, tasks_count)]
        m_st = [random_list(0, 1, data_entities_count)
                for i in range(0, final_states_count)]
        for i in range(0, final_states_count):
            if s_0 == m_st[i]:
                continue
        break

    e_t = list(map(lambda x: 1, m_tc))

    assert len(m_tc) == len(m_te)

    for row in m_tc:
        assert len(row) == len(s_0)
    for row in m_te:
        assert len(row) == len(s_0)
    for row in m_st:
        assert len(row) == len(s_0)

    return (s_0, m_tc, m_te, m_st, e_t)


def problem_as_text(s_0, m_tc, m_te, m_st, e_t):
    return '\n'.join([
        '# s_0',
        ', '.join(map(str, s_0)),
        '\n',
        '# m_tc',
        '\n'.join([', '.join(map(str, row)) for row in m_tc]),
        '\n',
        '# m_te',
        '\n'.join([', '.join(map(str, row)) for row in m_te]),
        '\n',
        '# m_st',
        '\n'.join([', '.join(map(str, row)) for row in m_st]),
        '# e_t',
        '\n',
        ', '.join(map(str, e_t))
    ])


if __name__ == "__main__":
    problems = []
    while len(problems) < 5:
        s_0, m_tc, m_te, m_st, e_t = generate_random_problem(6, 5, 3)
        traces = get_workflow_log(s_0, m_tc, m_te, m_st, e_t)
        if len(traces) > 3:
            problem = (s_0, m_tc, m_te, m_st, e_t)
            problems.append(problem)
            print(problem)

    for p in problems:
        problem_text = problem_as_text(*p)
        with open(join('problems', str(random.randint(100000000, 1000000000)) + '.txt'), 'w+') as file:
            file.write(problem_text)
        print(problem_text)
        print(p[4])
