document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('bot-form');
    const startBtn = document.getElementById('start-btn');
    const stopBtn = document.getElementById('stop-btn');
    const logsContainer = document.getElementById('logs-container');
    const statusBadge = document.getElementById('status-badge');

    let pollInterval;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const company = document.getElementById('company').value;
        const role = document.getElementById('role').value;
        const limit = document.getElementById('limit').value;

        setRunningState(true);

        try {
            const res = await fetch('/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ company, role, limit })
            });
            const data = await res.json();

            if (data.status === 'error') {
                alert(data.message);
                setRunningState(false);
            } else {
                startPolling();
            }
        } catch (err) {
            console.error(err);
            setRunningState(false);
        }
    });

    stopBtn.addEventListener('click', async () => {
        try {
            await fetch('/stop', { method: 'POST' });
            setRunningState(false);
            stopPolling();
        } catch (err) {
            console.error(err);
        }
    });

    document.getElementById('reset-btn').addEventListener('click', async () => {
        if (confirm("This will force close ALL Chrome windows. Are you sure?")) {
            try {
                await fetch('/reset', { method: 'POST' });
                setRunningState(false);
                stopPolling();
                alert("System reset complete.");
            } catch (err) {
                console.error(err);
            }
        }
    });

    function setRunningState(isRunning) {
        startBtn.disabled = isRunning;
        stopBtn.disabled = !isRunning;
        statusBadge.textContent = isRunning ? 'Running...' : 'Ready';
        statusBadge.style.color = isRunning ? '#22c55e' : '#94a3b8';
        statusBadge.style.borderColor = isRunning ? '#22c55e' : '#334155';
    }

    function startPolling() {
        pollInterval = setInterval(fetchLogs, 1000);
    }

    function stopPolling() {
        clearInterval(pollInterval);
    }

    async function fetchLogs() {
        try {
            const res = await fetch('/logs');
            const logs = await res.json();
            renderLogs(logs);
        } catch (err) {
            console.error(err);
        }
    }

    function renderLogs(logs) {
        logsContainer.innerHTML = '';
        logs.forEach(log => {
            if (log.message === "BOT_FINISHED") {
                setRunningState(false);
                stopPolling();
                return;
            }

            const div = document.createElement('div');
            div.className = `log-entry ${log.type}`;
            div.innerHTML = `
                <span class="time">${log.time}</span>
                <span class="msg">${log.message}</span>
            `;
            logsContainer.appendChild(div);
        });
        logsContainer.scrollTop = logsContainer.scrollHeight;
    }
});

function clearLogs() {
    document.getElementById('logs-container').innerHTML = '';
}
