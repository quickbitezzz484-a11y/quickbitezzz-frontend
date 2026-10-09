<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QuickBitezzz Admin</title>
    <style>
        * { box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f0f2f5;
            color: #2c3e50;
            margin: 0;
            padding: 20px;
        }
        .admin-container {
            max-width: 1200px;
            margin: 20px auto;
            background: #ffffff;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
        }
        h1 {
            color: #1a1a1a;
            font-size: 28px;
            margin-top: 0;
            margin-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
            padding-bottom: 12px;
        }
        h2 {
            color: #e65100;
            font-size: 22px;
            margin-top: 25px;
            margin-bottom: 15px;
        }
        .seat-controls {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
            background-color: #fff3e0;
            padding: 18px;
            border-radius: 8px;
            border: 1px solid #ffe0b2;
            margin-bottom: 25px;
        }
        .seat-info-badge {
            font-size: 16px;
            font-weight: bold;
            color: #d84315;
            background-color: #ffe0b2;
            padding: 8px 16px;
            border-radius: 6px;
        }
        .seat-input-group {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .seat-input-group label {
            font-size: 14px;
            font-weight: 600;
            color: #e65100;
        }
        .seat-controls input {
            padding: 8px 10px;
            width: 100px;
            border: 1px solid #cccccc;
            border-radius: 6px;
            font-size: 14px;
            color: #333333;
            outline: none;
        }
        .seat-controls button {
            padding: 8px 16px;
            background-color: #ff6f00;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
        }
        .token-controls {
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 15px;
            background-color: #e8f5e9;
            padding: 18px;
            border-radius: 8px;
            border: 1px solid #c8e6c9;
            margin-bottom: 25px;
        }
        .token-info-badge {
            font-size: 16px;
            font-weight: bold;
            color: #1b5e20;
            background-color: #c8e6c9;
            padding: 8px 16px;
            border-radius: 6px;
        }
        .token-input-group {
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }
        .token-input-group label {
            font-size: 14px;
            font-weight: 600;
            color: #2e7d32;
        }
        .token-controls input {
            padding: 8px 10px;
            width: 100px;
            border: 1px solid #cccccc;
            border-radius: 6px;
            font-size: 14px;
            color: #333333;
            outline: none;
        }
        .btn-token-set {
            padding: 8px 16px;
            background-color: #2e7d32;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
        }
        .btn-token-next {
            padding: 8px 16px;
            background-color: #1565c0;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
            cursor: pointer;
        }
        .preparing-banner {
            background-color: #e3f2fd;
            border: 2px dashed #1565c0;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .preparing-banner h3 {
            margin: 0;
            color: #0d47a1;
            font-size: 18px;
        }
        .preparing-token {
            font-size: 20px;
            font-weight: bold;
            color: #1565c0;
            background: #ffffff;
            padding: 6px 14px;
            border-radius: 6px;
            border: 1px solid #90caf9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 10px;
            background-color: #ffffff;
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
            font-size: 14px;
            color: #2c3e50;
        }
        th {
            background-color: #1a252f;
            color: #ffffff;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 13px;
        }
        tbody tr:hover { background-color: #f9f9f9; }
        .token-badge {
            font-size: 15px;
            font-weight: 700;
            color: #1565c0;
            background-color: #e3f2fd;
            padding: 4px 10px;
            border-radius: 6px;
            display: inline-block;
            border: 1px solid #bbdefb;
        }
        .btn-status {
            padding: 7px 12px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-right: 5px;
            color: #ffffff;
            font-weight: 600;
            font-size: 13px;
        }
        .btn-preparing { background-color: #ff9800; }
        .btn-ready { background-color: #2e7d32; }
        .btn-delete {
            background-color: #d32f2f;
            color: #ffffff;
            border: none;
            padding: 6px 10px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
        }
        .status-tag {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: #ffffff;
            display: inline-block;
        }
        .status-preparing { background-color: #ff9800; }
        .status-done { background-color: #2e7d32; }
        .paid-tag { 
            background-color: #e8f5e9; 
            color: #1b5e20; 
            padding: 4px 10px; 
            border-radius: 12px; 
            font-size: 12px;
            font-weight: 600;
            border: 1px solid #a5d6a7;
        }
        .no-orders {
            text-align: center;
            color: #7f8c8d;
            font-weight: bold;
            padding: 25px;
        }
    </style>
</head>
<body>

    <div class="admin-container">
        <h1>👨‍🍳 Kitchen Dashboard</h1>

        <div class="seat-controls">
            <div id="seatDisplay" class="seat-info-badge">🪑 Seats: Loading...</div>
            <div class="seat-input-group">
                <label>Available:</label>
                <input type="number" id="availSeatInput" placeholder="Avail">
                <label>Total:</label>
                <input type="number" id="totalSeatInput" placeholder="Total">
                <button onclick="updateSeats()">Update Seats</button>
            </div>
        </div>

        <div class="token-controls">
            <div id="tokenDisplay" class="token-info-badge">🎫 Now Serving Token: Loading...</div>
            <div class="token-input-group">
                <label>Set Token:</label>
                <input type="number" id="currentTokenInput" placeholder="Token #">
                <button class="btn-token-set" onclick="updateToken()">Set Token</button>
                <button class="btn-token-next" onclick="incrementToken()">Next Token (+1)</button>
            </div>
        </div>

        <div class="preparing-banner">
            <h3>🔥 Order Currently Being Prepared:</h3>
            <div id="nowPreparingToken" class="preparing-token">None</div>
        </div>

        <h2>Incoming Orders</h2>
        <table>
            <thead>
                <tr>
                    <th>Order ID</th>
                    <th>Token</th>
                    <th>Student Details</th>
                    <th>Items</th>
                    <th>Total</th>
                    <th>Payment Method</th>
                    <th>Payment</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody id="ordersTable">
                <tr><td colspan="9" class="no-orders">Loading orders...</td></tr>
            </tbody>
        </table>
    </div>

    <script>
        const API_BASE = "https://quickbitezzz-backend4.onrender.com";

        async function safeFetchJson(url, options = {}) {
            try {
                const res = await fetch(url, options);
                if (!res.ok) return null;
                const contentType = res.headers.get("content-type");
                if (contentType && contentType.includes("application/json")) {
                    return await res.json();
                }
                return null;
            } catch (err) {
                return null;
            }
        }

        async function fetchSeats() {
            const data = await safeFetchJson(`${API_BASE}/seats`);
            if (data) {
                document.getElementById("seatDisplay").innerText = `🪑 Available Seats: ${data.available_seats} / ${data.total_seats}`;
                if (!document.getElementById("availSeatInput").value) {
                    document.getElementById("availSeatInput").value = data.available_seats;
                }
                if (!document.getElementById("totalSeatInput").value) {
                    document.getElementById("totalSeatInput").value = data.total_seats;
                }
            }
        }

        async function updateSeats() {
            const availSeats = document.getElementById("availSeatInput").value;
            const totalSeats = document.getElementById("totalSeatInput").value;
            
            const res = await safeFetchJson(`${API_BASE}/seats`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ 
                    available_seats: parseInt(availSeats),
                    total_seats: parseInt(totalSeats)
                })
            });
            if (res) {
                alert("Seats updated successfully!");
                fetchSeats();
            }
        }

        async function fetchToken() {
            const data = await safeFetchJson(`${API_BASE}/current-token`);
            if (data) {
                const currentToken = data.current_token;
                document.getElementById("tokenDisplay").innerText = `🎫 Now Serving Token: #${currentToken}`;
                if (!document.getElementById("currentTokenInput").value) {
                    document.getElementById("currentTokenInput").value = currentToken;
                }
            }
        }

        async function updateToken() {
            const tokenVal = parseInt(document.getElementById("currentTokenInput").value);
            if (isNaN(tokenVal)) return alert("Please enter a valid token number");

            const res = await safeFetchJson(`${API_BASE}/admin/set-token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ token: tokenVal })
            });

            if (res) {
                alert("Token updated successfully!");
                fetchToken();
            }
        }

        async function incrementToken() {
            await safeFetchJson(`${API_BASE}/admin/next-token`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            fetchToken();
        }

        async function fetchOrders() {
            const orders = await safeFetchJson(`${API_BASE}/admin/orders`);
            const tableBody = document.getElementById("ordersTable");

            if (!orders || !Array.isArray(orders) || orders.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="9" class="no-orders">No active orders</td></tr>`;
                document.getElementById("nowPreparingToken").innerText = "None";
                return;
            }

            tableBody.innerHTML = "";
            let currentlyPreparing = null;

            orders.forEach(order => {
                let statusStr = order.status || "Preparing Your Order";
                if (statusStr === "Preparing Your Order") {
                    currentlyPreparing = order;
                }

                const row = document.createElement("tr");

                let rawItems = order.items || order.item;
                let itemsSummary = "N/A";
                if (Array.isArray(rawItems)) {
                    itemsSummary = rawItems.map(i => `${i.name} x ${i.quantity}`).join(", ");
                } else if (typeof rawItems === 'string') {
                    itemsSummary = rawItems;
                }

                let studentInfo = `${order.student_name || 'N/A'}<br><small style="color:#666;">(${order.roll_no || 'N/A'})</small>`;
                let statusClass = statusStr.toLowerCase().includes("ready") ? "status-done" : "status-preparing";

                const safeOrderId = String(order.order_id).replace(/'/g, "\\'");

                row.innerHTML = `
                    <td><strong>#${order.order_id ?? 'N/A'}</strong></td>
                    <td><span class="token-badge">Token #${order.token_number ?? 'N/A'}</span></td>
                    <td>${studentInfo}</td>
                    <td>${itemsSummary}</td>
                    <td><strong>₹${order.total_amount ?? 0}</strong></td>
                    <td>${order.payment_method || 'UPI'}</td>
                    <td><span class="paid-tag">${order.payment_status || 'Paid'}</span></td>
                    <td><span class="status-tag ${statusClass}">${statusStr}</span></td>
                    <td>
                        <button class="btn-status btn-preparing" onclick="updateOrderStatus('${safeOrderId}', 'Preparing Your Order')">Preparing</button>
                        <button class="btn-status btn-ready" onclick="updateOrderStatus('${safeOrderId}', 'Your Order is Ready')">Ready</button>
                        <button class="btn-delete" onclick="deleteOrder('${safeOrderId}')">❌</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });

            if (currentlyPreparing) {
                document.getElementById("nowPreparingToken").innerText = `Order #${currentlyPreparing.order_id} (Token #${currentlyPreparing.token_number})`;
            } else {
                document.getElementById("nowPreparingToken").innerText = "None";
            }
        }

        async function updateOrderStatus(orderId, newStatus) {
            const res = await safeFetchJson(`${API_BASE}/admin/update-status/${encodeURIComponent(orderId)}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status: newStatus })
            });

            if (res) {
                fetchOrders();
            }
        }

        async function deleteOrder(orderId) {
            if (!confirm(`Are you sure you want to clear Order #${orderId}?`)) return;

            const res = await safeFetchJson(`${API_BASE}/admin/delete-order/${encodeURIComponent(orderId)}`, {
                method: "DELETE",
                headers: { "Content-Type": "application/json" }
            });

            if (res) {
                fetchOrders();
                fetchSeats();
            } else {
                alert("Failed to delete order.");
            }
        }

        fetchSeats();
        fetchToken();
        fetchOrders();

        setInterval(fetchSeats, 3000);
        setInterval(fetchToken, 3000);
        setInterval(fetchOrders, 3000);
    </script>
</body>
</html>
