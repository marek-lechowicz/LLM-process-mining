import os

from pm4py.algo.discovery.simple.model.log import factory as simple_miner
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.petri.check_soundness import check_petri_wfnet_and_soundness
from pm4py.objects.conversion.petri_to_bpmn import factory as bpmn_converter
from pm4py.visualization.bpmn import factory as bpmn_vis_factory




def execute_script():
    # loads the log
    # log = xes_importer.apply(os.path.join("..", "tests", "input_data", "receipt.xes"))
    # log = xes_importer.import_log(os.path.join("input_data","running-example.xes"))
    log = xes_importer.import_log(os.path.join("input_data","receipt.xes"))
    # apply the simple miner
    # net, im, fm = simple_miner.apply(log, classic_output=True)
    net, initial_marking, final_marking = inductive_miner.apply(log)

    bpmn_graph, elements_correspondence, inv_elements_correspondence, el_corr_keys_map = bpmn_converter.apply(net, initial_marking, final_marking)

    bpmn_figure = bpmn_vis_factory.apply(bpmn_graph)
    # bpmn_vis_factory.view(bpmn_figure)
    bpmn_vis_factory.save(bpmn_figure, "receipt.png")

    # checks if the Petri net is a sound workflow net
    is_sound_wfnet = check_petri_wfnet_and_soundness(net)
    print("is_sound_wfnet = ", is_sound_wfnet)



if __name__ == "__main__":
    execute_script()
