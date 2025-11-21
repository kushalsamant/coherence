import fs from 'fs'
import path from 'path'
import matter from 'gray-matter'
import { remark } from 'remark'
import remarkHtml from 'remark-html'
import remarkGfm from 'remark-gfm'

export async function getMarkdownContent(filePath: string) {
  const fullPath = path.join(process.cwd(), filePath)
  const fileContents = fs.readFileSync(fullPath, 'utf8')
  const { data, content } = matter(fileContents)
  
  // Pre-process Jekyll image syntax {:width="150"} to HTML attributes
  // Handle both standard markdown images and Jekyll extended syntax
  let processedContent = content.replace(
    /!\[([^\]]*)\]\(([^)]+)\)\{:width="(\d+)"\}/g,
    (match, alt, src, width) => {
      return `<img src="${src}" alt="${alt}" width="${width}" style="max-width: 100%; height: auto; display: block; margin: var(--space-lg) 0;" />`
    }
  )
  
  const result = await remark()
    .use(remarkGfm)
    .use(remarkHtml, { sanitize: false })
    .process(processedContent)
  
  let contentHtml = result.toString()
  
  // Ensure image paths starting with /assets/ are preserved
  contentHtml = contentHtml.replace(
    /src="\/assets\//g,
    'src="/assets/'
  )
  
  return {
    frontmatter: data,
    content: contentHtml,
  }
}

