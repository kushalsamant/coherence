# Migrate to Self-Hosted Oracle (₹0/month)

## Goal

Get Reframe AI running on Oracle Cloud Free Tier with local Ollama models, PostgreSQL, and Redis. Achieve ₹0/month operating costs and validate quality before building anything else.

---

## 📋 PHASE 1: Oracle Cloud Setup (2 hours)

### 1.1 Create Oracle Account

1. Visit cloud.oracle.com/free
2. Sign up with your email
3. Choose region: **ap-mumbai-1** (closest to Navi Mumbai)
4. Verify phone + credit card (won't be charged)

### 1.2 Launch Always Free Instance

**Configuration:**

- **Shape:** VM.Standard.A1.Flex (ARM-based)
- **OCPUs:** 4 (use all 4 free cores)
- **RAM:** 24 GB (use all free RAM)
- **OS:** Ubuntu 22.04 LTS
- **Boot Volume:** 200 GB (maximum free)
- **Public IP:** Assign one (free)

### 1.3 Security Setup

```bash
# SSH into server
ssh ubuntu@<your-oracle-ip>

# Update system
sudo apt update && sudo apt upgrade -y

# Configure firewall
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

---

## 🐳 PHASE 2: Install Docker (30 min)

```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify
docker --version
docker-compose --version
```

---

## 🤖 PHASE 3: Setup Ollama & Models (1 hour)

### 3.1 Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 3.2 Download Best Models

Based on your D:\models\ collection, download these 3:

```bash
# Best quality (for paid users)
ollama pull nous-hermes2    # ~4.1 GB

# Fastest (for free tier)
ollama pull phi             # ~1.6 GB

# Balanced (general use)
ollama pull openchat        # ~4.1 GB
```

**Total:** ~10 GB (fits easily in 200 GB)

### 3.3 Test Models

```bash
# Test quality
ollama run nous-hermes2 "Rewrite professionally: hey what's up?"

# Test speed
time ollama run phi "Make this conversational: The data indicates significant improvement"

# Test balanced
ollama run openchat "Write academically: Cool AI stuff"
```

**Pick best one for production based on:**

- Speed (tokens/sec)
- Quality (does it sound human?)
- Resource usage (RAM)

---

## 🗄️ PHASE 4: Create docker-compose.yml (1 hour)

**File:** `docker-compose.yml` (in projects repo)

```yaml
version: '3.8'

services:
  # Next.js Application
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
      - DATABASE_URL=postgresql://reframe:${DB_PASSWORD}@postgres:5432/reframe_db
      - REDIS_URL=redis://redis:6379
      - OLLAMA_URL=http://host.docker.internal:11434
      - NEXTAUTH_URL=https://projects.kvshvl.in
      - NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
      - GOOGLE_CLIENT_ID=${GOOGLE_CLIENT_ID}
      - GOOGLE_CLIENT_SECRET=${GOOGLE_CLIENT_SECRET}
      - STRIPE_PUBLISHABLE_KEY=${STRIPE_PUBLISHABLE_KEY}
      - STRIPE_SECRET_KEY=${STRIPE_SECRET_KEY}
      - STRIPE_WEBHOOK_SECRET=${STRIPE_WEBHOOK_SECRET}
    depends_on:
      - postgres
      - redis
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    environment:
      - POSTGRES_USER=reframe
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=reframe_db
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    restart: unless-stopped

  # Redis Cache
  redis:
    image: redis:7-alpine
    command: redis-server --appendonly yes
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    restart: unless-stopped

  # Caddy Reverse Proxy (Auto SSL)
  caddy:
    image: caddy:latest
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    restart: unless-stopped

volumes:
  postgres_data:
  redis_data:
  caddy_data:
  caddy_config:
```

**File:** `Caddyfile`

```
projects.kvshvl.in {
    reverse_proxy app:3000
}
```

**File:** `Dockerfile`

```dockerfile
FROM node:20-alpine AS base

# Install dependencies
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Build application
FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

# Production image
FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT 3000

CMD ["node", "server.js"]
```

**File:** `next.config.js` (update)

```js
module.exports = {
  output: 'standalone', // Critical for Docker
  // ... rest of config
};
```

---

## 🔧 PHASE 5: Adapt Code for Self-Hosted (3 hours)

### 5.1 Replace Groq with Ollama

**File:** `lib/ai.ts` (new file, replaces groq.ts)

```typescript
export async function generateText(
  prompt: string,
  model: string = "nous-hermes2"
): Promise<string> {
  const ollamaUrl = process.env.OLLAMA_URL || "http://localhost:11434";
  
  const response = await fetch(`${ollamaUrl}/api/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: model,
      prompt: prompt,
      stream: false,
      options: {
        temperature: 0.7,
        num_predict: 2000,
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Ollama error: ${response.statusText}`);
  }

  const data = await response.json();
  return data.response;
}
```

### 5.2 Update Reframe API

**File:** `app/api/reframe/route.ts`

```typescript
// Remove this
import { groq } from "@/lib/groq";

// Add this
import { generateText } from "@/lib/ai";

// Replace this
const completion = await groq.chat.completions.create({...});
const reframedText = completion.choices[0]?.message?.content;

// With this
const reframedText = await generateText(fullPrompt);
```

### 5.3 Replace Upstash with PostgreSQL + Redis

**File:** `lib/database.ts` (new)

```typescript
import { Pool } from 'pg';
import { createClient } from 'redis';

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
});

const redis = createClient({
  url: process.env.REDIS_URL,
});

redis.connect();

export { pool, redis };
```

**Install dependencies:**

```bash
npm install pg redis
```

### 5.4 Create Schema

**File:** `scripts/init-db.sql`

```sql
CREATE TABLE users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  name TEXT,
  subscription TEXT,
  credits INTEGER DEFAULT 0,
  usage_count INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_email ON users(email);
```

### 5.5 Update All DB Calls

**Pattern:**

```typescript
// Old (Upstash)
const usage = await redis.get(`usage:${userId}:total`);

// New (PostgreSQL)
const result = await pool.query(
  'SELECT usage_count FROM users WHERE id = $1',
  [userId]
);
const usage = result.rows[0]?.usage_count || 0;
```

---

## 🚀 PHASE 6: Deploy to Oracle (2 hours)

### 6.1 Push Code to GitHub

```bash
git add .
git commit -m "Migrate to self-hosted: Ollama + PostgreSQL + Redis"
git push origin main
```

### 6.2 Clone on Oracle

```bash
# On Oracle server
git clone https://github.com/kushalsamant/projects.git
cd projects
```

### 6.3 Create .env File

**File:** `.env.production` (on Oracle)

```env
DB_PASSWORD=your_secure_password
NEXTAUTH_SECRET=your_secret_here
NEXTAUTH_URL=https://projects.kvshvl.in
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
STRIPE_PUBLISHABLE_KEY=pk_live_xxx
STRIPE_SECRET_KEY=sk_live_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
OLLAMA_URL=http://host.docker.internal:11434
```

### 6.4 Deploy

```bash
# Build and start all services
docker-compose up -d

# Check logs
docker-compose logs -f

# Run database migrations
docker exec -it projects-app-1 node scripts/migrate-db.js
```

---

## 🌐 PHASE 7: DNS Configuration (15 min)

### 7.1 Add DNS Record

Go to kvshvl.in DNS settings:

**Add A Record:**

- **Name:** `projects`
- **Type:** A
- **Value:** `<Your Oracle VM IP>`
- **TTL:** 300

### 7.2 Wait for Propagation

```bash
# Test DNS (5-60 minutes)
nslookup projects.kvshvl.in
```

### 7.3 SSL Auto-Provision

Caddy will automatically get Let's Encrypt SSL when DNS resolves.

---

## ✅ PHASE 8: Testing & Validation (2 hours)

### 8.1 Smoke Tests

- [ ] https://projects.kvshvl.in loads
- [ ] Sign in with Google works
- [ ] Free tier counter shows 0/5
- [ ] Text reframing works (test all 6 tones)
- [ ] Generation selector works (test 3 generations)
- [ ] Pricing page loads with currency conversion
- [ ] Stripe checkout works
- [ ] SSL certificate valid

### 8.2 Quality Comparison

**Test same text with:**

1. Current Groq (on Vercel)
2. New Ollama (on Oracle)

**Compare:**

- Speed (response time)
- Quality (human-like output?)
- Consistency (same input = similar outputs?)

**If Ollama quality is <80% of Groq → pick better model or tweak prompts**

### 8.3 Load Testing

```bash
# Simulate 10 concurrent requests
for i in {1..10}; do
  curl -X POST https://projects.kvshvl.in/api/reframe &
done
```

Monitor:

- Response time
- CPU usage
- RAM usage
- Success rate

---

## 🎯 Success Criteria

**Must achieve ALL before building Medium Extension:**

- [ ] projects.kvshvl.in fully functional
- [ ] ₹0 monthly costs (verified - no surprise bills)
- [ ] Ollama quality acceptable (≥80% of Groq quality)
- [ ] Response time acceptable (<10 seconds per request)
- [ ] Free tier counter working (0/5 → 5/5)
- [ ] All 6 tones working
- [ ] All 9 generations working
- [ ] Stripe payments working
- [ ] No errors in production logs
- [ ] Can handle 10 concurrent users

---

## ⏱️ Timeline

| Task | Time |
|------|------|
| Oracle account + VM setup | 2 hrs |
| Install Docker | 30 min |
| Install Ollama + models | 1 hr |
| Code adaptation | 3 hrs |
| docker-compose setup | 1 hr |
| Deploy to Oracle | 2 hrs |
| DNS + SSL | 30 min |
| Testing & validation | 2 hrs |
| **TOTAL** | **12 hours** |

**= 1.5 days of focused work**

---

## 💰 Cost Breakdown

**Before:**

- Vercel: ₹0-2,000/mo
- Upstash: ₹0-1,500/mo
- Groq: ₹500-2,000/mo
- **Total: ₹1,000-5,500/month**

**After:**

- Oracle Free Tier: ₹0
- PostgreSQL: ₹0
- Redis: ₹0
- Ollama: ₹0
- **Total: ₹0/month**

**Annual Savings: ₹12,000-66,000**

---

## 🚫 What We're NOT Doing (Yet)

Deliberately excluded until Oracle works:

- ❌ Medium Chrome Extension
- ❌ SEO optimization
- ❌ Analytics setup
- ❌ Email newsletter
- ❌ Image optimization
- ❌ Ask AI
- ❌ Emoji Mosaic
- ❌ Marketing campaigns

**All come AFTER we prove self-hosted works.**

---

## 🎯 Phase 2 (After Validation)

**IF** Oracle setup works well:

1. Build Medium Extension (2 days)
2. Launch validation campaign
3. Get 50+ interested users
4. **THEN** decide: scale Reframe or pivot

**IF** Oracle has issues (slow, unstable, poor quality):

1. Debug and optimize
2. Consider hybrid (Oracle backend + Vercel frontend)
3. Or stay on current stack but optimize costs

---

## 🔧 Quick Wins to Include

### Delete Duplicate Folders

Clean up repo before deploying:

```bash
rm -rf reframe-ai/        # Old standalone version
rm -rf ask/               # Unrelated Python project
rm -rf emoji-mosaic/      # Unrelated static site
```

### Update Environment Variables

Consolidate all .env files:

- Delete `.env.local` after migration
- Keep `.env.production` only

---

## ✅ Deliverable

**One command deployment:**

```bash
# On Oracle
git pull
docker-compose up -d
```

**Live URL:**

https://projects.kvshvl.in

**Cost:**

₹0/month

**Quality:**

Tested and validated

**Then:**

Build Medium Extension

---

**This is the lean, focused plan. Ready to execute?**

