import { Component, OnInit, OnDestroy } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MapComponent } from './components/map/map.component';
import { MenuComponent } from './components/menu/menu.component';
import { GraphService } from './core/services/graph.service';
import { City } from './core/models/city';
import { Algorithm, NodeState } from './core/algorithms/algorithm';
import { BFS } from './core/algorithms/bfs';
import { DFS } from './core/algorithms/dfs';
import { AStar } from './core/algorithms/aStar';
import { Dijkstra } from './core/algorithms/dijkstra';
import { Greedy } from './core/algorithms/greedy';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, MapComponent, MenuComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent implements OnInit, OnDestroy {
  cities: City[] = [];
  graph: number[][] = [];

  startNode: number = 0;
  endNode: number = 0;

  frontier: Set<number> = new Set();
  visited: Set<number> = new Set();
  currentNode: number | null = null;
  path: number[] = [];

  activeAlgo: string | null = null;
  activeDataset: string = 'chn31';

  fps = 10;

  isPaused = false;
  algoGenerator: Generator<NodeState, void, unknown> | null = null;

  private animationFrameId: number | null = null;
  private lastFrameTime = 0;

  constructor(private graphService: GraphService) { }

  ngOnInit() {
    this.loadDataset(this.activeDataset);

    // Listen for space key to pause/play
    window.addEventListener('keydown', this.handleKeyDown);
    this.animationLoop(performance.now());
  }

  ngOnDestroy() {
    window.removeEventListener('keydown', this.handleKeyDown);
    if (this.animationFrameId !== null) {
      cancelAnimationFrame(this.animationFrameId);
    }
  }

  private handleKeyDown = (event: KeyboardEvent) => {
    if (event.code === 'Space') {
      this.isPaused = !this.isPaused;
      event.preventDefault();
    }
  };

  async loadDataset(dataset: string) {
    this.isPaused = true;
    this.algoGenerator = null;
    this.activeDataset = dataset;

    try {
      const data = await this.graphService.loadGraph(dataset);
      this.cities = data.cities;
      this.graph = data.graph;

      this.startNode = 0;
      this.endNode = this.cities.length > 0 ? this.cities.length - 1 : 0;
      this.resetState();

      if (this.activeAlgo) {
        this.runAlgorithm(this.activeAlgo);
      }
    } catch (e) {
      console.error('Error loading dataset', e);
    }
  }

  resetState() {
    this.frontier = new Set();
    this.visited = new Set();
    this.currentNode = null;
    this.path = [];
  }

  runAlgorithm(algoName: string | null) {
    this.activeAlgo = algoName;
    this.resetState();
    this.algoGenerator = null;

    if (!algoName) return;

    let algo: Algorithm;
    switch (algoName) {
      case 'BFS':
        algo = new BFS(this.graph, this.startNode, this.endNode);
        break;
      case 'DFS':
        algo = new DFS(this.graph, this.startNode, this.endNode);
        break;
      case 'A*':
        algo = new AStar(this.graph, this.startNode, this.endNode, this.cities);
        break;
      case 'Dijkstra':
        algo = new Dijkstra(this.graph, this.startNode, this.endNode);
        break;
      case 'Greedy':
        algo = new Greedy(this.graph, this.startNode, this.endNode, this.cities);
        break;
      default:
        return;
    }

    this.algoGenerator = algo.solve();
    this.isPaused = false;
  }

  onNodeLeftClick(index: number) {
    this.startNode = index;
    if (this.activeAlgo) {
      this.runAlgorithm(this.activeAlgo);
    } else {
      this.resetState();
    }
  }

  onNodeRightClick(index: number) {
    this.endNode = index;
    if (this.activeAlgo) {
      this.runAlgorithm(this.activeAlgo);
    } else {
      this.resetState();
    }
  }

  onSelectAlgo(algo: string) {
    this.runAlgorithm(algo);
  }

  onSelectDataset(ds: string) {
    this.loadDataset(ds);
  }

  onSpeedChange(newFps: number) {
    this.fps = newFps;
  }

  onTogglePause() {
    this.isPaused = !this.isPaused;
  }

  private animationLoop = (timestamp: number) => {
    if (!this.isPaused && this.algoGenerator) {
      const msPerFrame = 1000 / this.fps;
      if (timestamp - this.lastFrameTime >= msPerFrame) {
        const result = this.algoGenerator.next();
        if (!result.done && result.value) {
          this.frontier = result.value.frontier;
          this.visited = result.value.visited;
          this.currentNode = result.value.currentNode;
          this.path = result.value.path;
        } else {
          this.algoGenerator = null; // finished
        }
        this.lastFrameTime = timestamp;
      }
    }

    this.animationFrameId = requestAnimationFrame(this.animationLoop);
  };
}
