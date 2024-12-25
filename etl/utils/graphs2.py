import networkx as nx
import json



def generate_html(G, output_file):
    """
    Generate an interactive HTML visualization of a directed graph using d3.js
    
    Parameters:
    G (networkx.DiGraph): Input directed graph
    output_file (str): Output HTML file name
    """
    
    # Convert graph to dict of nodes and links
    nodes = []
    for node, attrs in G.nodes(data=True):
        nodes.append({
            'id': node,
            'label': attrs.get('label', node)
        })
    
    links = []
    for source, target in G.edges():
        links.append({
            'source': source,
            'target': target
        })
    
    graph_data = {
        'nodes': nodes,
        'links': links
    }
    
    html_template = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>DAG Visualization</title>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/d3/7.8.5/d3.min.js"></script>
        <style>
            .node {
                fill: #69b3a2;
                stroke: #fff;
                stroke-width: 2px;
            }
            .link {
                stroke: #999;
                stroke-opacity: 0.6;
                stroke-width: 2px;
                marker-end: url(#arrowhead);
            }
            .tooltip {
                position: absolute;
                background-color: white;
                padding: 5px;
                border: 1px solid #ddd;
                border-radius: 5px;
                pointer-events: none;
                opacity: 0;
            }
        </style>
    </head>
    <body>
        <svg width="800" height="600"></svg>
        <script>
            const data = GRAPH_DATA;
            
            const svg = d3.select('svg');
            const width = +svg.attr('width');
            const height = +svg.attr('height');
            
            // Add arrow marker
            svg.append('defs').append('marker')
                .attr('id', 'arrowhead')
                .attr('viewBox', '-0 -5 10 10')
                .attr('refX', 20)
                .attr('refY', 0)
                .attr('orient', 'auto')
                .attr('markerWidth', 6)
                .attr('markerHeight', 6)
                .append('path')
                .attr('d', 'M0,-5L10,0L0,5')
                .attr('fill', '#999');
            
            // Create tooltip
            const tooltip = d3.select('body').append('div')
                .attr('class', 'tooltip');
            
            // Create simulation
            const simulation = d3.forceSimulation(data.nodes)
                .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
                .force('charge', d3.forceManyBody().strength(-300))
                .force('center', d3.forceCenter(width / 2, height / 2))
                .force('x', d3.forceX(width / 2).strength(0.1))
                .force('y', d3.forceY(height / 2).strength(0.1));
            
            // Create links
            const link = svg.append('g')
                .selectAll('line')
                .data(data.links)
                .enter().append('line')
                .attr('class', 'link');
            
            // Create nodes
            const node = svg.append('g')
                .selectAll('circle')
                .data(data.nodes)
                .enter().append('circle')
                .attr('class', 'node')
                .attr('r', 10)
                .on('mouseover', function(event, d) {
                    tooltip.transition()
                        .duration(200)
                        .style('opacity', .9);
                    tooltip.html(d.label)
                        .style('left', (event.pageX + 10) + 'px')
                        .style('top', (event.pageY - 10) + 'px');
                })
                .on('mouseout', function() {
                    tooltip.transition()
                        .duration(500)
                        .style('opacity', 0);
                })
                .call(d3.drag()
                    .on('start', dragstarted)
                    .on('drag', dragged)
                    .on('end', dragended));
            
            // Add node labels
            const label = svg.append('g')
                .selectAll('text')
                .data(data.nodes)
                .enter().append('text')
                .text(d => d.id)
                .attr('font-size', 12)
                .attr('dx', 15)
                .attr('dy', 4);
            
            // Update positions on simulation tick
            simulation.on('tick', () => {
                link
                    .attr('x1', d => d.source.x)
                    .attr('y1', d => d.source.y)
                    .attr('x2', d => d.target.x)
                    .attr('y2', d => d.target.y);
                
                node
                    .attr('cx', d => d.x)
                    .attr('cy', d => d.y);
                
                label
                    .attr('x', d => d.x)
                    .attr('y', d => d.y);
            });
            
            // Drag functions
            function dragstarted(event) {
                if (!event.active) simulation.alphaTarget(0.3).restart();
                event.subject.fx = event.subject.x;
                event.subject.fy = event.subject.y;
            }
            
            function dragged(event) {
                event.subject.fx = event.x;
                event.subject.fy = event.y;
            }
            
            function dragended(event) {
                if (!event.active) simulation.alphaTarget(0);
                event.subject.fx = null;
                event.subject.fy = null;
            }
        </script>
    </body>
    </html>
    '''
    
    # Replace placeholder with actual graph data
    html_content = html_template.replace('GRAPH_DATA', json.dumps(graph_data))
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(html_content)
    
    print(f"DAG visualization has been saved to {output_file}")