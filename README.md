# xiaoshuo

硬规则驱动的多视角小说世界模拟 / 生成系统。

当前阶段重点：

- 建立 BDD 验收规则。
- 提炼世界规则、角色视角、资源消耗、信息危险等硬约束。
- 搭建后续实现所需的领域模型、生成流程和验证器目录结构。

## 本地验证

运行单元测试：

```powershell
python -m unittest discover -s src/tests
```

运行当前世界图谱和第一章结构验证：

```powershell
python scripts/validate_project.py
```
