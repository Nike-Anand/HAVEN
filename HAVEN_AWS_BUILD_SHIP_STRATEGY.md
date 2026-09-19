# 🎯 HAVEN - AWS BUILD IT vs SHIP IT STRATEGY
## Service Selection, Cost Optimization & $100 Credit Budget Planning

---

# 📊 QUICK DECISION MATRIX

## **HAVEN Requirements vs First Commit Tracks**

| Requirement | Build It (LocalStack) | Ship It (AWS Cloud) | Recommended | Cost |
|---|---|---|---|---|
| **Agents & AI** | Strands SDK + LocalStack | SageMaker / Bedrock | **Bedrock (Ship It)** | $0.03-0.15/1K tokens |
| **Serverless Backend** | SAM CLI + LocalStack | Lambda + API Gateway | **Lambda (Ship It)** | FREE (1M invocations) |
| **Database** | OpenSearch | DynamoDB + S3 | **DynamoDB (Ship It)** | ~$1-5/month (on-demand) |
| **Authentication** | Cedar | Cognito | **Cognito (Ship It)** | FREE (50K MAU) |
| **Frontend Hosting** | Local dev server | Amplify | **Amplify (Ship It)** | $0-5/month |
| **Messaging (SMS/Email)** | Mock/Local | SNS + SES | **SNS (Ship It)** | FREE (first 1K) |
| **File Storage** | Local FS | S3 | **S3 (Ship It)** | ~$1/month |
| **Monitoring** | CloudWatch Local | CloudWatch | **CloudWatch (Ship It)** | FREE (basic tier) |

**Verdict:** 🏆 **SHIP IT** (Deploy on AWS) - Better for hackathon, judges love live URLs, and $100 credit covers costs

---

# 💰 $100 AWS CREDIT BUDGET ALLOCATION

## **Cost Breakdown (36-72 hour hackathon)**

```
Total Budget: $100 USD (from first commit)

ESSENTIAL SERVICES (Will use):
├─ Lambda:              $0 (1M free invocations/month)
├─ API Gateway:         $0 (first 1M requests free)
├─ Cognito:             $0 (free for <50K MAU)
├─ CloudWatch:          $0 (basic monitoring free)
├─ SNS:                 $0 (first 1K SMS free/month)
├─ SES:                 $0 (first 62K emails free/month)
├─ S3:                  $0.023 (small storage)
└─ DynamoDB:           $5-15 (on-demand, pay-per-request)

PREMIUM SERVICES (Need credits):
├─ Amazon Bedrock:     $20-40 (AI model calls)
│   └─ Claude 3 Sonnet: $0.003/1K input, $0.015/1K output
│   └─ Llama 2:         $0.00075/1K input, $0.001/1K output
├─ Amplify Hosting:     $5-10 (frontend deployment)
├─ Data Transfer:       $5 (cross-region, if any)
└─ Buffer/Contingency:  $20

TOTAL ESTIMATED: $55-85 (Well within $100 budget)
REMAINING BUFFER: $15-45
```

---

## **Detailed AWS Service Selection for HAVEN**

# 🔧 SHIP IT TRACK - RECOMMENDED ARCHITECTURE

## **Selected AWS Services**

### **1. COMPUTE & BACKEND** ✅

```yaml
Service: AWS Lambda
├─ Why: Serverless, auto-scaling, perfect for 36-hour hackathon
├─ Cost: FREE (1M invocations/month)
├─ Use Case: 
│   ├─ SOS Handler (trigger alerts)
│   ├─ Therapy Bot (Bedrock calls)
│   ├─ Legal Bot (Bedrock calls)
│   └─ Contact Notifier (SNS calls)
├─ Estimated Invocations (36 hrs):
│   ├─ SOS triggers: 100-500 (typical hackathon)
│   ├─ Therapy messages: 2,000-5,000
│   ├─ Legal queries: 100-200
│   └─ Total: ~5,000 invocations (ALL FREE)
└─ Memory/Timeout: 256-512 MB, 30-60 second timeout

---

Service: API Gateway
├─ Why: REST API endpoint for mobile/web
├─ Cost: FREE (first 1M requests/month)
├─ Features:
│   ├─ HTTP/REST API
│   ├─ Authentication (JWT)
│   ├─ Rate limiting
│   ├─ CORS configuration
│   └─ Request logging
├─ Endpoints Needed:
│   ├─ POST /sos/trigger
│   ├─ POST /therapy/send-message
│   ├─ POST /legal/ask
│   ├─ POST /auth/login
│   └─ GET /contacts
└─ Estimated Requests: 5K-10K (ALL FREE)

---

Service: AWS App Runner (OPTIONAL)
├─ Why: If you want Node.js/Python backend server
├─ Cost: $0.07/vCPU-hour (only if used)
├─ Alternative: Just use Lambda + API Gateway (simpler, cheaper)
└─ Recommendation: Skip this, use Lambda only
```

### **2. DATABASE** ✅

```yaml
Service: DynamoDB (PRIMARY)
├─ Why: 
│   ├─ NoSQL, scalable, encryption-ready
│   ├─ Perfect for real-time data
│   ├─ TTL (auto-delete old SOS records)
│   └─ Pay-per-request (no pre-provisioning)
├─ Billing Mode: ON-DEMAND
├─ Cost: ~$0.00013 per write, ~$0.000026 per read
├─ Estimated Usage (36 hrs):
│   ├─ SOS writes: 300 events × 1 write = 300 WCU
│   ├─ User profile reads: 1K reads × 1 RCU = 1K RCU
│   ├─ Therapy messages: 5K writes = 5K WCU
│   ├─ Total: ~$5-10 for hackathon
│   └─ Daily cost: ~$0.15-0.30
├─ Tables Needed:
│   ├─ users (profile data)
│   ├─ sos_events (critical)
│   ├─ therapy_sessions (conversation history)
│   ├─ emergency_contacts (contact list)
│   ├─ alert_logs (audit trail)
│   └─ legal_queries (knowledge base)
└─ Encryption: KMS-backed (built-in)

---

Service: S3 (FILE STORAGE)
├─ Why: Store encrypted conversations, logs, user uploads
├─ Billing Model: PAY-PER-USE
├─ Cost: 
│   ├─ Storage: $0.023/GB (minimal for hackathon)
│   ├─ Requests: FREE (first 2K puts/gets)
│   └─ Data transfer: FREE (within AWS)
├─ Estimated Usage: 100 MB = $0.002/month
├─ Buckets Needed:
│   ├─ haven-conversation-logs (encrypted)
│   ├─ haven-legal-kb (legal knowledge base)
│   └─ haven-uploads (user files)
├─ Configuration:
│   ├─ Server-side encryption (SSE-S3)
│   ├─ Versioning enabled
│   ├─ Access logs enabled
│   └─ Lifecycle policy (delete after 90 days)
└─ NO cost for basics

---

Service: RDS (OPTIONAL - NOT RECOMMENDED)
├─ Why: SQL database (alternative to DynamoDB)
├─ Cost: $0.17/hour (PostgreSQL micro) = $4/day
├─ Recommendation: SKIP THIS
│   └─ Too expensive, DynamoDB is better
└─ Use DynamoDB instead
```

### **3. AI & AGENTS** ✅

```yaml
Service: Amazon Bedrock
├─ Why: 
│   ├─ Access to Claude 3, Llama, etc.
│   ├─ No model management needed
│   ├─ Pay-per-token (cheap!)
│   └─ Built-in safety features
├─ Billing: Token-based (input + output)
├─ Models Available:
│   ├─ Claude 3 Sonnet: $0.003 input, $0.015 output per 1K
│   ├─ Llama 2 Chat: $0.00075 input, $0.001 output per 1K
│   └─ Mistral: Cheaper alternative
├─ Estimated Usage (36 hrs):
│   ├─ Therapy bot: 2,000 messages × 2K tokens avg = 4M tokens
│   │  └─ Cost: (4M × 0.003 / 1000) + (4M × 0.015 / 1000) = $72
│   ├─ Legal bot: 200 queries × 5K tokens = 1M tokens
│   │  └─ Cost: (1M × 0.003 / 1000) + (1M × 0.015 / 1000) = $18
│   ├─ TOTAL: ~$90 (within budget!)
│   └─ **USE LLAMA 2 INSTEAD** (60% cheaper):
│      ├─ Therapy: ~$30
│      ├─ Legal: ~$8
│      └─ Total: ~$38
├─ Recommended Model: **Claude 3 Haiku** (fastest, cheapest)
│   └─ Input: $0.00025/1K, Output: $0.00125/1K
│   └─ Same 2K messages: only ~$7 total! ✨
├─ Cost Optimization:
│   ├─ Use Haiku for therapy (perfectly adequate)
│   ├─ Use Haiku for legal (faster, cheaper)
│   ├─ Batch requests (if possible)
│   └─ Cache prompts (Bedrock supports prompt caching)
└─ BUDGET IMPACT: $7-40 depending on model choice
```

### **4. AUTHENTICATION** ✅

```yaml
Service: AWS Cognito
├─ Why: 
│   ├─ User sign-up, login, 2FA
│   ├─ JWT token generation
│   ├─ Social login (optional)
│   └─ Security best practices built-in
├─ Billing: FREE (up to 50K monthly active users)
├─ Features Needed:
│   ├─ User pool (user registration)
│   ├─ App client (OAuth credentials)
│   ├─ MFA (SMS or email-based)
│   ├─ Temporary tokens (1 hour expiry)
│   └─ Password hashing (bcrypt)
├─ Configuration:
│   ├─ Username + password login
│   ├─ Email verification on signup
│   ├─ SMS 2FA (optional, may cost)
│   └─ Account recovery (email link)
├─ Estimated Users (36 hrs): 100-500 (ALL FREE)
└─ **COST: $0 (well within free tier)**

---

Service: AWS KMS (Key Management Service)
├─ Why: Encrypt sensitive data keys
├─ Billing Model: $1/month per key
├─ Keys Needed: 1 master key (for all user data)
├─ Estimated Cost: $1/month
└─ **COST: ~$0.03 for hackathon** (negligible)
```

### **5. NOTIFICATIONS** ✅

```yaml
Service: Amazon SNS (Simple Notification Service)
├─ Why: Send SMS/email alerts to emergency contacts
├─ Billing: 
│   ├─ SMS: $0.00645 per message (US), varies by country
│   ├─ Email: FREE
│   └─ Free tier: First 1K SMS per month
├─ Estimated Usage (36 hrs):
│   ├─ SOS triggers: 300 events × 3 contacts = 900 SMS
│   ├─ Therapy escalations: 20 events × 1 SMS = 20 SMS
│   └─ Total: ~920 SMS (within FREE TIER!)
├─ Configuration:
│   ├─ Topic per SOS type
│   ├─ Subscriptions: email + SMS
│   ├─ Message filtering
│   └─ Delivery retry policy
└─ **COST: $0 (within free 1K SMS)**

---

Service: Amazon SES (Simple Email Service)
├─ Why: Send password reset, notifications, therapy summaries
├─ Billing: FREE (first 62K emails per month)
├─ Estimated Usage: 500-1K emails (ALL FREE)
├─ Configuration:
│   ├─ Verified email domain
│   ├─ Email templates
│   ├─ Bounce/complaint handling
│   └─ Delivery logs
└─ **COST: $0 (within free tier)**
```

### **6. FRONTEND HOSTING** ✅

```yaml
Service: AWS Amplify Hosting
├─ Why: 
│   ├─ Deploy React/Vue web app
│   ├─ Built-in CI/CD (GitHub integration)
│   ├─ Custom domains
│   ├─ HTTPS automatic
│   └─ Fast CDN
├─ Billing Model: Pay-per-use
│   ├─ Build minutes: $0.01/minute
│   ├─ Hosting: $0.15/GB-month
│   └─ Data transfer: $0.15/GB (first 1GB free)
├─ Estimated Usage (36 hrs):
│   ├─ Build: 10 builds × 5 minutes = 50 minutes = $0.50
│   ├─ Hosting: ~100 MB = $0.015/month
│   ├─ Traffic: ~1 GB = FREE
│   └─ Total: ~$1-2 for hackathon
├─ Alternative: Use GitHub Pages + CloudFront
│   ├─ GitHub Pages: FREE
│   ├─ CloudFront: ~$0.085/GB (first 50GB)
│   └─ Savings: ~90%
└─ **RECOMMENDED: Amplify (simpler setup, worth the $1-2)**

---

Service: CloudFront (CDN - OPTIONAL)
├─ Why: Cache static assets, reduce latency
├─ Cost: $0.085/GB data transfer
├─ Recommendation: Include Amplify (has CDN built-in)
└─ **SKIP separate CloudFront**
```

### **7. MONITORING & LOGGING** ✅

```yaml
Service: CloudWatch
├─ Why:
│   ├─ Lambda logs (automatic)
│   ├─ DynamoDB metrics
│   ├─ Custom metrics
│   ├─ Error tracking
│   └─ Performance monitoring
├─ Billing:
│   ├─ Logs: $0.50/GB ingested
│   ├─ Metrics: $0.10 per metric (first 10K free)
│   ├─ Alarms: $0.10 per alarm
│   └─ Free tier: 5GB logs, 1K custom metrics
├─ Estimated Usage (36 hrs):
│   ├─ Lambda logs: ~100 MB (FREE)
│   ├─ Custom metrics: 5-10 metrics (FREE)
│   └─ Alarms: 2-3 alarms (FREE)
├─ Dashboard:
│   ├─ SOS events count
│   ├─ Lambda invocation errors
│   ├─ Bedrock API latency
│   ├─ DynamoDB throttling
│   └─ User signup count
└─ **COST: $0 (within free tier)**

---

Service: X-Ray (Distributed Tracing)
├─ Why: Debug requests across Lambda, API Gateway, DynamoDB
├─ Billing: $0.50 per million traces recorded
├─ Estimated Usage: 5K traces = $0.0025
├─ Recommendation: OPTIONAL (nice-to-have for debugging)
└─ **COST: <$0.01 (negligible)**
```

### **8. NETWORKING & ROUTING** ✅

```yaml
Service: Route 53 (DNS)
├─ Why: Custom domain (haven-app.com)
├─ Billing: $0.50/month per hosted zone
├─ Recommendation: OPTIONAL (can use free domain)
├─ Alternatives:
│   ├─ GitHub Pages: namecheap.com (free domain)
│   ├─ Amplify custom domain: $0.50/month
│   └─ No custom domain: FREE
└─ **COST: $0 (use free domain provider)**

---

Service: EventBridge (Event Bus)
├─ Why: Trigger Lambda on scheduled events
├─ Use Case: Check for inactive SOS every 5 mins
├─ Billing: $0.30 per million events
├─ Estimated Usage: ~500 events (FREE tier)
└─ **COST: $0 (within free tier)**
```

### **9. SECURITY & POLICY** ✅

```yaml
Service: AWS WAF (Web Application Firewall)
├─ Why: Protect API from DDoS, bot attacks
├─ Billing: $5/month + per-rule costs
├─ Recommendation: OPTIONAL (not critical for hackathon)
└─ **SKIP for now**

---

Service: AWS Secrets Manager
├─ Why: Store API keys, database passwords
├─ Billing: $0.40 per secret per month
├─ Secrets Needed:
│   ├─ Bedrock API key
│   ├─ Twilio API key (if using)
│   ├─ Database connection string
│   └─ JWT signing key
├─ Estimated: 4 secrets × $0.40 = $1.60/month
└─ **COST: <$0.05 for 36-hour hackathon**
```

---

# 📋 FINAL AWS SERVICE CHECKLIST (SHIP IT TRACK)

## **ESSENTIAL (Must have)**

- [x] **Lambda** - Backend serverless ($0)
- [x] **API Gateway** - REST endpoints ($0)
- [x] **DynamoDB** - Database ($5-15)
- [x] **Cognito** - Authentication ($0)
- [x] **S3** - File storage (<$0.01)
- [x] **Bedrock** - AI models ($7-40, depending on model)
- [x] **Amplify** - Frontend hosting ($1-2)
- [x] **CloudWatch** - Logs & monitoring ($0)
- [x] **SNS** - SMS alerts ($0, within free tier)
- [x] **SES** - Email notifications ($0)

**Total Essential: $13-57 (Within $100 budget)**

## **OPTIONAL (Nice-to-have)**

- [ ] Route 53 - Custom domain ($0.50/mo)
- [ ] X-Ray - Distributed tracing (<$0.01)
- [ ] KMS - Advanced encryption key ($1/mo)
- [ ] EventBridge - Scheduled events ($0)
- [ ] CloudFront - CDN (included in Amplify)
- [ ] App Runner - Alternative compute (skip)
- [ ] RDS - SQL database (skip, use DynamoDB)

---

# 💾 MINIMAL $100 ARCHITECTURE

## **Build It Track (LOCAL)**

If you want to avoid AWS costs entirely and use $100 for something else:

```yaml
LocalStack Setup:
├─ SAM CLI (build Lambda locally)
├─ Docker (run LocalStack)
├─ OpenSearch (local database)
├─ Local Bedrock emulation (mock)
└─ React dev server (frontend)

Cost: $0 (everything local)
Pros:
  ├─ No AWS charges
  ├─ Faster development
  ├─ Works offline
  └─ Can use $100 for prizes instead

Cons:
  ├─ No live URL (can't share easily)
  ├─ Demo is on localhost
  ├─ Judges less impressed (no production)
  └─ Bedrock mocking is limited

Recommendation: NO
Why: For hackathon, live URL matters for judging
     Bedrock mock won't work well
     Ship It with $100 credits is better
```

---

# 🚀 RECOMMENDED HAVEN ARCHITECTURE (OPTIMIZED FOR $100)

## **Architecture Diagram**

```
┌─────────────────────────────────────────────────────────┐
│                  HAVEN APP USERS                         │
│          (Mobile App + Web Browser)                      │
└──────────────────┬──────────────────────────────────────┘
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   ┌─────────────┐      ┌──────────────┐
   │ Amplify     │      │ Mobile App   │
   │ (React)     │      │ (React Native)
   └──────┬──────┘      └──────┬───────┘
          │                    │
          └────────┬───────────┘
                   │ HTTPS/TLS
        ┌──────────▼──────────┐
        │  API Gateway        │
        │  (REST endpoints)   │
        └────────┬────────────┘
                 │
    ┌────────────┼────────────┬─────────────┐
    ▼            ▼            ▼             ▼
 Lambda      Lambda       Lambda        Lambda
 (SOS)      (Therapy)    (Legal)      (Contact)
    │            │            │             │
    └────────────┼────────────┴─────────────┘
                 │ JSON
        ┌────────▼────────┐
        │  DynamoDB       │
        │  (encrypted)    │
        │  - Users        │
        │  - SOS events   │
        │  - Messages     │
        │  - Contacts     │
        └────────┬────────┘
                 │
    ┌────────────┼────────────┬───────────────┐
    ▼            ▼            ▼               ▼
  Bedrock      S3        Cognito           SNS
  (Claude)  (Logs)      (Auth)          (Alerts)
            (KBs)                       (SMS/Email)


EXTERNAL INTEGRATIONS:
├─ Bedrock API (Claude 3 Haiku)
├─ SNS (SMS to contacts)
├─ SES (Email notifications)
└─ CloudWatch (Logs + monitoring)

SECURITY:
├─ HTTPS/TLS everywhere
├─ JWT tokens (Cognito)
├─ Encrypted at rest (KMS)
├─ Encrypted in transit (TLS 1.3)
└─ No plaintext sensitive data

COST FOR HACKATHON:
├─ Lambda: $0
├─ API Gateway: $0
├─ Cognito: $0
├─ DynamoDB: $5-10
├─ Bedrock (Claude Haiku): $5-10
├─ Amplify: $1-2
├─ S3: <$0.01
├─ SNS/SES: $0
└─ TOTAL: $11-22 (Well within $100 budget!)
```

---

# 💳 PAYMENT & BILLING STRATEGY

## **How to Use $100 Credits Efficiently**

```
Step 1: Set up AWS Billing Alert
└─ Go to Billing → Preferences
   └─ Alert when usage > $50

Step 2: Enable Cost Explorer
└─ View daily costs in real-time
   └─ Catch expensive services early

Step 3: Use AWS Free Tier First
├─ Lambda: 1M invocations FREE
├─ DynamoDB: 25 GB storage FREE (first 12 months)
├─ API Gateway: 1M requests FREE
├─ SNS: 1K SMS FREE
├─ SES: 62K emails FREE
└─ S3: 5 GB storage FREE

Step 4: Monitor Bedrock (Most Expensive)
├─ Start with Claude Haiku (cheapest)
├─ Track tokens used daily
├─ Set CloudWatch alert at $20 spent
└─ Switch to Llama if over budget

Step 5: Disable/Delete After Hackathon
├─ Delete Lambda functions
├─ Stop RDS instances (if used)
├─ Delete unused DynamoDB tables
├─ Clear S3 buckets
└─ Prevent accidental charges
```

## **Sample Daily Cost Breakdown (36-hour hackathon)**

```
Day 1 (First 24 hours):
├─ Lambda: $0.00
├─ API Gateway: $0.00
├─ DynamoDB: $2.50 (writes growing)
├─ Bedrock: $5.00 (therapy bot active)
├─ Amplify: $0.50 (first deploy)
├─ Others: $0.10
└─ Day 1 Total: $8.10

Day 2 (Next 12 hours):
├─ Lambda: $0.00
├─ API Gateway: $0.00
├─ DynamoDB: $1.50 (less traffic, more optimized)
├─ Bedrock: $2.00 (fewer queries, final testing)
├─ Amplify: $0.20
├─ Others: $0.05
└─ Day 2 Total: $3.75

HACKATHON TOTAL: ~$12 (89% saving!)
Remaining Budget: $88
```

---

# 🎯 STEP-BY-STEP AWS SETUP

## **Phase 1: AWS Account & Credentials (1 hour)**

```bash
# 1. Create AWS Account
# Go to: https://aws.amazon.com
# Sign up, add payment method (won't be charged, just verification)
# Add $100 credit code at: https://console.aws.amazon.com/cost-management/home#/custom-cost

# 2. Create IAM User (don't use root)
# AWS Console → IAM → Users → Create user
# Attach policy: AdministratorAccess (for hackathon only)
# Create access keys
# Save: Access Key ID + Secret Access Key

# 3. Configure AWS CLI
aws configure
# AWS Access Key ID: [paste from IAM]
# AWS Secret Access Key: [paste from IAM]
# Default region: ap-south-1 (Mumbai - closest to India)
# Default output format: json

# 4. Verify setup
aws sts get-caller-identity
# Output: Account ID, User ARN, etc.
```

## **Phase 2: DynamoDB Setup (30 min)**

```bash
# Create tables using AWS SDK or Console
aws dynamodb create-table \
  --table-name haven_users \
  --attribute-definitions AttributeName=user_id,AttributeType=S \
  --key-schema AttributeName=user_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST

aws dynamodb create-table \
  --table-name haven_sos_events \
  --attribute-definitions \
    AttributeName=sos_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=S \
  --key-schema \
    AttributeName=sos_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --ttl-specification AttributeName=ttl,Enabled=true

# Repeat for: therapy_sessions, emergency_contacts, alert_logs, legal_queries
```

## **Phase 3: Lambda Setup (1 hour)**

```bash
# 1. Create Lambda execution role
aws iam create-role \
  --role-name haven-lambda-role \
  --assume-role-policy-document file://trust-policy.json

# 2. Attach permissions
aws iam attach-role-policy \
  --role-name haven-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# 3. Create Lambda function
aws lambda create-function \
  --function-name haven-sos-handler \
  --runtime python3.11 \
  --role arn:aws:iam::ACCOUNT_ID:role/haven-lambda-role \
  --handler index.lambda_handler \
  --zip-file fileb://lambda_function.zip

# 4. Set environment variables
aws lambda update-function-configuration \
  --function-name haven-sos-handler \
  --environment Variables={DYNAMODB_TABLE=haven_sos_events}
```

## **Phase 4: API Gateway Setup (30 min)**

```bash
# Create REST API
aws apigateway create-rest-api \
  --name haven-api \
  --description "HAVEN Safety Platform API"

# Create endpoints
# POST /sos/trigger
# POST /therapy/send-message
# POST /legal/ask
# POST /auth/login
# GET /contacts

# Integrate with Lambda
# Enable CORS
# Deploy to stage: dev
```

## **Phase 5: Cognito Setup (30 min)**

```bash
# Create User Pool
aws cognito-idp create-user-pool \
  --pool-name haven_users \
  --policies file://password-policy.json

# Create App Client
aws cognito-idp create-user-pool-client \
  --user-pool-id [POOL_ID] \
  --client-name haven-app

# Enable MFA (optional)
aws cognito-idp set-user-pool-mfa-config \
  --user-pool-id [POOL_ID] \
  --mfa-configuration OPTIONAL
```

## **Phase 6: Bedrock Setup (15 min)**

```bash
# Request Bedrock access (usually automatic)
# AWS Console → Bedrock → Model Access
# Enable: Claude 3 Haiku, Llama 2

# Test API call
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-haiku-20240307-v1:0 \
  --body '{"messages":[{"role":"user","content":"Hello"}]}'
```

## **Phase 7: Amplify Hosting (30 min)**

```bash
# Install Amplify CLI
npm install -g @aws-amplify/cli

# Initialize Amplify project
amplify init
# Project name: haven
# Environment: dev
# Editor: VS Code
# App type: javascript
# Framework: react

# Add hosting
amplify add hosting
# Hosting service: Amplify Hosting
# Deployment type: Manual

# Deploy
amplify publish
# Output: Live URL
```

---

# 📱 DEVELOPMENT WORKFLOW

## **Local Development (First 12 hours)**

```bash
# 1. Clone repo
git clone https://github.com/your-team/haven.git
cd haven

# 2. Install backend dependencies
cd backend
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 3. Install frontend dependencies
cd ../frontend
npm install

# 4. Start local stack (mock AWS)
docker-compose up -d localstack

# 5. Create local DynamoDB tables
bash scripts/setup-local-db.sh

# 6. Start backend (SAM CLI)
sam local start-api --port 3001

# 7. Start frontend (React dev server)
npm start
# Opens: http://localhost:3000

# 8. Test API locally
curl -X POST http://localhost:3001/sos/trigger \
  -H "Content-Type: application/json" \
  -d '{"location": {"latitude": 19.07, "longitude": 72.88}}'
```

## **Deployment Workflow (Last 12 hours)**

```bash
# 1. Build Lambda functions
cd backend/lambdas
pip install -r requirements.txt -t .
zip -r sos-handler.zip .

# 2. Deploy to AWS
aws lambda update-function-code \
  --function-name haven-sos-handler \
  --zip-file fileb://sos-handler.zip

# 3. Build React app
cd frontend
npm run build
# Output: ./dist

# 4. Deploy to Amplify
amplify publish
# Outputs: https://[random].amplify.com

# 5. Smoke test live URL
curl -X POST https://api.[random].amplify.com/sos/trigger

# 6. Test mobile app pointing to live API
# Update mobile app API_BASE_URL to live URL

# 7. Final testing (36 minutes before deadline)
- Test SOS trigger on live
- Test therapy bot response
- Test emergency alert
- Test legal query
```

---

# 🎬 DEMO SETUP

## **What Judges Will See**

```
LAPTOP SCREEN:
├─ Web app (Amplify URL): https://haven-[random].amplify.com
│  ├─ Dashboard with SOS button
│  ├─ Login screen
│  ├─ Contacts management
│  └─ Therapy history
│
├─ Terminal (showing live logs)
│  ├─ CloudWatch logs for Lambda
│  ├─ Bedrock API calls
│  ├─ DynamoDB writes
│  └─ Cost monitoring
│
└─ Phone (mobile app demo)
   ├─ React Native app on iOS/Android
   ├─ Press SOS button
   ├─ Show therapy chat
   └─ Show contact alerts

DEMO SCRIPT:
0-30 sec: "This is HAVEN, AI safety platform for women"
30-60 sec: Show live web app, explain dashboard
60-120 sec: "Press SOS button to trigger emergency"
           Show alert to contacts (via terminal logs)
           Show therapy bot responding
120-180 sec: "All built on AWS: Lambda, DynamoDB, Bedrock"
            Show CloudWatch metrics
180-240 sec: "Cost: $12 for full hackathon, using $100 credits"
            Show AWS billing page
240+ sec: "Questions?"
```

---

# ✅ FINAL CHECKLIST

## **Before Judging (30 minutes before)**

- [ ] All Lambda functions deployed
- [ ] API Gateway endpoints live
- [ ] Amplify hosting URL working
- [ ] Bedrock API key configured
- [ ] Cognito user pool ready (test account created)
- [ ] DynamoDB tables populated with test data
- [ ] Mobile app API points to live URL
- [ ] CloudWatch dashboard created
- [ ] Test SMS alert (have judge's phone ready)
- [ ] Test therapy bot with live Bedrock
- [ ] Test legal query bot
- [ ] Demo slides prepared
- [ ] README on GitHub updated
- [ ] Architecture diagram ready
- [ ] Cost breakdown documented
- [ ] Backup demo (screenshots) if anything fails

---

# 🎯 FINAL VERDICT: BUILD IT vs SHIP IT

| Aspect | Build It (Local) | Ship It (AWS) |
|---|---|---|
| **Cost** | $0 | $12-25 |
| **Live URL** | No (localhost) | Yes ✅ |
| **Judge Appeal** | 3/5 | 5/5 ✅ |
| **Bedrock Integration** | Mock only | Real ✅ |
| **Mobile Testing** | Hard (localhost) | Easy ✅ |
| **Scalability Demo** | Not visible | Can show ✅ |
| **Production-ready** | No | Yes ✅ |
| **Setup Time** | 2 hours | 3 hours |
| **Debugging** | Easy (local) | Harder (AWS) |
| **Prize Tier** | Lower | Higher ✅ |

## **🏆 RECOMMENDATION: SHIP IT**

**Why:**
- $100 credit covers ALL costs ($12-25 only)
- Live URL impresses judges
- Real Bedrock AI (not mocked)
- Shows cloud architecture knowledge
- Production-ready code
- Fast-track Amazon interview potential

**Budget Allocation:**
```
DynamoDB:     $10
Bedrock:      $8 (Claude Haiku)
Amplify:      $2
Others:       $2
────────────────
TOTAL:        $22
Remaining:    $78 (buffer for overages)
```

Let's build HAVEN on AWS Ship It! 🚀
