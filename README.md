# huatu-skill

Codex 画图 skill。用于生成、重画或修改正式图件，包括流程图、E-R 图、数据库关系图、系统架构图、UML 图、类图、时序图、论文图和答辩图。

核心原则：所有正式图件都必须使用 draw.io/diagrams.net 作为生产格式，最终交付 `.drawio` 可编辑源文件；需要插入论文、Word、PPT 或 Markdown 时，再从 `.drawio` 导出 `.png` 或 `.svg`。

## 内容

```text
skills/huatu-skill/
  SKILL.md
  agents/openai.yaml
```

## 主要约束

- 必须创建或更新 `.drawio` 源文件。
- 不使用 Graphviz、Mermaid、PlantUML、ASCII 图或纯图片作为最终图源。
- 导出图片后必须做视觉检查。
- 不允许线条交叉、线穿过文字、线穿过实体框、线穿过属性椭圆或标签，除非用户看过后明确接受。
- 如果发现交叉或拥挤，必须返工重排、重新导出、重新检查。
- 论文或正式文档中的图不在画布里写“流程图 / 架构图 / E-R 图”这类标题，标题应放在文档图注中。

## 使用

把 `skills/huatu-skill` 安装或复制到 Codex skills 目录中，然后在需要画图时使用它。

典型任务：

- “帮我画数据库 E-R 图”
- “把这个流程重画成论文里的流程图”
- “生成系统总体架构图”
- “画一张 UML 类图 / 时序图”

## License

MIT
