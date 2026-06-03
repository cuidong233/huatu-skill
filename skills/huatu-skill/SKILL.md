---
name: huatu-skill
description: 画图skill。Use when the agent needs to create, redraw, modify, or insert structural diagrams/画图 artifacts: flowcharts, E-R diagrams, architecture diagrams, UML/class diagrams, sequence diagrams, database relationship diagrams, thesis figures, Word/PPT/Markdown document figures, or system design diagrams. For diagram tasks, draw.io/diagrams.net is the mandatory production tool and `.drawio` is the required source format. Excludes data plots, screenshots, photos, raster illustrations, icons, logos, and pure visual design.
---

# 画图skill

## Core Rule

Use draw.io/diagrams.net as the only production format for diagrams.

Deliver a `.drawio` source whenever creating or substantially redrawing a diagram. Export a clean `.png` or `.svg` only after the editable source is correct. If inserting into `.docx`, `.pptx`, Markdown, or HTML, keep the `.drawio` source beside the document or in a sensible assets folder unless the user explicitly asks not to.

Do not use Graphviz, Mermaid, PlantUML, ASCII diagrams, canvas sketches, generated bitmaps, or quick layout generators as final outputs for any drawing task. They may be used only as temporary private scratch work, and the final editable source must still be recreated in draw.io.

## Request Routing

Classify the request before drawing:

| User request | This skill applies? | Required action |
|---|---:|---|
| Flowchart, E-R, architecture, UML/class, sequence, system, module, relationship, thesis structural figure | Yes | Create or update `.drawio`, export preview, validate |
| "示意图", "结构图", "关系图", "系统图" with boxes, arrows, entities, modules, or process steps | Yes | Create or update `.drawio`, export preview, validate |
| Existing raster diagram that needs editable boxes/arrows/labels | Yes | Recreate the diagram layer in `.drawio`; keep the raster only as reference |
| Bar, line, scatter, pie, heatmap, statistical chart, experimental result plot | No | Use a data visualization workflow; do not force draw.io |
| Screenshot, photo, raster illustration, texture, sprite, icon, logo, UI mockup | No | Use the appropriate visual workflow |

## Thesis / Graduation Project Defaults

Most thesis users are not blocked by "drawing"; they are blocked by formal document fit. For graduation-project and thesis requests, default to these constraints:

- Target medium is A4 Word unless the user says otherwise.
- Do not put the figure title inside the canvas; the title belongs in the document caption.
- Prefer black/gray academic styling, white/light fills, 12-14 pt body text, and 14-16 pt group headings.
- Keep the diagram readable after Word insertion at about 14-16 cm width.
- Use paired filenames, such as `system-architecture.drawio` and `system-architecture.png`.
- Put assets beside the document or in an existing `assets/`, `figures/`, `media/`, or `images/` folder.

If the user only says "帮我画一个毕设系统架构图" or another underspecified thesis prompt, ask at most three questions before drawing:

1. 系统主题/业务对象是什么？
2. 需要哪类图：架构图、功能模块图、流程图、E-R 图、类图、时序图？
3. 要插入 Word 还是 PPT？

If the user wants immediate output or does not answer, proceed with a conservative default: four-layer architecture (`用户端 / 表现层 / 业务服务层 / 数据层`) or a standard top-to-bottom flowchart, and state the assumption in the final note.

## Layout Standards

Prioritize readability over compactness:

- Use orthogonal connectors for flowcharts, E-R diagrams, architecture diagrams, and UML-style diagrams.
- Avoid crossing lines. A crossing includes connector-vs-connector intersections, connector lines passing through entity boxes/shapes, connector lines passing through text, and connector lines running through attribute ovals or labels. If any crossing appears, restructure the diagram first: change orientation, split the diagram, move attributes away from relationship paths, group related nodes, or add clear connector waypoints.
- Keep related nodes aligned on a visible grid.
- Leave enough whitespace around labels, connectors, decision diamonds, and table/entity boxes.
- Use consistent node sizes within the same diagram type.
- Use consistent arrow direction: top-to-bottom or left-to-right, not both unless there is a clear reason.
- Keep text large enough to read after insertion into Word or PPT.
- Prefer plain black/gray academic styling for thesis figures unless the document has an established visual system.
- For thesis, Word, PPT, or other captioned document figures, do not put the figure title/name inside the diagram canvas. For example, when creating "系统总体功能架构图", the diagram should show only the architecture content; the title belongs in the document caption, not inside the image.
- Prefer fewer, clearer nodes over exhaustive text dumps. If a diagram would exceed 12 entities/classes/modules or become unreadable at Word size, split it or ask for confirmation before splitting.

## Diagram Type Rules

For flowcharts:

- Use standard flowchart shapes: oval for start/end, rectangle for process, diamond for decision, parallelogram for input/output when useful.
- Label every decision branch, such as `是/否`, `成功/失败`, or `通过/不通过`.
- Keep the main path visually dominant and route exception paths to the side or bottom.
- Do not compress a long process into a single horizontal strip if the target document is A4/Word.

For E-R diagrams and database relationship diagrams:

- Show primary keys and important foreign keys.
- Show relationship cardinality, such as `1:N`, `1:1`, or `N:M`.
- Put central entities near the center and dependent tables around them.
- Route relationship lines orthogonally and avoid crossing through entity boxes.
- Prefer splitting into multiple diagrams if one E-R diagram becomes dense.

For architecture diagrams:

- Group by runtime responsibility, role, or deployment boundary.
- Label interfaces or data flows when the relationship is not obvious.
- Avoid vague stacked boxes that merely list technology names.
- For thesis architecture, prefer functional boundaries over technology buzzwords. A useful box says what the system does, not only "Spring Boot", "Vue", or "MySQL".

For UML/class diagrams:

- Include only fields and methods that explain the design.
- Avoid drawing controller/service/DAO chains as class diagrams unless the user specifically needs that view.
- If the purpose is functional design, prefer module or role diagrams over technology-layer diagrams.

For sequence diagrams:

- Put actors/services as lifelines from left to right in interaction order.
- Time flows from top to bottom.
- Use horizontal message arrows; use dashed return arrows only when the return value matters.
- Keep activation bars aligned to the messages that trigger them.
- Do not turn a sequence diagram into a flowchart. If branching dominates the picture, use a flowchart or activity diagram instead.

## Workflow

1. Identify the diagram purpose, diagram type, target medium, and target file location.
2. Decide whether the request is a structural diagram. If it is a data plot, screenshot, photo, raster illustration, icon, logo, or pure visual design task, route to a non-diagram workflow.
3. Resolve missing information using the Thesis / Graduation Project Defaults when applicable.
4. Sketch the layout mentally or in a temporary draft, choosing top-to-bottom or left-to-right orientation.
5. Create or modify a draw.io-compatible `.drawio` file.
6. Export to `.png` or `.svg` at a readable size for the target document.
7. Open or view the exported image and perform a visual validation pass before responding.
8. If the validation finds crossing lines, lines touching or running through text, cramped labels, unclear arrows, cut-off content, or inconsistent shape use, revise the `.drawio`, re-export, and visually validate again. Repeat until the image passes or the user explicitly accepts the defect.
9. If replacing an image inside a document, preserve captions and update the embedded image without degrading surrounding formatting.
10. Report the final source and exported image only after the validation gates pass, or report the exact export/validation blocker.

## Export and Validation

Validation must be visual, not only syntactic:

- Exported image must not be clipped.
- Text must be readable at the target document size.
- Connectors must not cross other connectors, pass through boxes, pass through labels, or touch text.
- Branch labels, relationship cardinalities, and message names must be visible.
- Similar nodes should have consistent size, spacing, and alignment.

Failure branches:

- If no local draw.io exporter is available, still create the `.drawio` source, then state that local export and visual validation could not be completed because the exporter is unavailable.
- If export fails because the source is invalid, fix the `.drawio` before responding.
- If export fails because the local tool is missing or broken, keep the `.drawio` as the source of truth and report the command failure.
- If image viewing fails, do not claim visual validation succeeded. State that only source creation/export succeeded.
- If document image replacement fails, keep the original document unchanged when possible, save the diagram assets separately, and report the insertion failure.

## Document Insertion Rules

When inserting or replacing a figure in Word, PPT, Markdown, or HTML:

- Preserve existing captions, numbering, surrounding paragraphs, and document styles.
- Replace only the requested figure unless the user explicitly asks for document restructuring.
- Keep the `.drawio` source beside the exported image.
- Do not degrade the document by flattening unrelated content or rebuilding the whole document.
- If the target figure is ambiguous, stop and ask which figure to replace.

Use explicit checkpoints when the next action can damage user work or change scope:

- CHECKPOINT before replacing a user's clean original diagram with a materially different layout.
- CHECKPOINT before splitting one requested figure into multiple figures.
- CHECKPOINT before changing surrounding Word/PPT/Markdown structure beyond replacing the requested figure.
- CHECKPOINT before omitting export/visual validation because local tooling is unavailable.

## Hard Constraints

- For every drawing/diagram task, create or update a `.drawio` source. Other tools are not acceptable final production tools.
- Do not submit a final diagram without exporting it and visually inspecting the exported image unless the final response explicitly reports the export or visual-validation blocker.
- Do not leave crossed lines in a final diagram unless the user explicitly accepts the specific crossing after seeing it. "Crossed lines" includes connector intersections, connectors through shapes, connectors through text, and connectors through attribute ovals/labels.
- If a crossing is found during validation, the next action must be a layout revision and re-export, not a final answer.
- Do not submit a final diagram that is visibly a cramped auto-layout artifact.
- Do not replace a user's clean original diagram with a worse generated one.
- Do not use a raster-only image as the source of truth for a diagram.
- Do not put multiple unrelated figures on one line in a thesis or formal document unless the document explicitly uses subfigures with labels.
- Do not include self-referential title text such as "系统总体功能架构图", "流程图", "E-R 图", or "架构图" inside the diagram when the surrounding document already provides a caption.
- Do not claim export or visual validation succeeded unless it actually did.
- Do not force draw.io onto data plots such as bar charts, line charts, scatter plots, statistical charts, heatmaps, or other numeric visualizations.

## Boundary

If the user asks for "画图", "生成图", "重画图", "流程图", "E-R 图", "架构图", "类图", "时序图", "系统图", "论文图", "结构图", "关系图", "示意图", or any comparable structural diagram artifact, this skill applies and draw.io is mandatory.

This skill does not govern non-diagram visual work such as screenshots, photos, raster illustrations, textures, sprites, icons, logos, pure UI mockups, or data plots. If a non-diagram visual later needs labels, arrows, structure, or formal diagram treatment, create that diagram layer in draw.io while leaving the underlying non-diagram asset to the appropriate tool.
