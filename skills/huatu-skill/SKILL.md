---
name: huatu-skill
description: 画图skill。Use when Codex needs to create, redraw, modify, or insert any diagram/画图 artifact, including flowcharts, E-R diagrams, architecture diagrams, UML/class diagrams, sequence diagrams, database relationship diagrams, thesis figures, Word/PPT/Markdown document figures, or system design diagrams. For all diagram drawing tasks, draw.io/diagrams.net is the mandatory production tool and `.drawio` is the required source format. Do not use Graphviz, Mermaid, PlantUML, ASCII diagrams, generated bitmaps, or ad hoc drawing methods as final diagram outputs.
---

# 画图skill

## Core Rule

Use draw.io/diagrams.net as the only production format for diagrams.

Deliver a `.drawio` source whenever creating or substantially redrawing a diagram. Export a clean `.png` or `.svg` only after the editable source is correct. If inserting into `.docx`, `.pptx`, Markdown, or HTML, keep the `.drawio` source beside the document or in a sensible assets folder unless the user explicitly asks not to.

Do not use Graphviz, Mermaid, PlantUML, ASCII diagrams, canvas sketches, generated bitmaps, or quick layout generators as final outputs for any drawing task. They may be used only as temporary private scratch work, and the final editable source must still be recreated in draw.io.

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

For UML/class diagrams:

- Include only fields and methods that explain the design.
- Avoid drawing controller/service/DAO chains as class diagrams unless the user specifically needs that view.
- If the purpose is functional design, prefer module or role diagrams over technology-layer diagrams.

## Workflow

1. Identify the diagram purpose and target medium.
2. Sketch the layout mentally or in a temporary draft, choosing top-to-bottom or left-to-right orientation.
3. Create or modify a draw.io-compatible `.drawio` file.
4. Export to `.png` or `.svg` at a readable size for the target document.
5. Open or view the exported image and perform a visual validation pass before responding.
6. If the validation finds crossing lines, lines touching or running through text, cramped labels, unclear arrows, cut-off content, or inconsistent shape use, revise the `.drawio`, re-export, and visually validate again. Repeat until the image passes or the user explicitly accepts the defect.
7. If replacing an image inside a document, preserve captions and update the embedded image without degrading surrounding formatting.
8. Report the final source and exported image only after the visual validation pass succeeds.

## Hard Constraints

- For every drawing/diagram task, create or update a `.drawio` source. Other tools are not acceptable final production tools.
- Do not submit a final diagram without exporting it and visually inspecting the exported image.
- Do not leave crossed lines in a final diagram unless the user explicitly accepts the specific crossing after seeing it. "Crossed lines" includes connector intersections, connectors through shapes, connectors through text, and connectors through attribute ovals/labels.
- If a crossing is found during validation, the next action must be a layout revision and re-export, not a final answer.
- Do not submit a final diagram that is visibly a cramped auto-layout artifact.
- Do not replace a user's clean original diagram with a worse generated one.
- Do not use a raster-only image as the source of truth for a diagram.
- Do not put multiple unrelated figures on one line in a thesis or formal document unless the document explicitly uses subfigures with labels.
- Do not include self-referential title text such as "系统总体功能架构图", "流程图", "E-R 图", or "架构图" inside the diagram when the surrounding document already provides a caption.

## Boundary

If the user asks for "画图", "生成图", "重画图", "流程图", "E-R 图", "架构图", "类图", "系统图", "论文图", "图表", or any comparable diagram artifact, this skill applies and draw.io is mandatory.

This skill does not govern non-diagram visual work such as screenshots, photos, raster illustrations, textures, sprites, icons, logos, or data plots. If a non-diagram visual later needs labels, arrows, structure, or formal diagram treatment, convert that diagram layer into draw.io.
