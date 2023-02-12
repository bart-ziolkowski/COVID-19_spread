### Table 1: Benchmarks table for uninformed search.

| Level             | Eval   | Heuristic  | States Generated | Time/s  | Solution length |
|-------------------|--------|------------|------------------|---------|-----------------|
| MAPF00            | A*     | Goal Count | < 10 000         | 0,146   | 14              |
| MAPF00            | Greedy | Goal Count | < 10 000         | 0,047   | 16              |
| MAPF01            | A*     | Goal Count | < 10 000         | 0,113   | 14              |
| MAPF01            | Greedy | Goal Count | < 10 000         | 0,084   | 137             |
| MAPF02            | A*     | Goal Count | 105 834          | 6,192   | 14              |
| MAPF02            | Greedy | Goal Count | < 10 000         | 0,166   | 206             |
| MAPF03            | A*     | Goal Count | 881 237          | 175,709 | -               |
| MAPF03            | Greedy | Goal Count | < 10 000         | 0,477   | 364             |
