# 旁白系统

## 功能说明
实现游戏开头或特定场景的旁白功能，支持自动播放、淡入淡出动画、音效等效果。

## 实现步骤

### 1. 创建UI元素
1. **创建Canvas**：
   - 在Hierarchy窗口中，右键点击空白处，选择 `UI > Canvas`
   - 命名为"NarratorCanvas"

2. **创建旁白面板**：
   - 在Canvas下创建一个Panel，命名为"NarrationPanel"
   - 调整Panel的大小和位置（建议在屏幕中央或底部）
   - 设置Panel的背景颜色为半透明黑色（如RGBA: 0, 0, 0, 0.7）
   - 添加CanvasGroup组件，用于淡入淡出动画

3. **创建文本组件**：
   - 在NarrationPanel下创建一个TextMeshPro - Text，命名为"NarratorNameText"（显示旁白名字）
   - 在NarrationPanel下创建另一个TextMeshPro - Text，命名为"NarrationText"（显示旁白内容）
   - 调整文本的字体、大小和颜色

4. **初始状态**：
   - 确保NarrationPanel的初始状态为未激活（在Inspector面板中禁用）

### 2. 添加脚本
1. 将 `Narrator.cs` 脚本复制到Unity项目的 `Assets` 文件夹中
2. 创建一个空游戏对象，命名为"NarratorManager"
3. 将 `Narrator.cs` 脚本附加到该对象上

### 3. 配置脚本参数
1. 选中"NarratorManager"对象
2. 在Inspector面板中找到 `Narrator` 组件
3. 配置以下参数：

   **旁白设置**：
   - `Narration Lines`：点击"+"按钮添加旁白文本，输入旁白内容
   - `Narration Duration`：设置每句旁白显示的持续时间（默认3秒）
   - `Line Interval`：设置旁白之间的间隔时间（默认1秒）
   - `Auto Play`：是否自动播放（默认true）
   - `Start Delay`：游戏开始后延迟播放的时间（默认1秒）
   - `Auto Destroy`：播放完成后是否自动销毁（默认true）

   **UI设置**：
   - `Narration UI`：拖拽NarrationPanel对象到该字段
   - `Narration Text`：拖拽NarrationText对象到该字段
   - `Narrator Name Text`：拖拽NarratorNameText对象到该字段
   - `Narrator Name`：输入旁白的名字（默认"旁白"）

   **动画设置**：
   - `Fade In Duration`：淡入动画持续时间（默认0.5秒）
   - `Fade Out Duration`：淡出动画持续时间（默认0.5秒）

   **音频设置**：
   - `Narration Sounds`：添加旁白音效（可选）
   - `Audio Source`：拖拽音频源组件（如果没有会自动创建）

### 4. 测试功能
1. 运行游戏
2. 观察是否自动播放旁白
3. 检查旁白是否按顺序显示，并有淡入淡出效果
4. 检查音效是否正常播放

## 脚本说明

### Narrator.cs
- 支持自动播放和手动触发
- 支持淡入淡出动画
- 支持旁白音效
- 可自定义旁白显示时间和间隔时间

## 扩展功能
- **条件触发**：可以根据游戏进度或玩家状态触发不同的旁白
- **场景切换**：可以在旁白结束后自动切换场景
- **多语言支持**：可以根据玩家语言设置显示不同语言的旁白

## 注意事项
- 确保Canvas的渲染模式设置为 `Screen Space - Overlay`
- 如果需要在特定场景触发旁白，可以关闭Auto Play，然后通过其他脚本调用StartNarration()方法
- 可以根据需要调整UI样式和动画效果