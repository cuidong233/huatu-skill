# Undergrad Thesis Formatter

本科论文格式助手。目标流程：

1. 导入学校官方 `.docx` 模板
2. 识别模板里的页面设置、正文样式、标题样式
3. 导入自己的论文 `.docx`
4. 按模板样式生成一份格式化后的论文

第一版先做本地命令行工具，后续可以在这个核心能力上接网页上传界面。

## 能做什么

- 读取学校 Word 模板的页边距、纸张大小、方向
- 识别常见样式：正文、标题 1、标题 2、标题 3
- 将模板的常用样式复制到目标论文
- 根据段落内容识别常见本科论文标题：
  - 摘要 / Abstract
  - 第 1 章 / 第一章
  - 一、二、三、
  - （一）（二）（三）
  - 参考文献 / 致谢 / 附录
- 输出新的 `.docx`，不覆盖原论文

## 不能保证的事

学校模板常常有很细的人工格式，本工具第一版不承诺 100% 自动处理：

- 封面字段精准填充
- 页眉页脚分节
- 目录自动更新
- 图表目录
- 奇偶页不同页眉
- 学校特殊声明页

现实工作流应该是：自动处理主体格式，再用 Word/WPS 做最后检查。

## 安装

```bash
cd undergrad-thesis-formatter
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

## 使用

先分析学校模板：

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

## React 前端

启动 API：

```bash
python api_server.py
```

启动 React：

```bash
cd web
npm install
npm run dev
```

浏览器打开 Vite 输出的本地地址。前端会通过 `/api/analyze` 识别学校模板，通过 `/api/apply` 生成格式化后的 `.docx`。

也可以不安装，直接运行：

```bash
python -m thesis_formatter.cli analyze path/to/school-template.docx
python -m thesis_formatter.cli apply --template path/to/school-template.docx --input path/to/my-thesis.docx --output output/formatted-thesis.docx
```

## 推荐项目结构

```text
undergrad-thesis-formatter/
  references/
    figure-skill.md
  examples/
    .gitkeep
  output/
    formatted-thesis.docx
```

## 公开版本说明

公开仓库不携带学校官方模板、学生论文样例或生成结果。使用时请自行准备学校模板 `.docx` 和自己的论文 `.docx`。

论文图表和 AI 作图规则保存在：

```text
references/figure-skill.md
```

这份规则用于约束论文插图、架构图、流程图、系统截图和 AI 生成图片，避免把概念图误用成实验结果或真实系统证据。

## 后续版本

- Web 上传界面
- 模板识别报告可视化
- 参考文献 GB/T 7714 检查
- 目录/图表编号检查
- 封面字段映射
- Pandoc + reference.docx 工作流
