# 门场景切换按钮功能

## 功能说明
实现当主角靠近"门"时显示"next scene"按钮，点击后跳转到"地图二"场景的功能。

## 实现步骤

### 1. 添加场景到Build Settings
1. 在Unity编辑器中，打开 `File` > `Build Settings`
2. 确保"地图二"场景已添加到 `Scenes In Build` 列表中
3. 如果没有，打开"地图二"场景，点击 `Add Open Scenes` 添加

### 2. 创建脚本
1. 将 `DoorNextSceneButton.cs` 脚本复制到Unity项目的 `Assets` 文件夹中
2. 将脚本附加到"门"对象上

### 3. 配置脚本参数
1. 选中"门"对象
2. 在Inspector面板中找到 `DoorNextSceneButton` 组件
3. 将"next scene"按钮对象拖拽到 `NextSceneButton` 字段中
4. 设置 `InteractionDistance` 为合适的值（默认2f）

### 4. 配置按钮点击事件
1. 选中"next scene"按钮对象
2. 在Inspector面板中找到 `Button` 组件
3. 点击 `On Click()` 下的 `+` 按钮
4. 将"门"对象拖拽到事件槽中
5. 在函数下拉菜单中选择 `DoorNextSceneButton` > `LoadNextScene`

### 5. 检查玩家设置
1. 确保玩家对象的Tag设置为 `Player`
2. 确保玩家对象有 `Rigidbody2D` 和 `Collider2D` 组件

### 6. 测试功能
1. 运行游戏
2. 控制主角靠近"门"
3. 观察"next scene"按钮是否出现
4. 点击按钮，观察是否跳转到"地图二"场景
5. 控制主角远离"门"，观察按钮是否消失

## 脚本说明

### DoorNextSceneButton.cs
- 使用 `GameObject.FindWithTag("Player")` 查找玩家
- 使用 `Vector2.Distance` 计算玩家与门的距离（2D游戏）
- 根据距离显示或隐藏按钮
- 使用 `SceneManager.LoadScene()` 加载场景

## 注意事项
- 确保场景名称与代码中的名称完全一致（区分大小写）
- 确保场景已添加到Build Settings中
- 确保玩家对象的Tag设置为 `Player`
- 确保按钮对象有 `Button` 组件
- 可以根据需要调整 `InteractionDistance` 的值