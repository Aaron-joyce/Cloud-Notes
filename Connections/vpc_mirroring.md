## 🛡️ AWS Traffic Mirroring Challenge Guide
**Objective:** Capture a malicious beacon message sent from a compromised host (**JamInstanceA**) to a target (**JamInstanceB**) using a monitoring station (**JamMonitorStation**).

---

### 1. Key Concepts & Definitions
Before starting, it helps to understand the "language" of the challenge:

* **Traffic Mirroring:** A feature that copies network traffic from a source (like a compromised server) and sends it to a security appliance or monitor without interrupting the original flow.
* **ENI (Elastic Network Interface):** The "virtual NIC" attached to your EC2 instance. Mirroring happens at the interface level, not the instance level.
* **VXLAN (Virtual Extensible LAN):** A "tunneling" protocol. AWS wraps the mirrored traffic in a VXLAN "envelope" (using **UDP Port 4789**) to transport it across the VPC to your monitor.
* **VNI (VXLAN Network Identifier):** A unique ID (like `100`) used to identify the specific traffic tunnel.
* **`tcpdump`:** A command-line tool used to "sniff" or analyze network packets in real-time.

---

### 2. Implementation Steps

#### **Step 1: Gather your Interface IDs**
1.  Go to the **EC2 Dashboard**.
2.  Select **JamMonitorStation** -> **Networking** tab -> Copy the **Network Interface ID** (e.g., `eni-123...`).
3.  Select **JamInstanceA** -> **Networking** tab -> Copy the **Network Interface ID** (e.g., `eni-456...`).

#### **Step 2: Set up the Infrastructure (VPC Dashboard)**
1.  **Create Mirror Target:**
    * Navigate to **VPC** > **Mirror Targets** > **Create**.
    * Target type: **Network Interface**.
    * Target: Paste the **JamMonitorStation** ENI ID.
    * Name: `mirror-target`.
2.  **Create Mirror Filter:**
    * Navigate to **VPC** > **Mirror Filters** > **Create**.
    * Name: `mirror-filter`.
    * **Inbound Rules:** Action: `accept`, Protocol: `All`, Source/Dest CIDR: `10.0.0.0/8`.
    * **Outbound Rules:** Action: `accept`, Protocol: `All`, Source/Dest CIDR: `10.0.0.0/8`.
    *(Note: `10.0.0.0/8` ensures we catch all internal VPC traffic.)*
3.  **Create Mirror Session:**
    * Navigate to **VPC** > **Mirror Sessions** > **Create**.
    * **Mirror Source:** JamInstanceA ENI ID.
    * **Mirror Target:** `mirror-target`.
    * **Session Number:** `1`.
    * **VNI:** `100`.
    * **Filter:** `mirror-filter`.

#### **Step 3: Open the Firewall (Security Groups)**
1.  Find the **Security Group** attached to **JamMonitorStation**.
2.  Add an **Inbound Rule**:
    * **Type:** Custom UDP.
    * **Port Range:** `4789`.
    * **Source:** `0.0.0.0/0` (or the VPC CIDR).
    * *Why?* Without this, the OS will block the VXLAN packets before you can read them.

---

### 3. Capturing the Flag
Now, log in to the **JamMonitorStation** via **Systems Manager (SSM) Session Manager**.

#### **Option A: The Shortcut (Raw Capture)**
This looks at the raw, encapsulated packets. You will see the hex data and the flag on the right.
```bash
sudo tcpdump -lnvX icmp
```

#### **Option B: The "Proper" Way (Decapsulation)**
This creates a virtual interface that "unwraps" the VXLAN envelope so you can see the clean traffic.
1.  **Create the virtual interface:**
    ```bash
    sudo ip link add vxlan0 type vxlan id 100 dev eth0 local 10.0.1.11 dstport 4789
    ```
2.  **Turn the interface on:**
    ```bash
    sudo ip link set vxlan0 up
    ```
3.  **Sniff the clean traffic:**
    ```bash
    sudo tcpdump -lnvXi vxlan0 icmp
    ```

---

### 🏁 Final Flag
Look for the ASCII text in the packet payload. Based on your capture, the flag is:
> **`j4mc0mPl3t3d`**

---

Did you manage to get the `vxlan0` interface up and running, or did you stick with the shortcut?
