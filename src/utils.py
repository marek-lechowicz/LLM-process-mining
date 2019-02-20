from os.path import join, exists, basename, splitext, dirname

def convert_traces_to_csv(traces):
    csv = []
    csv.append('case:concept:name,concept:name')
    for trace_idx, trace in enumerate(traces):
        for entry_idx, entry in enumerate(trace):
            csv.append(f'{trace_idx},"{entry}"')
    return '\n'.join(csv)


def name_tasks(log, task_names):
    task_names = ['dummy'] + task_names
    log_with_named_tasks = []
    for s in log:
        trace, _, last = s
        trace = trace[0:last]
        trace = list(map(lambda x: task_names[x], trace))
        log_with_named_tasks.append(trace)
        print(trace)
    return log_with_named_tasks


def get_task_names(input_file, task_count):
    base = basename(input_file)
    name = splitext(base)[0]
    directory = dirname(input_file)
    task_names_file = join(directory, name + '.task_names')
    if exists(task_names_file):
        with open(task_names_file) as file:
            file_contents = file.read().splitlines()
            file_contents = list(map(lambda line: line.strip(), file_contents))
            assert len(file_contents) == task_count
            return file_contents
    else:
        return [chr(65 + i) for i in range(0, task_count)] # [A, B, C, ... ]

