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
  
  const processedContent = await remark()
    .use(remarkGfm)
    .use(remarkHtml, { sanitize: false })
    .process(content)
  
  const contentHtml = processedContent.toString()
  
  return {
    frontmatter: data,
    content: contentHtml,
  }
}

