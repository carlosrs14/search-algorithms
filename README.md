# Algorithms Visualizer

This project aims to implement and visualize various search algorithms. Through an intuitive user interface, you can explore and understand the functioning of classic algorithms such as BFS, DFS, A*, Dijkstra, and Greedy Search.

## How to Run Locally

1. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python main.py
   ```

## GitHub Pages Deployment

This project uses `pygbag` to compile the Pygame application to WebAssembly and deploy it to GitHub Pages. It allows anyone to play the simulation directly from their browser here is the url.
```
https://carlosrs14.github.io/search-algorithms/
```

If you are a contributor deploying this project, the GitHub Actions workflow will automatically build and publish to the `gh-pages` branch on push to the `main` branch.
