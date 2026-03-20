import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-menu',
  standalone: true,
  template: `
    <div class="menu-panel">
      <h2>Algorithms</h2>
      <div class="instructions">
        <p>Left Click Node: Set Start</p>
        <p>Right Click Node: Set End</p>
        <p>Space: Play/Pause</p>
      </div>

      <div class="button-group">
        @for (algo of algorithms; track algo) {
          <button 
            [class.active]="activeAlgo === algo"
            (click)="selectAlgo.emit(algo)">
            {{algo}}
          </button>
        }
      </div>

      <h2>Datasets</h2>
      <div class="button-group">
        @for (ds of datasets; track ds) {
          <button 
            [class.active]="activeDataset === ds"
            (click)="selectDataset.emit(ds)">
            {{ds}}
          </button>
        }
      </div>

      <h2>Speed: {{fps}} FPS</h2>
      <div class="speed-slider-container">
        <input type="range" 
               class="speed-slider"
               min="1" 
               max="60" 
               [value]="fps" 
               (input)="onSpeedChange($event)">
      </div>
    </div>
  `,
  styles: [`
    .menu-panel {
      padding: 20px;
      color: #abb2bf;
      background-color: #282c34;
      height: 100%;
      border-left: 2px solid #32323c;
      box-sizing: border-box;
      display: flex;
      flex-direction: column;
      gap: 15px;
    }
    h2 {
      margin: 10px 0 5px 0;
      font-size: 1.2rem;
      color: #e5c07b;
    }
    .instructions {
      font-size: 0.8rem;
      color: #7f848e;
    }
    .instructions p {
      margin: 2px 0;
    }
    .button-group {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .speed-slider-container {
      width: 100%;
      padding: 10px 0;
    }
    .speed-slider {
      width: 100%;
      cursor: pointer;
      accent-color: #61afef;
    }
    button {
      padding: 10px;
      border: none;
      border-radius: 8px;
      background-color: #3e4451;
      color: #abb2bf;
      cursor: pointer;
      font-weight: bold;
      flex: 1;
      transition: background-color 0.2s;
    }
    button:hover {
      background-color: #4b5363;
    }
    button.active {
      background-color: #61afef;
      color: #282c34;
    }
  `]
})
export class MenuComponent {
  @Input() algorithms: string[] = ['BFS', 'DFS', 'A*', 'Dijkstra', 'Greedy'];
  @Input() datasets: string[] = ['chn31', 'att48', 'chn144'];

  @Input() activeAlgo: string | null = null;
  @Input() activeDataset: string = 'chn31';
  @Input() fps: number = 20;

  @Output() selectAlgo = new EventEmitter<string>();
  @Output() selectDataset = new EventEmitter<string>();
  @Output() speedChange = new EventEmitter<number>();

  onSpeedChange(event: Event) {
    const val = +(event.target as HTMLInputElement).value;
    this.speedChange.emit(val);
  }
}
