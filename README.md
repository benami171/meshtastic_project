# 📡 Basic Meshtastic Network Simulator

A simple and educational Meshtastic mesh network simulator that demonstrates core concepts of decentralized radio communication networks.

## Purpose

This simulator showcases the fundamental principles of Meshtastic networks:
- **Mesh networking** - Nodes relay messages for each other
- **Range limitations** - Realistic radio communication constraints  
- **Multi-hop routing** - Messages travel through intermediate nodes
- **Network resilience** - Multiple paths for message delivery
- **Decentralized operation** - No central servers required

## Features

### User-Friendly GUI
- **Interactive network map** with visual node positioning
- **Real-time message routing** visualization with colored paths
- **Simple message sending** interface with dropdown menus
- **Network status monitoring** with live statistics
- **Message log** tracking all communication attempts

### 🌐 Network Simulation
- **Configurable network size** (1-100 nodes)
- **Automatic node placement** with realistic geographic distribution
- **Communication range visualization** with dotted circles
- **Dynamic connectivity** based on node positions
- **Realistic routing algorithms** using breadth-first search

### Prerequisites
```bash
pip install matplotlib networkx tkinter
```

### Running the Simulator
```bash
python main.py
```

### Basic Usage
1. **Launch** the application
2. **Choose network size** (1-100 nodes) and click "Create Network"
3. **Select sender and receiver** from dropdown menus
4. **Type your message** and click "Send Message"
5. **Watch the routing** - red arrows show the message path
6. **View statistics** - click "Show Statistics" for detailed metrics

## How to Use

### Creating Networks
- Use the **Nodes** spinbox to select 1-100 nodes
- Click **"Create Network"** to generate a new random topology
- Nodes are automatically named "Node 1", "Node 2", etc.

### Sending Messages
- Choose **From** and **To** nodes from dropdowns
- Enter your **message text**
- Click **"Send Message"** to attempt delivery
- **Green connections** show direct communication links
- **Red arrows** show successful message paths

### Understanding the Display
- **🟢 Green dots** = Active nodes
- **Green lines** = Direct communication links
- **Dotted circles** = Communication range for each node
- **Red arrows** = Message routing paths
- **Node labels** = Show node ID and position

## Technical Details

### Network Generation
- Nodes are placed randomly in a 350x350 coordinate space
- Communication range is automatically adjusted based on network size
- Smaller networks (≤10 nodes): 100-unit range
- Medium networks (11-50 nodes): 80-unit range  
- Large networks (≥51 nodes): 60-unit range

### Routing Algorithm
- Uses breadth-first search (BFS) for pathfinding
- Simulates realistic 3-hop limit (typical Meshtastic TTL)
- Messages fail if no path exists within hop limit
- Demonstrates network partitioning effects

### Visualization
- Real-time network topology display
- Color-coded message paths
- Distance-based connectivity
- Statistical performance tracking

## 📖 References

- [Meshtastic Project](https://meshtastic.org/) - Official Meshtastic documentation
- [LoRa Technology](https://lora-alliance.org/) - Learn about LoRa wireless protocol
- [Mesh Networking](https://en.wikipedia.org/wiki/Mesh_networking) - General mesh network concepts
