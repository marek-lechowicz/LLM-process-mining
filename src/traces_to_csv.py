def convert_traces_to_csv(traces):
    csv = []
    csv.append('case:concept:name,concept:name')
    for trace_idx, trace in enumerate(traces):
        for entry_idx, entry in enumerate(trace):
            csv.append(f'{trace_idx},{entry}')

    return '\n'.join(csv)


if __name__ == '__main__':
    traces = [
        ['A', 'B', 'C', 'E'],
        ['A', 'C', 'B', 'E'],
        ['A', 'D', 'E']
    ]

    csv = convert_traces_to_csv(traces)
    print(csv)
