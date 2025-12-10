#!/usr/bin/env tsx
/**
 * Dynamic Sitemap Generator for KVSHVL Platform
 * Generates sitemap.xml and sitemap index dynamically
 * Run: npx tsx scripts/generate-sitemap.ts
 */

import { writeFileSync } from 'fs';
import { join } from 'path';
import { readdirSync, statSync } from 'fs';

const BASE_URL = 'https://kvshvl.in';
const OUTPUT_DIR = join(process.cwd(), 'public');

interface SitemapEntry {
  url: string;
  lastMod: Date;
  changeFreq: 'always' | 'hourly' | 'daily' | 'weekly' | 'monthly' | 'yearly' | 'never';
  priority: number;
}

// Static routes
const staticRoutes: SitemapEntry[] = [
  { url: '/', lastMod: new Date(), changeFreq: 'daily', priority: 1.0 },
  { url: '/history', lastMod: new Date(), changeFreq: 'monthly', priority: 0.8 },
  { url: '/projects', lastMod: new Date(), changeFreq: 'monthly', priority: 0.8 },
  { url: '/account', lastMod: new Date(), changeFreq: 'daily', priority: 0.7 },
  { url: '/subscribe', lastMod: new Date(), changeFreq: 'weekly', priority: 0.9 },
  { url: '/getintouch', lastMod: new Date(), changeFreq: 'monthly', priority: 0.6 },
  { url: '/privacypolicy', lastMod: new Date(), changeFreq: 'yearly', priority: 0.5 },
  { url: '/termsofservice', lastMod: new Date(), changeFreq: 'yearly', priority: 0.5 },
  { url: '/cancellationrefund', lastMod: new Date(), changeFreq: 'yearly', priority: 0.5 },
];

// Get all anthology content
function getAnthologyRoutes(): SitemapEntry[] {
  const anthologyDir = join(process.cwd(), 'content', 'anthology');
  const routes: SitemapEntry[] = [];
  
  try {
    const files = readdirSync(anthologyDir);
    for (const file of files) {
      if (file.endsWith('.md')) {
        const slug = file.replace('.md', '');
        const filePath = join(anthologyDir, file);
        const stats = statSync(filePath);
        
        routes.push({
          url: `/anthology/${slug}`,
          lastMod: stats.mtime,
          changeFreq: 'monthly',
          priority: 0.7,
        });
      }
    }
  } catch (error) {
    console.error('Error reading anthology directory:', error);
  }
  
  return routes;
}

// Get all project routes
function getProjectRoutes(): SitemapEntry[] {
  const projectsDir = join(process.cwd(), 'content', 'projects');
  const routes: SitemapEntry[] = [];
  
  try {
    const files = readdirSync(projectsDir);
    for (const file of files) {
      if (file.endsWith('.md')) {
        const slug = file.replace('.md', '');
        const filePath = join(projectsDir, file);
        const stats = statSync(filePath);
        
        routes.push({
          url: `/projects/${slug}`,
          lastMod: stats.mtime,
          changeFreq: 'monthly',
          priority: 0.8,
        });
      }
    }
  } catch (error) {
    console.error('Error reading projects directory:', error);
  }
  
  return routes;
}

// Generate XML sitemap
function generateSitemapXML(entries: SitemapEntry[]): string {
  const urls = entries.map(entry => `
  <url>
    <loc>${BASE_URL}${entry.url}</loc>
    <lastmod>${entry.lastMod.toISOString()}</lastmod>
    <changefreq>${entry.changeFreq}</changefreq>
    <priority>${entry.priority}</priority>
  </url>`).join('');
  
  return `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls}
</urlset>`;
}

// Main execution
async function main() {
  console.log('Generating sitemap...');
  
  // Collect all routes
  const allRoutes = [
    ...staticRoutes,
    ...getAnthologyRoutes(),
    ...getProjectRoutes(),
  ];
  
  console.log(`Found ${allRoutes.length} routes`);
  
  // Generate sitemap
  const sitemapXML = generateSitemapXML(allRoutes);
  
  // Write sitemap.xml
  const sitemapPath = join(OUTPUT_DIR, 'sitemap.xml');
  writeFileSync(sitemapPath, sitemapXML);
  console.log(`✅ Sitemap generated: ${sitemapPath}`);
  
  // Generate robots.txt
  const robotsTxt = `# Robots.txt for kvshvl.in
User-agent: *
Allow: /
Disallow: /api/
Disallow: /account
Disallow: /admin

Sitemap: ${BASE_URL}/sitemap.xml`;
  
  const robotsPath = join(OUTPUT_DIR, 'robots.txt');
  writeFileSync(robotsPath, robotsTxt);
  console.log(`✅ Robots.txt generated: ${robotsPath}`);
  
  console.log('Sitemap generation complete!');
}

main().catch(console.error);

