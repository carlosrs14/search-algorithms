import { Algorithm, NodeState } from './algorithm';
import { City } from '../models/city';

export class AStar extends Algorithm {
  private closedSet: Set<number> = new Set();
  private frontierSet: Set<number> = new Set();
  private openSet: { fScore: number, node: number }[] = [];
  private cameFrom: Map<number, number> = new Map();
  private gScore: Map<number, number> = new Map();
  private fScore: Map<number, number> = new Map();
  private cities: City[];

  constructor(graph: number[][], startNode: number, endNode: number, cities: City[]) {
    super(graph, startNode, endNode);
    this.cities = cities;

    for (let i = 0; i < graph.length; i++) {
      this.gScore.set(i, Infinity);
      this.fScore.set(i, Infinity);
    }

    this.gScore.set(startNode, 0);
    this.fScore.set(startNode, this.heuristic(startNode, endNode));
    this.openSet.push({ fScore: this.fScore.get(startNode)!, node: startNode });
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

    while (this.openSet.length > 0) {
      this.openSet.sort((a, b) => a.fScore - b.fScore);
      const current = this.openSet.shift()!;
      const currentNode = current.node;

      this.frontierSet.delete(currentNode);

      if (currentNode === this.endNode) {
        yield {
          frontier: new Set(this.frontierSet),
          visited: new Set(this.closedSet),
          currentNode: currentNode,
          path: this.reconstructPath()
        };
        return;
      }

      this.closedSet.add(currentNode);

      for (let neighbor = 0; neighbor < this.graph[currentNode].length; neighbor++) {
        const weight = this.graph[currentNode][neighbor];
        if (weight > 0) {
          if (this.closedSet.has(neighbor)) {
            continue;
          }

          const tentativeGScore = this.gScore.get(currentNode)! + weight;

          if (tentativeGScore < this.gScore.get(neighbor)!) {
            this.cameFrom.set(neighbor, currentNode);
            this.gScore.set(neighbor, tentativeGScore);
            const neighborFScore = tentativeGScore + this.heuristic(neighbor, this.endNode);
            this.fScore.set(neighbor, neighborFScore);

            const inOpenSet = this.openSet.find(n => n.node === neighbor);
            if (!inOpenSet) {
              this.openSet.push({ fScore: neighborFScore, node: neighbor });
              this.frontierSet.add(neighbor);
            } else {
              inOpenSet.fScore = neighborFScore;
            }
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
