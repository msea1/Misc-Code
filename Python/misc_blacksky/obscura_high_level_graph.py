import graphviz

sqs_color = 'blue'
fx_call = 'darkgreen'
data_color = 'red'

service_shape = 'doubleoctagon'
process = 'oval'
data_store = 'cylinder'
queue = 'note'

G = graphviz.Digraph(format='png', filename='obscura_overview.dg')

G.node('platform', label='PLATFORM', shape=service_shape)
G.edge('platform', 'tdm', color=data_color)
G.edge('tdm', 'planner', color=data_color)

# SATELLITE
with G.subgraph(name='clustersat') as c:
    c.attr(label='SATELLITE', style='dotted')
    c.node('image', label='downlink_image', shape=process)
    c.node('metadata', label='downlink_metadata', shape=process)

G.edge('image', 'xband_radio', color=data_color)
G.edge('metadata', 'xband_radio', color=data_color)
G.edge('planner', 'metadata', lhead='clustersat', color=data_color)

# GROUNDSTATION
with G.subgraph(name='clustergroundstation') as c:
    c.attr(label='GROUND STATION')
    c.node('xband_radio', label='radio', shape=service_shape)
    c.node('rlm', label='sfx_file_monitor', shape=process)
    c.node('sft_file', label='<sft_file_transfer<BR/><I>via sft-packet-router</I>>', shape=process)
    c.node('trebuchet', shape=service_shape)

G.edge('rlm', 'xband_radio', dir='forward', arrowhead='inv', color=data_color)
G.edge('sft_file', 'xband_radio', dir='forward', arrowhead='inv', color=data_color)
G.edge('rlm', 'trebuchet', color=fx_call)
G.edge('sft_file', 'trebuchet', color=fx_call)
G.edge('trebuchet', 'files_s3', color=data_color)
G.edge('trebuchet', 'env_files', color=sqs_color)
G.edge('pdp', 'env_files', dir='forward', arrowhead='inv', color=sqs_color)


# AWS
with G.subgraph(name='clusteraws') as c:
    c.attr(label='AWS', style='filled', color='lightgrey')
    # c.node_attr.update(style='filled', color='white')
    c.node('files_s3', label='files', shape=data_store)

    c.node('obscura_queue', label='<obscura_queue<BR/><I>ENV-obscura-requests</I>>', shape=queue)
    c.node('env_files', label='<files from trebuchet<BR/><I>groundstation-ENV-files</I>>', shape=queue)
    c.node('final_product', label='<products<BR/><I>images-ENV-obscura-products</I>>', shape=queue)


# GEMINI
with G.subgraph(name='clustergemini') as gem:
    gem.attr(label='GEMINI', style='dotted')
    gem.node('pdp', label='<pass-data-processor<BR/><I>file_listener.py</I>>', shape=service_shape)
    gem.node('satmodel', label='satellite model', shape=service_shape)
    gem.node('compliance', label='image order compliance', shape=service_shape)
    gem.node('catalog', label='image catalog', shape=service_shape)
    gem.node('planner', label='<mission planner<BR/><I>task data</I>>', shape=service_shape)
    gem.node('cmd_gen', label='<command<BR/>generator>', shape=service_shape)
    gem.node('tdm', label='tgt-deck-mgr', shape=service_shape)

    # OBSCURA
    with gem.subgraph(name='clusterobscura') as c:
        c.attr(label='OBSCURA', style='dashed')
        c.node('img_req', label='ImageRequest', shape=service_shape)
        c.node('workflow', label='WorkFlow', shape=service_shape)
        c.node('upload', label='Upload', shape=service_shape)
        c.node('run_wf', label='run workflow', shape=process)
        c.node('examine_task', label='<compare accuracy<BR/>vs task data>', shape=process)

G.edge('pdp', 'satmodel', arrowhead='inv', dir='forward', color=data_color)
G.edge('pdp', 'cmd_gen', arrowhead='inv', dir='forward', color=data_color)
G.edge('pdp', 'files_s3', color=data_color)  # decrypted image_metadata files
G.edge('pdp', 'obscura_queue', color=sqs_color)

G.edge('img_req', 'obscura_queue', arrowhead='inv', dir='forward', color=sqs_color)
G.edge('img_req', 'files_s3', arrowhead='inv', dir='forward', color=data_color)
G.edge('img_req', 'pdp', arrowhead='inv', dir='forward', color=data_color)
G.edge('img_req', 'planner', arrowhead='inv', dir='forward', color=data_color)

G.edge('img_req', 'workflow', color=sqs_color)
G.edge('workflow', 'run_wf', arrowhead='inv', dir='forward', color=data_color)
G.edge('workflow', 'examine_task', color=fx_call)

G.edge('workflow', 'upload', color=sqs_color)
G.edge('upload', 'final_product', color=data_color)
G.edge('upload', 'satmodel', color=fx_call)
G.edge('upload', 'compliance', color=fx_call)
G.edge('compliance', 'catalog', color=fx_call)
G.edge('catalog', 'platform', color=fx_call)


with G.subgraph(name='clusterlegend') as legend:
    legend.attr(label='LEGEND')
    legend.node('a', label='service', shape=service_shape)
    legend.node('b', label='function', shape=process)
    legend.node('c', label='data store', shape=data_store)
    legend.node('d', label='SQS queue', shape=queue)

    legend.edge('a', 'b', label=' foo()', color=fx_call)
    legend.edge('b', 'c', label=' pull data', arrowhead='inv', color=data_color)
    legend.edge('c', 'd', label=' SQS', color=sqs_color)

G.attr(splines='ortho')
G.attr(compound='true')
G.attr(overlap='scale')
G.attr(overlap_shrink='true')
G.render()
