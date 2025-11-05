# KVSHVL - Official Website

> "Memento Mori, Amor Fati." — Marcus Aurelius

**Live Site:** [https://kvshvl.in](https://kvshvl.in) | [https://kushalsamant.github.io](https://kushalsamant.github.io)

A professional portfolio, architecture showcase, and enterprise SaaS business platform built with Jekyll and hosted on GitHub Pages. This repository contains the complete website for Kushal Dhananjay Samant, featuring an extensive project portfolio, 296 anthology blog posts, and enterprise-grade legal documentation.

---

## 📋 Key Documentation

This repository includes comprehensive documentation for different aspects of the website:

### [📄 IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)
Complete overview of the enterprise-grade legal documentation implementation (November 5, 2025):
- Terms of Service (743 lines, 27 sections)
- Privacy Policy (910 lines, 20 sections) - GDPR, CCPA, Indian IT Act compliant
- Cancellation & Refund Policy (633 lines, 16 sections)
- Stripe business integration instructions
- Multi-jurisdiction compliance coverage

### [🎨 SCSS_IMPLEMENTATION_GUIDE.md](SCSS_IMPLEMENTATION_GUIDE.md)
Modern architecture portfolio styling guide:
- SCSS structure and organization
- Custom theme based on jekyll-theme-minimal
- Typography system (Noto Sans family)
- Responsive design implementation
- Color schemes and design tokens

### [✅ WEBSITE_VALIDATION_REPORT.md](WEBSITE_VALIDATION_REPORT.md)
Comprehensive validation and production readiness report:
- Content audit results (325+ files validated)
- Navigation and UX testing
- Legal documentation verification
- Business information consistency check
- Technical implementation validation
- **Status: Production Ready (100%)**

---

## 🌟 Features

- **Static Site Architecture** - Built with Jekyll for speed, security, and reliability
- **Extensive Portfolio** - 142+ architecture and design projects documented
- **Rich Content** - 296 anthology blog posts covering various topics
- **Enterprise Legal Documentation** - GDPR, CCPA, and Indian IT Act compliant policies
- **Professional Services Platform** - Custom SaaS development, consulting, and products
- **Integrated Booking** - Setmore consultation scheduling
- **Analytics Integration** - Google Analytics 4 and Tag Manager
- **SEO Optimized** - Proper meta tags, structured data, and sitemap
- **Mobile Responsive** - Optimized for all device sizes
- **Fast Loading** - Static HTML generation for optimal performance

---

## 📁 Repository Structure

```
kushalsamant.github.io/
├── _config.yml                          # Jekyll configuration
├── _layouts/                            # HTML layout templates
│   ├── default.html                     # Main site layout
│   └── post.html                        # Blog post layout
├── _sass/                               # SCSS stylesheets
│   ├── fonts.scss                       # Typography definitions
│   ├── jekyll-theme-minimal-modern-architecture.scss
│   └── rouge-github.scss                # Code syntax highlighting
├── _includes/                           # Reusable components
│   └── youtube_embed.html
├── assets/                              # Static assets
│   ├── css/                            # Compiled CSS
│   ├── fonts/                          # Noto Sans font family
│   ├── img/                            # Images (114 files)
│   └── js/                             # JavaScript files
├── anthology/                           # 296 blog posts
├── projects/                            # Portfolio project pages
├── marketing/                           # SEO and marketing
│   ├── rss.xml                         # RSS feed
│   └── sitemap/                        # XML sitemaps (1144 files)
├── dotgithub/workflows/                 # GitHub Actions CI/CD
│   ├── update_rss.yml
│   └── update_sitemap.yml
│
├── Core Pages:
├── index.md                            # Homepage (SVMVNT)
├── about.md                            # Professional biography
├── people.md                           # Acknowledgments (136 people)
├── projects.md                         # Portfolio index
├── anthology.md                        # Blog index
├── support.md                          # Business contact & services
├── contact.md                          # Personal contact page
│
├── Legal Documentation:
├── termsofservice.md                   # Terms of Service (743 lines)
├── privacypolicy.md                    # Privacy Policy (910 lines)
├── cancellationandrefundpolicy.md      # Refund Policy (633 lines)
│
├── Repository Documentation:
├── README.md                           # This file
├── IMPLEMENTATION_SUMMARY.md           # Legal docs implementation
├── SCSS_IMPLEMENTATION_GUIDE.md        # Styling guide
├── WEBSITE_VALIDATION_REPORT.md        # Validation report
├── STRIPE_BUSINESS_INFORMATION.md      # Stripe setup guide
│
└── Configuration Files:
    ├── CNAME                           # Custom domain (kvshvl.in)
    ├── Gemfile                         # Ruby dependencies
    ├── jekyll-theme-minimal.gemspec    # Theme specification
    └── LICENSE                         # License information
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Static Site Generator** | [Jekyll](https://jekyllrb.com/) 4.x |
| **Hosting** | [GitHub Pages](https://pages.github.com/) |
| **Domain** | kvshvl.in (custom domain) |
| **Styling** | SCSS/CSS (custom minimal theme) |
| **Typography** | Noto Sans font family |
| **Analytics** | Google Analytics 4 (G-0LNSC1VBGQ) |
| **Tag Management** | Google Tag Manager (GTM-KXDZLM4W) |
| **Booking System** | [Setmore](https://kvshvl.setmore.com) |
| **CI/CD** | GitHub Actions (RSS, sitemap generation) |
| **Version Control** | Git / GitHub |
| **Content Format** | Markdown |

---

## 🚀 Getting Started

### Prerequisites

- Ruby 2.7+ ([Install Ruby](https://www.ruby-lang.org/en/documentation/installation/))
- Bundler (`gem install bundler`)
- Git

### Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/kushalsamant/kushalsamant.github.io.git
   cd kushalsamant.github.io
   ```

2. **Install dependencies:**
   ```bash
   bundle install
   ```

3. **Run the development server:**
   ```bash
   bundle exec jekyll serve
   ```

4. **Access the site locally:**
   ```
   http://localhost:4000
   ```

5. **Build for production:**
   ```bash
   bundle exec jekyll build
   ```
   Output will be in the `_site/` directory.

### Making Changes

- **Content:** Edit markdown files (`.md`) in the root or respective directories
- **Layouts:** Modify HTML templates in `_layouts/`
- **Styles:** Update SCSS files in `_sass/` (see [SCSS_IMPLEMENTATION_GUIDE.md](SCSS_IMPLEMENTATION_GUIDE.md))
- **Configuration:** Edit `_config.yml` for site-wide settings

---

## 📄 Key Pages

### Main Navigation
- **[Home](https://kvshvl.in)** - SVMVNT introduction and philosophy
- **[About](https://kvshvl.in/about.html)** - Professional biography and career timeline (2006-2024)
- **[People](https://kvshvl.in/people.html)** - Acknowledgments of 136 mentors and collaborators
- **[Projects](https://kvshvl.in/projects.html)** - Portfolio of 142+ architecture and design projects
- **[Get in Touch](https://kvshvl.in/support.html)** - Business services and contact information

### Content Collections
- **[Anthology](https://kvshvl.in/anthology.html)** - Index of 296 blog posts on architecture, creativity, life, and technology

### Legal Pages
- **[Terms of Service](https://kvshvl.in/termsofservice.html)** - Comprehensive service terms (27 sections)
- **[Privacy Policy](https://kvshvl.in/privacypolicy.html)** - GDPR/CCPA compliant privacy policy (20 sections)
- **[Cancellation & Refund Policy](https://kvshvl.in/cancellationandrefundpolicy.html)** - Detailed refund terms (16 sections)

---

## 💼 Business Information

**Business Name:** Kushal Dhananjay Samant  
**Industry:** Software as a Service (SaaS), Architecture, Design

### Services Offered
- **Custom SaaS Development** - Full-stack application development, cloud solutions, API integrations
- **SaaS Product Subscriptions** - Proprietary software platforms (monthly/annual plans)
- **Technical Consulting** - Architecture planning, technology selection, digital transformation
- **Free Initial Consultations** - 30-60 minute meetings via [Setmore](https://kvshvl.setmore.com)

### Contact Information
- **Email:** writetokushaldsamant@gmail.com
- **Phone:** +91 87796 32310
- **Support Hours:** Monday–Saturday, 10:00 AM – 8:00 PM IST
- **Book Consultation:** [kvshvl.setmore.com](https://kvshvl.setmore.com)

### Registered Address
Kushal Dhananjay Samant  
H.No. 2337, "Visava"  
Swami Samarth Nagar, Near Dattanagar  
Kavilgaon, Nerur  
Kudal – 416520, Taluka Kudal  
District Sindhudurg, Maharashtra, India

---

## 🔒 Compliance & Legal

This website and business operations comply with international data protection and consumer protection standards:

### Data Protection
- ✅ **GDPR** (European Union) - Full user rights implementation
- ✅ **CCPA/CPRA** (California) - Complete consumer rights coverage
- ✅ **Indian IT Act 2000** - SPDI Rules and CERT-In compliance
- ✅ **Consumer Protection Act 2019** (India)

### Security Standards
- ✅ **SOC 2 Type II** - Security and availability commitments
- ✅ **ISO 27001** - Information security management practices
- ✅ **HIPAA** - Available for healthcare projects (with BAA)

### Service Level Agreements
- **SLA Uptime Target:** 99.9% monthly
- **Support Response Times:**
  - Critical: 2 hours
  - High: 8 business hours
  - Medium: 24 business hours
  - Low: 48 business hours
- **Refund Processing:** 14 business days

---

## 📊 Content Statistics

| Metric | Count |
|--------|-------|
| **Blog Posts** | 296 |
| **Portfolio Projects** | 142+ |
| **People Acknowledged** | 136 |
| **Legal Document Lines** | 2,286 (across 3 files) |
| **Total Markdown Files** | 325+ |
| **Images** | 114 |
| **Font Files** | 20 |
| **Sitemap Entries** | 1,144 |

---

## 🎯 Notable Achievements

- **GitHub Archive Program** (2020) - Repository selected for Arctic Code Vault
- **WikiHouse / BOM Chapter** (2015) - Founded Mumbai chapter of The WikiHouse Project
- **Published by MAO & FAP** (2016) - GRÜHAM project featured by Museum of Architecture and Design
- **Airbnb Superhost** (2017) - Top-rated hospitality host
- **Top Medium Writer** (2017) - Featured writer on multiple topics
- **University of Westminster Design Trophy** - Shortlisted at International Rank No. 4
- **NASA Design Competition** - Shortlisted for 5 consecutive years
- **Assistant Professor** (2022-2023) - Dr. D. Y. Patil School of Architecture, Navi Mumbai

---

## 🤝 Contributing

This is a personal website repository. While direct contributions are not accepted, feedback and suggestions are always welcome.

### Reporting Issues
If you find broken links, typos, or technical issues:
1. Open an issue on [GitHub Issues](https://github.com/kushalsamant/kushalsamant.github.io/issues)
2. Or contact via email: writetokushaldsamant@gmail.com

### Collaboration Opportunities
For project collaborations, consulting, or partnership inquiries:
- **Book a consultation:** [kvshvl.setmore.com](https://kvshvl.setmore.com)
- **Email:** writetokushaldsamant@gmail.com
- **LinkedIn:** [linkedin.com/in/kvshvl](https://www.linkedin.com/in/kvshvl)

---

## 📜 License & Copyright

**Content & Intellectual Property:**  
© Kushal Dhananjay Samant  
This website and its content are the intellectual property of Architect Kushal Dhananjay Samant under the **Architect's Act, 1972 of India**. Unauthorized use is an offense.

**Code & Theme:**  
Based on [jekyll-theme-minimal](https://github.com/pages-themes/minimal) with extensive custom modifications.

**Third-Party Assets:**
- Font: Noto Sans (Google Fonts) - [Apache License 2.0](https://fonts.google.com/noto/license)
- Icons and images: © respective owners

---

## 🙏 Acknowledgments

This website represents years of work, learning, and collaboration. Special thanks to:

- **136 individuals** acknowledged in [people.md](people.md) who taught things that couldn't be learned otherwise
- The **Jekyll community** for creating an excellent static site generator
- **GitHub Pages** for free, reliable hosting
- **Open source contributors** whose tools and libraries made this possible

For the complete list of collaborators, mentors, and inspirations, see the [People page](https://kvshvl.in/people.html).

---

## 🔗 Connect

### Professional Networks
- **LinkedIn:** [linkedin.com/in/kvshvl](https://www.linkedin.com/in/kvshvl)
- **GitHub:** [github.com/kushalsamant](https://github.com/kushalsamant)
- **GitHub Sponsors:** [github.com/sponsors/kushalsamant](https://github.com/sponsors/kushalsamant)

### Creative Portfolios
- **Behance:** [behance.net/kvshvl](https://www.behance.net/kvshvl)
- **Adobe Stock:** [stock.adobe.com/contributor/212199501/KVSHVL](https://stock.adobe.com/contributor/212199501/KVSHVL)
- **Alamy:** [alamy.com/portfolio/kvshvl](https://www.alamy.com/portfolio/kvshvl)
- **Shutterstock:** [shutterstock.com/g/kvshvl](https://www.shutterstock.com/g/kvshvl)
- **Unsplash:** [@kvshvl](https://unsplash.com/@kvshvl)
- **Sketchfab:** [SHLVNG Project](https://www.sketchfab.com/3d-models/shelving-complete-cutting-files-guide-135b548e7c5e4b28a0aae1777c99840e)

### Social Media
- **Instagram:** [@kvshvl](https://www.instagram.com/kvshvl)
- **Twitter:** [@kvshvl_](https://twitter.com/kvshvl_)
- **Pinterest:** [in.pinterest.com/kvshvl](https://in.pinterest.com/kvshvl)

### Content & Writing
- **Medium:** [kvshvl.medium.com](https://kvshvl.medium.com)
- **YouTube:** [@kvshvl](https://www.youtube.com/@kvshvl/videos)
- **SoundCloud:** [soundcloud.com/kvshvl](https://soundcloud.com/kvshvl)
- **Twitch:** [twitch.tv/kvshvl](https://twitch.tv/kvshvl)

### E-Commerce & Merchandise
- **Geometry Store:** [geometry.printify.com](https://geometry.printify.com)
- **Gumroad:** [kvshvl.gumroad.com](https://kvshvl.gumroad.com)
- **Shopify:** [311290.myshopify.com](https://311290.myshopify.com)
- **Threadless:** [kvshvl.threadless.com](https://kvshvl.threadless.com)
- **Spoonflower:** [spoonflower.com/profiles/geometry](https://www.spoonflower.com/profiles/geometry?sub_action=shop)

### Support & Community
- **Patreon:** [patreon.com/c/kvshvl](https://www.patreon.com/c/kvshvl)
- **Fiverr:** [Professional Services](http://www.fiverr.com/s/2Kqy7Ve)
- **Hacker News:** [news.ycombinator.com/user?id=kvshvl](https://news.ycombinator.com/user?id=kvshvl)
- **Airbnb:** [Profile](https://www.airbnb.co.in/users/show/21563871)

---

## 📞 Schedule a Consultation

Interested in working together? Book a **free 1:1 consultation** to discuss your project:

**[📅 Book a Meeting on Setmore](https://kvshvl.setmore.com)**

- Duration: 30-60 minutes
- Format: Video conference or phone call
- No payment required, no commitment necessary
- Discuss your needs, project scope, and next steps

---

## 📝 Additional Resources

- **[STRIPE_BUSINESS_INFORMATION.md](STRIPE_BUSINESS_INFORMATION.md)** - Stripe payment integration setup
- **[export.xml](export.xml)** - Content backup and export file
- **GitHub Actions Workflows:**
  - [update_rss.yml](dotgithub/workflows/update_rss.yml) - Automated RSS feed generation
  - [update_sitemap.yml](dotgithub/workflows/update_sitemap.yml) - Automated sitemap updates

---

## 🔄 Recent Updates

**November 5, 2025:**
- ✅ Comprehensive legal documentation implementation
- ✅ Terms of Service (743 lines, 27 sections)
- ✅ Privacy Policy (910 lines, 20 sections) - GDPR/CCPA compliant
- ✅ Cancellation & Refund Policy (633 lines, 16 sections)
- ✅ Complete website validation (Production Ready status)
- ✅ Enterprise-grade SaaS business platform ready

**2024:**
- ✅ Launched Geometry merchandising venture
- ✅ Developed ASK Daily Research tool (open-source AI platform)

**2020:**
- ✅ Repository selected for GitHub Archive Program Arctic Code Vault

---

<p align="center">
  <strong>Built with ❤️ by <a href="https://kvshvl.in">Kushal Dhananjay Samant</a></strong><br>
  <em>Architect | Developer | Creator</em>
</p>

<p align="center">
  <a href="https://kvshvl.in">Website</a> •
  <a href="https://kvshvl.setmore.com">Book Consultation</a> •
  <a href="https://www.linkedin.com/in/kvshvl">LinkedIn</a> •
  <a href="https://github.com/kushalsamant">GitHub</a>
</p>

