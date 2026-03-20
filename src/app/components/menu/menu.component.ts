import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-menu',
  standalone: true,
  templateUrl: './menu.component.html',
  styleUrl: './menu.component.css'
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
