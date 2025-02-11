# 🎨 Heuristics for Graph Coloring

This project explores **graph coloring**, a fundamental problem in graph theory with applications in scheduling, frequency assignment, and resource allocation. It focuses on developing **efficient heuristic algorithms**, particularly an **optimized hybrid approach** combining **DSATUR** and **greedy heuristics**.

## 🚀 Key Features
- **DSATUR Algorithm** – A heuristic approach minimizing the chromatic number.
- **Hybrid Parallelized Approach** – Combines **greedy coloring** with **parallelized DSATUR** for improved efficiency.
- **Graph Parsing & Visualization** – Reads **DIMACS-formatted graphs** and provides **visual representations**.
- **Benchmarking & Performance Evaluation** – Tests algorithms on **large and dense graphs**.
- **Multi-Threaded Execution** – Implements **parallel graph coloring** to optimize processing time.

## ⚙️ Tech Stack
- **Programming Language**: Python
- **Libraries Used**: `networkx`, `matplotlib`, `concurrent.futures`
- **Data Format**: DIMACS Graph Representation

## 📊 Results & Findings
- The **hybrid approach** significantly **reduces execution time** while maintaining **coloring accuracy**.
- Parallelized DSATUR achieves a **24× speedup** over traditional methods.
- The system efficiently handles **large, high-density graphs** with up to **1,000 vertices and 245,000 edges**.

### 🔍 Future Enhancements
- **Adaptive thread management** for better scalability.
- **Integration of evolutionary algorithms** for improved optimization.
- **Extended benchmark datasets** for further validation.

This project bridges the gap between **theoretical research and real-world applications**, providing a **scalable and high-performance** solution for complex graph coloring problems. 🚀
