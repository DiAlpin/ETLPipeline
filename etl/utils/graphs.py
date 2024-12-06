import networkx as nx


def generate_html(G, path):
    # Create HTML content
    html_content = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Interactive Graph Visualization with Arrows</title>
            <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
            <style type="text/css">
                #mynetwork {
                    width: 1200px;
                    height: 800px;
                    border: 1px solid lightgray;
                }
            </style>
        </head>
        <body>
            <div id="mynetwork"></div>

            <script type="text/javascript">
                // Create nodes
                var nodes = new vis.DataSet([
    '''
    
    # Add nodes
    for node in G.nodes(data=True):
        label = node[1].get('label', '')
        html_content += f"            {{id: '{node[0]}', label: '{node[0]}', title: '{label}'}},\n"
    
    html_content += '''
        ]);

        // Create edges
        var edges = new vis.DataSet([
    '''
    
    # Add edges with arrows
    for edge in G.edges():
        html_content += f"            {{from: '{edge[0]}', to: '{edge[1]}', arrows: 'to'}},\n"
    
    html_content += '''
                ]);

                // Create a network
                var container = document.getElementById('mynetwork');
                var data = {
                    nodes: nodes,
                    edges: edges
                };
                var options = {
                    nodes: {
                        shape: 'dot',
                        size: 30,
                        font: {
                            size: 14
                        }
                    },
                    edges: {
                        width: 2,
                        arrows: {
                            to: {
                                enabled: true,
                                scaleFactor: 1
                            }
                        }
                    },
                    interaction: {
                        hover: true
                    }
                };
                var network = new vis.Network(container, data, options);
            </script>
        </body>
        </html>
    '''
    
    with open(path, 'w') as f:
        f.write(html_content)

    print(f'graph saved!')
    # return html_content

