# 2D游戏人物自由移动代码

## 功能说明
实现2D游戏中人物的简单上下左右移动功能。

## 实现步骤

### 1. 准备工作
1. 在Unity场景中创建一个玩家游戏对象
2. 为玩家添加Rigidbody2D组件
3. 为玩家添加Collider2D组件（如BoxCollider2D）

### 2. 添加脚本
1. 将PlayerMovement2D.cs脚本复制到Unity项目的Assets文件夹中
2. 将脚本附加到玩家游戏对象上
3. 在Inspector面板中设置以下参数：
   - moveSpeed: 设置移动速度（默认5f）

### 3. 测试功能
1. 运行游戏
2. 使用方向键（或WASD键）控制玩家移动
3. 观察玩家是否能够自由上下左右移动

## 脚本说明

### PlayerMovement2D.cs
- 使用Input.GetAxis获取水平和垂直输入
- 通过修改Rigidbody2D的velocity实现移动
- 适用于2D游戏

### 注意事项
- 确保玩家游戏对象有Rigidbody2D组件
- 可以根据需要调整移动速度