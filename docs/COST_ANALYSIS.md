# Comprehensive Infrastructure Cost Analysis
## For /sketch2bim, /ask, /reframe, and /kushalsamant.github.io

**Date:** January 2025  
**Currency:** USD (converted from INR where applicable)

---

## Services Inventory

### Currently Used Services:

1. **Vercel** - Frontend hosting (all 4 projects: sketch2bim, ask, reframe, kushalsamant.github.io)
2. **Render** - Backend hosting (sketch2bim, ask)
3. **PostgreSQL** - Database (sketch2bim via Render, ask needs it for payments)
4. **Redis** - Caching (sketch2bim: Render Redis, reframe: Upstash)
5. **Razorpay** - Payments (sketch2bim, ask, reframe)
6. **Groq** - AI inference (ask, reframe)
7. **BunnyCDN** - File storage/CDN (sketch2bim)
8. **Google OAuth** - Authentication (all 4 projects - FREE)

---

## Detailed Cost Breakdown

### 1. VERCEL (Frontend Hosting)
**Used by:** sketch2bim, ask, reframe, kushalsamant.github.io (4 frontends)

**Note:** kushalsamant.github.io uses static export (minimal resource usage)

**Pricing:**
- **Pro Plan:** $20/user/month (minimum 1 user)
- **Free Tier:** Not suitable for production (limited features)

**Included in Pro:**
- 100 GB bandwidth/month
- 1M function invocations/month
- 5,000 image optimizations/month
- Unlimited deployments

**Additional Costs:**
- Extra bandwidth: $0.15/GB beyond 100GB
- Extra function invocations: $0.60 per million
- Extra image optimizations: $0.05 per 1,000

**Estimated Monthly Cost:**
- Base: **$20/month** (1 Pro user covers all 4 projects)
- Additional usage (assume 50GB extra bandwidth): $7.50
- **Total: ~$27.50/month**

---

### 2. RENDER (Backend Hosting)
**Used by:** sketch2bim, ask (2 backends)

#### Web Services:
- **Starter Plan:** $7/month per service
- **Standard Plan:** $25/month per service (if needed)

**Estimated:** 2 services × $7 = **$14/month**

#### PostgreSQL Database:
- **Starter Plan:** $7/month (1GB storage)
- **Standard Plan:** $20/month (10GB storage)

**Used by:** sketch2bim (currently), ask (needs for payments)

**Estimated:** 1 database × $7 = **$7/month** (can share or separate)

#### Redis (via Render):
- **Starter Plan:** $7/month

**Used by:** sketch2bim

**Estimated:** **$7/month**

**Render Total: $14 + $7 + $7 = $28/month**

---

### 3. UPSTASH (Redis for reframe)
**Used by:** reframe

**Pricing:**
- **Free Tier:** 256MB, 500K commands/month
- **Pay-as-you-go:** $0.20 per 100K commands
- **Fixed Plan:** $10/month (250MB, unlimited commands)

**Estimated:** 
- If low usage: **$0/month** (free tier)
- If moderate usage (1M commands): **$2/month**
- If high usage: **$10/month** (fixed plan)

**Estimated: ~$2/month** (assuming moderate usage)

---

### 4. GROQ (AI Inference)
**Used by:** ask, reframe

**Pricing (Llama 3.1 70B):**
- **Input tokens:** $0.59 per 1M tokens
- **Output tokens:** $0.79 per 1M tokens

**Usage Estimates:**

**For /ask:**
- Each research session: ~500 input tokens + ~2,000 output tokens
- 100 sessions/month = 50K input + 200K output tokens
- Cost: (0.05 × $0.59) + (0.2 × $0.79) = $0.03 + $0.16 = **$0.19/month**

**For /reframe:**
- Each reframe: ~1,000 input tokens + ~3,000 output tokens (10K words)
- 1,000 reframes/month = 1M input + 3M output tokens
- Cost: (1 × $0.59) + (3 × $0.79) = $0.59 + $2.37 = **$2.96/month**

**Groq Total: ~$3.15/month** (low usage scenario)

**At scale (10K ask sessions, 10K reframes/month):**
- Ask: $1.90/month
- Reframe: $29.60/month
- **Total: ~$31.50/month**

---

### 5. RAZORPAY (Payments)
**Used by:** sketch2bim, ask, reframe (3 projects)

**Pricing:**
- **Domestic transactions:** 2% per transaction
- **International transactions:** 3% per transaction
- **No setup fees, no monthly fees**

**Cost depends on revenue:**
- ₹1,00,000 revenue = ₹2,000 fees (~$24)
- ₹5,00,000 revenue = ₹10,000 fees (~$120)
- ₹10,00,000 revenue = ₹20,000 fees (~$240)

**Estimated:** Variable based on sales
**Example:** ₹2,00,000/month revenue = **~$48/month** in fees

---

### 6. BUNNYCDN (File Storage & CDN)
**Used by:** sketch2bim

**Pricing:**
- **Storage:** $0.01/GB/month
- **Bandwidth:** 
  - Europe & North America: $0.01/GB
  - Asia & Oceania: $0.03/GB
  - South America: $0.045/GB
  - Africa: $0.06/GB

**Usage Estimates:**
- Storage: 50GB files = $0.50/month
- Bandwidth: 500GB/month (Asia) = $15/month

**Estimated: ~$15.50/month**

---

### 7. GOOGLE OAUTH
**Used by:** All 4 projects

**Pricing:** **FREE** (unlimited)

---

## REPOSITORY-BY-REPOSITORY COST BREAKDOWN

### sketch2bim
**Type:** Full-stack application  
**Services Used:**
- Vercel (frontend hosting) - Shared cost
- Render (backend hosting) - $7/month
- PostgreSQL (via Render) - Shared cost
- Redis (via Render) - $7/month
- Razorpay (payments) - Variable (2% of revenue)
- BunnyCDN (file storage/CDN) - $15.50/month
- Google OAuth - FREE

**Estimated Monthly Cost:**
- Fixed: ~$29.50/month (proportional share of shared services + dedicated services)
- Variable: 2% of revenue via Razorpay

---

### ask
**Type:** Full-stack application  
**Services Used:**
- Vercel (frontend hosting) - Shared cost
- Render (backend hosting) - $7/month
- PostgreSQL (via Render) - Shared cost
- Razorpay (payments) - Variable (2% of revenue)
- Groq (AI inference) - Variable (~$0.19-$1.90/month based on usage)
- Google OAuth - FREE

**Estimated Monthly Cost:**
- Fixed: ~$14/month (proportional share of shared services + dedicated services)
- Variable: 2% of revenue via Razorpay + Groq usage

---

### reframe
**Type:** Frontend-only application (serverless)  
**Services Used:**
- Vercel (frontend hosting) - Shared cost
- Upstash Redis (usage tracking) - $2/month
- Razorpay (payments) - Variable (2% of revenue)
- Groq (AI inference) - Variable (~$2.96-$29.60/month based on usage)
- Google OAuth - FREE

**Estimated Monthly Cost:**
- Fixed: ~$9/month (proportional share of shared services + dedicated services)
- Variable: 2% of revenue via Razorpay + Groq usage

---

### kushalsamant.github.io
**Type:** Static site (Next.js static export)  
**Services Used:**
- Vercel (frontend hosting) - Shared cost
- Google OAuth - FREE (if used)

**Estimated Monthly Cost:**
- Fixed: ~$7/month (proportional share of Vercel Pro plan)
- Variable: $0/month (static site, no backend costs)

**Note:** This is a low-cost static site with minimal resource usage.

---

## TOTAL MONTHLY COST SUMMARY

### Fixed Costs (Infrastructure):
| Service | Cost |
|---------|------|
| Vercel Pro | $27.50 |
| Render (2 web services) | $14.00 |
| Render PostgreSQL | $7.00 |
| Render Redis | $7.00 |
| Upstash Redis | $2.00 |
| BunnyCDN | $15.50 |
| **Subtotal (Fixed)** | **$74.00/month** |

### Variable Costs (Usage-Based):
| Service | Low Usage | Medium Usage | High Usage |
|---------|-----------|--------------|------------|
| Groq AI | $3.15 | $15.00 | $50.00 |
| Razorpay (2% of revenue, all 3 projects) | $36.00 | $180.00 | $720.00 |
| **Subtotal (Variable)** | **$39.15** | **$195.00** | **$770.00** |

### TOTAL MONTHLY COST:
- **Low Usage:** $74.00 + $39.15 = **~$113/month** (~₹9,400)
- **Medium Usage:** $74.00 + $195.00 = **~$269/month** (~₹22,300)
- **High Usage:** $74.00 + $770.00 = **~$844/month** (~₹70,000)

---

## AFFORDABILITY ANALYSIS

### Revenue Needed to Break Even:

**Low Usage Scenario:**
- Fixed costs: $74/month
- Variable costs: $39/month
- **Total: $113/month**
- **Break-even revenue: ~₹9,400/month** (₹113,000/year)

**Medium Usage Scenario:**
- Fixed costs: $74/month
- Variable costs: $195/month
- **Total: $269/month**
- **Break-even revenue: ~₹22,300/month** (₹267,600/year)

**High Usage Scenario:**
- Fixed costs: $74/month
- Variable costs: $770/month
- **Total: $844/month**
- **Break-even revenue: ~₹70,000/month** (₹840,000/year)

### Current Pricing Analysis:

**Unified Pricing (All Projects):**
- **Week:** ₹1,299/week = ₹5,196/month (if used weekly)
- **Month:** ₹3,499/month
- **Year:** ₹29,999/year = ₹2,500/month (best value - 33% savings)

**Note:** All three products (ASK, Reframe, Sketch2BIM) use the same weekly, monthly, and yearly pricing. This unified pricing strategy simplifies customer understanding and makes cross-selling easier.

### Customers Needed to Break Even:

**Medium Usage Scenario ($269/month = ₹22,300):**

**Option 1: Single Product Focus**
- **Sketch2BIM:** 7 monthly subscribers (₹3,499 × 7 = ₹24,493)
- **ASK:** 7 monthly subscribers (₹3,499 × 7 = ₹24,493)
- **Reframe:** 7 monthly subscribers (₹3,499 × 7 = ₹24,493)

**Option 2: Mixed Products (Recommended)**
- **Combined:** 2 Sketch2BIM + 2 ASK + 2 Reframe monthly = ₹6,998 + ₹6,998 + ₹6,998 = ₹20,994
- **Or:** 1 Sketch2BIM + 2 ASK + 3 Reframe monthly = ₹3,499 + ₹6,998 + ₹10,497 = ₹20,994
- **Or:** 3 Sketch2BIM + 1 ASK + 1 Reframe monthly = ₹10,497 + ₹3,499 + ₹3,499 = ₹17,495

**Option 3: Annual Subscriptions (Best Value for Customers)**
- **Combined:** 1 Sketch2BIM + 1 ASK + 1 Reframe annual = ₹2,500 + ₹2,500 + ₹2,500 = ₹7,500/month equivalent
- Need 3 sets = 9 annual customers = ₹22,500/month equivalent

**Note:** Since all products use unified pricing (₹3,499/month or ₹29,999/year), customers can easily understand and compare across products, making cross-selling and upselling more straightforward.

**Conclusion:** With **6-9 paying customers** across all products (monthly or annual), you can cover infrastructure costs. This is very achievable!

---

## COST OPTIMIZATION RECOMMENDATIONS

### 1. **Consolidate Services:**
- Use one Render PostgreSQL for both sketch2bim and ask (save $7/month)
- Consider sharing Upstash Redis if possible

### 2. **Monitor Groq Usage:**
- Implement caching for similar queries
- Set rate limits to prevent abuse
- Current cost is very low, but monitor as usage grows

### 3. **Optimize BunnyCDN:**
- Compress images before upload
- Use CDN caching effectively
- Consider if all files need CDN (some could be direct storage)

### 4. **Payment Gateway:**
- All 3 payment-enabled projects (sketch2bim, ask, reframe) now use Razorpay
- Razorpay offers competitive 2% fees with no per-transaction charges
- Unified payment gateway simplifies management

### 5. **Vercel Optimization:**
- Monitor function invocations across all 4 projects
- Optimize image sizes (especially for kushalsamant.github.io)
- Current $27.50 is reasonable for 4 projects
- kushalsamant.github.io uses static export (minimal resource usage)

---

## SCALING COSTS

### If you reach 100 paying customers:

**Revenue:** ~₹3,50,000/month (~$4,200)
- Razorpay fees (all 3 projects): ₹7,000 (~$84)
- Groq: ~$50 (higher usage)
- **Total variable: ~$134**
- **Total cost: $74 + $134 = $208/month**

**Profit margin: 95%** (very healthy!)

---

## BUSINESS VIABILITY ASSESSMENT

### ✅ **VERDICT: HIGHLY VIABLE BUSINESS**

**Why This Business Model Works:**

1. **Ultra-Low Fixed Costs:** $74/month (~₹6,150) for 4 products is exceptional
   - Most SaaS businesses spend $200-500/month on infrastructure
   - Your cost structure is 3-7x more efficient

2. **Scalable Revenue Model:**
   - **Monthly ARPU (Average Revenue Per User):** ₹3,499/month per product
   - **Annual ARPU:** ₹2,500/month equivalent (better retention)
   - **Break-even:** Only 6-9 customers needed across all products

3. **Excellent Unit Economics:**
   - **Cost per customer:** ~₹680/month (at 9 customers)
   - **Revenue per customer:** ₹3,499/month (monthly) or ₹2,500/month (annual)
   - **Gross margin:** 80-85% (after payment processing)
   - **Infrastructure cost as % of revenue:** <20% at break-even, <5% at scale

4. **Low Risk Profile:**
   - **Zero revenue cost:** Only $74/month (~₹6,150) - very manageable
   - **Variable costs scale with success:** Payment fees only when you make sales
   - **No long-term commitments:** Most services are pay-as-you-go

5. **High Growth Potential:**
   - **At 50 customers:** ₹1,74,950/month revenue, ~₹1,40,000/month profit (80% margin)
   - **At 100 customers:** ₹3,49,900/month revenue, ~₹2,80,000/month profit
   - **At 500 customers:** ₹17,49,500/month revenue, ~₹14,00,000/month profit

### 📊 **REVENUE PROJECTIONS**

**Conservative Scenario (Year 1):**
- Month 1-3: 0 customers (building/launching)
- Month 4-6: 5 customers/month average = ₹17,495/month = ₹1,04,970/quarter
- Month 7-9: 10 customers/month average = ₹34,990/month = ₹2,09,940/quarter
- Month 10-12: 15 customers/month average = ₹52,485/month = ₹3,14,910/quarter
- **Year 1 Total Revenue:** ~₹6,29,820 (~$7,600)
- **Year 1 Infrastructure Cost:** ~$1,356 (~₹1,12,500)
- **Year 1 Net Profit:** ~$6,244 (~₹5,17,320) - **82% margin**

**Moderate Scenario (Year 1):**
- Month 1-3: 0 customers
- Month 4-6: 10 customers/month = ₹34,990/month
- Month 7-9: 20 customers/month = ₹69,980/month
- Month 10-12: 30 customers/month = ₹1,04,970/month
- **Year 1 Total Revenue:** ~₹12,59,640 (~$15,200)
- **Year 1 Net Profit:** ~$13,844 (~₹11,47,140) - **91% margin**

**Optimistic Scenario (Year 1):**
- Month 1-3: 5 customers/month
- Month 4-6: 20 customers/month = ₹69,980/month
- Month 7-9: 40 customers/month = ₹1,39,960/month
- Month 10-12: 60 customers/month = ₹2,09,940/month
- **Year 1 Total Revenue:** ~₹25,19,280 (~$30,400)
- **Year 1 Net Profit:** ~$29,044 (~₹24,06,780) - **95% margin**

### 🎯 **IS THIS BUSINESS USEFUL?**

**YES - Here's Why:**

1. **Market Need:** All three products solve real problems:
   - **Reframe:** AI text humanization (growing market)
   - **ASK:** Daily research automation (time-saving)
   - **Sketch2BIM:** Architectural conversion (niche but valuable)

2. **Competitive Pricing:** Your prices are competitive:
   - Reframe: ₹99-3,499/month (vs competitors at ₹500-5,000/month)
   - ASK: ₹1,299-3,499/month (vs similar tools at ₹2,000-10,000/month)
   - Sketch2BIM: ₹1,299-3,499/month (vs enterprise tools at ₹50,000+/month)

3. **Low Customer Acquisition Cost Potential:**
   - With only 6-9 customers needed to break even, even expensive marketing ($100-200/customer) is viable
   - Word-of-mouth and organic growth can work well at this scale

4. **High Retention Potential:**
   - Annual plans offer 33% savings, encouraging long-term commitment
   - Products solve ongoing needs (not one-time purchases)

5. **Scalability:**
   - Infrastructure costs grow slowly (mostly variable)
   - Can handle 10x growth with minimal infrastructure changes
   - Profit margins improve with scale

### ⚠️ **RISKS & MITIGATION**

**Risk 1: Low Customer Acquisition**
- **Mitigation:** Focus on one product initially, build case studies, use free tier to attract users

**Risk 2: High Churn**
- **Mitigation:** Annual plans lock in customers, focus on value delivery

**Risk 3: Infrastructure Costs Spike**
- **Mitigation:** Cost monitoring in place, usage alerts configured, can optimize as needed

**Risk 4: Competition**
- **Mitigation:** Focus on unique value propositions, customer service, rapid iteration

### 💡 **RECOMMENDATIONS**

1. **Immediate (Month 1-3):**
   - ✅ Current infrastructure setup is perfect - no changes needed
   - Focus on product-market fit and user acquisition
   - Use free tiers to attract initial users

2. **Short-term (Month 4-6):**
   - Target 5-10 paying customers
   - Monitor actual costs vs projections
   - Optimize based on real usage patterns

3. **Medium-term (Month 7-12):**
   - Scale to 20-30 customers
   - Consider infrastructure upgrades only if needed
   - Build annual subscription base for stability

4. **Long-term (Year 2+):**
   - Scale to 100+ customers
   - Consider additional products or features
   - Optimize for profitability over growth

### 🏆 **FINAL VERDICT**

**This is a HIGHLY VIABLE and USEFUL business because:**

✅ **Ultra-low break-even point** (6-9 customers)  
✅ **Excellent unit economics** (80-95% margins)  
✅ **Scalable infrastructure** (costs grow slowly)  
✅ **Multiple revenue streams** (3 products)  
✅ **Low risk** (only $74/month at zero revenue)  
✅ **High growth potential** (can scale 10x+ easily)  
✅ **Real market need** (solves actual problems)  
✅ **Competitive pricing** (attractive to customers)

**Recommendation:** **PROCEED WITH CONFIDENCE** - This business model is sound, cost-effective, and has strong potential for profitability and growth.

---

## ACTION ITEMS

1. ✅ Set up cost monitoring (Render dashboard, Vercel dashboard)
   - **Status**: Implemented monitoring endpoints in ASK (`/api/monitoring/*`)
   - **Location**: `ask/api/routes/monitoring.py`
   - **Usage**: Access via authenticated API calls

2. ✅ Set up usage alerts for Groq (prevent unexpected bills)
   - **Status**: Implemented for ASK and Reframe
   - **ASK**: `ask/api/utils/groq_monitor.py` - Database-based tracking with alerts
   - **Reframe**: `reframe/lib/groq-monitor.ts` - Redis-based tracking with alerts
   - **Alerts**: Daily ($10) and monthly ($50) thresholds, usage spike detection
   - **Configurable**: Via `GROQ_DAILY_COST_THRESHOLD` and `GROQ_MONTHLY_COST_THRESHOLD` env vars

3. ✅ Monitor BunnyCDN bandwidth monthly
   - **Status**: Already implemented in sketch2bim
   - **Location**: `sketch2bim/backend/app/monitoring/storage_monitor.py`
   - **Usage**: Part of existing monitoring system

4. ✅ Track payment processing fees vs revenue
   - **Status**: Implemented for all 3 payment-enabled projects
   - **ASK**: `ask/api/routes/payments.py` - Calculates and stores 2% fee per payment
   - **Sketch2BIM**: `sketch2bim/backend/app/routes/payments.py` - Calculates and stores 2% fee per payment
   - **Reframe**: `reframe/app/api/razorpay-webhook/route.ts` - Tracks fees in Redis
   - **Endpoints**: `GET /api/payments/fees` (ASK, Sketch2BIM)

5. ✅ Review costs quarterly and optimize
   - **Status**: Monitoring infrastructure in place
   - **Next Steps**: 
     - Set up quarterly review schedule
     - Use `/api/monitoring/summary` endpoint for comprehensive reports
     - Compare costs vs revenue using payment fee tracking

---

**Last Updated:** January 2025  
**Next Review:** April 2025

