"""
Basic Meshtastic Simulator
Simple showcase of core Meshtastic functionality with clear GUI
"""
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import random
import math
import time

class MeshtasticNode:
    def __init__(self, node_id, x, y, name=None):
        self.id = node_id
        self.x = x
        self.y = y
        self.name = name or f"Node {node_id}"
        self.messages = []  # Messages this node has
        self.battery = 100
        self.is_online = True
        
class MeshtasticMessage:
    def __init__(self, msg_id, from_node, to_node, text, hops_left=3):
        self.id = msg_id
        self.from_node = from_node
        self.to_node = to_node
        self.text = text
        self.hops_left = hops_left
        self.path = [from_node]  # Track which nodes it's been through
        self.delivered = False
        self.timestamp = time.time()

class BasicMeshtasticGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Basic Meshtastic Network Simulator")
        self.root.geometry("1200x800")
        
        # Network data
        self.nodes = {}
        self.messages = []
        self.message_counter = 0
        
        # Dynamic range based on network size (will be set when network is created)
        self.max_range = 150
        
        # Setup GUI
        self.setup_gui()
        self.create_custom_network()  # Start with default 6 nodes
        self.update_display()
        
    def setup_gui(self):
        """Create the main GUI layout"""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        control_frame = ttk.LabelFrame(main_frame, text="📡 Meshtastic Controls", padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Network status
        ttk.Label(control_frame, text="🌐 Network Status", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(0, 10))
        
        self.status_text = tk.Text(control_frame, height=8, width=30, wrap=tk.WORD)
        self.status_text.pack(pady=(0, 10))
        
        # Message controls
        ttk.Label(control_frame, text="📝 Send Message", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        ttk.Label(control_frame, text="From:").pack(anchor=tk.W)
        self.from_var = tk.StringVar()
        self.from_combo = ttk.Combobox(control_frame, textvariable=self.from_var, width=25)
        self.from_combo.pack(pady=(0, 5))
        
        ttk.Label(control_frame, text="To:").pack(anchor=tk.W)
        self.to_var = tk.StringVar()
        self.to_combo = ttk.Combobox(control_frame, textvariable=self.to_var, width=25)
        self.to_combo.pack(pady=(0, 5))
        
        ttk.Label(control_frame, text="Message:").pack(anchor=tk.W)
        self.message_entry = tk.Entry(control_frame, width=28)
        self.message_entry.pack(pady=(0, 10))
        
        ttk.Button(control_frame, text="📤 Send Message", 
                  command=self.send_message).pack(pady=(0, 10))
        
        # Network actions
        ttk.Label(control_frame, text="⚙️ Network Actions", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(10, 5))
        
        ttk.Button(control_frame, text="🔄 Refresh Network", 
                  command=self.update_display).pack(pady=2, fill=tk.X)
        
        ttk.Button(control_frame, text="📊 Show Statistics", 
                  command=self.show_statistics).pack(pady=2, fill=tk.X)
        
        # Node count selection
        node_frame = ttk.Frame(control_frame)
        node_frame.pack(pady=2, fill=tk.X)
        
        ttk.Label(node_frame, text="Nodes:").pack(side=tk.LEFT)
        self.node_count_var = tk.StringVar(value="10")
        self.node_count_spinbox = tk.Spinbox(node_frame, from_=1, to=100, width=5, 
                                           textvariable=self.node_count_var)
        self.node_count_spinbox.pack(side=tk.LEFT, padx=(5, 0))
        
        ttk.Button(control_frame, text="🆕 Create Network", 
                  command=self.create_custom_network).pack(pady=2, fill=tk.X)
        
        # Message log
        ttk.Label(control_frame, text="📋 Message Log", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=(20, 5))
        
        self.log_text = tk.Text(control_frame, height=10, width=30, wrap=tk.WORD)
        log_scroll = ttk.Scrollbar(control_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scroll.set)
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Right panel - Network visualization
        viz_frame = ttk.LabelFrame(main_frame, text="🗺️ Network Map", padding=10)
        viz_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def create_sample_network(self):
        """Create a sample Meshtastic network"""
        self.nodes.clear()
        self.messages.clear()
        self.message_counter = 0
        
        # Create nodes in a realistic pattern
        node_configs = [
            (0, 100, 100, "Home Base"),
            (1, 200, 150, "Alice's Phone"),
            (2, 300, 120, "Bob's Device"),
            (3, 150, 250, "Car Radio"),
            (4, 350, 200, "Hiking Beacon"),
            (5, 250, 300, "Camp Site"),
        ]
        
        for node_id, x, y, name in node_configs:
            self.nodes[node_id] = MeshtasticNode(node_id, x, y, name)
        
        # Update UI
        self.update_node_lists()
        self.update_display()
        self.log_message("🌐 New Meshtastic network created with 6 nodes")
        
    def create_custom_network(self):
        """Create a network with user-specified number of nodes"""
        try:
            num_nodes = int(self.node_count_var.get())
            if num_nodes < 1 or num_nodes > 100:
                messagebox.showwarning("Invalid Input", "Please choose between 1 and 100 nodes")
                return
                
            self.nodes.clear()
            self.messages.clear()
            self.message_counter = 0
            
            # Create nodes in a grid pattern with some randomness
            grid_size = math.ceil(math.sqrt(num_nodes))
            spacing = 60  # Space between nodes
            margin = 50   # Margin from edges
            
            for i in range(num_nodes):
                # Calculate grid position
                row = i // grid_size
                col = i % grid_size
                
                # Base position with some random offset for natural look
                base_x = margin + col * spacing + random.uniform(-15, 15)
                base_y = margin + row * spacing + random.uniform(-15, 15)
                
                # Ensure nodes stay within bounds
                x = max(margin, min(400 - margin, base_x))
                y = max(margin, min(350 - margin, base_y))
                
                node_name = f"Node {i + 1}"
                self.nodes[i] = MeshtasticNode(i, x, y, node_name)
            
            # Adjust communication range based on network size for better connectivity
            if num_nodes <= 10:
                self.max_range = 120
            elif num_nodes <= 25:
                self.max_range = 100
            elif num_nodes <= 50:
                self.max_range = 85
            else:
                self.max_range = 75
            
            # Update UI
            self.update_node_lists()
            self.update_display()
            self.log_message(f"🌐 New Meshtastic network created with {num_nodes} nodes")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of nodes")
        
    def update_node_lists(self):
        """Update the dropdown lists with current nodes"""
        node_names = [f"{node.id + 1}: {node.name}" for node in self.nodes.values()]
        self.from_combo['values'] = node_names
        self.to_combo['values'] = node_names
        
    def can_communicate(self, node1_id, node2_id):
        """Check if two nodes can communicate directly"""
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]
        
        distance = math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)
        return distance <= self.max_range and node1.is_online and node2.is_online
        
    def send_message(self):
        """Send a message through the mesh network"""
        try:
            from_text = self.from_var.get()
            to_text = self.to_var.get()
            message_text = self.message_entry.get().strip()
            
            if not from_text or not to_text or not message_text:
                messagebox.showwarning("Missing Info", "Please fill all fields")
                return
                
            from_id = int(from_text.split(':')[0]) - 1  # Convert to 0-based index
            to_id = int(to_text.split(':')[0]) - 1    # Convert to 0-based index
            
            if from_id == to_id:
                messagebox.showwarning("Invalid", "Cannot send message to same node")
                return
                
            # Create message
            msg = MeshtasticMessage(self.message_counter, from_id, to_id, message_text)
            self.message_counter += 1
            self.messages.append(msg)
            
            # Try to route the message
            success = self.route_message(msg)
            
            if success:
                self.log_message(f"✅ Message sent: '{message_text}' from {self.nodes[from_id].name} to {self.nodes[to_id].name}")
            else:
                self.log_message(f"❌ Message failed: No route to {self.nodes[to_id].name}")
                
            # Clear form
            self.message_entry.delete(0, tk.END)
            self.update_display()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send message: {str(e)}")
            
    def route_message(self, message):
        """Route message through the mesh network using simple flooding"""
        visited = set([message.from_node])
        queue = [message.from_node]
        parent = {message.from_node: None}
        
        # BFS to find path
        while queue and message.hops_left > 0:
            current = queue.pop(0)
            
            # Check all neighbors
            for node_id in self.nodes:
                if node_id not in visited and self.can_communicate(current, node_id):
                    visited.add(node_id)
                    parent[node_id] = current
                    queue.append(node_id)
                    
                    # Found destination
                    if node_id == message.to_node:
                        # Reconstruct path
                        path = []
                        node = node_id
                        while node is not None:
                            path.append(node)
                            node = parent[node]
                        message.path = list(reversed(path))
                        message.delivered = True
                        return True
                        
            message.hops_left -= 1
            
        return False
        
    def update_display(self):
        """Update the network visualization"""
        self.ax.clear()
        
        # Draw communication ranges (light circles)
        for node in self.nodes.values():
            if node.is_online:
                circle = patches.Circle((node.x, node.y), self.max_range, 
                                      fill=False, color='lightblue', alpha=0.3, linestyle='--')
                self.ax.add_patch(circle)
        
        # Draw connections
        for node1_id in self.nodes:
            for node2_id in self.nodes:
                if node1_id < node2_id and self.can_communicate(node1_id, node2_id):
                    node1 = self.nodes[node1_id]
                    node2 = self.nodes[node2_id]
                    self.ax.plot([node1.x, node2.x], [node1.y, node2.y], 
                               'g-', alpha=0.6, linewidth=1)
        
        # Draw message paths
        for msg in self.messages:
            if msg.delivered and len(msg.path) > 1:
                path_x = [self.nodes[node_id].x for node_id in msg.path]
                path_y = [self.nodes[node_id].y for node_id in msg.path]
                self.ax.plot(path_x, path_y, 'r-', linewidth=3, alpha=0.7)
                
                # Add arrows
                for i in range(len(msg.path) - 1):
                    x1, y1 = self.nodes[msg.path[i]].x, self.nodes[msg.path[i]].y
                    x2, y2 = self.nodes[msg.path[i+1]].x, self.nodes[msg.path[i+1]].y
                    self.ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                                   arrowprops=dict(arrowstyle='->', color='red', lw=2))
        
        # Draw nodes
        for node in self.nodes.values():
            color = 'green' if node.is_online else 'red'
            # Adjust node size based on number of nodes
            size = max(100, 400 - len(self.nodes) * 3)  # Smaller nodes for larger networks
            self.ax.scatter(node.x, node.y, c=color, s=size, alpha=0.8, edgecolors='black')
            
            # Add node labels (adjust font size for larger networks)
            font_size = max(6, 10 - len(self.nodes) // 10)
            self.ax.annotate(f"{node.id + 1}\n{node.name}", 
                           (node.x, node.y), 
                           xytext=(0, -30), 
                           textcoords='offset points',
                           ha='center', va='top',
                           fontsize=font_size,
                           bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
        
        # Dynamic bounds based on node positions
        if self.nodes:
            x_coords = [node.x for node in self.nodes.values()]
            y_coords = [node.y for node in self.nodes.values()]
            x_min, x_max = min(x_coords) - 50, max(x_coords) + 50
            y_min, y_max = min(y_coords) - 50, max(y_coords) + 50
            self.ax.set_xlim(x_min, x_max)
            self.ax.set_ylim(y_min, y_max)
        else:
            self.ax.set_xlim(0, 450)
            self.ax.set_ylim(0, 400)
        self.ax.set_title("Meshtastic Network - Green connections show direct communication range")
        self.ax.grid(True, alpha=0.3)
        self.canvas.draw()
        
        # Update status
        self.update_status()
        
    def update_status(self):
        """Update network status display"""
        self.status_text.delete(1.0, tk.END)
        
        online_nodes = sum(1 for node in self.nodes.values() if node.is_online)
        total_connections = sum(1 for n1 in self.nodes for n2 in self.nodes 
                              if n1 < n2 and self.can_communicate(n1, n2))
        
        status = f"""📊 NETWORK STATUS
        
Nodes Online: {online_nodes}/{len(self.nodes)}
Direct Links: {total_connections}
Max Range: {self.max_range}m

💬 MESSAGES
Total Sent: {len(self.messages)}
Delivered: {sum(1 for m in self.messages if m.delivered)}
Failed: {sum(1 for m in self.messages if not m.delivered)}

🔋 NODE STATUS
"""
        
        for node in self.nodes.values():
            status_icon = "🟢" if node.is_online else "🔴"
            status += f"{status_icon} {node.name}\n"
            
        self.status_text.insert(1.0, status)
        
    def log_message(self, text):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {text}\n")
        self.log_text.see(tk.END)
        
    def show_statistics(self):
        """Show detailed network statistics"""
        stats = f"""
📊 MESHTASTIC NETWORK STATISTICS

🌐 Network Overview:
• Total Nodes: {len(self.nodes)}
• Online Nodes: {sum(1 for n in self.nodes.values() if n.is_online)}
• Communication Range: {self.max_range} meters
• Network Connectivity: {self.calculate_connectivity():.1f}%

💬 Message Statistics:
• Total Messages: {len(self.messages)}
• Successfully Delivered: {sum(1 for m in self.messages if m.delivered)}
• Failed Deliveries: {sum(1 for m in self.messages if not m.delivered)}
• Average Hops per Message: {self.calculate_avg_hops():.1f}

🔗 Key Meshtastic Features Demonstrated:
• Mesh networking (nodes relay messages)
• Automatic routing (finds best path)
• Range limitations (realistic RF constraints)
• Multi-hop communication (extends network reach)
• Decentralized operation (no central server)
"""
        
        messagebox.showinfo("Network Statistics", stats)
        
    def calculate_connectivity(self):
        """Calculate network connectivity percentage"""
        if len(self.nodes) < 2:
            return 0
        total_possible = len(self.nodes) * (len(self.nodes) - 1) // 2
        actual_connections = sum(1 for n1 in self.nodes for n2 in self.nodes 
                               if n1 < n2 and self.can_communicate(n1, n2))
        return (actual_connections / total_possible) * 100 if total_possible > 0 else 0
        
    def calculate_avg_hops(self):
        """Calculate average hops per delivered message"""
        delivered_msgs = [m for m in self.messages if m.delivered]
        if not delivered_msgs:
            return 0
        return sum(len(m.path) - 1 for m in delivered_msgs) / len(delivered_msgs)
        
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

def main():
    """Main entry point"""
    app = BasicMeshtasticGUI()
    app.run()

if __name__ == "__main__":
    main()
