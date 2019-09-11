import graphviz

# DEFINING SOME CONSTANTS
PASS_OFF = 'black'
fx_call = 'black'
data_color = 'black'
new_line = 'blue'
dead_line = 'red'

service_shape = 'doubleoctagon'
process = 'oval'
data_store = 'cylinder'
queue = 'note'

G = graphviz.Digraph(format='png', filename='rgt_overview.dg')

# SATELLITE
with G.subgraph(name='clustersat') as c:
    c.attr(label='SATELLITE', style='dotted')
    c.node('image', label='downlink_image', shape=process)
    c.node('metadata', label='SFT (file)', shape=process, color=new_line)
    c.node('script', label='script', shape=data_store)

G.edge('image', 'xband_radio', color=data_color)
G.edge('metadata', 'xband_radio', color=new_line)
G.edge('metadata', 'xband_radio', color=new_line)
# G.edge('planner', 'metadata', lhead='clustersat', color=new_line)
G.edge('metadata', 'script', arrowhead='inv', color=new_line)

# GROUNDSTATION
with G.subgraph(name='clustergroundstation') as c:
    c.attr(label='GROUND STATION')
    c.node('xband_radio', label='radio', shape=service_shape)
    c.node('rlm', label='sfx_file_monitor', shape=process)
    c.node('sft_old', label='sft_file_transfer', shape=process, color=dead_line)
    c.node('sft', label='<sft_packet_router<BR/><I>creates files</I>>', shape=process, color=new_line)
    c.node('trebuchet', shape=service_shape, color=dead_line)
    c.node('local_storage', label='<local<BR/>disk>', shape=data_store, color=new_line)

    # OBSCURA
    with c.subgraph(name='clusterobscura') as obs:
        obs.attr(label='OBSCURA', style='dashed')
        obs.node('img_req', label='ImageRequest', shape=service_shape)
        obs.node('workflow', label='WorkFlow', shape=service_shape)
        obs.node('upload', label='Upload', shape=service_shape)
        obs.node('get_sfx', label='SFX file', shape=process)
        obs.node('get_metadata', label='image metadata', shape=process)
        obs.node('get_task', label='task metadata', shape=process)
        obs.node('run_wf', label='run workflow', shape=process)
        obs.node('examine_task', label='<compare accuracy<BR/>vs task data>', shape=process)

        G.edge('img_req', 'get_sfx', arrowhead='inv', color=data_color)
        G.edge('img_req', 'get_task', arrowhead='inv', color=data_color)
        G.edge('img_req', 'get_metadata', arrowhead='inv', color=data_color)
        G.edge('get_sfx', 'local_storage', arrowhead='inv', color=new_line)
        G.edge('get_task', 'local_storage', arrowhead='inv', color=new_line)
        G.edge('get_metadata', 'local_storage', arrowhead='inv', color=new_line)
        G.edge('img_req', 'workflow', color=PASS_OFF)
        G.edge('workflow', 'run_wf', arrowhead='inv', color=data_color)
        G.edge('workflow', 'examine_task', color=fx_call)
        G.edge('workflow', 'upload', color=dead_line)


G.edge('rlm', 'xband_radio', arrowhead='inv', color=data_color)
G.edge('sft', 'xband_radio', arrowhead='inv', color=data_color)
G.edge('sft_old', 'sft', arrowhead='inv', color=dead_line)
G.edge('rlm', 'trebuchet', color=dead_line)
G.edge('sft_old', 'trebuchet', color=dead_line)
G.edge('rlm', 'local_storage', color=data_color)
G.edge('sft', 'local_storage', color=new_line)
G.edge('sft', 'local_storage', color=new_line)


with G.subgraph(name='clusterlegend') as legend:
    legend.attr(label='LEGEND')
    legend.node('a', label='service', shape=service_shape)
    legend.node('b', label='function', shape=process)
    legend.node('c', label='data store', shape=data_store)
    legend.node('d', label='SQS queue', shape=queue)
    legend.node('e', label='N/A', shape=process)

    legend.edge('a', 'b', label=' foo()', color=fx_call)
    legend.edge('b', 'c', label=' pull data', arrowhead='inv', color=data_color)
    legend.edge('c', 'd', label=' SQS', color=PASS_OFF)
    legend.edge('d', 'e', label='<<BR/><BR/><BR/><BR/> new>', color=new_line)
    legend.edge('e', 'd', label='<--dead', color=dead_line)

# G.attr(engine='neato')
# G.attr(layout='fdp')
# G.attr(splines='ortho')
G.attr(overlap='scale')
G.attr(overlap_shrink='true')
G.attr(compound='true')
G.render()
