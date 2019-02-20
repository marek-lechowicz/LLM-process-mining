from os.path import join

from pm4py.objects.log.importer.csv import factory as csv_importer
from pm4py.objects.conversion.petri_to_bpmn import factory as bpmn_converter
from pm4py.visualization.bpmn import factory as bpmn_vis_factory
from pm4py.objects.bpmn.exporter import bpmn20 as bpmn_exporter
from pm4py.visualization.petrinet import factory as pn_vis_factory



def explore_process(name, csv, miner, miner_name):
    event_log = csv_importer.import_log_from_string(csv)

    net, initial_marking, final_marking = miner.apply(event_log)
    gviz = pn_vis_factory.apply(net, initial_marking, final_marking)
    pn_vis_factory.save(gviz, join('solutions', name + '_' + miner_name + '_petri_net.png'))
    pn_vis_factory.save(gviz, join('solutions', name + '_' + miner_name + '_petri_net.pdf'))

    bpmn_graph, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = bpmn_converter.apply(net, initial_marking, final_marking)

    bpmn_exporter.export_bpmn(bpmn_graph, join('solutions', name + '_' + miner_name + '.bpmn'))
    bpmn_figure = bpmn_vis_factory.apply(bpmn_graph)
    bpmn_vis_factory.save(bpmn_figure, join('solutions', name + '_' + miner_name + '_bpmn.png'))
    bpmn_vis_factory.save(bpmn_figure, join('solutions', name + '_' + miner_name + '_bpmn.pdf'))
