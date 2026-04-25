# 从地图二转到SimpleScene场景的门交互功能

## 功能说明
实现当主角靠近门时显示UI按钮，点击后从"地图二"场景切换到"SimpleScene"场景的功能。

## 实现步骤

### 1. 添加场景到Build Settings
1. 在Unity编辑器中，打开 `File` > `Build Settings`
2. 确保"地图二"和"SimpleScene"场景都已添加到 `Scenes In Build` 列表中
3. 如果没有，点击 `Add Open Scenes` 按钮添加当前打开的场景

### 2. 创建脚本
1. 将 `DoorToSimpleScene.cs` 脚本复制到Unity项目的 `Assets` 文件夹中
2. 在"地图二"场景中，选择或创建一个门对象
3. 将 `DoorToSimpleScene.cs` 脚本附加到门对象上

### 3. 创建UI按钮
1. 在"地图二"场景中，创建一个Canvas对象（如果还没有）
2. 在Canvas下创建一个Button对象，命名为"back"
3. 调整按钮的位置、大小和样式
4. 确保按钮的初始状态为未激活（在Inspector面板中禁用按钮）

### 4. 配置脚本参数
1. 选中门对象
2. 在Inspector面板中找到 `DoorToSimpleScene` 组件
3. 将"back"按钮对象拖拽到 `BackButton` 字段中
4. 设置 `InteractionDistance` 为合适的值（默认2f）

### 5. 配置按钮点击事件
1. 选中"back"按钮对象
2. 在Inspector面板中找到 `Button` 组件
3. 点击 `On Click()` 下的 `+` 按钮
4. 将门对象拖拽到事件槽中
5. 在函数下拉菜单中选择 `DoorToSimpleScene` > `LoadNextScene`

### 6. 检查玩家设置
1. 确保玩家对象的Tag设置为 `Player`
2. 确保玩家对象有 `Rigidbody2D` 和 `Collider2D` 组件

### 7. 测试功能
1. 运行游戏，进入"地图二"场景
2. 控制主角靠近门，观察"back"按钮是否出现
3. 点击按钮，观察是否跳转到"SimpleScene"场景
4. 控制主角远离门，观察按钮是否消失

## 脚本说明

### DoorToSimpleScene.cs
- 使用 `GameObject.FindWithTag("Player")` 查找玩家
- 使用 `Vector2.Distance` 计算玩家与门的距离（2D游戏）
- 根据距离显示或隐藏"back"按钮
- 使用 `SceneManager.LoadScene()` 加载"SimpleScene"场景

## 注意事项
- 确保场景名称与代码中的名称完全一致（区分大小写）
- 确保场景已添加到Build Settings中
- 确保玩家对象的Tag设置为 `Player`
- 确保按钮对象有 `Button` 组件
- 可以根据需要调整 `InteractionDistance` 的值