from os.path import join

from pm4py.visualization.bpmn import visualizer as bpmn_vis_factory
from pm4py.objects.bpmn.exporter import exporter as bpmn_exporter
from pm4py.visualization.petri_net import visualizer as pn_vis_factory
from pm4py.convert import convert_to_event_log, convert_to_bpmn
import pm4py

import pandas as pd

def import_csv(csv_path):
    df = pd.read_csv(csv_path)
    # rename columns to case and activity
    df.columns = ['CaseID', 'Activity']
    # dummy add timestamp column
    df['Timestamp'] = pd.to_datetime('now')
    # convert case and activity to string
    df['CaseID'] = df['CaseID'].astype(str)
    df['Activity'] = df['Activity'].astype(str)
    df = pm4py.format_dataframe(df, case_id='CaseID', activity_key='Activity', timestamp_key='Timestamp')
    return convert_to_event_log(df)

def explore_process(name, csv_path, miner, miner_name):
    event_log = import_csv(csv_path)

    if miner_name == 'alpha_miner':
        net, initial_marking, final_marking = miner.apply(event_log)
        gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
        pn_vis_factory.save(gviz, join('solutions', name + '_' + miner_name + '_petri_net.png'))
        pn_vis_factory.save(gviz, join('solutions', name + '_' + miner_name + '_petri_net.pdf'))
        bpmn_graph = convert_to_bpmn(net, initial_marking, final_marking)
    elif miner_name == 'inductive_miner':
        process_tree = miner.apply(event_log)
        bpmn_graph = convert_to_bpmn(process_tree)
    else:
        raise ValueError('Unknown miner name')

    bpmn_exporter.apply(bpmn_graph, join('solutions', name + '_' + miner_name + '.bpmn'))
    bpmn_figure = bpmn_vis_factory.apply(bpmn_graph)
    bpmn_vis_factory.save(bpmn_figure, join('solutions', name + '_' + miner_name + '_bpmn.png'))
    bpmn_vis_factory.save(bpmn_figure, join('solutions', name + '_' + miner_name + '_bpmn.pdf'))
