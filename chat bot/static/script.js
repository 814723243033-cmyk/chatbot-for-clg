document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('chat-messages');
    const clearBtn = document.getElementById('clear-btn');
    const exportBtn = document.getElementById('export-btn');
    const micBtn = document.getElementById('mic-btn');

    let chatHistory = [];

    // Auto-resize textarea
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight < 150 ? this.scrollHeight : 150) + 'px';
    });

    function resetInput() {
        userInput.value = '';
        userInput.style.height = 'auto';
        userInput.focus();
    }

    function addMessage(content, sender, isHtml = false) {
        // Track history
        chatHistory.push({ role: sender, content: content, timestamp: new Date() });

        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', sender);

        let avatarHtml = sender === 'bot'
            ? '<div class="avatar-small"><i class="fas fa-robot"></i></div>'
            : '<div class="avatar-small"><i class="fas fa-user"></i></div>';

        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message-content');

        if (isHtml) {
            contentDiv.innerHTML = content;
        } else {
            contentDiv.textContent = content;
        }

        messageDiv.innerHTML = avatarHtml;
        messageDiv.appendChild(contentDiv);

        messagesContainer.appendChild(messageDiv);
        scrollToBottom();

        // Highlight code blocks and add Copy button
        if (isHtml && window.hljs) {
            messageDiv.querySelectorAll('pre').forEach((pre) => {
                // Syntax Highlight
                pre.querySelectorAll('code').forEach((block) => hljs.highlightElement(block));

                // Add Copy Button
                const copyBtn = document.createElement('button');
                copyBtn.classList.add('copy-btn');
                copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy';
                copyBtn.addEventListener('click', () => {
                    const code = pre.querySelector('code').innerText;
                    navigator.clipboard.writeText(code).then(() => {
                        copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';
                        setTimeout(() => copyBtn.innerHTML = '<i class="fas fa-copy"></i> Copy', 2000);
                    }).catch(err => console.error('Copy failed:', err));
                });

                pre.insertBefore(copyBtn, pre.firstChild);
            });
        }
    }

    function showTypingIndicator() {
        const indicatorDiv = document.createElement('div');
        indicatorDiv.classList.add('message', 'bot', 'typing');
        indicatorDiv.innerHTML = `
            <div class="avatar-small"><i class="fas fa-robot"></i></div>
            <div class="message-content">
                <div class="typing-dots">
                    <div class="dot"></div>
                    <div class="dot"></div>
                    <div class="dot"></div>
                </div>
            </div>
        `;
        messagesContainer.appendChild(indicatorDiv);
        scrollToBottom();
        return indicatorDiv;
    }

    function scrollToBottom() {
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function handleSendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        addMessage(text, 'user');
        resetInput();

        const typingIndicator = showTypingIndicator();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: text })
            });

            const data = await response.json();
            typingIndicator.remove();

            const rawAnswer = data.answer || "Sorry, I couldn't get a response.";

            let htmlAnswer;
            if (window.marked) {
                htmlAnswer = marked.parse(rawAnswer);
                addMessage(htmlAnswer, 'bot', true);
            } else {
                addMessage(rawAnswer, 'bot', false);
            }

        } catch (error) {
            typingIndicator.remove();
            addMessage("Error communicating with server.", 'bot');
            console.error('Error:', error);
        }
    }

    // --- Voice Input Logic ---
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.lang = 'en-US';

        micBtn.addEventListener('click', () => {
            if (micBtn.classList.contains('recording')) {
                recognition.stop();
            } else {
                recognition.start();
            }
        });

        recognition.onstart = () => {
            micBtn.classList.add('recording');
        };

        recognition.onend = () => {
            micBtn.classList.remove('recording');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            userInput.value += transcript + ' ';
            // Trigger auto-resize
            userInput.dispatchEvent(new Event('input'));
            userInput.focus();
        };
    } else {
        micBtn.style.display = 'none'; // Hide if not supported
    }

    // --- Export Logic ---
    exportBtn.addEventListener('click', () => {
        if (chatHistory.length === 0) {
            alert("No chat history to export!");
            return;
        }
        let exportText = "Chat History - AI Tutor\n=======================\n\n";
        chatHistory.forEach(msg => {
            const time = msg.timestamp.toLocaleTimeString();
            exportText += `[${time}] ${msg.role.toUpperCase()}:\n${msg.content}\n\n`;
        });

        const blob = new Blob([exportText], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `chat_history_${Date.now()}.txt`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    // Event Listeners
    sendBtn.addEventListener('click', handleSendMessage);

    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    clearBtn.addEventListener('click', () => {
        messagesContainer.innerHTML = '';
        chatHistory = [];
        addMessage('Chat cleared. How can I help you now?', 'bot');
    });
});
