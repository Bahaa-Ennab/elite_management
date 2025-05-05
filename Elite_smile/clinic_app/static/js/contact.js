
        // Tabs Switching Logic
        function showTab(tabId) {
            // إخفاء كل التبويبات
            document.getElementById('chat-tab').classList.add('hidden');
            document.getElementById('contact-tab').classList.add('hidden');
        
            // إزالة اللون الغامق من الأزرار
            document.getElementById('chat-tab-btn').classList.remove('bg-pink-600', 'text-white');
            document.getElementById('contact-tab-btn').classList.remove('bg-pink-600', 'text-white');
        
            // إظهار التبويب المختار
            document.getElementById(tabId).classList.remove('hidden');
        
            // تمييز الزر المفتوح بلون غامق
            if (tabId === 'chat-tab') {
                document.getElementById('chat-tab-btn').classList.add('bg-pink-600', 'text-white');
            } else {
                document.getElementById('contact-tab-btn').classList.add('bg-pink-600', 'text-white');
            }
        }

        // Chat functionality
        const chatBox = document.getElementById('chat-box');
        const userInput = document.getElementById('user-input');
        const sendBtn = document.getElementById('send-btn');

        sendBtn.addEventListener('click', () => {
            const message = userInput.value.trim();
            if (message === '') {
                alert('يرجى كتابة رسالة قبل الإرسال');
                return;
            }

            chatBox.innerHTML += `<div class="text-right"><div class="inline-block bg-blue-100 px-4 py-2 rounded-lg">${message} <span>🙂</span></div></div>`;
            userInput.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            const notification = document.createElement('div');
            notification.classList.add('text-center', 'bg-green-200', 'p-2', 'rounded-lg', 'my-2');
            notification.textContent = 'تم إرسال الرسالة بنجاح!';
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 3000);

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
                    chatBox.innerHTML += `<div class="text-left"><div class="inline-block bg-gray-100 px-4 py-2 rounded-lg">${data.response}</div></div>`;
                } else {
                    chatBox.innerHTML += `<div class="text-left"><div class="inline-block bg-red-200 px-4 py-2 rounded-lg">حدث خطأ: ${data.error}</div></div>`;
                }
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        });

        userInput.addEventListener("keypress", function (e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendBtn.click();
            }
        });

        showTab('contact-tab');
