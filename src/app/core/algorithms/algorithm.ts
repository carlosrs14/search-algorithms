export interface NodeState {
  frontier: Set<number>;
  visited: Set<number>;
  currentNode: number | null;
  path: number[];
}

export abstract class Algorithm {
  constructor(
    protected graph: number[][],
    protected startNode: number,
    protected endNode: number
  ) {}

  abstract solve(): Generator<NodeState, void, unknown>;
}
