// 八字计算器前端逻辑

// API配置
let API_BASE_URL = 'http://localhost:8000';

// DOM元素
const form = document.getElementById('baziForm');
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');
const resultSection = document.getElementById('resultSection');
const submitBtn = document.getElementById('submitBtn');
const apiUrlInput = document.getElementById('apiUrl');
const apiUrlDisplay = document.getElementById('apiUrlDisplay');

// 更新API地址
apiUrlInput.addEventListener('change', (e) => {
    API_BASE_URL = e.target.value.trim().replace(/\/$/, '');
    apiUrlDisplay.textContent = API_BASE_URL;
});

// 表单提交
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // 隐藏错误和结果
    hideError();
    resultSection.classList.remove('active');
    
    // 显示加载状态
    showLoading();
    
    // 获取表单数据
    const formData = {
        year: parseInt(document.getElementById('year').value),
        month: parseInt(document.getElementById('month').value),
        day: parseInt(document.getElementById('day').value),
        hour: parseInt(document.getElementById('hour').value),
        minute: parseInt(document.getElementById('minute').value),
        timezone: document.getElementById('timezone').value,
        user_id: document.getElementById('userId').value || null
    };
    
    try {
        // 调用API
        const response = await fetch(`${API_BASE_URL}/api/v1/bazi/calculate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || '计算失败');
        }
        
        const data = await response.json();
        
        // 显示结果
        displayResult(data);
        
    } catch (error) {
        showError(`错误：${error.message}\n\n请确保：\n1. 后端服务已启动\n2. API地址正确\n3. 网络连接正常`);
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
});

// 显示结果
function displayResult(data) {
    // 显示四柱
    document.getElementById('yearPillar').textContent = data.year_pillar;
    document.getElementById('monthPillar').textContent = data.month_pillar;
    document.getElementById('dayPillar').textContent = data.day_pillar;
    document.getElementById('hourPillar').textContent = data.hour_pillar;
    
    // 显示天干地支详情
    document.getElementById('yearDetail').textContent = 
        `${data.sizhu.year.tian} ${data.sizhu.year.di}`;
    document.getElementById('monthDetail').textContent = 
        `${data.sizhu.month.tian} ${data.sizhu.month.di}`;
    document.getElementById('dayDetail').textContent = 
        `${data.sizhu.day.tian} ${data.sizhu.day.di}`;
    document.getElementById('hourDetail').textContent = 
        `${data.sizhu.hour.tian} ${data.sizhu.hour.di}`;
    
    // 显示日主
    document.getElementById('rigan').textContent = data.rigan;
    document.getElementById('riganWuxing').textContent = `五行属${data.rigan_wuxing}`;
    
    // 显示五行分析
    const wuxing = data.wuxing_analysis.count;
    document.getElementById('wuxingWood').textContent = wuxing['木'] || 0;
    document.getElementById('wuxingFire').textContent = wuxing['火'] || 0;
    document.getElementById('wuxingEarth').textContent = wuxing['土'] || 0;
    document.getElementById('wuxingMetal').textContent = wuxing['金'] || 0;
    document.getElementById('wuxingWater').textContent = wuxing['水'] || 0;
    
    // 显示命理解读
    const interpretation = data.interpretation;
    document.getElementById('basicInterpretation').textContent = 
        interpretation.basic + ' ' + interpretation.wuxing_distribution + ' ' + interpretation.wuxing_balance;
    document.getElementById('personality').textContent = interpretation.personality;
    document.getElementById('xiyongshen').textContent = interpretation.xiyongshen;
    document.getElementById('advice').textContent = interpretation.advice;
    
    // 显示结果区域
    resultSection.classList.add('active');
    
    // 滚动到结果区域
    resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    
    // 记录ID
    if (data.id) {
        console.log('记录ID:', data.id);
    }
}

// 显示加载状态
function showLoading() {
    loading.classList.add('active');
    submitBtn.disabled = true;
}

// 隐藏加载状态
function hideLoading() {
    loading.classList.remove('active');
    submitBtn.disabled = false;
}

// 显示错误
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.add('active');
}

// 隐藏错误
function hideError() {
    errorDiv.classList.remove('active');
}

// 页面加载完成后检测API连接
window.addEventListener('load', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: 'GET',
        });
        
        if (response.ok) {
            console.log('✅ API连接正常');
        } else {
            console.warn('⚠️ API连接异常');
        }
    } catch (error) {
        console.warn('⚠️ 无法连接到API服务器，请确保后端服务已启动');
    }
});

// 使用示例：快速填充测试数据
function fillTestData() {
    const now = new Date();
    document.getElementById('year').value = 1990;
    document.getElementById('month').value = 5;
    document.getElementById('day').value = 15;
    document.getElementById('hour').value = 14;
    document.getElementById('minute').value = 30;
    document.getElementById('timezone').value = 'Asia/Shanghai';
    document.getElementById('userId').value = 'test_user_001';
}

// 键盘快捷键：Ctrl+T 填充测试数据
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 't') {
        e.preventDefault();
        fillTestData();
        console.log('已填充测试数据');
    }
});

console.log('八字计算器已加载');
console.log('提示：按 Ctrl+T 可快速填充测试数据');

