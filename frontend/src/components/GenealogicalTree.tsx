import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import type { GenealogicalNode } from '../types';

interface GenealogicalTreeProps {
  ancestors: GenealogicalNode[];
  descendants: GenealogicalNode[];
  rootConcept: string;
  rootJurisdiction: string;
  onNodeClick?: (node: GenealogicalNode) => void;
}

interface TreeNode extends d3.HierarchyPointNode<TreeNodeData> {
  data: TreeNodeData;
}

interface TreeNodeData {
  name: string;
  jurisdiction: string;
  confidence: number;
  year?: number;
  influence_score?: number;
  children?: TreeNodeData[];
  type: 'ancestor' | 'root' | 'descendant';
}

export const GenealogicalTree: React.FC<GenealogicalTreeProps> = ({
  ancestors,
  descendants,
  rootConcept,
  rootJurisdiction,
  onNodeClick,
}) => {
  const svgRef = useRef<SVGSVGElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [dimensions, setDimensions] = useState({ width: 800, height: 600 });

  useEffect(() => {
    const updateDimensions = () => {
      if (containerRef.current) {
        setDimensions({
          width: containerRef.current.clientWidth,
          height: Math.max(600, ancestors.length * 80 + descendants.length * 80 + 200),
        });
      }
    };

    updateDimensions();
    window.addEventListener('resize', updateDimensions);
    return () => window.removeEventListener('resize', updateDimensions);
  }, [ancestors.length, descendants.length]);

  useEffect(() => {
    if (!svgRef.current) return;

    // Clear previous render
    d3.select(svgRef.current).selectAll('*').remove();

    // Build hierarchical data structure
    const rootData: TreeNodeData = {
      name: rootConcept,
      jurisdiction: rootJurisdiction,
      confidence: 1.0,
      type: 'root',
      children: descendants.map((d) => ({
        name: d.concept,
        jurisdiction: d.jurisdiction,
        confidence: d.confidence,
        year: d.year,
        influence_score: d.influence_score,
        type: 'descendant' as const,
      })),
    };

    // Create ancestor tree (reversed)
    const ancestorTree: TreeNodeData[] = ancestors.map((a) => ({
      name: a.concept,
      jurisdiction: a.jurisdiction,
      confidence: a.confidence,
      year: a.year,
      influence_score: a.influence_score,
      type: 'ancestor' as const,
    }));

    // Setup SVG
    const svg = d3.select(svgRef.current);
    const margin = { top: 40, right: 120, bottom: 40, left: 120 };
    const width = dimensions.width - margin.left - margin.right;
    const height = dimensions.height - margin.top - margin.bottom;

    const g = svg
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom as any);

    // Create tree layout for descendants
    const treeLayout = d3.tree<TreeNodeData>().size([width, height / 2]);
    const rootHierarchy = d3.hierarchy(rootData);
    const treeData = treeLayout(rootHierarchy) as TreeNode;

    // Draw descendants
    const descendantLinks = treeData.links();
    const descendantNodes = treeData.descendants();

    g.selectAll('.link-descendant')
      .data(descendantLinks)
      .enter()
      .append('path')
      .attr('class', 'link-descendant')
      .attr('d', d3.linkVertical<any, any>()
        .x((d: any) => d.x)
        .y((d: any) => d.y + height / 2))
      .attr('fill', 'none')
      .attr('stroke', '#10b981')
      .attr('stroke-width', (d: any) => Math.max(1, d.target.data.confidence * 3))
      .attr('stroke-opacity', 0.6);

    // Draw ancestors (reversed direction)
    const ancestorYScale = d3.scaleLinear()
      .domain([0, ancestors.length])
      .range([height / 2, 0]);

    ancestorTree.forEach((ancestor, i) => {
      const y = ancestorYScale(i);
      
      // Link from ancestor to root
      g.append('path')
        .attr('class', 'link-ancestor')
        .attr('d', `M${width / 2},${height / 2} L${width / 2},${y}`)
        .attr('fill', 'none')
        .attr('stroke', '#f59e0b')
        .attr('stroke-width', Math.max(1, ancestor.confidence * 3))
        .attr('stroke-opacity', 0.6)
        .attr('stroke-dasharray', '5,5');

      // Ancestor node
      const nodeGroup = g.append('g')
        .attr('class', 'node-ancestor')
        .attr('transform', `translate(${width / 2},${y})`)
        .style('cursor', 'pointer')
        .on('click', () => onNodeClick?.(ancestors[i]));

      nodeGroup.append('circle')
        .attr('r', 8)
        .attr('fill', '#f59e0b')
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);

      nodeGroup.append('text')
        .attr('x', -15)
        .attr('text-anchor', 'end')
        .attr('font-size', '12px')
        .attr('font-weight', 'bold')
        .attr('fill', '#1f2937')
        .text(ancestor.name);

      nodeGroup.append('text')
        .attr('x', -15)
        .attr('y', 15)
        .attr('text-anchor', 'end')
        .attr('font-size', '10px')
        .attr('fill', '#6b7280')
        .text(ancestor.jurisdiction + (ancestor.year ? ` (${ancestor.year})` : ''));
    });

    // Draw root node
    const rootNode = g.append('g')
      .attr('class', 'node-root')
      .attr('transform', `translate(${width / 2},${height / 2})`)
      .style('cursor', 'pointer');

    rootNode.append('circle')
      .attr('r', 12)
      .attr('fill', '#0ea5e9')
      .attr('stroke', '#fff')
      .attr('stroke-width', 3);

    rootNode.append('text')
      .attr('x', 0)
      .attr('y', -20)
      .attr('text-anchor', 'middle')
      .attr('font-size', '14px')
      .attr('font-weight', 'bold')
      .attr('fill', '#1f2937')
      .text(rootConcept);

    rootNode.append('text')
      .attr('x', 0)
      .attr('y', 25)
      .attr('text-anchor', 'middle')
      .attr('font-size', '12px')
      .attr('fill', '#6b7280')
      .text(rootJurisdiction);

    // Draw descendant nodes
    descendantNodes.forEach((node) => {
      if (node.depth === 0) return; // Skip root

      const nodeGroup = g.append('g')
        .attr('class', 'node-descendant')
        .attr('transform', `translate(${node.x},${node.y + height / 2})`)
        .style('cursor', 'pointer')
        .on('click', () => {
          const descendantNode = descendants.find(
            (d) => d.concept === node.data.name && d.jurisdiction === node.data.jurisdiction
          );
          if (descendantNode) onNodeClick?.(descendantNode);
        });

      nodeGroup.append('circle')
        .attr('r', 8)
        .attr('fill', '#10b981')
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);

      nodeGroup.append('text')
        .attr('x', 15)
        .attr('text-anchor', 'start')
        .attr('font-size', '12px')
        .attr('font-weight', 'bold')
        .attr('fill', '#1f2937')
        .text(node.data.name);

      nodeGroup.append('text')
        .attr('x', 15)
        .attr('y', 15)
        .attr('text-anchor', 'start')
        .attr('font-size', '10px')
        .attr('fill', '#6b7280')
        .text(node.data.jurisdiction + (node.data.year ? ` (${node.data.year})` : ''));
    });

    // Add legend
    const legend = g.append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(10, 10)`);

    const legendItems = [
      { label: 'Ancestors', color: '#f59e0b' },
      { label: 'Root Concept', color: '#0ea5e9' },
      { label: 'Descendants', color: '#10b981' },
    ];

    legendItems.forEach((item, i) => {
      const legendRow = legend.append('g')
        .attr('transform', `translate(0, ${i * 25})`);

      legendRow.append('circle')
        .attr('r', 6)
        .attr('fill', item.color);

      legendRow.append('text')
        .attr('x', 15)
        .attr('y', 5)
        .attr('font-size', '12px')
        .attr('fill', '#1f2937')
        .text(item.label);
    });

  }, [ancestors, descendants, rootConcept, rootJurisdiction, dimensions, onNodeClick]);

  return (
    <div ref={containerRef} className="w-full h-full bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="p-4 border-b border-gray-200 bg-gray-50">
        <h3 className="text-lg font-serif font-bold text-gray-900">
          Legal Genealogy Tree
        </h3>
        <p className="text-sm text-gray-600 mt-1">
          {ancestors.length} ancestors • {descendants.length} descendants • Use scroll to zoom
        </p>
      </div>
      <svg
        ref={svgRef}
        width={dimensions.width}
        height={dimensions.height}
        className="bg-gray-50"
      />
    </div>
  );
};

export default GenealogicalTree;
