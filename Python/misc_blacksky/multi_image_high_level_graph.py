import graphviz

sqs_color = 'blue'
fx_call = 'darkgreen'
data_color = 'red'
new_line = 'purple'

service_shape = 'doubleoctagon'
process = 'oval'
data_store = 'cylinder'
queue = 'note'

G = graphviz.Digraph(format='png', filename='multi_overview.dg')

# SATELLITE
with G.subgraph(name='clustersat') as c:
    c.attr(label='SATELLITE', style='dotted')
    c.node('image', label='downlink_image', shape=process)
    c.node('metadata', label='downlink_metadata', shape=process)

G.edge('image', 'xband_radio', color=data_color)
G.edge('image', 'xband_radio', color=new_line)
G.edge('metadata', 'xband_radio', color=data_color)


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
    gem.node('planner', label='<mission planner<BR/><I>task data</I>>', shape=service_shape)
    gem.node('cmd_gen', label='<command<BR/>generator>', shape=service_shape)

    # OBSCURA
    with gem.subgraph(name='clusterobscura') as c:
        c.attr(label='OBSCURA', style='dashed')
        c.node('img_req', label='ImageRequest', shape=service_shape)
        c.node('workflow', label='WorkFlow', shape=service_shape)
        c.node('multi', label='Multi Check', shape=service_shape, color=new_line)
        c.node('upload', label='Upload', shape=service_shape)
        c.node('get_sfx', label='SFX file', shape=process)
        c.node('get_metadata', label='image metadata', shape=process)
        c.node('get_task', label='task metadata', shape=process)
        c.node('run_wf', label='run workflow', shape=process)
        c.node('examine_task', label='<compare accuracy<BR/>vs task data>', shape=process)
        c.node('post_process_check', label='<Part of multi<BR/>order and all<BR/>images processed?>', shape=process, color=new_line)
        c.node('gather_multi_images', label='<Gather images<BR/>and create task<BR/>with stereo wf>', shape=process, color=new_line)

G.edge('pdp', 'satmodel', arrowhead='inv', dir='forward', color=data_color)
G.edge('pdp', 'cmd_gen', arrowhead='inv', dir='forward', color=data_color)
G.edge('pdp', 'files_s3', color=data_color)  # decrypted image_metadata files
G.edge('pdp', 'obscura_queue', color=sqs_color)

G.edge('img_req', 'obscura_queue', arrowhead='inv', dir='forward', color=sqs_color)
G.edge('img_req', 'get_sfx', arrowhead='inv', dir='forward', color=data_color)
G.edge('img_req', 'get_task', arrowhead='inv', dir='forward', color=data_color)
G.edge('get_sfx', 'files_s3', dir='both', color=data_color)
G.edge('img_req', 'get_metadata', arrowhead='inv', dir='forward', color=data_color)
G.edge('get_metadata', 'pdp', arrowhead='inv', dir='forward', color=data_color)
G.edge('get_task', 'planner', arrowhead='inv', dir='forward', color=data_color)

G.edge('img_req', 'workflow', color=sqs_color)
G.edge('workflow', 'run_wf', arrowhead='inv', dir='forward', color=data_color)
G.edge('workflow', 'examine_task', color=fx_call)

G.edge('workflow', 'multi', color=new_line)
G.edge('multi', 'upload', color=new_line)
G.edge('upload', 'final_product', color=data_color)
G.edge('multi', 'post_process_check', color=new_line)
G.edge('post_process_check', 'satmodel', label='No', color=new_line)
G.edge('post_process_check', 'gather_multi_images', label=' Yes', color=new_line)
G.edge('gather_multi_images', 'workflow',color=new_line)
G.edge('upload', 'compliance', color=fx_call)


with G.subgraph(name='clusterlegend') as legend:
    legend.attr(label='LEGEND')
    legend.node('a', label='service', shape=service_shape)
    legend.node('b', label='function', shape=process)
    legend.node('c', label='data store', shape=data_store)
    legend.node('d', label='SQS queue', shape=queue)
    legend.node('e', label='N/A', shape=process)

    legend.edge('a', 'b', label=' foo()', color=fx_call)
    legend.edge('b', 'c', label=' pull data', arrowhead='inv', color=data_color)
    legend.edge('c', 'd', label=' SQS', color=sqs_color)
    legend.edge('d', 'e', label=' new', color=new_line)

# G.attr(engine='neato')
# G.attr(layout='fdp')
# G.attr(splines='ortho')
G.attr(overlap='scale')
G.attr(overlap_shrink='true')
G.render()
