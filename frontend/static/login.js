/**
 * 处理登录请求
 * @param {string} url - 提交的URL
 * @param {Object} formData - 表单数据
 * @throws {Error} - 如果网络请求失败
 */
function getCSRFToken() {
    // 这里可以扩展为从cookie或meta标签中获取CSRF Token
    return "sample_csrf_token";  // 示例，实际应用中应动态获取
}

async function handleLogin(url, formData) {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', 'X-CSRF-Token': getCSRFToken() },
            body: JSON.stringify(formData),
        });
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || '网络错误');
        }

        const result = await response.json();
        displayResult(result.message);
        if (result.redirect_url) {
            window.location.href = result.redirect_url;
        }
    } catch (error) {
        displayResult(`操作失败: ${error.message}`, true);
    }
}

/**
 * 用户登录
 */
function login() {
    const formData = getFormData('login');
    handleLogin('/login', formData);
}

function displayResult(message, isError = false) {
    const resultDiv = document.getElementById('result');
    resultDiv.textContent = message;
    resultDiv.style.color = isError ? 'red' : 'green';
}