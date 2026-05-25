import { useMemo, useState } from 'react'
import './App.css'

type TemplateProfile = {
  page: Record<string, number | null>
  body_style: {
    name: string
    font_name: string | null
    font_size_pt: number | null
  } | null
  heading_styles: Record<
    string,
    {
      name: string
      font_name: string | null
      font_size_pt: number | null
      bold: boolean | null
    }
  >
  paragraph_style_count: number
  sample_headings: string[]
}

type FilePickerProps = {
  id: string
  label: string
  hint: string
  file: File | null
  onChange: (file: File | null) => void
}

function FilePicker({ id, label, hint, file, onChange }: FilePickerProps) {
  return (
    <label className="file-picker" htmlFor={id}>
      <span>{label}</span>
      <strong>{file ? file.name : '选择 .docx 文件'}</strong>
      <small>{hint}</small>
      <input
        id={id}
        type="file"
        accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        onChange={(event) => onChange(event.target.files?.[0] ?? null)}
      />
    </label>
  )
}

function App() {
  const [templateFile, setTemplateFile] = useState<File | null>(null)
  const [thesisFile, setThesisFile] = useState<File | null>(null)
  const [profile, setProfile] = useState<TemplateProfile | null>(null)
  const [status, setStatus] = useState('等待导入学校模板')
  const [isBusy, setIsBusy] = useState(false)

  const canApply = useMemo(() => Boolean(templateFile && thesisFile), [templateFile, thesisFile])

  async function analyzeTemplate() {
    if (!templateFile) return
    setIsBusy(true)
    setStatus('正在识别学校模板')

    const formData = new FormData()
    formData.append('template', templateFile)

    try {
      const response = await fetch('/api/analyze', {
        method: 'POST',
        body: formData,
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || '模板识别失败')
      setProfile(data)
      setStatus('模板识别完成')
    } catch (error) {
      setStatus(error instanceof Error ? error.message : '模板识别失败')
    } finally {
      setIsBusy(false)
    }
  }

  async function applyFormat() {
    if (!templateFile || !thesisFile) return
    setIsBusy(true)
    setStatus('正在生成格式化论文')

    const formData = new FormData()
    formData.append('template', templateFile)
    formData.append('thesis', thesisFile)

    try {
      const response = await fetch('/api/apply', {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) {
        const data = await response.json()
        throw new Error(data.error || '格式化失败')
      }

      const blob = await response.blob()
      const url = URL.createObjectURL(blob)
      const anchor = document.createElement('a')
      anchor.href = url
      anchor.download = 'formatted-thesis.docx'
      anchor.click()
      URL.revokeObjectURL(url)
      setStatus('格式化论文已生成')
    } catch (error) {
      setStatus(error instanceof Error ? error.message : '格式化失败')
    } finally {
      setIsBusy(false)
    }
  }

  return (
    <main className="workspace">
      <header className="topbar">
        <div>
          <p className="eyebrow">本科论文格式助手</p>
          <h1>用学校模板整理你的论文格式</h1>
        </div>
        <span className="status">{status}</span>
      </header>

      <section className="layout">
        <div className="panel upload-panel">
          <div className="section-heading">
            <h2>文件导入</h2>
            <p>先上传学校官方模板，再上传自己的论文。</p>
          </div>

          <FilePicker
            id="template"
            label="学校模板"
            hint="建议使用学院给出的最终版 Word 模板"
            file={templateFile}
            onChange={(file) => {
              setTemplateFile(file)
              setProfile(null)
              setStatus(file ? '模板已选择，可以开始识别' : '等待导入学校模板')
            }}
          />

          <FilePicker
            id="thesis"
            label="我的论文"
            hint="上传需要套格式的正文 .docx"
            file={thesisFile}
            onChange={(file) => {
              setThesisFile(file)
              setStatus(file ? '论文已选择，可以生成格式化文件' : '等待导入论文')
            }}
          />

          <div className="actions">
            <button type="button" onClick={analyzeTemplate} disabled={!templateFile || isBusy}>
              识别模板
            </button>
            <button type="button" className="primary" onClick={applyFormat} disabled={!canApply || isBusy}>
              生成论文
            </button>
          </div>
        </div>

        <div className="panel profile-panel">
          <div className="section-heading">
            <h2>模板识别</h2>
            <p>系统会读取页面设置、正文样式和标题样式。</p>
          </div>

          {profile ? (
            <div className="profile-grid">
              <div>
                <span>页边距</span>
                <strong>
                  上 {profile.page.top_margin_cm ?? '-'} / 下 {profile.page.bottom_margin_cm ?? '-'} cm
                </strong>
                <small>
                  左 {profile.page.left_margin_cm ?? '-'} / 右 {profile.page.right_margin_cm ?? '-'} cm
                </small>
              </div>
              <div>
                <span>正文</span>
                <strong>{profile.body_style?.font_name || profile.body_style?.name || '未识别'}</strong>
                <small>{profile.body_style?.font_size_pt ?? '-'} pt</small>
              </div>
              <div>
                <span>标题样式</span>
                <strong>{Object.keys(profile.heading_styles).length} 级</strong>
                <small>{profile.paragraph_style_count} 个段落样式</small>
              </div>
              <div className="wide">
                <span>样例标题</span>
                <strong>{profile.sample_headings[0] || '模板中未发现标题样例'}</strong>
                <small>后续可扩展为更完整的格式报告</small>
              </div>
            </div>
          ) : (
            <div className="empty-state">
              <strong>尚未识别模板</strong>
              <p>上传学校模板后点击“识别模板”。</p>
            </div>
          )}
        </div>
      </section>
    </main>
  )
}

export default App
