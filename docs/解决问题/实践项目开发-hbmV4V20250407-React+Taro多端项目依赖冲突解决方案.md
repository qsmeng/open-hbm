# React+Taro多端项目依赖冲突解决方案

## 问题背景
在开发基于React+Taro的多端项目时，经常会遇到各种依赖版本冲突问题，特别是当项目同时需要支持小程序、H5和React Native时。本文记录了一个实际项目中遇到的依赖冲突问题及完整解决方案。

## 环境信息
- 项目结构：React 18 + Taro 4 + React Native 0.73
- 操作系统：Windows 10
- 包管理工具：npm/yarn

## 主要问题表现
1. Taro相关包版本不一致（3.x和4.x混用）
2. babel-preset-taro版本不匹配
3. typescript版本不存在问题
4. peer dependencies冲突

## 完整解决方案

### 第一步：统一Taro版本
将所有Taro相关包统一为4.0.12版本：

```json
"dependencies": {
  "@tarojs/components": "4.0.12",
  "@tarojs/components-rn": "4.0.12",
  "@tarojs/plugin-framework-react": "4.0.12",
  // 其他Taro包...
},
"devDependencies": {
  "@tarojs/cli": "4.0.12",
  "@tarojs/rn-runner": "4.0.12",
  // 其他Taro开发依赖...
}
```

### 第二步：解决babel-preset-taro冲突
将babel-preset-taro也更新到匹配版本：

```json
"babel-preset-taro": "4.0.12"
```

### 第三步：调整TypeScript版本
将typescript改为稳定版本：

```json
"typescript": "^4.9.5"
```

### 第四步：清理和重新安装
Windows PowerShell下执行：

```powershell
# 清除缓存
npm cache clean --force

# 删除旧依赖
Remove-Item -Recurse -Force node_modules
Remove-Item -Force package-lock.json

# 推荐使用yarn安装
npm install -g yarn
yarn install

# 或者使用npm安装
npm install --legacy-peer-deps
```

### 第五步：验证和启动
```powershell
yarn dev
# 或
npm run dev
```

## 常见问题排查
1. **版本不存在错误**：检查npm仓库中是否存在指定版本
2. **peer dependencies冲突**：使用--legacy-peer-deps参数
3. **Windows命令问题**：PowerShell使用Remove-Item代替rm -rf
4. **网络问题**：检查代理或切换npm源

## 总结
通过统一版本、清理缓存和正确使用包管理工具，可以有效解决React+Taro多端项目中的依赖冲突问题。建议使用yarn管理依赖，并保持所有相关包的版本一致性。

> 本文记录的实际问题解决方案，希望对遇到类似问题的开发者有所帮助。
