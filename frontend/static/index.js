/**
 * 处理聊天消息
 * @param {string} url - 提交的URL
 * @param {string} messagetext - 消息内容
 * @throws {Error} - 如果网络请求失败
 */
async function message(url, messagetext) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': getCSRFToken() },
            body: JSON.stringify(messagetext),
        });
        if (!response.ok) throw new Error('网络错误');

        const result = await response.json();
        displayResult(result.message);
    } catch (error) {
        alert(`操作失败，请重试: ${error.message}`);
    }
}

/**
 * HTML转义
 * @param {string} unsafe - 需要转义的字符串
 * @returns {string} - 转义后的字符串
 */
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * 获取CSRF令牌
 * @returns {string} - CSRF令牌
 * @throws {Error} - 如果找不到CSRF令牌
 */
function getCSRFToken() {
    const cookies = document.cookie.split('; ');
    for (const cookie of cookies) {
        const [name, value] = cookie.split('=');
        if (name === 'csrfToken') {
            return value;
        }
    }
    throw new Error('CSRF 令牌未找到');
}

/**
 * 显示结果消息
 * @param {string} message - 消息文本
 */
function displayResult(message) {
    const resultElement = document.getElementById('result');
    resultElement.textContent = message;
}

/**
 * 显示错误消息
 * @param {string} message - 错误文本
 */
function displayError(message) {
    alert(message);
}

/**
 * 处理用户操作
 * @param {string} action - 操作类型
 * @param {string} prompt - 提示词
 */
async function handleAction(action, prompt) {
    try {
        const response = await callOpenAPI(prompt);
        if (prompt.includes('角色')) {
            selectedCharacter = response;
        } else {
            storyBackground = response;
        }
        displayResult(escapeHtml(response));
    } catch (error) {
        displayError(`生成内容失败，请重试: ${error.message}`);
    }
}



document.addEventListener('DOMContentLoaded', () => {
    const toggleSidebarButton = document.getElementById('hamburger-button');
    toggleSidebarButton.addEventListener('click', toggleSidebar);
});


function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('open'); // 切换 open 类
    const hamburger = document.getElementsByClassName('hamburger-button')[0];
    hamburger.classList.toggle('open'); // 切换 open 类
    const bars = document.querySelectorAll('.bar');
    bars.forEach(bar => {
        bar.classList.toggle('open'); // 切换 open 类
    });}

function handleNavigation(sectionId) {
    try {
        console.log(`导航到 ${sectionId}`);
        // 在这里添加实际的导航逻辑，例如改变页面和加载内容
    } catch (error) {
        console.error(`导航到 ${sectionId} 失败: ${error.message}`);
    }
}
async function sendMessage() {
    const input = document.getElementById('chat-input');
    const message = input.value.trim();
    if (message) {
        // 显示用户输入的消息
        displayMessage(message, 'user');

        try {
            const response = await callOpenAPI(message);
            // 显示API返回的消息
            displayMessage(response, 'bot');
        } catch (error) {
            displayError(`生成内容失败，请重试: ${error.message}`);
        }

        input.value = '';
    }
}

// 显示消息的辅助函数
function displayMessage(message, sender) {
    const messageArea = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.textContent = message;
    messageDiv.className = sender === 'user' ? 'user-message' : 'bot-message'; // 可使用不同的样式来区分用户和机器人消息
    messageArea.appendChild(messageDiv);
    messageArea.scrollTop = messageArea.scrollHeight; // 确保显示最新消息
}

const images = [
    'images/background.png',
    'images/hbm.png',
    'images/background3.png',
];

let currentIndex = 0;

function updateImage() {
    const imgElement = document.getElementById('action-image');
    imgElement.src = images[currentIndex];
}

function prevImage() {
    currentIndex = (currentIndex > 0) ? currentIndex - 1 : images.length - 1;
    updateImage();
}

function nextImage() {
    currentIndex = (currentIndex < images.length - 1) ? currentIndex + 1 : 0;
    updateImage();
}
