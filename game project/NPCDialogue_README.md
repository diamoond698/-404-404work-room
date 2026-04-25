# NPC对话系统

## 功能说明
实现主角靠近NPC时显示对话提示和交互按钮，按E键或点击按钮开始对话，按E键切换对话内容，对话结束后自动关闭的功能。同时支持显示NPC和玩家的照片。

## 实现步骤

### 1. 创建对话UI
1. **创建Canvas**：
   - 在Hierarchy窗口中，右键点击空白处，选择 `UI > Canvas`
   - 命名为"DialogueCanvas"

2. **创建对话面板**：
   - 在Canvas下创建一个Panel，命名为"DialoguePanel"
   - 调整Panel的大小和位置（建议在屏幕底部）
   - 设置Panel的背景颜色为半透明黑色（如RGBA: 0, 0, 0, 0.7）

3. **创建文本组件**：
   - 在DialoguePanel下创建一个Text，命名为"NameText"（显示NPC名字）
   - 在DialoguePanel下创建另一个Text，命名为"DialogueText"（显示对话内容）
   - 调整文本的字体、大小和颜色

4. **创建照片组件**：
   - 在DialoguePanel下创建一个Image，命名为"PhotoImage"（显示NPC或玩家照片）
   - 调整Image的大小和位置

5. **创建交互提示**：
   - 在Canvas下创建一个Text，命名为"InteractPrompt"
   - 文本内容设为"按E键交谈"
   - 调整位置和样式

6. **创建交互按钮**：
   - 在Canvas下创建一个Button，命名为"InteractButton"
   - 设置按钮文本为"交谈"
   - 调整位置和样式

7. **初始状态**：
   - 确保DialoguePanel、InteractPrompt和InteractButton的初始状态为未激活（在Inspector面板中禁用）

### 2. 添加脚本
1. 将 `NPCDialogue.cs` 脚本复制到Unity项目的 `Assets` 文件夹中
2. 将脚本附加到NPC对象上

### 3. 配置脚本参数
1. 选中NPC对象
2. 在Inspector面板中找到 `NPCDialogue` 组件
3. 配置以下参数：

   **对话设置**：
   - `Npc Name`：输入NPC的名字
   - `Dialogue Lines`：点击"+"按钮添加对话内容，输入对话文本
   - `Interaction Distance`：设置交互距离（默认2f）

   **照片设置**：
   - `Npc Photo`：拖拽NPC的照片 sprite 到该字段
   - `Player Photo`：拖拽玩家的照片 sprite 到该字段

   **UI设置**：
   - `Dialogue UI`：拖拽DialoguePanel对象到该字段
   - `Name Text`：拖拽NameText对象到该字段
   - `Dialogue Text`：拖拽DialogueText对象到该字段
   - `Interact Prompt`：拖拽InteractPrompt对象到该字段
   - `Interact Button`：拖拽InteractButton对象到该字段
   - `Photo Image`：拖拽PhotoImage对象到该字段

### 4. 测试功能
1. 运行游戏
2. 控制主角靠近NPC，观察是否显示"按E键交谈"提示和交互按钮
3. 按E键或点击按钮开始对话，观察是否显示对话内容和照片
4. 按E键切换对话内容，观察照片是否随说话者变化
5. 对话结束后，观察对话UI是否自动关闭

## 脚本说明

### NPCDialogue.cs
- 检测主角与NPC的距离
- 显示/隐藏交互提示和按钮
- 处理E键和按钮交互
- 显示对话内容和照片
- 处理对话切换和结束

## 注意事项
- 确保主角对象的Tag设置为"Player"
- 确保Canvas的渲染模式设置为 `Screen Space - Overlay`
- 可以根据需要调整交互距离和UI样式
- 可以添加多个对话内容，形成完整的对话流程
- 确保为NPC和玩家设置了照片sprite

## 扩展功能
- **添加对话选项**：可以扩展脚本，添加对话选择功能
- **添加音效**：可以在对话开始和切换时添加音效
- **添加动画**：可以为NPC添加对话时的动画效果
- **添加条件对话**：可以根据游戏进度或玩家状态显示不同的对话内容