import type { Metadata } from 'next'
import { Card } from '@kushalsamant/design-template'

export const metadata: Metadata = {
  title: 'Links | KVSHVL',
  description: 'Connect with Kushal Samant across professional networks, portfolio platforms, social media, and e-commerce stores.',
}

export default function LinksPage() {
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: 'https://kvshvl.in',
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Links',
        item: 'https://kvshvl.in/links',
      },
    ],
  }

  const linkCategories = [
    {
      title: 'Professional',
      links: [
        { name: 'LinkedIn', url: 'https://www.linkedin.com/in/kvshvl', description: 'Professional network and career updates' },
        { name: 'GitHub', url: 'https://github.com/kushalsamant', description: 'Open source projects and code repositories' },
        { name: 'GitHub Sponsors', url: 'https://github.com/sponsors/kushalsamant', description: 'Support open source development' },
      ],
    },
    {
      title: 'Portfolio',
      links: [
        { name: 'Behance', url: 'https://www.behance.net/kvshvl', description: 'Design portfolio and creative projects' },
        { name: 'Adobe Stock', url: 'https://stock.adobe.com/contributor/212199501/KVSHVL', description: 'Stock photography and design assets' },
        { name: 'Alamy', url: 'https://www.alamy.com/portfolio/kvshvl', description: 'Stock photography portfolio' },
        { name: 'Shutterstock', url: 'https://www.shutterstock.com/g/kvshvl', description: 'Stock images and creative content' },
        { name: 'Unsplash', url: 'https://unsplash.com/@kvshvl', description: 'Free high-resolution photography' },
      ],
    },
    {
      title: 'Social',
      links: [
        { name: 'Instagram', url: 'https://www.instagram.com/kvshvl', description: 'Visual storytelling and design work' },
        { name: 'Twitter', url: 'https://twitter.com/kvshvl_', description: 'Thoughts on architecture, design, and technology' },
        { name: 'Medium', url: 'https://kvshvl.medium.com', description: 'Essays and articles on design and architecture' },
        { name: 'YouTube', url: 'https://www.youtube.com/@kvshvl/videos', description: 'Video content and tutorials' },
      ],
    },
    {
      title: 'E-Commerce',
      links: [
        { name: 'Geometry Store', url: 'https://geometry.printify.com', description: 'Geometric design products and prints' },
        { name: 'Gumroad', url: 'https://kvshvl.gumroad.com', description: 'Digital products and design resources' },
        { name: 'Threadless', url: 'https://kvshvl.threadless.com', description: 'Designer apparel and merchandise' },
      ],
    },
  ]

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />
      <main style={{ padding: 'var(--space-xl) var(--space-md)', maxWidth: 'var(--container-max-width)', margin: '0 auto' }}>
        <article className="fade-in">
        <section className="hero" aria-labelledby="links-title">
          <h1 id="links-title" className="hero-title">Links</h1>
          <p className="hero-subtitle">
            Connect with me across professional networks, portfolio platforms, social media, and e-commerce stores.
          </p>
        </section>

        {linkCategories.map((category, categoryIndex) => (
          <section key={category.title} className="section" aria-labelledby={`${category.title.toLowerCase()}-title`}>
            <h2 id={`${category.title.toLowerCase()}-title`} className="section-title">
              {category.title}
            </h2>
            
            <div className="grid grid-2">
              {category.links.map((link, linkIndex) => (
                <a
                  key={link.name}
                  href={link.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ display: 'block', textDecoration: 'none', color: 'inherit', cursor: 'pointer' }}
                >
                  <Card
                    variant="elevated"
                    className="slide-up"
                  >
                    <div>
                      <h3 style={{ 
                        fontSize: 'var(--font-size-xl)', 
                        marginBottom: 'var(--space-sm)',
                      }}>
                        {link.name}
                      </h3>
                      <p style={{ 
                        color: 'var(--color-text-secondary)',
                        margin: 0,
                        lineHeight: 'var(--line-height-relaxed)',
                      }}>
                        {link.description}
                      </p>
                      <p style={{ 
                        fontSize: 'var(--font-size-sm)',
                        color: 'var(--color-text-muted)',
                        marginTop: 'var(--space-sm)',
                        margin: 0,
                      }}>
                        {new URL(link.url).hostname.replace('www.', '')} →
                      </p>
                    </div>
                  </Card>
                </a>
              ))}
            </div>
          </section>
        ))}
      </article>
    </main>
    </>
  )
}

