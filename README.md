# 📡 Time-Discrete Meshtastic Network Simulator

A comprehensive time-discrete Meshtastic mesh network simulator that demonstrates core concepts of decentralized radio communication networks with realistic timing and message propagation.

<img width="1346" height="941" alt="Image" src="https://github.com/user-attachments/assets/8ea075a1-a4fb-4e09-b8d2-ee3f18933a1d" />


## Purpose

This simulator showcases the fundamental principles of Meshtastic networks with time-discrete simulation:
- **Time-discrete simulation** - Advances in configurable time steps (100ms default)
- **Mesh networking** - Nodes relay messages for each other over time
- **Realistic transmission delays** - Messages take time to propagate through hops
- **Range limitations** - Realistic radio communication constraints  
- **Multi-hop routing** - Messages travel through intermediate nodes with timing
- **Network resilience** - Multiple paths for message delivery
- **Decentralized operation** - No central servers required

## Features

### ⏱️ Time-Discrete Simulation
- **Simulation clock** advancing in discrete time steps (0.1s default)
- **Real-time message propagation** with transmission delays
- **Message queue processing** showing pending, transmitting, and delivered states
- **Start/Stop/Reset simulation controls**
- **Live simulation time display**
- **Message timing statistics** including delivery times

### User-Friendly GUI
- **Interactive network map** with visual node positioning
- **Real-time message routing** visualization with colored paths
- **Simulation controls** - Start, Stop, Reset simulation
- **Message states visualization** - Pending (queued), Transmitting (orange dashed), Delivered (red solid)
- **Simple message sending** interface with dropdown menus
- **Network status monitoring** with live statistics including simulation state
- **Message log** tracking all communication attempts with timestamps

### 🌐 Network Simulation
- **Configurable network size** (1-100 nodes)
- **Automatic node placement** with realistic geographic distribution
- **Communication range visualization** with dotted circles
- **Dynamic connectivity** based on node positions
- **Realistic routing algorithms** using breadth-first search
- **Time-based message transmission** (0.1s per hop default)

### Prerequisites
```bash
pip install matplotlib networkx tkinter threading
```

### Running the Simulator
```bash
python meshtastic_sim.py
```

### Basic Usage
1. **Launch** the application
2. **Choose network size** (1-100 nodes) and click "Create Network"
3. **Start the simulation** by clicking "▶️ Start Simulation"
4. **Select sender and receiver** from dropdown menus
5. **Type your message** and click "Send Message"
6. **Watch real-time routing** - orange dashed lines show transmitting messages, red solid lines show delivered messages
7. **Monitor simulation time** and message states in the status panel
8. **View statistics** - click "Show Statistics" for detailed timing metrics

## How to Use

### Starting Simulation
- **▶️ Start Simulation** - Begins the time-discrete simulation clock
- **⏸️ Stop Simulation** - Pauses the simulation (messages remain in queue)
- **🔄 Reset** - Resets simulation time to 0 and clears all messages
- **Simulation Time** - Displays current simulation time in seconds

### Creating Networks
- Use the **Nodes** spinbox to select 1-100 nodes
- Click **"Create Network"** to generate a new random topology
- Nodes are automatically named "Node 1", "Node 2", etc.
- Communication range automatically adjusts based on network size

### Sending Messages
- **Start the simulation first** for time-discrete message processing
- Choose **From** and **To** nodes from dropdowns
- Enter your **message text**
- Click **"Send Message"** to add message to queue
- Messages are processed in discrete time steps with realistic delays

### Understanding the Display
- **🟢 Green dots** = Active nodes
- **Green lines** = Direct communication links
- **Dotted circles** = Communication range for each node
- **Orange dashed lines** = Messages currently transmitting
- **Red solid lines** = Successfully delivered messages
- **Red X marks** = Failed message attempts
- **Node labels** = Show node ID and position

### Message States
- **Pending** = Queued for transmission, waiting for routing
- **Transmitting** = Currently being sent through the network (orange visualization)
- **Delivered** = Successfully reached destination (red visualization)
- **Failed** = Could not find route or delivery failed

## Technical Details

### Time-Discrete Simulation
- **Time Step**: 0.1 seconds (100ms) - configurable
- **Simulation Speed**: Runs at 10x real-time for demonstration
- **Message Transmission**: Each hop takes 0.1 simulation seconds
- **Threading**: Simulation runs in separate thread from GUI
- **Event Processing**: Messages queued and processed at each time step

### Network Generation
- Nodes are placed in a grid pattern with random offsets
- Communication range is automatically adjusted based on network size:
  - Small networks (≤10 nodes): 120-unit range
  - Medium networks (11-25 nodes): 100-unit range  
  - Large networks (26-50 nodes): 85-unit range
  - Extra large networks (≥51 nodes): 75-unit range

### Routing Algorithm
- Uses breadth-first search (BFS) for pathfinding
- Simulates realistic 3-hop limit (typical Meshtastic TTL)
- Messages fail if no path exists within hop limit
- Path is calculated once, then message follows predetermined route
- Each hop experiences realistic transmission delay

### Message Processing
- **Queue System**: Messages enter queue when sent
- **State Tracking**: Each message has status (pending/transmitting/delivered/failed)
- **Timing**: Creation time, hop timing, and delivery time tracked
- **Path Visualization**: Real-time display of message progress through network

### Performance Metrics
- **Delivery Statistics**: Success/failure rates
- **Timing Analysis**: Average delivery times
- **Network Analysis**: Connectivity percentages
- **Queue Monitoring**: Real-time queue size tracking

## Key Improvements in Time-Discrete Version

### ✅ Assignment Requirements Met
- **Time-discrete simulation**: Advances in fixed 0.1s time steps
- **100+ client support**: Tested up to 100 nodes with dynamic scaling
- **Flexible configuration**: Node count, simulation parameters
- **Message statistics**: Complete tracking with timing data
- **RF link budget model**: Distance-based with range limitations
- **Comprehensive GUI**: Full debugging and monitoring interface

### 🔧 Enhanced Features
- **Real-time message propagation** with visible transmission delays
- **Simulation controls** for start/stop/reset functionality  
- **Message state tracking** (pending → transmitting → delivered/failed)
- **Performance timing** analysis with delivery time metrics
- **Queue visualization** showing message processing pipeline
- **Thread-safe operation** with GUI responsiveness maintained

## 📖 References

- [Meshtastic Project](https://meshtastic.org/) - Official Meshtastic documentation
- [LoRa Technology](https://lora-alliance.org/) - Learn about LoRa wireless protocol
- [Mesh Networking](https://en.wikipedia.org/wiki/Mesh_networking) - General mesh network concepts
- [Discrete Event Simulation](https://en.wikipedia.org/wiki/Discrete_event_simulation) - Simulation methodology
