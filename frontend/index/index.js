
// 封装通用API调用函数
export async function callAPI(url, method = 'GET', params = {}, headers = { 'Content-Type': 'application/json' }) {
    try {
        const requestOptions = {
            method,
            headers: {
                ...headers,
                'X-CSRF-Token': getCSRFToken(),
            },
        };

        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(method)) {
            requestOptions.body = JSON.stringify(params);
        }

        const response = await fetch(url, requestOptions);
        if (!response.ok) throw new Error('网络请求失败');
        return await response.json();
    } catch (error) {
        console.error(`API调用失败: ${url}`, error);
        throw error;
    }
}

// 通用错误处理函数
export function handleError(error, options = {}) {
    const { useAlert = false, containerId = 'error-container', customMessage } = options;
    const message = customMessage || error.message || '操作失败，请重试';

    if (useAlert) {
        alert(message);
    } else {
        const errorContainer = document.getElementById(containerId);
        if (errorContainer) {
            errorContainer.innerText = message;
        } else {
            console.error(message, error);
        }
    }
}

// 处理表单数据提交的工具函数
export async function submitFormData(url, formData, method = 'POST', headers = {}) {
    try {
        const response = await fetch(url, {
            method,
            headers: {
                ...headers,
                'X-CSRF-Token': getCSRFToken(),
            },
            body: formData,
        });
        if (!response.ok) throw new Error('表单提交失败');
        return await response.json();
    } catch (error) {
        console.error(`表单提交失败: ${url}`, error);
        throw error;
    }
}

// 通用消息显示函数
export function displayMessage(message, options = {}) {
    const { containerId = 'message-container', isError = false, sender = 'system' } = options;
    const container = document.getElementById(containerId);

    if (container) {
        const messageElement = document.createElement('p');
        messageElement.innerText = message;
        messageElement.className = `message ${sender} ${isError ? 'error' : ''}`;
        container.appendChild(messageElement);
    } else {
        console.log(message);
    }
}

// HTML转义工具函数
export function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// 处理文件上传的工具函数
export async function uploadFile(url, file, method = 'POST', headers = {}) {
    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(url, {
            method,
            headers: {
                ...headers,
                'X-CSRF-Token': getCSRFToken(),
            },
            body: formData,
        });
        if (!response.ok) throw new Error('文件上传失败');
        return await response.json();
    } catch (error) {
        console.error(`文件上传失败: ${url}`, error);
        throw error;
    }
}

// 获取CSRF令牌工具函数
export function getCSRFToken() {
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
 * 处理聊天消息
 * @param {string} url - 提交的URL
 * @param {string} messagetext - 消息内容
 * @throws {Error} - 如果网络请求失败
 */
async function message(url, messagetext) {
    try {
        const result = await callAPI(url, 'POST', messagetext, { 'Content-Type': 'application/json', 'X-CSRF-Token': getCSRFToken() });
        displayMessage(result.message, { containerId: 'result' });
    } catch (error) {
        handleError(error, { useAlert: true });
    }
}
// 检查用户登录状态的函数
function checkLoginStatus() {
    // 示例逻辑，实际项目应从服务器或本地存储中获取登录状态
    return Boolean(localStorage.getItem('isLoggedIn'));
}

/**
 * 处理侧边栏的显示和隐藏逻辑。
 */
export function initSidebar() {
    document.addEventListener('DOMContentLoaded', () => {
        const toggleSidebarButton = document.getElementById('hamburger-button');
        if (toggleSidebarButton) {
            toggleSidebarButton.addEventListener('click', toggleSidebar);
        }
    });
}

/**
 * 切换侧边栏的显示状态。
 */
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    } else {
        console.error('Sidebar element not found');
    }
}

// 定义 loadPage 函数
window.loadPage = async function(page) {
    try {
        // 调用后端接口获取静态文件内容
        const response = await fetch(`/static/${page}.html`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const content = await response.text();

        // 获取 main 元素并更新其内容
        const main = document.querySelector('main');
        if (main) {
            main.innerHTML = content;
        } else {
            console.error('Main element not found');
        }
    } catch (error) {
        console.error(`加载页面 ${page} 失败:`, error);
    }
};

// 添加事件监听器
document.addEventListener('DOMContentLoaded', () => {
    // 导航链接
    document.querySelectorAll('a[data-page]').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            loadPage(link.dataset.page);
        });
    });

    // 按钮
    document.querySelectorAll('button[data-page]').forEach(button => {
        button.addEventListener('click', () => {
            loadPage(button.dataset.page);
        });
    });

    // 侧边栏切换按钮
    const toggleSidebarButton = document.getElementById('hamburger-button');
    if (toggleSidebarButton) {
        toggleSidebarButton.addEventListener('click', toggleSidebar);
    }

    // 发送消息按钮
    const sendMessageButton = document.querySelector('.chatbox-button');
    if (sendMessageButton) {
        sendMessageButton.addEventListener('click', sendMessage);
    }
});

// 实现 sendMessage 函数以集成 Ollama API
window.sendMessage = async function() {
    const input = document.getElementById('chat-input').value.trim();
    if (!input) {
        alert('请输入消息');
        return;
    }

    try {
        // 显示用户消息
        const chatMessages = document.getElementById('chat-messages');
        const userMessage = document.createElement('p');
        userMessage.innerText = `用户: ${input}`;
        chatMessages.appendChild(userMessage);

        // 调用后端 API 获取 AI 响应
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: input }),
        });

        if (!response.ok) {
            throw new Error('AI 响应失败');
        }

        const result = await response.json();
        const aiMessage = document.createElement('p');
        aiMessage.innerText = `AI: ${result.message}`;
        chatMessages.appendChild(aiMessage);
    } catch (error) {
        console.error('发送消息失败:', error);
        alert('发送消息失败，请重试');
    }
};
