const SESSION_ID = "session_" + Math.random().toString(36).substr(2, 9);
let ws = null;
let isStreaming = false;

function connectWebSocket() {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    ws = new WebSocket(`${protocol}//${window.location.host}/ws/chat`);

    ws.onopen = () => {
        console.log("AgentVault connected");
        document.querySelector(".status-dot").style.background = "#22c55e";
    };

    ws.onclose = () => {
        document.querySelector(".status-dot").style.background = "#ef4444";
        setTimeout(connectWebSocket, 3000);
    };

    ws.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleStreamEvent(data);
    };
}

let currentAssistantBubble = null;
let currentContent = "";
let typingIndicator = null;

function handleStreamEvent(data) {
    const messages = document.getElementById("messages");

    if (data.type === "start") {
        typingIndicator = addTypingIndicator();
        currentAssistantBubble = null;
        currentContent = "";

    } else if (data.type === "token") {
        if (typingIndicator) {
            typingIndicator.remove();
            typingIndicator = null;
        }
        if (!currentAssistantBubble) {
            currentAssistantBubble = addAssistantMessage("");
        }
        currentContent += data.content;
        currentAssistantBubble.querySelector(".bubble").innerHTML = renderMarkdown(currentContent);
        messages.scrollTop = messages.scrollHeight;

    } else if (data.type === "end") {
        if (typingIndicator) {
            typingIndicator.remove();
            typingIndicator = null;
        }
        isStreaming = false;
        document.getElementById("send-btn").disabled = false;
        messages.scrollTop = messages.scrollHeight;

    } else if (data.type === "error") {
        if (typingIndicator) {
            typingIndicator.remove();
            typingIndicator = null;
        }
        addErrorMessage(data.content);
        isStreaming = false;
        document.getElementById("send-btn").disabled = false;
    }
}

function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message || isStreaming) return;

    addUserMessage(message);
    input.value = "";
    input.style.height = "auto";

    isStreaming = true;
    document.getElementById("send-btn").disabled = true;

    if (ws && ws.readyState === WebSocket.OPEN) {
        ws.send(JSON.stringify({ message, session_id: SESSION_ID }));
    } else {
        sendViaHTTP(message);
    }
}

async function sendViaHTTP(message) {
    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, session_id: SESSION_ID }),
        });
        const data = await response.json();
        addAssistantMessage(data.response);
    } catch (error) {
        addErrorMessage("Failed to get a response. Please try again.");
    } finally {
        isStreaming = false;
        document.getElementById("send-btn").disabled = false;
    }
}

function addUserMessage(text) {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = "message user";
    div.innerHTML = `
        <div>
            <div class="bubble">${escapeHtml(text)}</div>
            <div class="message-meta">${formatTime(new Date())}</div>
        </div>
        <div class="avatar">You</div>
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
}

function addAssistantMessage(text) {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = "message assistant";
    div.innerHTML = `
        <div class="avatar">AV</div>
        <div>
            <div class="bubble">${renderMarkdown(text)}</div>
            <div class="message-meta">AgentVault · ${formatTime(new Date())}</div>
        </div>
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
}

function addTypingIndicator() {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = "message assistant";
    div.innerHTML = `
        <div class="avatar">AV</div>
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
    return div;
}

function addErrorMessage(text) {
    const messages = document.getElementById("messages");
    const div = document.createElement("div");
    div.className = "message assistant";
    div.innerHTML = `
        <div class="avatar">AV</div>
        <div>
            <div class="bubble" style="background: #fef2f2; border-color: #fecaca; color: #dc2626;">
                ⚠️ ${escapeHtml(text)}
            </div>
        </div>
    `;
    messages.appendChild(div);
    messages.scrollTop = messages.scrollHeight;
}

async function uploadFile(input) {
    const file = input.files[0];
    if (!file) return;

    const status = document.getElementById("upload-status");
    status.style.display = "block";
    status.textContent = `Uploading ${file.name}...`;
    status.style.color = "#64748b";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch("/api/documents", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();

        if (response.ok) {
            status.textContent = `✓ ${file.name} added (${data.chunks_indexed} chunks indexed)`;
            status.style.color = "#22c55e";
            addAssistantMessage(
                `I've added **${file.name}** to the knowledge base (${data.chunks_indexed} chunks indexed). ` +
                `You can now ask me questions about its contents.`
            );
        } else {
            status.textContent = `✗ Upload failed: ${data.detail}`;
            status.style.color = "#ef4444";
        }
    } catch (error) {
        status.textContent = "✗ Upload failed — network error";
        status.style.color = "#ef4444";
    }

    input.value = "";
    setTimeout(() => { status.style.display = "none"; }, 5000);
}

function setInput(text) {
    const input = document.getElementById("user-input");
    input.value = text;
    input.focus();
    autoResize(input);
}

function handleKeyDown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

function autoResize(textarea) {
    textarea.style.height = "auto";
    textarea.style.height = Math.min(textarea.scrollHeight, 160) + "px";
}

function renderMarkdown(text) {
    return text
        .replace(/```(\w+)?\n([\s\S]*?)```/g, "<pre><code>$2</code></pre>")
        .replace(/`([^`]+)`/g, "<code>$1</code>")
        .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
        .replace(/\*([^*]+)\*/g, "<em>$1</em>")
        .replace(/\n\n/g, "<br><br>")
        .replace(/\n/g, "<br>");
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

function formatTime(date) {
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

connectWebSocket();
