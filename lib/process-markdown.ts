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
  
  // Unwrap paragraphs inside .content-columns divs to allow CSS columns to work properly
  // This handles cases where remark wraps content in <p> tags inside the div
  // The regex handles optional whitespace and paragraph attributes
  contentHtml = contentHtml.replace(
    /<div class="content-columns">\s*<p[^>]*>(.*?)<\/p>\s*<\/div>/gs,
    (match, content) => {
      return `<div class="content-columns">${content}</div>`
    }
  )
  
  return {
    frontmatter: data,
    content: contentHtml,
  }
}

