const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

sendBtn.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message === '') return;

    // عرض رسالة المستخدم
    chatBox.innerHTML += `
        <div class="text-right">
            <div class="inline-block bg-blue-100 text-right px-4 py-2 rounded-lg">
                ${message}
            </div>
        </div>`;
    userInput.value = '';
    chatBox.scrollTop = chatBox.scrollHeight;

    // إرسال إلى الخادم
    fetch('/chat/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: 'user_input=' + encodeURIComponent(message)
    })
    .then(res => res.json())
    .then(data => {
        if (data.response) {
            chatBox.innerHTML += `
                <div class="text-left">
                    <div class="inline-block bg-gray-100 text-left px-4 py-2 rounded-lg">
                        ${data.response}
                    </div>
                </div>`;
        } else {
            chatBox.innerHTML += `
                <div class="text-left">
                    <div class="inline-block bg-red-200 px-4 py-2 rounded-lg">
                        حدث خطأ: ${data.error}
                    </div>
                </div>`;
        }
        chatBox.scrollTop = chatBox.scrollHeight;
    });
});

// إرسال بالضغط على Enter
userInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendBtn.click();
    }
});
