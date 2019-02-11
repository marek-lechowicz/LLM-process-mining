def read_input_file(file_name):
    with open(file_name) as file:
        file_contents = file.read().splitlines()
        file_contents = list(map(lambda line: line.strip(), file_contents))

        idx = 0

        def read_line():
            nonlocal idx
            while idx < len(file_contents):
                line = file_contents[idx]
                # skip comments
                if line.startswith('#'):
                    idx += 1
                    continue
                # skip beginning empty lines
                if line == '':
                    idx += 1
                    continue

                idx += 1
                return [x.strip() for x in line.split(',')]

        def read_matrix():
            nonlocal idx
            result = []
            while idx < len(file_contents):
                line = file_contents[idx]
                # skip comments
                if line.startswith('#'):
                    idx += 1
                    continue
                # skip beginning empty lines
                # or end reading rows on empty line
                if line == '':
                    idx += 1
                    if len(result) > 0:
                        break
                    else:
                        continue

                idx += 1
                result.append([x.strip() for x in line.split(',')])
            return result

        s_0 = read_line()
        m_tc = read_matrix()
        m_te = read_matrix()
        m_st = read_matrix()

        return (s_0, m_tc, m_te, m_st)
