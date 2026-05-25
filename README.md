# Student Project Toolkit

给大学生、研究生做课程设计、毕设、竞赛项目时使用的一组 AI skills 和本地工具。

这个仓库的目标不是替代学生完成项目，而是把那些重复、容易出错、但又很耗时间的工程化工作标准化：画图、论文排版、文档整理、格式检查、项目交付物生成等。

## 当前内容

### Skills

- `skills/huatu-skill`：画图 skill。用于流程图、E-R 图、架构图、UML 图、论文图等正式图件。强制使用 draw.io/diagrams.net 作为源格式，并要求导出后做视觉检查，避免线条交叉、文字被穿线、图形拥挤等问题。

### Tools

- `tools/undergrad-thesis-formatter`：本科论文 Word 格式助手。读取学校 `.docx` 模板的页面设置和常见样式，再把这些格式应用到自己的论文 `.docx`，生成新的格式化文档。

## 目录结构

```text
student-project-toolkit/
  skills/
    huatu-skill/
      SKILL.md
      agents/openai.yaml
  tools/
    undergrad-thesis-formatter/
```

## 适用场景

- 本科毕业设计、课程设计、实验报告
- 研究生课程项目、开题材料、论文辅助整理
- 创新创业、互联网+、挑战杯、数学建模等竞赛项目材料
- 需要把“能运行的项目”整理成“能交付、能展示、能答辩”的场景

## 使用方式

### 使用画图 skill

把 `skills/huatu-skill` 复制或安装到你的 Codex skills 目录中，然后在需要画图时触发它。

核心要求：

- 最终必须交付 `.drawio` 可编辑源文件
- 需要插论文或报告时再导出 `.png` / `.svg`
- 导出后必须检查图中是否有交叉线、线穿过文字、线穿过形状、标签拥挤等问题

### 使用论文格式工具

进入工具目录：

```bash
cd tools/undergrad-thesis-formatter
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

分析学校模板：

```bash
thesis-format analyze path/to/school-template.docx
```

套用格式：

```bash
thesis-format apply \
  --template path/to/school-template.docx \
  --input path/to/my-thesis.docx \
  --output output/formatted-thesis.docx
```

## 公开仓库说明

这个仓库不包含学校官方模板、学生论文原文、带个人信息的文档或生成结果。使用时请自行准备自己的 `.docx` 模板和论文文件。

## License

MIT
