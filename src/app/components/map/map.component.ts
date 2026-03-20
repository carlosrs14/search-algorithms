import { Component, ElementRef, EventEmitter, Input, OnChanges, Output, SimpleChanges, ViewChild } from '@angular/core';
import { City } from '../../core/models/city';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [],
  template: `
    <div class="map-container">
      <canvas #canvas
        (mousedown)="onMouseDown($event)"
        (contextmenu)="onContextMenu($event)"></canvas>
    </div>
  `,
  styles: [`
    .map-container {
      width: 100%;
      height: 100%;
      background-color: #21252b;
    }
    canvas {
      display: block;
      width: 100%;
      height: 100%;
    }
  `]
})
export class MapComponent implements OnChanges {
  @ViewChild('canvas', { static: true }) canvasRef!: ElementRef<HTMLCanvasElement>;
  
  @Input() cities: City[] = [];
  @Input() graph: number[][] = [];
  @Input() frontier: Set<number> = new Set();
  @Input() visited: Set<number> = new Set();
  @Input() currentNode: number | null = null;
  @Input() path: number[] = [];
  @Input() startNode: number = 0;
  @Input() endNode: number = 0;
  
  @Output() nodeLeftClick = new EventEmitter<number>();
  @Output() nodeRightClick = new EventEmitter<number>();

  private ctx!: CanvasRenderingContext2D;
  private width = 0;
  private height = 0;
  private padding = 50;
  private scaleX = 0;
  private scaleY = 0;

  // Colors from colors.py
  private BACKGROUND = '#21252b';
  private NODE_COLOR = '#abb2bf';
  private EDGE_COLOR = '#3e4451';
  private START_COLOR = '#98c379';
  private END_COLOR = '#e06c75';
  private VISITED_COLOR = '#c678dd';
  private FRONTIER_COLOR = '#61afef';
  private PATH_COLOR = '#e5c07b';

  ngAfterViewInit() {
    const canvas = this.canvasRef.nativeElement;
    this.ctx = canvas.getContext('2d')!;
    
    // Setup resize observer
    const observer = new ResizeObserver(entries => {
      for (let entry of entries) {
        this.width = entry.contentRect.width;
        this.height = entry.contentRect.height;
        canvas.width = this.width;
        canvas.height = this.height;
        this.updateScale();
        this.draw();
      }
    });
    observer.observe(canvas.parentElement!);
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (this.ctx) {
      if (changes['cities'] || changes['graph']) {
        this.updateScale();
      }
      this.draw();
    }
  }

  private updateScale() {
    this.scaleX = this.width - 2 * this.padding;
    this.scaleY = this.height - 2 * this.padding;
  }

  private scalePoint(city: City): { x: number, y: number } {
    return {
      x: city.x * this.scaleX + this.padding,
      y: city.y * this.scaleY + this.padding
    };
  }

  private draw() {
    if (!this.ctx || this.width === 0) return;
    
    this.ctx.fillStyle = this.BACKGROUND;
    this.ctx.fillRect(0, 0, this.width, this.height);

    const rank = this.cities.length;
    
    // Draw edges
    this.ctx.strokeStyle = this.EDGE_COLOR;
    this.ctx.lineWidth = 1;
    this.ctx.beginPath();
    for (let i = 0; i < rank; i++) {
      for (let j = i + 1; j < rank; j++) {
        if (this.graph[i][j] > 0) {
          const p1 = this.scalePoint(this.cities[i]);
          const p2 = this.scalePoint(this.cities[j]);
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
        }
      }
    }
    this.ctx.stroke();

    // Draw path
    if (this.path && this.path.length > 1) {
      this.ctx.strokeStyle = this.PATH_COLOR;
      this.ctx.lineWidth = 4;
      this.ctx.beginPath();
      const pFirst = this.scalePoint(this.cities[this.path[0]]);
      this.ctx.moveTo(pFirst.x, pFirst.y);
      for (let i = 1; i < this.path.length; i++) {
        const p = this.scalePoint(this.cities[this.path[i]]);
        this.ctx.lineTo(p.x, p.y);
      }
      this.ctx.stroke();
    }

    // Draw nodes
    for (let i = 0; i < rank; i++) {
      const pos = this.scalePoint(this.cities[i]);
      let color = this.NODE_COLOR;
      let radius = 4;

      if (this.visited.has(i)) {
        color = this.VISITED_COLOR;
        radius = 5;
      }
      if (this.frontier.has(i)) {
        color = this.FRONTIER_COLOR;
        radius = 6;
      }
      if (i === this.startNode) {
        color = this.START_COLOR;
        radius = 8;
      } else if (i === this.endNode) {
        color = this.END_COLOR;
        radius = 8;
      }

      this.ctx.fillStyle = color;
      this.ctx.beginPath();
      this.ctx.arc(pos.x, pos.y, radius, 0, Math.PI * 2);
      this.ctx.fill();
    }
  }

  getCityAtPos(x: number, y: number, radius = 15): number | null {
    for (let i = 0; i < this.cities.length; i++) {
      let p = this.scalePoint(this.cities[i]);
      if (Math.pow(x - p.x, 2) + Math.pow(y - p.y, 2) <= radius * radius) {
        return i;
      }
    }
    return null;
  }

  onMouseDown(event: MouseEvent) {
    if (event.button === 0) { // Left click
      let cityIdx = this.getCityAtPos(event.offsetX, event.offsetY);
      if (cityIdx !== null) this.nodeLeftClick.emit(cityIdx);
    }
  }

  onContextMenu(event: MouseEvent) {
    event.preventDefault(); // Prevent native menu
    let cityIdx = this.getCityAtPos(event.offsetX, event.offsetY);
    if (cityIdx !== null) this.nodeRightClick.emit(cityIdx);
  }
}
