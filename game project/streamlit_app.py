import streamlit as st
import base64
import time

st.set_page_config(
    page_title="赵思城 | 个人作品集",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except Exception as e:
        st.warning(f"图片加载失败: {e}")
        return ""

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def main():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Noto+Sans+SC:wght@300;400;500;600;700&display=swap');

    :root {
        --gold: #FFD700;
        --accent-color: #C9A962;
        --bg-dark: #1A1A2E;
        --text-primary: #F5F5DC;
        --text-secondary: #C0C0C0;
    }

    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: 'Noto Serif SC', 'Noto Sans SC', serif, sans-serif;
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
        color: #F5F5DC;
    }

    .loader {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, #050510 0%, #0a0a2e 30%, #0d1b2a 60%, #1b263b 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        z-index: 99999;
        overflow: hidden;
    }

    .loader-bg-grid {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(255, 215, 0, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 215, 0, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: gridMove 20s linear infinite;
    }

    @keyframes gridMove {
        0% { transform: translate(0, 0); }
        100% { transform: translate(50px, 50px); }
    }

    .loader-content {
        position: relative;
        z-index: 10;
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    .loader-geometry {
        position: relative;
        width: 200px;
        height: 200px;
        margin-bottom: 30px;
    }

    .loader-triangle {
        position: absolute;
        width: 0;
        height: 0;
        border-left: 60px solid transparent;
        border-right: 60px solid transparent;
        border-bottom: 104px solid rgba(255, 215, 0, 0.3);
        animation: triangleAnim 3s ease-in-out infinite;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(0deg);
    }

    .loader-triangle:nth-child(2) {
        transform: translate(-50%, -50%) rotate(120deg);
        animation-delay: 1s;
    }

    .loader-triangle:nth-child(3) {
        transform: translate(-50%, -50%) rotate(240deg);
        animation-delay: 2s;
    }

    @keyframes triangleAnim {
        0%, 100% { opacity: 0.3; transform: translate(-50%, -50%) scale(1); }
        50% { opacity: 0.8; transform: translate(-50%, -50%) scale(1.1); }
    }

    .loader-polygon {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 120px;
        height: 120px;
    }

    .loader-polygon svg {
        width: 100%;
        height: 100%;
        animation: polygonRotate 8s linear infinite;
    }

    @keyframes polygonRotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    .loader-ring {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 180px;
        height: 180px;
        border: 2px solid rgba(255, 215, 0, 0.2);
        border-radius: 50%;
        animation: ringPulse 3s ease-in-out infinite;
    }

    .loader-ring::before {
        content: '';
        position: absolute;
        top: -2px;
        left: 50%;
        transform: translateX(-50%);
        width: 10px;
        height: 10px;
        background: #FFD700;
        border-radius: 50%;
        box-shadow: 0 0 20px #FFD700, 0 0 40px #FFD700;
    }

    @keyframes ringPulse {
        0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
        50% { transform: translate(-50%, -50%) scale(1.05); opacity: 0.8; }
    }

    .loader-percentage {
        font-family: 'Courier New', monospace;
        font-size: 3rem;
        font-weight: bold;
        color: #FFD700;
        text-shadow: 0 0 30px rgba(255, 215, 0, 0.5);
        margin-bottom: 10px;
    }

    .loader-label {
        font-size: 1rem;
        color: rgba(255, 215, 0, 0.7);
        letter-spacing: 0.3em;
        text-transform: uppercase;
    }

    .loader-line {
        width: 200px;
        height: 2px;
        background: rgba(255, 215, 0, 0.2);
        margin-top: 20px;
        overflow: hidden;
        border-radius: 1px;
    }

    .loader-line-progress {
        height: 100%;
        background: linear-gradient(90deg, #FFD700, #FFA500);
        border-radius: 1px;
        transition: width 0.1s linear;
        box-shadow: 0 0 10px #FFD700;
    }

    .hero-section {
        text-align: center;
        padding: 6rem 2rem;
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }

    .avatar {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        border: 4px solid #FFD700;
        box-shadow: 0 0 30px rgba(255, 215, 0, 0.4);
        margin-bottom: 2rem;
        transition: transform 0.3s ease;
    }

    .avatar:hover {
        transform: scale(1.05);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #FFD700, #D4A574);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        color: #C0C0C0;
        margin-bottom: 2rem;
    }

    .tags-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1rem;
    }

    .tag {
        padding: 0.5rem 1.5rem;
        background: rgba(201, 169, 98, 0.1);
        border: 1px solid #C9A962;
        border-radius: 25px;
        font-size: 0.9rem;
        color: #C9A962;
        transition: all 0.3s ease;
    }

    .tag:hover {
        background: rgba(201, 169, 98, 0.2);
        transform: translateY(-3px);
    }

    .section {
        padding: 4rem 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }

    .section-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #FFD700;
        margin-bottom: 3rem;
        position: relative;
    }

    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 80px;
        height: 3px;
        background: linear-gradient(90deg, transparent, #FFD700, transparent);
    }

    .skills-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
    }

    .skill-card {
        background: rgba(45, 45, 68, 0.6);
        border: 1px solid rgba(201, 169, 98, 0.2);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }

    .skill-card:hover {
        transform: translateY(-8px);
        border-color: #C9A962;
    }

    .skill-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }

    .games-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 2.5rem;
    }

    .game-card {
        background: linear-gradient(145deg, rgba(45, 45, 68, 0.8), rgba(26, 26, 46, 0.9));
        border: 1px solid rgba(201, 169, 98, 0.3);
        border-radius: 20px;
        overflow: hidden;
        transition: all 0.4s ease;
    }

    .game-card:hover {
        transform: translateY(-10px);
        border-color: #FFD700;
    }

    .game-cover {
        height: 250px;
        overflow: hidden;
    }

    .game-cover img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .game-info {
        padding: 1.5rem;
    }

    .game-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #FFD700;
        margin-bottom: 0.5rem;
    }

    .game-type {
        font-size: 0.9rem;
        color: #C9A962;
        margin-bottom: 1rem;
    }

    .game-desc {
        color: #C0C0C0;
        line-height: 1.6;
        margin-bottom: 1rem;
    }

    .game-highlights {
        list-style: none;
        padding-left: 0;
        margin-bottom: 1rem;
    }

    .game-highlights li {
        padding: 0.5rem 0;
        color: #C0C0C0;
        font-size: 0.9rem;
        padding-left: 1.5rem;
        position: relative;
    }

    .game-highlights li::before {
        content: '✦';
        position: absolute;
        left: 0;
        color: #FFD700;
    }

    .btn {
        display: inline-block;
        padding: 0.75rem 2rem;
        background: linear-gradient(135deg, #FFD700, #C9A962);
        color: #1A1A2E;
        text-decoration: none;
        border-radius: 25px;
        font-weight: 600;
        transition: all 0.3s ease;
    }

    .btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(255, 215, 0, 0.4);
    }

    .btn-outline {
        background: transparent;
        border: 1px solid #FFD700;
        color: #FFD700;
    }

    .literature-list {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }

    .literature-item {
        background: rgba(45, 45, 68, 0.6);
        border: 1px solid rgba(201, 169, 98, 0.2);
        border-radius: 15px;
        padding: 2rem;
        transition: all 0.3s ease;
    }

    .literature-item:hover {
        border-color: #C9A962;
        transform: translateX(10px);
    }

    .literature-item h3 {
        font-size: 1.3rem;
        color: #FFD700;
        margin-bottom: 0.5rem;
    }

    .literature-tags {
        display: flex;
        gap: 0.75rem;
        margin-bottom: 1rem;
    }

    .literature-tag {
        padding: 0.25rem 0.75rem;
        background: rgba(201, 169, 98, 0.1);
        border-radius: 10px;
        font-size: 0.8rem;
        color: #C9A962;
    }

    .literature-item p {
        color: #C0C0C0;
        line-height: 1.6;
    }

    .competition-card {
        background: linear-gradient(145deg, rgba(45, 45, 68, 0.8), rgba(26, 26, 46, 0.9));
        border: 1px solid rgba(201, 169, 98, 0.3);
        border-radius: 20px;
        padding: 3rem;
        text-align: center;
    }

    .competition-card h3 {
        font-size: 1.8rem;
        color: #FFD700;
        margin-bottom: 1rem;
    }

    .competition-info {
        color: #C9A962;
        margin-bottom: 2rem;
    }

    .competition-role {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        background: rgba(201, 169, 98, 0.1);
        border-radius: 20px;
        margin-bottom: 2rem;
        color: #F5F5DC;
    }

    .competition-desc {
        color: #C0C0C0;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    .social-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 2rem;
    }

    .social-stats-card {
        background: rgba(45, 45, 68, 0.6);
        border: 1px solid rgba(201, 169, 98, 0.2);
        border-radius: 15px;
        overflow: hidden;
    }

    .social-stats-card img {
        width: 100%;
        height: 200px;
        object-fit: cover;
    }

    .social-stats-info {
        padding: 1.5rem;
    }

    .social-stats-info h4 {
        color: #FFD700;
        margin-bottom: 0.5rem;
    }

    .social-stats-info p {
        color: #C0C0C0;
        font-size: 0.9rem;
    }

    .social-card {
        background: rgba(45, 45, 68, 0.6);
        border: 1px solid rgba(201, 169, 98, 0.2);
        border-radius: 15px;
        padding: 2rem;
        text-align: center;
    }

    .social-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }

    .social-card h3 {
        color: #F5F5DC;
        margin-bottom: 0.5rem;
    }

    .social-stats {
        color: #C9A962;
        font-size: 0.9rem;
    }

    .contact-section {
        background: linear-gradient(180deg, transparent 0%, rgba(201, 169, 98, 0.05) 100%);
        padding: 4rem 2rem;
    }

    .contact-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 2rem;
        text-align: center;
    }

    .contact-item {
        padding: 1.5rem;
    }

    .contact-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }

    .contact-item h3 {
        color: #F5F5DC;
        margin-bottom: 0.5rem;
    }

    .contact-item p, .contact-item a {
        color: #C0C0C0;
        text-decoration: none;
    }

    .contact-item a:hover {
        color: #FFD700;
    }

    .footer {
        background: rgba(26, 26, 46, 0.95);
        padding: 2rem;
        text-align: center;
        border-top: 1px solid rgba(201, 169, 98, 0.2);
    }

    .footer p {
        color: #C0C0C0;
        font-size: 0.9rem;
    }

    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .section {
            padding: 2rem 1rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero-section">
        <img src="data:image/png;base64,{}" alt="赵思城" class="avatar">
        <h1 class="hero-title">趙思城</h1>
        <p class="hero-subtitle">游戏策划 / 剧情文案 / 独立游戏开发 / 新媒体内容创作</p>
        <div class="tags-container">
            <span class="tag">独立游戏</span>
            <span class="tag">叙事设计</span>
            <span class="tag">Web开发</span>
            <span class="tag">内容创作</span>
            <span class="tag">团队管理</span>
        </div>
    </div>
    """.format(get_base64_image('images/头像.png')), unsafe_allow_html=True)

    st.markdown("""
    <div class="section" id="skills">
        <h2 class="section-title">核心能力</h2>
        <div class="skills-grid">
            <div class="skill-card">
                <div class="skill-icon">🎮</div>
                <h3>游戏全案开发</h3>
                <p>独立完成游戏全案开发：世界观、剧情、角色、脚本、交互设计</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">✍️</div>
                <h3>叙事文案</h3>
                <p>精通叙事文案：小说、游戏剧情、宣发文案、项目报告</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">💻</div>
                <h3>前端开发</h3>
                <p>掌握前端基础：HTML/CSS/JS，可独立部署网页游戏与官网</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">📺</div>
                <h3>新媒体运营</h3>
                <p>B站内容创作、爆款打造、流量运营</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">👥</div>
                <h3>项目统筹</h3>
                <p>竞赛项目负责人、团队协作、全案输出</p>
            </div>
            <div class="skill-card">
                <div class="skill-icon">🎨</div>
                <h3>美术设计</h3>
                <p>原创角色设计、场景概念、UI设计</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section" id="games">
        <h2 class="section-title">独立游戏作品</h2>
        <div class="games-grid">
            <div class="game-card">
                <div class="game-cover">
                    <img src="data:image/png;base64,{}" alt="断联404封面">
                </div>
                <div class="game-info">
                    <h3 class="game-title">断联 404</h3>
                    <p class="game-type">科幻悬疑 / 叙事冒险 / 网页可玩</p>
                    <p class="game-desc">一场跨越现实与虚拟的旅程，探索AI意识与人类情感的边界</p>
                    <ul class="game-highlights">
                        <li>双世界观：现实「新港市」× 虚拟「深度网域」</li>
                        <li>强情感叙事：AI意识、人机羁绊、牺牲与重生</li>
                        <li>完整四幕剧情：相遇 — 解谜 — 牺牲 — 重生</li>
                        <li>可直接在个人官网运行体验</li>
                    </ul>
                    <a href="https://404workroom-1420076748.cos-website.ap-nanjing.myqcloud.com/index.html" class="btn" target="_blank">立即体验</a>
                </div>
            </div>
            <div class="game-card">
                <div class="game-cover">
                    <img src="data:image/png;base64,{}" alt="游戏AI Agent">
                </div>
                <div class="game-info">
                    <h3 class="game-title">游戏AI Agent</h3>
                    <p class="game-type">AI工具 / 游戏设计 / 智能顾问</p>
                    <p class="game-desc">专业的游戏AI设计顾问，提供剧情生成、代码辅助和性能预估服务</p>
                    <ul class="game-highlights">
                        <li>智能对话系统，专业游戏设计咨询</li>
                        <li>代码生成功能，快速原型开发</li>
                        <li>性能预估模块，优化游戏性能</li>
                        <li>支持知识库加载，个性化定制</li>
                    </ul>
                    <a href="#" class="btn btn-outline">了解更多</a>
                </div>
            </div>
            <div class="game-card">
                <div class="game-cover">
                    <img src="data:image/png;base64,{}" alt="游戏AI Agent Pro">
                </div>
                <div class="game-info">
                    <h3 class="game-title">游戏AI Agent Pro</h3>
                    <p class="game-type">高级AI工具 / 进阶功能</p>
                    <p class="game-desc">增强版AI助手，提供更强大的游戏设计辅助功能</p>
                    <ul class="game-highlights">
                        <li>高级剧本生成引擎</li>
                        <li>智能关卡设计工具</li>
                        <li>角色关系图谱分析</li>
                        <li>实时协作编辑功能</li>
                    </ul>
                    <a href="#" class="btn btn-outline">了解更多</a>
                </div>
            </div>
        </div>
    </div>
    """.format(get_base64_image('images/cover.png'), get_base64_image('images/aiagent1.png'), get_base64_image('images/aiagent2.png')), unsafe_allow_html=True)

    st.markdown("""
    <div class="section" id="literature">
        <h2 class="section-title">文学 / 文案创作</h2>
        <div class="literature-list">
            <div class="literature-item">
                <h3>长篇小说《青川一纸：解开父亲的执念密码》</h3>
                <div class="literature-tags">
                    <span class="literature-tag">悬疑亲情</span>
                    <span class="literature-tag">科学反迷信</span>
                    <span class="literature-tag">民俗探案</span>
                </div>
                <p>完整四章，结构严谨，适合影视/游戏改编</p>
            </div>
            <div class="literature-item">
                <h3>现实小说《月映崇山》</h3>
                <div class="literature-tags">
                    <span class="literature-tag">反拐卖</span>
                    <span class="literature-tag">反迷信</span>
                    <span class="literature-tag">基层民警</span>
                </div>
                <p>强情绪、强画面，可做互动叙事剧本</p>
                <a href="https://www.kdocs.cn/l/cmkn2R7l6X6s" target="_blank" class="btn btn-outline">阅读全文</a>
            </div>
            <div class="literature-item">
                <h3>诗歌《白凤游九州》</h3>
                <div class="literature-tags">
                    <span class="literature-tag">家国情怀</span>
                    <span class="literature-tag">意象优美</span>
                </div>
                <p>家国情怀，意象优美，可用于游戏世界观/主题曲文案</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section" id="competition">
        <h2 class="section-title">竞赛项目成果</h2>
        <div class="competition-card">
            <h3>「诚」心「成」易 —— 电商平台真伪鉴别</h3>
            <p class="competition-info">全国大学生电子商务 "三创" 挑战赛</p>
            <div class="competition-role">队长、策划、主文案</div>
            <p class="competition-desc">完整项目报告书（市场/产品/运营/财务/风险）</p>
            <div class="tags-container">
                <span class="tag">商业逻辑</span>
                <span class="tag">文档撰写</span>
                <span class="tag">团队管理</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="section" id="social">
        <h2 class="section-title">新媒体运营</h2>
        <div class="social-grid">
            <div class="social-stats-card">
                <img src="data:image/png;base64,{}" alt="视频数据概览">
                <div class="social-stats-info">
                    <h4>数据概览</h4>
                    <p>总播放量5万+，互动数据稳定增长</p>
                </div>
            </div>
            <div class="social-stats-card">
                <img src="data:image/png;base64,{}" alt="作品分析">
                <div class="social-stats-info">
                    <h4>作品分析</h4>
                    <p>爆款视频9.8万播放，获流量激励</p>
                </div>
            </div>
            <div class="social-card">
                <div class="social-icon">📺</div>
                <h3>B站：斯程菌 jun</h3>
                <p class="social-stats">总播放：5万+ | 爆款视频：9.8万播放</p>
            </div>
            <div class="social-card">
                <div class="social-icon">💻</div>
                <h3>GitHub</h3>
                <p class="social-stats">版本控制 | 项目迭代</p>
            </div>
            <div class="social-card">
                <div class="social-icon">🌐</div>
                <h3>个人官网</h3>
                <p class="social-stats">作品展示 | 游戏体验</p>
            </div>
        </div>
    </div>
    """.format(get_base64_image('images/图片1.png'), get_base64_image('images/图片2.png')), unsafe_allow_html=True)

    st.markdown("""
    <div class="contact-section" id="contact">
        <h2 class="section-title">联系方式</h2>
        <div class="contact-grid">
            <div class="contact-item">
                <div class="contact-icon">📞</div>
                <h3>电话</h3>
                <p>15288487348</p>
            </div>
            <div class="contact-item">
                <div class="contact-icon">📧</div>
                <h3>邮箱</h3>
                <p><a href="mailto:1247235323@qq.com">1247235323@qq.com</a></p>
            </div>
            <div class="contact-item">
                <div class="contact-icon">🌐</div>
                <h3>官网</h3>
                <p><a href="https://404workroom-1420076748.cos-website.ap-nanjing.myqcloud.com/index.html">404workroom</a></p>
            </div>
            <div class="contact-item">
                <div class="contact-icon">🎮</div>
                <h3>游戏体验</h3>
                <p><a href="https://27hrmzcgkukiwwqb9ogwrh.streamlit.app/" target="_blank">断联 404</a></p>
            </div>
        </div>
    </div>

    <div class="footer">
        <p>&copy; 2024 赵思城 | 404 Work Room</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
