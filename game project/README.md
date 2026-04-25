# 主角与门的UI交互设计

## 功能说明
实现主角靠近门时显示交互提示，门会自动打开和关闭的功能，适用于2D游戏。

## 实现步骤

### 1. 准备工作
1. 确保Unity项目中已经有主角（标签为Player）和门的模型
2. 门已经附加了TriggerDoor脚本

### 2. 添加UI元素
1. 在场景中创建一个Canvas对象
2. 在Canvas下创建一个Text对象，用于显示交互提示
3. 设置Text的样式和位置
4. 初始状态下，Canvas设置为不激活

### 3. 添加脚本
1. 将DoorInteractionUI.cs脚本复制到Unity项目的Assets文件夹中
2. 将脚本附加到门上
3. 在Inspector面板中设置以下参数：
   - interactionCanvas: 选择创建的Canvas对象
   - interactionText: 选择Canvas下的Text对象
   - interactionDistance: 设置交互距离（默认2f）

### 4. 配置门的碰撞器
1. 确保门有一个Collider组件
2. 将Collider设置为Is Trigger
3. 调整Collider的大小，确保主角靠近时能触发交互

### 5. 测试功能
1. 运行游戏
2. 控制主角靠近门
3. 观察是否显示交互提示
4. 观察门是否自动打开
5. 控制主角离开门
6. 观察门是否自动关闭

## 脚本说明

### DoorInteractionUI.cs
- 监听玩家与门的距离，显示/隐藏交互提示
- 适用于2D游戏，只计算X和Y轴的距离

### TriggerDoor.cs
- 检测玩家进入和离开触发器
- 自动打开和关闭门

### 注意事项
- 确保主角的标签设置为"Player"
- 可以根据需要调整交互距离
- 可以自定义UI提示的样式和位置