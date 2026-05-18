import streamlit as st

st.set_page_config(page_title="赵思城 | 个人作品集", layout="wide")

st.markdown("""
    <style>
    body {
        background: linear-gradient(135deg, #1A1A2E 0%, #16213E 50%, #0F3460 100%);
        color: #F5F5DC;
    }
    .hero-title {
        font-size: 3rem;
        background: linear-gradient(135deg, #FFD700, #D4A574);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .section-title {
        color: #FFD700;
        border-bottom: 2px solid #FFD700;
        padding-bottom: 10px;
    }
    .skill-card {
        background: rgba(45, 45, 68, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(201, 169, 98, 0.3);
    }
    .game-card {
        background: rgba(45, 45, 68, 0.6);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid rgba(201, 169, 98, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1 class='hero-title'>趙思城 | 个人作品集</h1>", unsafe_allow_html=True)
st.write("## 游戏策划 / 剧情文案 / 独立游戏开发 / 新媒体内容创作")

st.markdown("---")

st.markdown("<h2 class='section-title'>核心能力</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("<div class='skill-card'>🎮 游戏全案开发</div>", unsafe_allow_html=True)
with col2:
    st.markdown("<div class='skill-card'>✍️ 叙事文案</div>", unsafe_allow_html=True)
with col3:
    st.markdown("<div class='skill-card'>💻 前端开发</div>", unsafe_allow_html=True)
col4, col5 = st.columns(2)
with col4:
    st.markdown("<div class='skill-card'>📺 新媒体运营</div>", unsafe_allow_html=True)
with col5:
    st.markdown("<div class='skill-card'>👥 项目统筹</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown("<h2 class='section-title'>独立游戏作品</h2>", unsafe_allow_html=True)
st.subheader("🎮 断联 404")
st.image("images/cover.png", width=400)
st.write("**类型**：科幻悬疑 / 叙事冒险 / 网页可玩")
st.write("**亮点**：双世界观、强情感叙事、完整四幕剧情")

st.subheader("🤖 游戏AI Agent")
st.image("images/aiagent1.png", width=400)
st.write("**功能**：智能对话系统、代码生成、性能预估")

st.markdown("---")

st.markdown("<h2 class='section-title'>文学创作</h2>", unsafe_allow_html=True)
st.write("- **长篇小说《青川一纸：解开父亲的执念密码》**：悬疑亲情 / 科学反迷信 / 民俗探案")
st.write("- **现实小说《月映崇山》**：反拐卖 / 反迷信 / 基层民警叙事")
st.write("- **诗歌《白凤游九州》**：家国情怀，意象优美")

st.markdown("---")

st.markdown("<h2 class='section-title'>新媒体运营</h2>", unsafe_allow_html=True)
st.image("images/图片1.png", width=500)
st.image("images/图片2.png", width=500)
st.write("📺 B站：斯程菌 jun | 总播放：5万+ | 爆款视频：9.8万播放")

st.markdown("---")

st.markdown("<h2 class='section-title'>联系方式</h2>", unsafe_allow_html=True)
st.write("📞 电话：15288487348")
st.write("📧 邮箱：1247235323@qq.com")
st.write("🌐 官网：https://404workroom-1420076748.cos-website.ap-nanjing.myqcloud.com")
st.write("🎮 游戏体验：https://27hrmzcgkukiwwqb9ogwrh.streamlit.app/")
