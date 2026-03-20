import { Algorithm, NodeState } from './algorithm';

export class BFS extends Algorithm {
  private queue: number[] = [];
  private visitedSet: Set<number> = new Set();
  private frontierSet: Set<number> = new Set();
  private cameFrom: Map<number, number | null> = new Map();

  constructor(graph: number[][], startNode: number, endNode: number) {
    super(graph, startNode, endNode);
    this.queue.push(this.startNode);
    this.visitedSet.add(this.startNode);
    this.cameFrom.set(this.startNode, null);
  }

  *solve(): Generator<NodeState, void, unknown> {
    this.frontierSet.add(this.startNode);
    yield {
      frontier: new Set(this.frontierSet),
      visited: new Set(this.visitedSet),
      currentNode: this.startNode,
      path: [this.startNode]
    };

    while (this.queue.length > 0) {
      const currentNode = this.queue.shift()!;
      this.frontierSet.delete(currentNode);
      this.visitedSet.add(currentNode);

      if (currentNode === this.endNode) {
        yield {
          frontier: new Set(this.frontierSet),
          visited: new Set(this.visitedSet),
          currentNode: currentNode,
          path: this.reconstructPath(currentNode)
        };
        return;
      }

      for (let neighbor = 0; neighbor < this.graph[currentNode].length; neighbor++) {
        const weight = this.graph[currentNode][neighbor];
        if (weight > 0 && !this.visitedSet.has(neighbor) && !this.frontierSet.has(neighbor)) {
          this.frontierSet.add(neighbor);
          this.cameFrom.set(neighbor, currentNode);
          this.queue.push(neighbor);
        }
      }

      yield {
        frontier: new Set(this.frontierSet),
        visited: new Set(this.visitedSet),
        currentNode: currentNode,
        path: this.reconstructPath(currentNode)
      };
    }
  }

  private reconstructPath(targetNode: number): number[] {
    const path: number[] = [];
    let current: number | null = targetNode;
    while (current !== null) {
      path.push(current);
      current = this.cameFrom.get(current) ?? null;
    }
    return path.reverse();
  }
}
