import { Algorithm, NodeState } from './algorithm';
import { City } from '../models/city';

export class Greedy extends Algorithm {
  private closedSet: Set<number> = new Set();
  private frontierSet: Set<number> = new Set();
  private pq: { hScore: number, node: number }[] = [];
  private cameFrom: Map<number, number> = new Map();
  private cities: City[];

  constructor(graph: number[][], startNode: number, endNode: number, cities: City[]) {
    super(graph, startNode, endNode);
    this.cities = cities;
    this.pq.push({ hScore: this.heuristic(startNode, endNode), node: startNode });
  }

  private heuristic(node1: number, node2: number): number {
    const c1 = this.cities[node1];
    const c2 = this.cities[node2];
    return Math.sqrt(Math.pow(c1.x - c2.x, 2) + Math.pow(c1.y - c2.y, 2));
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
      this.pq.sort((a, b) => a.hScore - b.hScore);
      const current = this.pq.shift()!;
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
        if (weight > 0) { // Connected
          if (!this.closedSet.has(neighbor)) {
            this.cameFrom.set(neighbor, currentNode);
            this.pq.push({ hScore: this.heuristic(neighbor, this.endNode), node: neighbor });
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
      if (current === this.startNode) break;
      current = this.cameFrom.get(current)!;
    }
    path.push(this.startNode);
    // Remove duplicates if start was pushed twice
    return Array.from(new Set(path)).reverse();
  }
}
