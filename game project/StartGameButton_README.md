# 登录界面按钮场景切换功能

## 功能说明
实现点击"start the game"按钮后切换到"SampleScene"场景的功能。

## 实现步骤

### 1. 添加场景到Build Settings
1. 在Unity编辑器中，打开 `File` > `Build Settings`
2. 确保登录界面场景和"SampleScene"都已添加到 `Scenes In Build` 列表中
3. 如果没有，点击 `Add Open Scenes` 按钮添加当前打开的场景

### 2. 创建脚本
1. 将 `StartGameButton.cs` 脚本复制到Unity项目的 `Assets` 文件夹中
2. 在Hierarchy窗口中创建一个空游戏对象，命名为 `GameManager`（或任何合适的名称）
3. 将 `StartGameButton.cs` 脚本附加到 `GameManager` 对象上

### 3. 配置脚本参数
1. 选中 `GameManager` 对象
2. 在Inspector面板中找到 `StartGameButton` 组件
3. 将"start the game"按钮对象拖拽到 `StartButton` 字段中

### 4. 测试功能
1. 运行游戏
2. 点击"start the game"按钮
3. 观察是否成功切换到"SampleScene"场景

## 脚本说明

### StartGameButton.cs
- 使用 `SceneManager.LoadScene()` 方法加载场景
- 通过 `Button.onClick.AddListener()` 添加点击事件监听
- 自动在Start方法中设置按钮点击事件

## 注意事项
- 确保场景名称与代码中的名称完全一致（区分大小写）
- 确保场景已添加到Build Settings中
- 按钮对象必须有 `Button` 组件
- 如果场景名称不同，请修改代码中的场景名称