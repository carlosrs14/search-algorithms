import { Algorithm, NodeState } from './algorithm';

export class Dijkstra extends Algorithm {
  private closedSet: Set<number> = new Set();
  private frontierSet: Set<number> = new Set();
  private pq: { distance: number, node: number }[] = [];
  private cameFrom: Map<number, number> = new Map();
  private distances: Map<number, number> = new Map();

  constructor(graph: number[][], startNode: number, endNode: number) {
    super(graph, startNode, endNode);

    for (let i = 0; i < graph.length; i++) {
      this.distances.set(i, Infinity);
    }

    this.distances.set(startNode, 0);
    this.pq.push({ distance: 0, node: startNode });
  }

  *solve(): Generator<NodeState, void, unknown> {
    this.frontierSet.add(this.startNode);
    yield {
      frontier: new Set(this.frontierSet),
      visited: new Set(this.closedSet),
      currentNode: this.startNode,
      path: [this.startNode]
    };

    while (this.pq.length > 0) {
      this.pq.sort((a, b) => a.distance - b.distance);
      const current = this.pq.shift()!;
      const currentDistance = current.distance;
      const currentNode = current.node;

      this.frontierSet.delete(currentNode);

      if (this.closedSet.has(currentNode)) {
        continue;
      }

      this.closedSet.add(currentNode);

      if (currentNode === this.endNode) {
        yield {
          frontier: new Set(this.frontierSet),
          visited: new Set(this.closedSet),
          currentNode: currentNode,
          path: this.reconstructPath()
        };
        return;
      }

      for (let neighbor = 0; neighbor < this.graph[currentNode].length; neighbor++) {
        const weight = this.graph[currentNode][neighbor];
        if (weight > 0) {
          const distance = currentDistance + weight;

          if (distance < this.distances.get(neighbor)!) {
            this.distances.set(neighbor, distance);
            this.cameFrom.set(neighbor, currentNode);
            this.pq.push({ distance, node: neighbor });
            this.frontierSet.add(neighbor);
          }
        }
      }

      yield {
        frontier: new Set(this.frontierSet),
        visited: new Set(this.closedSet),
        currentNode: currentNode,
        path: this.reconstructPath(currentNode)
      };
    }
  }

  private reconstructPath(targetNode: number | null = null): number[] {
    let current = targetNode !== null ? targetNode : this.endNode;
    const path: number[] = [];
    while (this.cameFrom.has(current)) {
      path.push(current);
      current = this.cameFrom.get(current)!;
    }
    path.push(this.startNode);
    return path.reverse();
  }
}
