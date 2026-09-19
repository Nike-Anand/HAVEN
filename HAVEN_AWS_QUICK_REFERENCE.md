# 🎯 HAVEN AWS SERVICES - QUICK REFERENCE CARD
## What to Use, What to Skip, and Exact Costs

---

# ⚡ ULTRA-QUICK DECISION TABLE

```
HAVEN NEEDS              → BUILD IT TRACK          → SHIP IT TRACK (RECOMMENDED)
─────────────────────────────────────────────────────────────────────────────
Backend                    SAM CLI + LocalStack       ✅ Lambda ($0)
API Endpoints              Local server               ✅ API Gateway ($0)
Database                   OpenSearch (local)         ✅ DynamoDB ($5-10)
Authentication             Cedar policy lang          ✅ Cognito ($0)
AI Models                  Mock/simulate              ✅ Bedrock Haiku ($5-10)
File Storage               Local filesystem           ✅ S3 (<$0.01)
Frontend Hosting           localhost:3000             ✅ Amplify ($1-2)
SMS/Email                  Mock/local                 ✅ SNS/SES ($0)
Monitoring                 Local logs                 ✅ CloudWatch ($0)
Mobile Testing             Simulator                  ✅ Real device ($0)
────────────────────────────────────────────────────────────────────────────
TOTAL COST                 $0                         $11-22 ✅
LIVE URL?                  NO ❌                      YES ✅
JUDGE APPEAL              Medium                     Excellent ✅
PRODUCTION               NO                          YES ✅
```

---

# 💰 EXACT COST BREAKDOWN (36-HOUR HACKATHON)

## **SHIP IT Track - What You'll Actually Pay**

```
╔════════════════════════════════════════════════════════════════╗
║               AWS SERVICE COSTS FOR HAVEN                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  FREE SERVICES (No charges):                                  ║
║  ─────────────────────────────────────────────────────────   ║
║  ✅ Lambda               1M invocations FREE     = $0.00      ║
║     └─ Your usage: ~5K invocations (Well within)             ║
║                                                               ║
║  ✅ API Gateway          1M requests FREE       = $0.00      ║
║     └─ Your usage: ~5K requests (Well within)               ║
║                                                               ║
║  ✅ Cognito              50K users FREE         = $0.00      ║
║     └─ Your usage: ~100-500 users (Well within)            ║
║                                                               ║
║  ✅ CloudWatch           5GB logs FREE          = $0.00      ║
║     └─ Your usage: ~100MB logs (Well within)               ║
║                                                               ║
║  ✅ SNS                  1K SMS FREE/month      = $0.00      ║
║     └─ Your usage: ~900 SMS (Well within)                  ║
║                                                               ║
║  ✅ SES                  62K emails FREE/month  = $0.00      ║
║     └─ Your usage: ~500 emails (Well within)               ║
║                                                               ║
║  ✅ S3                   5GB storage FREE       = $0.00      ║
║     └─ Your usage: ~100MB (Well within)                    ║
║                                                               ║
║ ────────────────────────────────────────────────────────────║
║ SUBTOTAL (Free):                                    $0.00   ║
║ ════════════════════════════════════════════════════════════║
║                                                               ║
║  PAID SERVICES (You'll pay from $100 credit):              ║
║  ─────────────────────────────────────────────────────────  ║
║  ✅ DynamoDB (On-demand)                                    ║
║     ├─ Writes: 5K writes × $0.00013         = $0.65       ║
║     ├─ Reads: 1K reads × $0.000026          = $0.03       ║
║     └─ Total DynamoDB                        = $5-10       ║
║                                                               ║
║  ✅ Bedrock Claude 3 Haiku (RECOMMENDED MODEL):            ║
║     ├─ Therapy bot: 2K messages × 2K tokens                ║
║     │  └─ Input: (4M tokens × $0.00025/1K)  = $1.00       ║
║     │  └─ Output: (4M tokens × $0.00125/1K) = $5.00       ║
║     ├─ Legal bot: 200 queries × 5K tokens                  ║
║     │  └─ Input: (1M tokens × $0.00025/1K)  = $0.25       ║
║     │  └─ Output: (1M tokens × $0.00125/1K) = $1.25       ║
║     └─ Total Bedrock                         = $7-10      ║
║     (Use Haiku - 10x cheaper than Sonnet!)               ║
║                                                               ║
║  ✅ Amplify Hosting:                                       ║
║     ├─ Build: 10 builds × 5 min × $0.01    = $0.50       ║
║     ├─ Hosting: ~100MB data                 = $0.02       ║
║     ├─ Traffic: <1GB                        = $0.00       ║
║     └─ Total Amplify                        = $1-2        ║
║                                                               ║
║  ✅ Misc (KMS, X-Ray, EventBridge):                        ║
║     └─ Total Misc                           = $0.05       ║
║                                                               ║
║ ────────────────────────────────────────────────────────────║
║ SUBTOTAL (Paid):                               $13-22      ║
║ ════════════════════════════════════════════════════════════║
║                                                               ║
║                    TOTAL COST: $13-22                       ║
║                   BUDGET GIVEN: $100                        ║
║                    REMAINING: $78-87 ✅✅✅                 ║
║                                                               ║
║ ════════════════════════════════════════════════════════════║
║ CONTINGENCY BUFFER: 30% of $100 = $30 (well covered!)    ║
║ ════════════════════════════════════════════════════════════║
║                                                               ║
╚════════════════════════════════════════════════════════════════╝
```

---

# 🎯 THE EXACT SERVICES YOU NEED

## **AWS Services Required for HAVEN (SHIP IT)**

### **Tier 1: Core Services (Absolutely Essential)**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  1️⃣  AWS LAMBDA                                            │
│      Purpose: Run SOS handler, therapy bot, legal bot     │
│      Cost: FREE (1M invocations)                           │
│      Runtime: Python 3.11                                  │
│      Memory: 256-512 MB                                    │
│      Timeout: 30-60 seconds                                │
│      What you'll use:                                      │
│      ├─ lambda-sos-handler.py                              │
│      ├─ lambda-therapy-bot.py                              │
│      ├─ lambda-legal-bot.py                                │
│      └─ lambda-contact-notifier.py                         │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  2️⃣  AWS API GATEWAY                                       │
│      Purpose: REST API for mobile/web app                 │
│      Cost: FREE (1M requests)                              │
│      Routes:                                               │
│      ├─ POST /auth/login                                  │
│      ├─ POST /sos/trigger                                 │
│      ├─ POST /therapy/send-message                        │
│      ├─ POST /legal/ask                                   │
│      ├─ GET /contacts                                     │
│      └─ POST /contacts/add                                │
│      Security: JWT + CORS                                  │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  3️⃣  AWS DYNAMODB                                          │
│      Purpose: NoSQL database for all data                 │
│      Cost: ~$5-10 (on-demand, pay-per-request)           │
│      Billing: $0.00013 per write, $0.000026 per read     │
│      Tables:                                               │
│      ├─ users (profile, encrypted)                        │
│      ├─ sos_events (SOS triggers)                         │
│      ├─ therapy_sessions (conversations)                  │
│      ├─ emergency_contacts (contact list)                 │
│      ├─ alert_logs (audit trail)                          │
│      └─ legal_queries (knowledge base)                    │
│      Encryption: Built-in KMS-backed                      │
│      TTL: Auto-delete old SOS records after 24hr          │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  4️⃣  AMAZON BEDROCK                                        │
│      Purpose: AI models for therapy + legal bots          │
│      Cost: ~$7-10 (token-based) ← USE HAIKU (CHEAPEST!)   │
│      Models Available:                                     │
│      ├─ Claude 3 Haiku: $0.00025 in, $0.00125 out ⭐      │
│      ├─ Llama 2: $0.00075 in, $0.001 out                 │
│      └─ Claude 3 Sonnet: $0.003 in, $0.015 out           │
│      Recommendation:                                       │
│      └─ Use HAIKU (10x cheaper than Sonnet, fast enough) │
│      Integration:                                          │
│      ├─ Therapy bot: Haiku with crisis prompt             │
│      └─ Legal bot: Haiku with legal knowledge context    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  5️⃣  AWS COGNITO                                           │
│      Purpose: User authentication + JWT tokens            │
│      Cost: FREE (up to 50K monthly active users)         │
│      Features:                                             │
│      ├─ Sign-up / Sign-in                                │
│      ├─ Email verification                               │
│      ├─ 2FA (SMS or authenticator app)                   │
│      ├─ JWT token generation                             │
│      └─ Password reset flow                              │
│      Security:                                             │
│      ├─ bcrypt password hashing                          │
│      ├─ Temporary tokens (1 hour expiry)                 │
│      └─ Secure session management                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  6️⃣  AMAZON S3                                             │
│      Purpose: Store conversation logs, legal KB, backups  │
│      Cost: ~$0.02 (minimal storage)                       │
│      Pricing: $0.023 per GB storage                       │
│      Buckets:                                              │
│      ├─ haven-logs (encrypted SOS/therapy logs)           │
│      ├─ haven-legal-kb (legal knowledge base JSON)        │
│      └─ haven-backups (DynamoDB backups)                  │
│      Security:                                             │
│      ├─ Server-side encryption (SSE-S3)                  │
│      ├─ Versioning enabled                               │
│      └─ Lifecycle: Delete after 90 days                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Tier 2: Communication Services (Important)**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  7️⃣  AMAZON SNS (Simple Notification Service)             │
│      Purpose: Send SMS alerts to emergency contacts       │
│      Cost: FREE (first 1K SMS per month)                  │
│      Pricing: $0.00645 per SMS (after free tier)         │
│      Usage:                                                │
│      ├─ SOS trigger → SMS to 3 contacts = 900 SMS        │
│      └─ Therapy escalation → SMS = 20 SMS                │
│      Total: ~920 SMS (WITHIN FREE TIER!)                 │
│      Topics:                                               │
│      ├─ sos-alerts (critical messages)                   │
│      ├─ therapy-escalation (counselor needed)            │
│      └─ user-notifications (general)                     │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  8️⃣  AMAZON SES (Simple Email Service)                    │
│      Purpose: Send password reset, verification emails    │
│      Cost: FREE (first 62K emails per month)             │
│      Pricing: $0.10 per 1K emails (after free tier)     │
│      Usage:                                                │
│      ├─ Verification emails: 200                          │
│      ├─ Password reset: 50                                │
│      ├─ Therapy summaries: 100                            │
│      └─ Total: ~350 emails (WITHIN FREE TIER!)           │
│      Features:                                             │
│      ├─ Email templates (for consistency)                 │
│      ├─ Bounce handling (remove bad emails)              │
│      └─ Delivery logs (tracking)                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Tier 3: Hosting & Monitoring (Important)**

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  9️⃣  AWS AMPLIFY HOSTING                                   │
│      Purpose: Deploy React web app with live URL          │
│      Cost: ~$1-2 (hosting + build minutes)               │
│      Pricing: $0.01/build minute, $0.15/GB/month        │
│      Features:                                             │
│      ├─ Auto-deploy from GitHub (push to main)           │
│      ├─ HTTPS automatic (SSL certificate free)           │
│      ├─ Custom domain support                            │
│      ├─ Built-in CDN (fast everywhere)                  │
│      └─ Environment variables (for API URL)             │
│      What it gives you:                                   │
│      └─ https://haven-[random].amplify.com              │
│      Setup:                                                │
│      ├─ npm build                                        │
│      ├─ Upload ./dist to Amplify                         │
│      └─ Done! (live in 2 minutes)                        │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  🔟  AMAZON CLOUDWATCH                                     │
│      Purpose: Logs, metrics, monitoring dashboard        │
│      Cost: FREE (basic tier)                              │
│      Pricing: $0.50/GB for logs > 5GB (won't hit)       │
│      Features:                                             │
│      ├─ Lambda logs (automatic)                          │
│      ├─ Custom metrics (SOS count, etc.)                 │
│      ├─ Alarms (notify if errors spike)                  │
│      └─ Dashboards (real-time monitoring)               │
│      Dashboard shows:                                      │
│      ├─ "SOS Events Today" (count)                       │
│      ├─ "Lambda Errors" (any failures?)                  │
│      ├─ "Bedrock API Latency" (speed)                   │
│      ├─ "DynamoDB Throttling" (over quota?)             │
│      └─ "Cost So Far" (how much spent)                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## **Services to SKIP (Don't Need)**

```
❌ RDS (SQL Database)
   └─ Why: Too expensive ($0.17/hour), DynamoDB is better

❌ EC2 (Virtual Machines)
   └─ Why: Lambda is serverless (pay only when running)

❌ ECS / Kubernetes
   └─ Why: Overkill for hackathon, Lambda is simpler

❌ SageMaker
   └─ Why: Bedrock is easier (no model management)

❌ Route 53 (Custom DNS)
   └─ Why: Free domain names work, Amplify includes it

❌ CloudFront (Extra CDN)
   └─ Why: Amplify includes CDN already

❌ WAF (Web Application Firewall)
   └─ Why: Not needed for hackathon demo

❌ App Runner
   └─ Why: Lambda is cheaper for this use case
```

---

# 📊 ARCHITECTURE FLOW (What Talks to What)

```
USER (Mobile/Web)
        │
        ↓ HTTPS
    ┌───────────────────────────┐
    │  Amplify (React App)      │
    │  https://haven-xxx.aws    │
    └──────────┬────────────────┘
               │ JSON over HTTPS
               ↓
    ┌──────────────────────────┐
    │  API Gateway             │
    │  (REST endpoints)        │
    └──┬──┬──┬────────────────┘
       │  │  │
    ┌──┘  │  └──┐
    ↓     ↓     ↓
┌────────────────────────────────┐
│  Lambda Functions              │
│  ├─ SOS Handler                │
│  ├─ Therapy Bot                │
│  ├─ Legal Bot                  │
│  └─ Contact Notifier           │
└────┬───────────┬────────────────┘
     │           │
     ↓           ↓
┌──────────┐  ┌─────────────────┐
│DynamoDB  │  │Amazon Bedrock   │
│(Storage) │  │(Claude Haiku)   │
└──────────┘  └─────────────────┘
     ↑
     │
     └─── SNS (SMS) → Emergency Contacts
     └─── SES (Email) → Notifications
     └─── S3 (Logs) → Storage
     └─── CloudWatch (Monitoring)
     └─── Cognito (Authentication)
```

---

# 🚀 DEPLOYMENT CHECKLIST

## **Before Submission (36 Hours)**

### **Hour 0-12: Setup**
- [ ] AWS Account created + $100 credit applied
- [ ] AWS CLI configured on laptop
- [ ] DynamoDB tables created (6 tables)
- [ ] Lambda functions created (4 functions)
- [ ] API Gateway endpoints mapped
- [ ] Cognito user pool + app client setup
- [ ] S3 buckets created
- [ ] Bedrock access enabled (Claude Haiku)
- [ ] SNS topic created
- [ ] SES verified email domain

### **Hour 12-24: Development**
- [ ] React frontend building
- [ ] Lambda functions coding
- [ ] Bedrock integration working
- [ ] DynamoDB read/writes working
- [ ] API endpoints tested locally
- [ ] Amplify deployment configured

### **Hour 24-30: Testing**
- [ ] Full SOS flow tested end-to-end
- [ ] Therapy bot responds with Haiku
- [ ] Legal bot provides information
- [ ] SMS alerts sent to test phone
- [ ] Mobile app points to live API
- [ ] Amplify hosting deployed + live URL

### **Hour 30-35: Monitoring & Optimization**
- [ ] CloudWatch dashboard showing metrics
- [ ] Costs tracked ($13-22 expected)
- [ ] Performance optimized
- [ ] Error handling tested

### **Hour 35-36: Final Checks**
- [ ] Demo flow rehearsed
- [ ] Screenshots/video backup ready
- [ ] Code pushed to GitHub
- [ ] README.md complete
- [ ] Architecture diagram prepared
- [ ] Cost breakdown documented
- [ ] All services tested 1 more time

---

# 🎯 COST MONITORING DURING HACKATHON

## **Set Up Billing Alerts NOW**

```bash
# AWS Console → Billing → Preferences
# Enable: "Receive CloudWatch Alarms for Billing"

# Create alert at $50 spent
# (Will alert if on track to exceed $100)

# Monitor daily:
# AWS Console → Cost Explorer
# Shows: Costs by service, Forecast, Trends
```

## **Daily Check (What to Watch)**

```
Day 1 Morning:
├─ DynamoDB: Should be $0 (no tables created yet)
├─ Bedrock: Should be $0 (not called yet)
└─ Amplify: Should be $0 (not deployed yet)

Day 1 Afternoon (Development):
├─ DynamoDB: Rising (~$0.50/1K writes)
├─ Bedrock: Rising (~$0.50/1M tokens)
└─ Amplify: Rising (~$0.10 per build)

Day 2 Evening (Final testing):
├─ DynamoDB: $5-8 (peak usage)
├─ Bedrock: $7-10 (therapy + legal calls)
├─ Amplify: $1-2 (multiple deploys)
└─ Total: $13-20 ✅

If any service > $30:
└─ STOP → Check what's expensive
   ├─ If Bedrock > $20 → Switch to Llama 2 (cheaper)
   ├─ If DynamoDB > $15 → Optimize queries
   └─ If Amplify > $5 → Reduce build frequency
```

---

# ✅ FINAL ANSWER: WHAT AWS SERVICES TO USE

## **MINIMUM VIABLE HAVEN (For $100 Budget)**

```
MUST HAVE (5 services):
✅ Lambda - Backend (FREE)
✅ API Gateway - REST API (FREE)
✅ DynamoDB - Database ($5-10)
✅ Bedrock - AI (Claude Haiku: $7-10)
✅ Amplify - Hosting ($1-2)

HIGHLY RECOMMENDED (3 services):
✅ Cognito - Auth (FREE)
✅ SNS - SMS alerts (FREE)
✅ CloudWatch - Monitoring (FREE)

NICE-TO-HAVE (2 services):
✅ S3 - Log storage (<$0.01)
✅ SES - Email (FREE)

SKIP (Don't use):
❌ RDS, EC2, ECS, SageMaker, Route 53, WAF, App Runner

TOTAL COST: $13-22 (Out of $100 budget)
REMAINING: $78-87 (Safe buffer!)
```

---

**Now you know EXACTLY what to build!** 🎉

Push this architecture forward and dominate First Commit! 🚀
