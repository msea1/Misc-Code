import graphviz

PASS_OFF = 'blue'
FX_CALL = 'darkgreen'
DATA = 'red'
NEW = 'purple'
DEAD = 'black'

SERVICE = 'doubleoctagon'
PROCESS = 'oval'
DATA_STORE = 'cylinder'
SQS_QUEUE = 'note'

CURRENT = False
MULTI = True
RGT = False

graph = graphviz.Digraph(format='png', filename='obscura')


def add_satellite_nodes(subgraph):
    subgraph.node('image', label='downlink_image', shape=PROCESS)
    subgraph.node('script', label='script', shape=DATA_STORE)

    graph.edge('image', 'xband_radio', color=DATA)
    graph.edge('image', 'xband_radio', color=NEW)
    graph.edge('metadata', 'xband_radio', color=DATA)
    
    if MULTI:
        subgraph.node('metadata', label='downlink_metadata', shape=PROCESS)
    elif RGT:
        subgraph.node('metadata', label='SFT (file)', shape=PROCESS, color=NEW)


# SATELLITE
with graph.subgraph(name='cluster_sat') as cluster_sat:
    cluster_sat.attr(label='SATELLITE', style='dotted')


def add_groundstation_nodes(subgraph):
    pass


# GROUNDSTATION
with graph.subgraph(name='clustergroundstation') as c:
    c.attr(label='GROUND STATION')
    c.node('xband_radio', label='radio', shape=SERVICE)
    c.node('rlm', label='sfx_file_monitor', shape=PROCESS)
    c.node('sft_file', label='<sft_file_transfer<BR/><I>via sft-packet-router</I>>', shape=PROCESS)
    c.node('trebuchet', shape=SERVICE)

graph.edge('rlm', 'xband_radio', dir='forward', arrowhead='inv', color=DATA)
graph.edge('sft_file', 'xband_radio', dir='forward', arrowhead='inv', color=DATA)
graph.edge('rlm', 'trebuchet', color=FX_CALL)
graph.edge('sft_file', 'trebuchet', color=FX_CALL)
graph.edge('trebuchet', 'files_s3', color=DATA)
graph.edge('trebuchet', 'env_files', color=PASS_OFF)
graph.edge('pdp', 'env_files', dir='forward', arrowhead='inv', color=PASS_OFF)


# AWS
with graph.subgraph(name='clusteraws') as c:
    c.attr(label='AWS', style='filled', color='lightgrey')
    # c.node_attr.update(style='filled', color='white')
    c.node('files_s3', label='files', shape=DATA_STORE)

    c.node('obscura_queue', label='<obscura_queue<BR/><I>ENV-obscura-requests</I>>', shape=SQS_QUEUE)
    c.node('env_files', label='<files from trebuchet<BR/><I>groundstation-ENV-files</I>>', shape=SQS_QUEUE)
    c.node('final_product', label='<products<BR/><I>images-ENV-obscura-products</I>>', shape=SQS_QUEUE)


# GEMINI
with graph.subgraph(name='clustergemini') as gem:
    gem.attr(label='GEMINI', style='dotted')
    gem.node('pdp', label='<pass-data-processor<BR/><I>file_listener.py</I>>', shape=SERVICE)
    gem.node('satmodel', label='satellite model', shape=SERVICE)
    gem.node('compliance', label='image order compliance', shape=SERVICE)
    gem.node('planner', label='<mission planner<BR/><I>task data</I>>', shape=SERVICE)
    gem.node('cmd_gen', label='<command<BR/>generator>', shape=SERVICE)

    # OBSCURA
    with gem.subgraph(name='clusterobscura') as c:
        c.attr(label='OBSCURA', style='dashed')
        c.node('img_req', label='ImageRequest', shape=SERVICE)
        c.node('single_instance', label='<Single-image<BR/>instance>', shape=SERVICE)
        c.node('multi_instance', label='<Multi-image<BR/>instance>', shape=SERVICE, color=NEW)
        c.node('multi', label='Multi Check', shape=SERVICE, color=NEW)
        c.node('upload', label='Upload', shape=SERVICE)
        c.node('get_sfx', label='SFX file', shape=PROCESS)
        c.node('get_metadata', label='image metadata', shape=PROCESS)
        c.node('get_task', label='task metadata', shape=PROCESS)
        c.node('examine_task', label='<compare accuracy<BR/>vs task data>', shape=PROCESS)
        c.node('post_process_check', label='<Part of multi<BR/>order and all<BR/>images processed?>', shape=PROCESS, color=NEW)

graph.edge('pdp', 'satmodel', arrowhead='inv', dir='forward', color=DATA)
graph.edge('pdp', 'cmd_gen', arrowhead='inv', dir='forward', color=DATA)
graph.edge('pdp', 'files_s3', color=DATA)  # decrypted image_metadata files
graph.edge('pdp', 'obscura_queue', color=PASS_OFF)

graph.edge('img_req', 'obscura_queue', arrowhead='inv', dir='forward', color=PASS_OFF)
graph.edge('img_req', 'get_sfx', arrowhead='inv', dir='forward', color=DATA)
graph.edge('img_req', 'get_task', arrowhead='inv', dir='forward', color=DATA)
graph.edge('get_sfx', 'files_s3', dir='both', color=DATA)
graph.edge('img_req', 'get_metadata', arrowhead='inv', dir='forward', color=DATA)
graph.edge('get_metadata', 'pdp', arrowhead='inv', dir='forward', color=DATA)
graph.edge('get_task', 'planner', arrowhead='inv', dir='forward', color=DATA)

graph.edge('img_req', 'single_instance', color=PASS_OFF)
graph.edge('single_instance', 'examine_task', color=FX_CALL)

graph.edge('single_instance', 'upload', color=PASS_OFF)
graph.edge('multi_instance', 'upload', color=NEW)
graph.edge('upload', 'multi', color=NEW)
graph.edge('upload', 'final_product', color=DATA)
graph.edge('multi', 'post_process_check', color=NEW)
graph.edge('post_process_check', 'satmodel', label='No', color=NEW)
graph.edge('post_process_check', 'multi_instance', label=' Yes', color=NEW)
graph.edge('upload', 'compliance', color=FX_CALL)


with graph.subgraph(name='cluster_legend') as legend:
    legend.attr(label='LEGEND')
    legend.node('a', label='service', shape=SERVICE)
    legend.node('b', label='function', shape=PROCESS)
    legend.node('c', label='data store', shape=DATA_STORE)
    legend.node('d', label='sqs queue', shape=SQS_QUEUE)
    legend.node('e', label='N/A', shape=PROCESS)

    legend.edge('a', 'b', label=' foo()', color=FX_CALL)
    legend.edge('b', 'c', label=' pull data', arrowhead='inv', color=DATA)
    legend.edge('c', 'd', label=' SQS', color=PASS_OFF)
    legend.edge('d', 'e', label=' new', color=NEW)

graph.attr(overlap='scale')
graph.attr(overlap_shrink='true')
graph.render()
