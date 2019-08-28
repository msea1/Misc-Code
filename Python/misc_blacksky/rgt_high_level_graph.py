import graphviz

sqs_color = 'blue'
fx_call = 'darkgreen'
data_color = 'red'

service_shape = 'doubleoctagon'
process = 'oval'
data_store = 'cylinder'
queue = 'note'

G = graphviz.Digraph(format='png', filename='rgt_overview.dg')

# SATELLITE
with G.subgraph(name='clustersat') as c:
    c.attr(label='SATELLITE', style='dotted')
    c.node('satellite', label='downlink_image', shape=process)

G.edge('satellite', 'xband_radio', color=data_color)


# GROUNDSTATION
with G.subgraph(name='clustergroundstation') as c:
    c.attr(label='GROUND STATION')
    c.node('xband_radio', shape=service_shape)
    c.node('rlm', label='sfx_file_monitor', shape=process)
    c.node('trebuchet', shape=service_shape)

G.edge('rlm', 'xband_radio', dir='forward', arrowhead='inv', color=data_color)
G.edge('rlm', 'trebuchet', color=fx_call)
G.edge('trebuchet', 'sfx_s3', color=data_color)
G.edge('trebuchet', 'env_files', color=sqs_color)
G.edge('pdp', 'env_files', dir='forward', arrowhead='inv', color=sqs_color)


# AWS
with G.subgraph(name='clusteraws') as c:
    c.attr(label='AWS', style='filled', color='lightgrey')
    # c.node_attr.update(style='filled', color='white')
    c.node('sfx_s3', label='sfx bucket', shape=data_store)

    c.node('obscura_queue', label='<obscura_queue<BR/><I>ENV-obscura-requests</I>>', shape=queue)
    c.node('env_files', label='<files from trebuchet<BR/><I>groundstation-ENV-files</I>>', shape=queue)
    c.node('final_product', label='<products<BR/><I>images-ENV-obscura-products</I>>', shape=queue)


# GEMINI
with G.subgraph(name='clustergemini') as gem:
    gem.attr(label='GEMINI', style='dotted')
    gem.node('pdp', label='<pass-data-processor<BR/><I>file_listener.py</I>>', shape=service_shape)

    # OBSCURA
    with gem.subgraph(name='clusterobscura') as c:
        c.attr(label='OBSCURA', style='dashed')
        c.node('img_req', label='ImageRequest', shape=service_shape)
        c.node('workflow', label='WorkFlow', shape=service_shape)
        c.node('upload', label='Upload', shape=service_shape)
        with c.subgraph(name='clusterimgreq') as cc:
            cc.attr(label='ImageReqest')
            cc.node('get_sfx', shape=process)
            cc.node('get_metadata', shape=process)
            cc.node('get_workflow', shape=process)
        with c.subgraph(name='clusterwf') as cc:
            cc.attr(label='Workflow', style='dotted')
        with c.subgraph(name='clusterupdload') as cc:
            cc.attr(label='Upload', style='dotted')

G.edge('pdp', 'obscura_queue', color=sqs_color, )  # label='<s3 key and bucket,<BR/>sat model, timestamp>', )

G.edge('img_req', 'obscura_queue', arrowhead='inv', dir='forward', color=sqs_color)
G.edge('img_req', 'get_sfx', arrowhead='inv', dir='forward', color=data_color)
G.edge('get_sfx', 'sfx_s3', dir='both', color=data_color)
G.edge('img_req', 'get_metadata', arrowhead='inv', dir='forward', color=data_color)
G.edge('get_metadata', 'pdp', color=fx_call)
G.edge('img_req', 'get_workflow', arrowhead='inv', dir='forward', color=data_color)

G.edge('img_req', 'workflow', color=fx_call)

G.edge('workflow', 'upload', color=fx_call)
G.edge('upload', 'final_product', color=data_color)


with G.subgraph(name='clusterlegend') as legend:
    legend.attr(label='LEGEND')
    legend.node('a', label='service', shape=service_shape)
    legend.node('b', label='function', shape=process)
    legend.node('c', label='data store', shape=data_store)
    legend.node('d', label='SQS queue', shape=queue)

    legend.edge('a', 'b', label=' foo()', color=fx_call)
    legend.edge('b', 'c', label=' data', color=data_color)
    legend.edge('c', 'd', label=' SQS', color=sqs_color)

# G.attr(splines='ortho')
G.render()
