import graphviz
from functools import reduce

class MyGraph(graphviz.Digraph):

    def __init__(self, *args):
        super(MyGraph, self).__init__(*args)
        self.graph_attr['rankdir'] = 'LR'
        self.node_attr['shape'] = 'Mrecord'
        self.graph_attr['splines'] = 'ortho'
        self.graph_attr['nodesep'] = '0.8'
        self.edge_attr.update(penwidth='2')
    
    def add_event(self, name):
        super(MyGraph, self).node(name, shape="circle", label="")
    
    def add_and_gateway(self, *args):
        super(MyGraph, self).node(*args, shape="diamond",
                                  width=".6",height=".6",
                                  fixedsize="true",
                                  fontsize="40",label="+")
        
    def add_xor_gateway(self, *args, **kwargs):
        super(MyGraph, self).node(*args, shape="diamond",
                                  width=".6",height=".6",
                                  fixedsize="true",
                                  fontsize="35",label="×")

    def add_and_split_gateway(self, source, targets, *args):
        gateway = 'ANDs '+str(source)+'->'+str(targets)        
        self.add_and_gateway(gateway,*args)
        super(MyGraph, self).edge(source, gateway)
        for target in targets:
            super(MyGraph, self).edge(gateway, target)

    def add_xor_split_gateway(self, source, targets, *args):
        gateway = 'XORs '+str(source)+'->'+str(targets) 
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).edge(source, gateway)
        for target in targets:
            super(MyGraph, self).edge(gateway, target)

    def add_and_merge_gateway(self, sources, target, *args):
        gateway = 'ANDm '+str(sources)+'->'+str(target)
        self.add_and_gateway(gateway,*args)
        super(MyGraph, self).edge(gateway,target)
        for source in sources:
            super(MyGraph, self).edge(source, gateway)

    def add_xor_merge_gateway(self, sources, target, *args):
        gateway = 'XORm '+str(sources)+'->'+str(target)
        self.add_xor_gateway(gateway, *args)
        super(MyGraph, self).edge(gateway,target)
        for source in sources:
            super(MyGraph, self).edge(source, gateway)




def build_bpmn(direct_succession, causality):
    ev_source = set(causality.keys())
    ev_target = reduce(lambda x,y: x|y, causality.values())
    start_set_events = ev_source - ev_target

    print("start_set_events: ",start_set_events)

    end_set_events = ev_target - ev_source

    print("end_set_events: ",end_set_events)

    parallel_events = set()
    causality_dict_new = dict()
    for event1 in direct_succession:
        for event2 in direct_succession[event1]:
            if event1 not in causality_dict_new:
                causality_dict_new[event1] = set()
            if event1 not in direct_succession.get(event2, {}): 
                causality_dict_new[event1].add(event2)
                print(event1, "->", event2)
            else:
                parallel_events.add(tuple([event1,event2]))
                print(event1, "||", event2)

    inv_causality = dict()
    for key in causality.keys():
        if len(causality[key]) > 1: 
            continue
        for new_key in causality[key]:
            if new_key not in inv_causality:
                inv_causality[new_key] = set()
            inv_causality[new_key].add(key)

    print('parallel_events', parallel_events)
    print('causality_dict_new', causality_dict_new)
    print('inv_causality', inv_causality)

    G = MyGraph()

    # adding split gateways based on causality
    for event in causality:
        if len(causality[event]) > 1:
            if tuple(causality[event]) in parallel_events:
                G.add_and_split_gateway(event,causality[event])
            else:
                G.add_xor_split_gateway(event,causality[event])

    # adding merge gateways based on inverted causality
    for event in inv_causality:
        if len(inv_causality[event]) > 1:
            if tuple(inv_causality[event]) in parallel_events:
                G.add_and_merge_gateway(inv_causality[event],event)
            else:
                G.add_xor_merge_gateway(inv_causality[event],event)
        elif len(inv_causality[event]) == 1:
            source = list(inv_causality[event])[0]
            G.edge(source,event)

    # adding start event
    G.add_event("start")
    if len(start_set_events) > 1:
        if tuple(start_set_events) in parallel_events: 
            G.add_and_split_gateway(event,start_set_events)
        else:
            G.add_xor_split_gateway(event,start_set_events)
    else: 
        G.edge("start",list(start_set_events)[0])

    # adding end event
    G.add_event("end")
    if len(end_set_events) > 1:
        if tuple(end_set_events) in parallel_events: 
            G.add_and_merge_gateway(end_set_events,event)
        else:
            G.add_xor_merge_gateway(end_set_events,event)    
    else: 
        G.edge(list(end_set_events)[0],"end")

    return G



if __name__ == '__main__':
    direct_succession = {
        'a': {'b', 'f'},
        'b': {'c', 'd'},
        'c': {'d', 'e'},
        'd': {'c', 'e'},
        'e': {'h'},
        'f': {'g'},
        'g': {'h'},
        'h': {'i', 'j'},
        'i': {'k'},
        'j': {'k'}
    }

    causality = {
        'a': {'b', 'f'},
        'b': {'c', 'd'},
        'c': {'e'},
        'd': {'e'},
        'e': {'h'},
        'f': {'g'},
        'g': {'h'},
        'h': {'i', 'j'},
        'i': {'k'},
        'j': {'k'}
    }

    G = build_bpmn(direct_succession, causality)
    G.render('simple_graphviz_graph')
    G.view('simple_graphviz_graph')