import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { firstValueFrom } from 'rxjs';
import { City } from '../models/city';

@Injectable({
  providedIn: 'root'
})
export class GraphService {
  constructor(private http: HttpClient) {}

  async loadGraph(datasetName: string, kNeighbors: number = 4): Promise<{ cities: City[], graph: number[][] }> {
    const data = await firstValueFrom(this.http.get(`data/${datasetName}.txt`, { responseType: 'text' }));
    return this.parseData(data, kNeighbors);
  }

  private parseData(data: string, kNeighbors: number): { cities: City[], graph: number[][] } {
    const lines = data.split('\n');
    let rawCities: { index: number, x: number, y: number }[] = [];

    for (const line of lines) {
      if (!line.trim()) continue;
      const parts = line.trim().split(/\s+/);
      if (parts.length >= 3) {
        rawCities.push({
          index: parseInt(parts[0], 10),
          x: parseFloat(parts[1]),
          y: parseFloat(parts[2])
        });
      }
    }

    const cities: City[] = [];
    if (rawCities.length > 0) {
      const minX = Math.min(...rawCities.map(c => c.x));
      const maxX = Math.max(...rawCities.map(c => c.x));
      const minY = Math.min(...rawCities.map(c => c.y));
      const maxY = Math.max(...rawCities.map(c => c.y));

      const rangeX = maxX > minX ? maxX - minX : 1;
      const rangeY = maxY > minY ? maxY - minY : 1;

      for (const city of rawCities) {
        // Normalize coordinates between 0.05 and 0.95
        const normX = 0.05 + 0.9 * ((city.x - minX) / rangeX);
        const normY = 0.05 + 0.9 * ((city.y - minY) / rangeY);
        cities.push({ index: city.index - 1, x: normX, y: normY });
      }
    }

    const rank = cities.length;
    let costMatrix: number[][] = Array(rank).fill(0).map(() => Array(rank).fill(0.0));

    for (let i = 0; i < rank; i++) {
      const distances: { dist: number, j: number }[] = [];
      for (let j = 0; j < rank; j++) {
        if (i !== j) {
          const dist = this.distance(cities[i], cities[j]);
          distances.push({ dist, j });
        }
      }

      distances.sort((a, b) => a.dist - b.dist);
      const kNearest = Math.min(kNeighbors, distances.length);
      for (let k = 0; k < kNearest; k++) {
        const item = distances[k];
        costMatrix[i][item.j] = item.dist;
        costMatrix[item.j][i] = item.dist;
      }
    }

    return { cities, graph: costMatrix };
  }

  private distance(city1: City, city2: City): number {
    return Math.sqrt(Math.pow(city1.x - city2.x, 2) + Math.pow(city1.y - city2.y, 2));
  }
}
