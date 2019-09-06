import graphviz

sqs_color = 'blue'
fx_call = 'darkgreen'
data_color = 'red'

service_shape = 'doubleoctagon'
process = 'oval'
data_store = 'cylinder'
queue = 'note'

G = graphviz.Digraph(format='png', filename='obscura_overview.dg')

# AWS
with G.subgraph(name='clusteraws') as c:
    c.attr(label='AWS', style='filled', color='lightgrey')
    c.node('files_s3', label='files', shape=data_store)
    c.node('obscura_queue', label='<obscura_queue<BR/><I>ENV-obscura-requests</I>>', shape=queue)
    c.node('env_files', label='<files from trebuchet<BR/><I>proc.oundstation-ENV-files</I>>', shape=queue)
    c.node('final_product', label='<products<BR/><I>imaproc.s-ENV-obscura-products</I>>', shape=queue)

# PLANNING SIDE
with G.subgraph(name='clusterplanning') as plan:
    plan.attr(label='PLANNING')
    plan.node('platform', label='PLATFORM', shape=service_shape)
    plan.edge('platform', 'tdm', color=data_color)
    plan.edge('tdm', 'planner_plan', color=data_color)
    plan.edge('planner_plan', 'script', lhead='clustersat_plan', color=data_color)
    
    with plan.subgraph(name='clustersat_plan') as c:
        c.attr(label='SATELLITE', style='dotted')
        c.node('script', label='script', shape=data_store)

    with plan.subgraph(name='clustergemini_plan') as gem:
        gem.attr(label='GEMINI', style='dotted')
        gem.node('planner_plan', label='mission planner', shape=service_shape)
        gem.node('tdm', label='tgt-deck-mgr', shape=service_shape)

# DOWNLINK SIDE
with G.subgraph(name='clusterdownlink') as proc:
    proc.attr(label='DOWNLINKING')

    # SATELLITE
    with proc.subgraph(name='clustersatdl') as c:
        c.attr(label='SATELLITE', style='dotted')
        c.node('image', label='downlink_image', shape=process)
        c.node('metadata', label='downlink_metadata', shape=process)

    proc.edge('image', 'xband_radio', color=data_color)
    proc.edge('metadata', 'xband_radio', color=data_color)

    # GROUNDSTATION
    with proc.subgraph(name='clustergroundstation') as c:
        c.attr(label='GROUND STATION')
        c.node('xband_radio', label='radio', shape=service_shape)
        c.node('rlm', label='sfx_file_monitor', shape=process)
        c.node('sft_file', label='<sft_file_transfer<BR/><I>via sft-packet-router</I>>', shape=process)
        c.node('trebuchet', shape=service_shape)

    proc.edge('rlm', 'xband_radio', dir='forward', arrowhead='inv', color=data_color)
    proc.edge('sft_file', 'xband_radio', dir='forward', arrowhead='inv', color=data_color)
    proc.edge('rlm', 'trebuchet', color=fx_call)
    proc.edge('sft_file', 'trebuchet', color=fx_call)
    proc.edge('trebuchet', 'files_s3', color=data_color)
    proc.edge('trebuchet', 'env_files', color=sqs_color)


# IMAGE PROCESSING
with G.subgraph(name='clusterprocessing') as proc:
    proc.attr(label='PROCESSING')

    # GEMINI
    with proc.subgraph(name='clustergemini') as proc_gem:
        proc_gem.attr(label='GEMINI', style='dotted')
        proc_gem.node('pdp', label='<pass-data-processor<BR/><I>file_listener.py</I>>', shape=service_shape)
        proc_gem.node('satmodel', label='satellite model', shape=service_shape)
        proc_gem.node('compliance', label='imaproc. order compliance', shape=service_shape)
        proc_gem.node('catalog', label='image catalog', shape=service_shape)
        proc_gem.node('planner', label='<mission planner<BR/><I>task data</I>>', shape=service_shape)
        proc_gem.node('cmd_gen', label='<command<BR/>generator>', shape=service_shape)
    
        # OBSCURA
        with proc_gem.subgraph(name='clusterobscura') as c:
            c.attr(label='OBSCURA', style='dashed')
            c.node('img_req', label='Imaproc.Request', shape=service_shape)
            c.node('workflow', label='WorkFlow', shape=service_shape)
            c.node('upload', label='Upload', shape=service_shape)
            c.node('run_wf', label='run workflow', shape=process)
            c.node('examine_task', label='<compare accuracy<BR/>vs task data>', shape=process)
    
    proc.edge('pdp', 'env_files', dir='forward', arrowhead='inv', color=sqs_color)
    proc.edge('pdp', 'satmodel', arrowhead='inv', dir='forward', color=data_color)
    proc.edge('pdp', 'cmd_gen', arrowhead='inv', dir='forward', color=data_color)
    proc.edge('pdp', 'files_s3', color=data_color)  # decrypted imaproc._metadata files
    proc.edge('pdp', 'obscura_queue', color=sqs_color)
    
    proc.edge('img_req', 'obscura_queue', arrowhead='inv', dir='forward', color=sqs_color)
    proc.edge('img_req', 'files_s3', arrowhead='inv', dir='forward', color=data_color)
    proc.edge('img_req', 'pdp', arrowhead='inv', dir='forward', color=data_color)
    proc.edge('img_req', 'planner', arrowhead='inv', dir='forward', color=data_color)
    
    proc.edge('img_req', 'workflow', color=sqs_color)
    proc.edge('workflow', 'run_wf', arrowhead='inv', dir='forward', color=data_color)
    proc.edge('workflow', 'examine_task', color=fx_call)
    
    proc.edge('workflow', 'upload', color=sqs_color)
    proc.edge('upload', 'final_product', color=data_color)
    proc.edge('upload', 'satmodel', color=fx_call)
    proc.edge('upload', 'compliance', color=fx_call)
    proc.edge('compliance', 'catalog', color=fx_call)
    proc.edge('catalog', 'platform', color=fx_call)
    
    
with G.subgraph(name='clusterlegend') as legend:
    legend.attr(label='legend')
    legend.node('a', label='service', shape=service_shape)
    legend.node('b', label='function', shape=process)
    legend.node('c', label='data store', shape=data_store)
    legend.node('d', label='SQS queue', shape=queue)

    legend.edge('a', 'b', label=' foo()', color=fx_call)
    legend.edge('b', 'c', label=' pull data', arrowhead='inv', color=data_color)
    legend.edge('c', 'd', label=' SQS', color=sqs_color)

# G.attr(engine='neato')
# G.attr(rankdir='RL')
# G.attr(layout='fdp')
# G.attr(splines='ortho')
G.attr(compound='true')
G.attr(overlap='scale')
G.attr(overlap_shrink='true')
G.attr(size='11.0, 8.5')
G.attr(ratio='fill')
G.render()
