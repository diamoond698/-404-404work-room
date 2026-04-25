# Esc菜单功能实现

## 功能说明
实现当按下键盘"esc"键时弹出esc菜单，包含继续游戏和退出游戏按钮的功能。

## 实现步骤

### 1. 创建UI面板
1. 在Unity编辑器中，选择或创建一个Canvas对象
2. 在Canvas下创建一个Panel对象，命名为"EscMenuPanel"
3. 调整Panel的大小和位置，使其覆盖整个屏幕
4. 设置Panel的背景颜色为半透明黑色（如RGBA: 0, 0, 0, 0.7）
5. 在Panel下创建两个Button对象：
   - 命名为"ContinueButton"，文本设为"继续游戏"
   - 命名为"QuitButton"，文本设为"退出游戏"
6. 调整按钮的位置和样式
7. 确保Panel的初始状态为未激活（在Inspector面板中禁用Panel）

### 2. 添加脚本
1. 将 `EscMenuManager.cs` 脚本复制到Unity项目的 `Assets` 文件夹中
2. 创建一个空GameObject，命名为"EscMenuManager"
3. 将 `EscMenuManager.cs` 脚本附加到该GameObject上

### 3. 配置脚本参数
1. 选中"EscMenuManager"对象
2. 在Inspector面板中找到 `EscMenuManager` 组件
3. 将"EscMenuPanel"对象拖拽到 `Esc Menu Panel` 字段中
4. 将"ContinueButton"对象拖拽到 `Continue Button` 字段中
5. 将"QuitButton"对象拖拽到 `Quit Button` 字段中

### 4. 测试功能
1. 运行游戏
2. 按下键盘上的"esc"键，观察esc菜单是否弹出
3. 点击"继续游戏"按钮，观察菜单是否关闭
4. 再次按下"esc"键，打开菜单
5. 点击"退出游戏"按钮，观察游戏是否退出

## 脚本说明

### EscMenuManager.cs
- 监听键盘"esc"键的按下事件
- 显示或隐藏esc菜单面板
- 暂停和恢复游戏时间（Time.timeScale）
- 实现继续游戏和退出游戏的功能

## 注意事项
- 确保Canvas的渲染模式设置为 `Screen Space - Overlay`
- 确保Panel和按钮的层级设置正确，使菜单显示在其他UI元素之上
- 可以根据需要调整菜单的样式和布局
- 退出游戏功能在Unity编辑器中会停止播放模式，在构建后的游戏中会退出程序