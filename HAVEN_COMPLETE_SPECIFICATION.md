# 🚀 HAVEN - COMPLETE PROJECT SPECIFICATION
## Women's Safety & Support Platform (First Commit 2026)

---

# 📋 PROJECT OVERVIEW

## **What is HAVEN?**
A comprehensive, AI-powered safety platform designed for women in crisis situations (domestic violence, harassment, abuse). HAVEN provides:
- **Discreet emergency alerts** (SOS system)
- **Real-time mental health support** (AI therapy bot)
- **Legal guidance** (AI legal advisor with Indian law knowledge)
- **Emergency network coordination** (notify trusted contacts)
- **Offline functionality** (works without internet)
- **Secure data storage** (end-to-end encrypted)

## **Vision**
HAVEN turns a woman's phone into a trusted safety companion. When she's in danger, one discreet action gives her immediate support, alerts her network, and coordinates with emergency services.

---

# 🎯 PROBLEM STATEMENT (FINAL VERSION)

```
PROBLEM:
Women in abusive situations face multiple barriers to safety:
1. Current crisis hotlines have 30+ minute wait times
2. Calling is risky (abuser might hear the phone)
3. Limited access to mental health support during crisis
4. Lack of legal knowledge about their rights
5. Emergency contacts don't know they're in danger
6. No privacy-preserving solution exists

SPECIFIC IMPACT:
- 1 in 3 women in India experience sexual harassment
- Average wait time for crisis hotline: 30-45 minutes
- 60% of abuse victims don't call for help (fear of retaliation)
- Mental health support during crisis is rare
- Women don't understand their legal rights

ROOT CAUSE:
Crisis support systems are outdated (phone-only). 
Technology has not evolved to meet modern safety needs.

SOLUTION:
HAVEN is an AI-powered platform providing:
1. Instant discreet SOS trigger (no calling needed)
2. Real-time AI therapy bot for de-escalation
3. Automated emergency contact alerts
4. Legal guidance (Indian Constitution + Women's Rights Acts)
5. Offline functionality
6. End-to-end encrypted communications

TARGET USERS:
- Women in abusive relationships
- Women experiencing sexual harassment
- Women in stalking situations
- Women in domestic violence crisis
- Women who feel unsafe

GEOGRAPHIC FOCUS:
India (cultural context: cultural barriers to reporting abuse, 
family pressure, legal system complexity)

IMPACT:
- Instant support (vs 30+ min wait)
- Reduced trauma (AI support while waiting for help)
- Empowered emergency response (contacts know location + situation)
- Legal knowledge (understand rights in Indian context)
- Life-saving intervention
```

---

# 🏗️ SYSTEM ARCHITECTURE

## **HIGH-LEVEL ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────────┐
│                    USERS (Women)                             │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
   ┌─────────┐      ┌──────────────┐
   │ Mobile  │      │  Web App     │
   │ App     │      │ (Dashboard)  │
   └────┬────┘      └──────┬───────┘
        │                  │
        │   API Gateway    │
        └────────┬─────────┘
                 │
    ┌────────────┼────────────┐
    ▼            ▼            ▼
  Lambda    Lambda        Lambda
  (SOS)     (Therapy)     (Legal)
    │            │           │
    └────────────┼───────────┘
                 │
        ┌────────┴────────┬──────────┐
        ▼                 ▼          ▼
    DynamoDB         S3         Bedrock
    (Data)        (Logs)       (AI Models)
        │
    ┌───┴───┬─────────┬──────────┐
    ▼       ▼         ▼          ▼
  Users Contacts  Messages  Emergency
  Table  Table    Table     Logs

External Integrations:
    ├─ SNS (SMS alerts to contacts)
    ├─ SES (Email notifications)
    ├─ Cognito (Authentication)
    └─ CloudWatch (Monitoring)
```

---

# 🛠️ COMPLETE TECH STACK

## **Frontend**

### Web Application
```yaml
Framework: React 18
UI Library: Material-UI (MUI)
State Management: Redux Toolkit
Real-time: Socket.io
Maps: Google Maps / Mapbox
Styling: Tailwind CSS
Package Manager: npm

Libraries:
  - axios (HTTP client)
  - react-router (navigation)
  - react-query (data fetching)
  - framer-motion (animations)
  - zustand (state)
  - react-hook-form (forms)
```

### Mobile Application
```yaml
Framework: React Native / Flutter
Option A - React Native:
  - React Native 0.72+
  - React Native Navigation
  - Redux or Zustand
  - React Native Geolocation
  - React Native Permissions
  
Option B - Flutter (Recommended):
  - Flutter 3.10+
  - Provider (state management)
  - GetIt (service locator)
  - Dio (HTTP)
  - Geolocator (location)
  - Local notifications
```

## **Backend**

### AWS Services
```yaml
Compute:
  - AWS Lambda (serverless functions)
  - AWS App Runner (for long-running processes)

API:
  - API Gateway (REST API)
  - EventBridge (event-driven architecture)

Database:
  - DynamoDB (primary database)
  - ElastiCache (Redis caching)
  - S3 (file storage)

AI/ML:
  - Amazon Bedrock (LLM access)
    - Claude 3 (therapy bot)
    - Llama 2 (legal bot)
  - Amazon Comprehend (sentiment analysis)
  - Amazon Rekognition (optional: image processing)

Security:
  - AWS Cognito (authentication)
  - AWS KMS (encryption keys)
  - AWS Secrets Manager (API keys)
  - AWS WAF (web application firewall)

Monitoring:
  - CloudWatch (logs & metrics)
  - X-Ray (tracing)
  - SNS (notifications)
  - SES (email service)

Hosting:
  - Amplify (frontend hosting)
  - Route 53 (DNS)
  - CloudFront (CDN)
```

### Runtime Environment
```yaml
Language: Python 3.11
Framework: FastAPI / Python AWS Lambda (serverless)
  
Core Libraries:
  - boto3 (AWS SDK)
  - fastapi (API framework)
  - uvicorn (ASGI server)
  - pydantic (data validation)
  - sqlalchemy (ORM - for local dev)
  - python-jose (JWT tokens)
  - passlib (password hashing)
  - cryptography (encryption)
```

## **Open Source / Third Party**

```yaml
Encryption:
  - libsodium (encryption primitives)
  - cryptography library

Steganography (Optional):
  - pillow (image processing)
  - pycryptodome (crypto algorithms)
  - scikit-image (image manipulation)

Messaging:
  - Twilio (SMS, optional)
  - SendGrid (email, optional)

Maps & Location:
  - Google Maps API
  - Mapbox API

Legal Database:
  - Indian Constitution API
  - LawDB (legal database)
  - Custom legal knowledge base

Analytics:
  - Mixpanel
  - Segment
```

## **Development Tools**

```yaml
Version Control: Git / GitHub
CI/CD: GitHub Actions
Container: Docker
Infrastructure as Code: AWS CloudFormation / Terraform
Testing: Pytest, Jest
Code Quality: Pylint, ESLint, SonarQube
Monitoring: Datadog / New Relic
API Testing: Postman, Thunder Client
```

---

# 📦 COMPLETE FEATURE SET

## **1. USER AUTHENTICATION & ONBOARDING**

### Features
```
✅ Secure signup (email/phone)
✅ Two-factor authentication (2FA)
✅ Biometric login (fingerprint, face recognition)
✅ Emergency account recovery
✅ Privacy-focused onboarding
✅ Legal consent agreements
✅ Offline mode setup
```

### Implementation
```
- AWS Cognito User Pools
- Custom MFA (SMS + authenticator app)
- Biometric APIs (native mobile)
- Encrypted session management
```

---

## **2. DISCREET SOS SYSTEM**

### How It Works
```
User presses SOS trigger:
  ↓
Triggers AWS Lambda function
  ↓
Records: Timestamp, Location, User ID
  ↓
Instantly alerts: Emergency contacts + authorities
  ↓
Starts: Therapy bot + legal guidance
  ↓
Logs: All interactions (encrypted)
```

### Technical Details

**SOS Button Options:**
1. **Hidden app icon** (looks like calculator/notes)
2. **Gesture trigger** (shake phone 3 times rapidly)
3. **Voice command** (say specific phrase)
4. **Widget shortcut** (lockscreen widget)
5. **Accessibility button** (built-in iOS/Android accessibility)

**Data Captured:**
```python
{
  "sos_id": "unique_id",
  "user_id": "encrypted_user_id",
  "timestamp": "ISO_8601",
  "location": {
    "latitude": float,
    "longitude": float,
    "accuracy": int,
    "address": "street, city, state"
  },
  "device_info": {
    "phone_type": "iOS/Android",
    "battery": int,
    "connectivity": "wifi/cellular/offline"
  },
  "contact_alerts_sent": int,
  "emergency_services_notified": bool
}
```

**Lambda Function (SOS Handler)**
```python
# Lambda: HandleSOS
import json
import boto3
import uuid
from datetime import datetime
from aws_lambda_powertools import Logger

logger = Logger()
dynamodb = boto3.resource('dynamodb')
sns_client = boto3.client('sns')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    """
    Handles SOS trigger from mobile/web app
    """
    try:
        # Parse incoming SOS
        body = json.loads(event['body'])
        user_id = body['user_id']
        location = body['location']
        
        # Create SOS record
        sos_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Store in DynamoDB
        sos_table = dynamodb.Table('sos_events')
        sos_table.put_item(Item={
            'sos_id': sos_id,
            'user_id': user_id,
            'timestamp': timestamp,
            'location': location,
            'status': 'active',
            'contacts_notified': 0,
            'ttl': int(time.time()) + 86400  # 24 hour TTL
        })
        
        # Get emergency contacts
        users_table = dynamodb.Table('users')
        user = users_table.get_item(Key={'user_id': user_id})['Item']
        emergency_contacts = user.get('emergency_contacts', [])
        
        # Send alerts to contacts
        for contact in emergency_contacts:
            send_alert_to_contact(contact, user_id, location, sos_id)
        
        # Alert authorities (if enabled)
        if user.get('notify_authorities'):
            alert_authorities(user_id, location, sos_id)
        
        # Start therapy bot conversation
        start_therapy_session(user_id, sos_id)
        
        logger.info(f"SOS triggered: {sos_id} for user {user_id}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'sos_id': sos_id,
                'status': 'SOS alert activated',
                'message': 'Help is on the way. AI support is ready.'
            })
        }
        
    except Exception as e:
        logger.error(f"SOS error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Failed to process SOS'})
        }

def send_alert_to_contact(contact, user_id, location, sos_id):
    """Send SMS/Email alert to emergency contact"""
    phone = contact['phone']
    name = contact['name']
    
    message = f"""
    URGENT: {name} has triggered a safety alert.
    Location: {location['address']}
    Coordinates: {location['latitude']}, {location['longitude']}
    
    They may need immediate help.
    Reply CONFIRM to acknowledge.
    """
    
    sns_client.publish(
        PhoneNumber=phone,
        Message=message
    )

def alert_authorities(user_id, location, sos_id):
    """Alert local authorities if enabled"""
    # Integration with local police/emergency services
    # Can use Twilio, custom API, or 112 service
    pass

def start_therapy_session(user_id, sos_id):
    """Start AI therapy bot conversation"""
    therapy_table = dynamodb.Table('therapy_sessions')
    therapy_table.put_item(Item={
        'session_id': sos_id,
        'user_id': user_id,
        'started_at': datetime.utcnow().isoformat(),
        'messages': [],
        'status': 'active'
    })
```

---

## **3. AI THERAPY BOT**

### Features
```
✅ De-escalation techniques
✅ Active listening responses
✅ Crisis intervention
✅ Safety planning
✅ Emotional validation
✅ Multi-language support (Hindi, Tamil, Telugu, Kannada, etc.)
✅ Context awareness (knows situation is crisis)
✅ Escalation to human support
```

### Architecture

**Using AWS Bedrock + Claude 3**

```python
# Lambda: TherapyBot
import json
import boto3
import json
from aws_lambda_powertools import Logger

logger = Logger()
bedrock_client = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')

THERAPY_SYSTEM_PROMPT = """
You are HAVEN, an AI counselor specializing in crisis support for women.
Your role:
1. Provide immediate emotional support
2. Validate her feelings
3. De-escalate the situation
4. Help her feel safe
5. Suggest practical safety steps
6. Never minimize her concerns
7. Maintain privacy and confidentiality

Important:
- She may be in immediate danger
- Respond with compassion and urgency
- Avoid long responses (she's in crisis)
- Ask clarifying questions to understand situation
- Suggest safety actions (leave room, lock door, call someone)
- If suicidal: IMMEDIATELY suggest crisis hotline

Response format: Keep messages under 100 words.
Use simple, clear language.
Show you understand her fear.
"""

def lambda_handler(event, context):
    """Handle therapy bot conversation"""
    body = json.loads(event['body'])
    user_id = body['user_id']
    sos_id = body.get('sos_id')
    message = body['message']
    language = body.get('language', 'en')
    
    # Get conversation history
    therapy_table = dynamodb.Table('therapy_sessions')
    session = therapy_table.get_item(
        Key={'session_id': sos_id}
    )['Item']
    
    conversation_history = session.get('messages', [])
    
    # Build messages for Bedrock
    messages = [
        {
            "role": "user",
            "content": message
        }
    ]
    
    # Add conversation history (last 10 messages)
    for hist_msg in conversation_history[-10:]:
        messages.append({
            "role": hist_msg['role'],
            "content": hist_msg['content']
        })
    
    # Call Bedrock Claude
    response = bedrock_client.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-06-01",
            "max_tokens": 500,
            "system": THERAPY_SYSTEM_PROMPT,
            "messages": messages
        })
    )
    
    # Parse response
    result = json.loads(response['body'].read())
    bot_response = result['content'][0]['text']
    
    # Translate if needed
    if language != 'en':
        bot_response = translate_to_language(bot_response, language)
    
    # Store conversation
    conversation_history.append({
        'role': 'user',
        'content': message,
        'timestamp': datetime.utcnow().isoformat()
    })
    conversation_history.append({
        'role': 'assistant',
        'content': bot_response,
        'timestamp': datetime.utcnow().isoformat()
    })
    
    therapy_table.update_item(
        Key={'session_id': sos_id},
        UpdateExpression='SET messages = :msg, last_updated = :ts',
        ExpressionAttributeValues={
            ':msg': conversation_history,
            ':ts': datetime.utcnow().isoformat()
        }
    )
    
    # Check for escalation triggers (suicidal ideation, etc.)
    if check_escalation_needed(message, bot_response):
        trigger_human_support(user_id, sos_id)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'response': bot_response,
            'session_id': sos_id,
            'needs_human_support': False
        })
    }

def translate_to_language(text, language_code):
    """Translate response to user's language"""
    translate_client = boto3.client('translate')
    result = translate_client.translate_text(
        Text=text,
        SourceLanguageCode='en',
        TargetLanguageCode=language_code
    )
    return result['TranslatedText']

def check_escalation_needed(user_msg, bot_response):
    """Check if human intervention needed"""
    escalation_keywords = [
        'suicide', 'kill myself', 'end my life',
        'no way out', 'give up',
        'murder', 'weapons', 'gun'
    ]
    
    for keyword in escalation_keywords:
        if keyword.lower() in user_msg.lower():
            return True
    return False

def trigger_human_support(user_id, sos_id):
    """Connect to human counselor"""
    # Can integrate with:
    # - iCall (India)
    # - Aasra
    # - AURA
    # - BEFRIENDERS
    logger.info(f"Escalating {sos_id} to human support")
```

---

## **4. LEGAL GUIDANCE BOT**

### Features
```
✅ Indian Women's Rights knowledge
✅ Dowry Prohibition Act
✅ Protection of Women from Domestic Violence Act, 2005
✅ Sexual Harassment of Women at Workplace Act, 2013
✅ Indian Penal Code sections (354, 355, 375, etc.)
✅ Filing FIR guidance
✅ Custody & inheritance rights
✅ Multi-language support
```

### Data Structure

**Legal Knowledge Base**
```json
{
  "acts": [
    {
      "id": "dowry_act_1961",
      "name": "Dowry Prohibition Act, 1961",
      "sections": [...],
      "penalties": "Imprisonment up to 6 months + fine",
      "how_to_file": "File complaint with police or women's commission"
    },
    {
      "id": "protection_women_dv_2005",
      "name": "Protection of Women from Domestic Violence Act, 2005",
      "key_points": [
        "Applies to married & unmarried women",
        "Covers physical, sexual, emotional, economic abuse",
        "Can file for protection order, residence order, monetary relief"
      ],
      "fir_process": "File with local police station",
      "ipc_sections": [498A, 406, 420]
    }
  ],
  "procedures": [
    {
      "id": "file_fir",
      "title": "How to file an FIR",
      "steps": [
        "Go to nearest police station",
        "Request FIR against abuser",
        "Provide details of incident",
        "Police will register and investigate"
      ]
    }
  ],
  "rights": [
    {
      "category": "property_rights",
      "rights": [
        "Streedhan (dowry) is wife's property",
        "Widow has inheritance rights",
        "Equal property rights as per Hindu Succession Act"
      ]
    }
  ]
}
```

**Lambda: Legal Bot**
```python
# Lambda: LegalBot
import json
import boto3
from aws_lambda_powertools import Logger

logger = Logger()
bedrock_client = boto3.client('bedrock-runtime')
dynamodb = boto3.resource('dynamodb')

LEGAL_SYSTEM_PROMPT = """
You are HAVEN Legal Advisor, specialized in Indian Women's Rights.
You provide guidance on:
- Dowry Prohibition Act
- Protection of Women from Domestic Violence Act, 2005
- Sexual Harassment of Women at Workplace Act, 2013
- Indian Penal Code sections related to women's safety
- Filing FIR (First Information Report)
- Custody and inheritance rights
- Women's commission resources

IMPORTANT:
- You are NOT a lawyer, provide general information only
- Always recommend consulting with actual lawyer for specific cases
- Point to legal aid organizations for free help
- Provide step-by-step processes in simple language
- Keep responses concise
- Cite specific acts and sections
- Provide local women's commission contact information

Do NOT provide personal legal advice or representation.
Always suggest: "Consult with a lawyer for your specific situation"
"""

def lambda_handler(event, context):
    """Handle legal guidance queries"""
    body = json.loads(event['body'])
    user_id = body['user_id']
    query = body['query']
    language = body.get('language', 'en')
    
    # Retrieve legal knowledge base
    legal_kb = load_legal_knowledge_base()
    
    # Build context for Bedrock
    legal_context = format_legal_context(legal_kb, query)
    
    messages = [
        {
            "role": "user",
            "content": f"{query}\n\nContext:\n{legal_context}"
        }
    ]
    
    # Call Bedrock
    response = bedrock_client.invoke_model(
        modelId='anthropic.claude-3-sonnet-20240229-v1:0',
        body=json.dumps({
            "anthropic_version": "bedrock-2023-06-01",
            "max_tokens": 800,
            "system": LEGAL_SYSTEM_PROMPT,
            "messages": messages
        })
    )
    
    result = json.loads(response['body'].read())
    legal_response = result['content'][0]['text']
    
    # Add resources
    resources = get_legal_aid_resources(user_id)
    final_response = f"{legal_response}\n\n**Legal Aid Resources:**\n{resources}"
    
    # Translate
    if language != 'en':
        final_response = translate_response(final_response, language)
    
    # Store query for analytics
    store_legal_query(user_id, query, legal_response)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'response': final_response,
            'disclaimer': 'This is general information. Consult a lawyer for your case.',
            'resources': resources
        })
    }

def load_legal_knowledge_base():
    """Load legal knowledge base from S3"""
    s3_client = boto3.client('s3')
    response = s3_client.get_object(
        Bucket='haven-legal-kb',
        Key='indian_womens_rights.json'
    )
    return json.loads(response['Body'].read())

def format_legal_context(legal_kb, query):
    """Extract relevant legal information for query"""
    # Use semantic search to find relevant sections
    # Can use DynamoDB with global secondary indexes
    relevant_acts = []
    query_lower = query.lower()
    
    for act in legal_kb['acts']:
        if any(keyword in query_lower for keyword in ['dowry', 'dowry prohibition']):
            if 'dowry' in act['id']:
                relevant_acts.append(act)
        elif any(keyword in query_lower for keyword in ['domestic violence', 'abuse']):
            if 'domestic_violence' in act['id']:
                relevant_acts.append(act)
    
    return json.dumps(relevant_acts, indent=2)

def get_legal_aid_resources(user_id):
    """Get location-based legal aid resources"""
    # Get user's state/location
    # Return NGOs, women's commissions, legal aid hotlines
    resources = {
        'national': [
            'National Commission for Women: 1800-120-1947',
            'AASRA: 9820466726',
            'iCall: 1800-229-5746'
        ],
        'state_specific': []  # Will populate based on user location
    }
    return json.dumps(resources, indent=2)

def store_legal_query(user_id, query, response):
    """Store for analytics and improvement"""
    table = dynamodb.Table('legal_queries')
    table.put_item(Item={
        'query_id': str(uuid.uuid4()),
        'user_id': user_id,
        'query': query,
        'response_summary': response[:500],
        'timestamp': datetime.utcnow().isoformat()
    })
```

---

## **5. EMERGENCY CONTACT MANAGEMENT**

### Features
```
✅ Add trusted contacts
✅ Quick alert system
✅ Location sharing
✅ SOS status updates
✅ Confirmation requests
✅ Contact priorities
✅ Custom alert messages
```

### Data Model

```python
# DynamoDB Table: emergency_contacts
{
  "contact_id": "pk",
  "user_id": "sk",
  "name": "string",
  "phone": "string",
  "email": "string",
  "relationship": "enum(friend, family, counselor, police)",
  "notify_immediately": "boolean",
  "can_view_location": "boolean",
  "alert_threshold": "enum(critical, high, medium)",
  "custom_message": "string",
  "verification_status": "enum(verified, unverified)",
  "verified_at": "timestamp",
  "added_at": "timestamp",
  "priority": "int(1-5)"
}
```

### Alert Logic

```python
def send_contact_alert(contact_id, sos_id, location, severity="critical"):
    """
    Send alert to emergency contact
    """
    sns = boto3.client('sns')
    dynamodb = boto3.resource('dynamodb')
    
    # Get contact details
    contacts_table = dynamodb.Table('emergency_contacts')
    contact = contacts_table.get_item(Key={'contact_id': contact_id})['Item']
    
    # Personalize alert
    alert_messages = {
        'critical': f"""
URGENT: {contact['name']} needs help NOW!
Location: {location['address']}
GPS: {location['latitude']}, {location['longitude']}

RESPOND: Reply 'ON_WAY' to confirm you're coming
Reply 'EMS' to alert emergency services
Reply 'POLICE' to alert police
        """,
        'high': f"""
ALERT: {contact['name']} is safe but needs your presence.
Location: {location['address']}
        """,
        'medium': f"""
CHECK-IN: {contact['name']} would like you to know she's safe.
Location: {location['address']}
        """
    }
    
    # Send via SMS + Email
    sns.publish(
        PhoneNumber=contact['phone'],
        Message=alert_messages[severity]
    )
    
    # Track alert
    alert_log_table = dynamodb.Table('alert_logs')
    alert_log_table.put_item(Item={
        'alert_id': str(uuid.uuid4()),
        'sos_id': sos_id,
        'contact_id': contact_id,
        'severity': severity,
        'sent_at': datetime.utcnow().isoformat(),
        'response_status': 'awaiting',
        'location': location
    })
```

---

## **6. OFFLINE MODE & DATA SYNC**

### Features
```
✅ Works without internet
✅ Auto-sync when connected
✅ Encrypted local storage
✅ Mesh network capabilities
✅ SMS as fallback
✅ Peer-to-peer sync
```

### Implementation

**Mobile (React Native/Flutter)**

```javascript
// React Native Offline Implementation
import AsyncStorage from '@react-native-async-storage/async-storage';
import NetInfo from '@react-native-community/netinfo';
import { openDatabase } from 'react-native-sqlite-storage';

class OfflineManager {
  constructor() {
    this.db = openDatabase({ name: 'haven_local.db' });
    this.queue = [];
    this.isOnline = false;
    this.setupNetworkListener();
  }

  setupNetworkListener() {
    NetInfo.addEventListener(state => {
      this.isOnline = state.isConnected;
      if (this.isOnline && this.queue.length > 0) {
        this.syncQueue();
      }
    });
  }

  async sendSOSOffline(data) {
    /*
    If offline:
    1. Store locally with timestamp
    2. Generate unique ID
    3. Show "SOS Queued - Will send when online"
    4. When online, transmit to server
    */
    
    if (!this.isOnline) {
      // Store locally
      await this.db.executeSql(
        'INSERT INTO sos_queue (sos_data, created_at, synced) VALUES (?, ?, ?)',
        [JSON.stringify(data), Date.now(), 0]
      );
      
      // Add to queue
      this.queue.push({
        type: 'SOS',
        data: data,
        timestamp: Date.now()
      });
      
      return { status: 'queued', message: 'SOS will send when online' };
    } else {
      // Send immediately
      return this.sendSOSOnline(data);
    }
  }

  async syncQueue() {
    /*
    When connection restored:
    1. Get all queued items
    2. Send in order (oldest first)
    3. Mark as synced
    4. Handle conflicts
    */
    
    for (let item of this.queue) {
      try {
        const response = await this.sendToServer(item);
        await this.markAsSynced(item.id);
      } catch (error) {
        // Keep in queue, retry later
        console.error('Sync failed:', error);
      }
    }
    
    this.queue = []; // Clear queue
  }

  async sendToServer(item) {
    const response = await fetch(
      'https://api.haven-safety.com/sync',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${await this.getToken()}`
        },
        body: JSON.stringify(item.data)
      }
    );
    return response.json();
  }

  async markAsSynced(itemId) {
    await this.db.executeSql(
      'UPDATE sos_queue SET synced = 1 WHERE id = ?',
      [itemId]
    );
  }
}

export default OfflineManager;
```

**Server-Side Sync Handler**

```python
# Lambda: SyncHandler
@app.post("/sync")
async def sync_offline_data(request: Request):
    """
    Receive offline data from mobile app and process
    """
    data = await request.json()
    user_id = request.headers.get('user-id')
    
    # Verify signature (to prevent tampering)
    if not verify_signature(data):
        raise HTTPException(status_code=401)
    
    # Process in order of timestamp
    for item in sorted(data['queue'], key=lambda x: x['timestamp']):
        if item['type'] == 'SOS':
            process_offline_sos(user_id, item)
        elif item['type'] == 'MESSAGE':
            process_offline_message(user_id, item)
    
    return {"status": "synced", "items_processed": len(data['queue'])}
```

---

## **7. DATA SECURITY & ENCRYPTION**

### Architecture

```
┌─────────────────────────────────────────────────┐
│           Data at Different States              │
└─────────────────────────────────────────────────┘

1. AT REST (In Database)
   ├─ DynamoDB: Encrypted with AWS KMS
   ├─ S3 buckets: Server-side encryption (SSE-S3)
   ├─ User data: Client-side encryption before storage
   └─ Personal info: Tokenized (no plain names/emails)

2. IN TRANSIT (Over Network)
   ├─ HTTPS/TLS 1.3 for all API calls
   ├─ Certificate pinning in mobile app
   ├─ API Gateway WAF rules
   └─ DDoS protection (AWS Shield)

3. IN APPLICATION
   ├─ Sensitive data not logged
   ├─ No location in logs
   ├─ User IDs hashed
   └─ Short-lived tokens (1 hour expiry)
```

### Encryption Implementation

```python
# Lambda: EncryptionService
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import base64
import os

class EncryptionService:
    """Encrypt/decrypt user data"""
    
    def __init__(self):
        self.kms_client = boto3.client('kms')
        
    def encrypt_user_data(self, data, user_id):
        """
        Encrypt sensitive user data
        - Location data
        - Contact information
        - Messages
        - Emergency logs
        """
        # Get or create data encryption key per user
        dek = self.get_or_create_data_key(user_id)
        
        cipher = Fernet(dek)
        encrypted = cipher.encrypt(json.dumps(data).encode())
        
        return encrypted.decode()
    
    def decrypt_user_data(self, encrypted_data, user_id):
        """Decrypt user data"""
        dek = self.get_or_create_data_key(user_id)
        cipher = Fernet(dek)
        
        decrypted = cipher.decrypt(encrypted_data.encode())
        return json.loads(decrypted)
    
    def get_or_create_data_key(self, user_id):
        """
        Get data encryption key from AWS KMS
        KMS Master Key is managed by AWS
        Each user has unique DEK (Data Encryption Key)
        """
        secrets = boto3.client('secretsmanager')
        
        try:
            response = secrets.get_secret_value(
                SecretId=f"haven/user-dek/{user_id}"
            )
            return response['SecretString'].encode()
        except:
            # Create new DEK for this user
            response = self.kms_client.generate_data_key(
                KeyId='arn:aws:kms:region:account:key/xxx',
                KeySpec='AES_256'
            )
            
            # Store in Secrets Manager
            secrets.create_secret(
                Name=f"haven/user-dek/{user_id}",
                SecretString=base64.b64encode(
                    response['Plaintext']
                ).decode()
            )
            
            return response['Plaintext']
    
    def hash_phone_number(self, phone):
        """Hash phone before storing (no plain text)"""
        import hashlib
        return hashlib.sha256(phone.encode()).hexdigest()
    
    def tokenize_location(self, location):
        """
        Tokenize location for privacy
        Store token → location mapping in separate secure table
        """
        token = str(uuid.uuid4())
        
        # Store mapping in encrypted table
        location_table = dynamodb.Table('location_tokens')
        location_table.put_item(Item={
            'token': token,
            'location': self.encrypt_user_data(location, 'system'),
            'created_at': datetime.utcnow().isoformat(),
            'ttl': int(time.time()) + (24 * 3600)  # 24hr expiry
        })
        
        return token
```

### API Security

```python
# Security middleware
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthCredentials
import jwt

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthCredentials = Security(security)):
    """
    Verify JWT token for all API calls
    """
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=["HS256"]
        )
        user_id = payload.get("sub")
        return user_id
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/api/sos")
async def trigger_sos(
    sos_data: SOSRequest,
    user_id: str = Depends(verify_token)
):
    """All requests must have valid JWT"""
    # Process SOS
    pass

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://haven-app.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["Authorization"],
)

# Rate limiting (prevent abuse)
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/sos")
@limiter.limit("5/minute")  # Max 5 SOS per minute
async def trigger_sos(...):
    pass
```

---

# 💾 DATABASE SCHEMA

## **DynamoDB Tables**

### 1. Users Table
```
PrimaryKey: user_id (UUID)
Attributes:
- email: string
- phone_number: string (hashed)
- name: string (encrypted)
- password_hash: string
- profile_image_s3_url: string
- date_of_birth: string (encrypted)
- address: string (encrypted)
- emergency_contacts: list
- legal_aid_preferences: list
- therapy_preferences: object
- language: string
- notification_settings: object
- created_at: timestamp
- updated_at: timestamp
- last_login: timestamp
- account_status: enum(active, suspended, deleted)
- is_2fa_enabled: boolean

GlobalSecondaryIndexes:
- email-index (for quick email lookup)
- phone-index (for phone-based recovery)
```

### 2. SOS Events Table
```
PrimaryKey: sos_id (UUID)
SortKey: timestamp (ISO8601)
Attributes:
- user_id: string
- status: enum(active, resolved, cancelled)
- location: object
  - latitude: number
  - longitude: number
  - address: string
  - accuracy: int
- device_info: object
- contacts_notified: int
- authorities_notified: boolean
- duration_seconds: int
- resolution_notes: string
- created_at: timestamp
- resolved_at: timestamp
- ttl: int (24 hour expiry)

GlobalSecondaryIndexes:
- user_id-timestamp (for user's SOS history)
- status-timestamp (for analytics)
```

### 3. Therapy Sessions Table
```
PrimaryKey: session_id (UUID)
SortKey: created_at (timestamp)
Attributes:
- user_id: string
- sos_id: string (foreign key)
- messages: list of objects
  - role: enum(user, assistant)
  - content: string (encrypted)
  - timestamp: timestamp
  - sentiment: string
- session_status: enum(active, paused, completed)
- escalation_triggered: boolean
- human_support_offered: boolean
- duration_minutes: int
- notes: string (encrypted)
- created_at: timestamp
- ended_at: timestamp
- ttl: int (30 day expiry)

GlobalSecondaryIndexes:
- user_id-created_at (user's therapy history)
```

### 4. Emergency Contacts Table
```
PrimaryKey: contact_id (UUID)
SortKey: user_id (string)
Attributes:
- name: string (encrypted)
- phone: string (hashed)
- email: string (encrypted)
- relationship: enum(friend, family, counselor, authority)
- notify_immediately: boolean
- can_view_location: boolean
- alert_threshold: enum(critical, high, medium)
- custom_message: string
- verification_status: enum(verified, unverified, blocked)
- verified_at: timestamp
- added_at: timestamp
- priority: int (1-5)
- is_active: boolean

GlobalSecondaryIndexes:
- user_id-priority (for quick contact retrieval)
```

### 5. Alert Logs Table
```
PrimaryKey: alert_id (UUID)
SortKey: sent_at (timestamp)
Attributes:
- sos_id: string
- contact_id: string
- user_id: string
- alert_type: enum(sms, email, app_notification)
- severity: enum(critical, high, medium, low)
- message_content: string (encrypted)
- delivery_status: enum(sent, delivered, failed, bounced)
- response_status: enum(awaiting, confirmed, cancelled)
- response_content: string
- responded_at: timestamp
- created_at: timestamp
- ttl: int (90 day retention)

GlobalSecondaryIndexes:
- sos_id-sent_at (alerts for specific SOS)
- user_id-delivery_status (for audit)
```

### 6. Legal Queries Table
```
PrimaryKey: query_id (UUID)
SortKey: created_at (timestamp)
Attributes:
- user_id: string
- query_text: string
- query_category: enum(dowry, domestic_violence, workplace, custody, etc.)
- response_summary: string
- sources_cited: list
- user_satisfaction: int (1-5)
- feedback: string
- created_at: timestamp
- ttl: int (2 year retention)

GlobalSecondaryIndexes:
- user_id-category (for personalized legal resources)
```

### 7. Device Registrations Table
```
PrimaryKey: device_id (UUID)
SortKey: user_id (string)
Attributes:
- user_id: string
- device_type: enum(ios, android, web)
- device_name: string
- push_notification_token: string
- is_active: boolean
- last_synced: timestamp
- offline_data_size_bytes: int
- created_at: timestamp
- updated_at: timestamp
- ttl: int (2 year expiry)
```

---

# 🔌 REST API SPECIFICATION

## **Base URL**
```
https://api.haven-safety.com/v1
```

## **Authentication**
```
All endpoints require:
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json
```

## **Endpoints**

### **1. Authentication**

```
POST /auth/signup
Request:
{
  "email": "user@example.com",
  "phone": "+91-98765-43210",
  "password": "SecurePass123!",
  "name": "Priya Sharma"
}

Response:
{
  "user_id": "uuid",
  "token": "jwt_token",
  "expires_in": 3600,
  "requires_2fa": true
}

---

POST /auth/login
Request:
{
  "email": "user@example.com",
  "password": "SecurePass123!"
}

Response:
{
  "token": "jwt_token",
  "expires_in": 3600,
  "requires_2fa": true
}

---

POST /auth/verify-2fa
Request:
{
  "otp": "123456"
}

Response:
{
  "token": "jwt_token",
  "expires_in": 3600
}
```

### **2. SOS System**

```
POST /sos/trigger
Request:
{
  "location": {
    "latitude": 19.0760,
    "longitude": 72.8777,
    "address": "123 Main Street, Mumbai"
  },
  "severity": "critical"
}

Response:
{
  "sos_id": "uuid",
  "status": "active",
  "message": "Emergency alert activated",
  "contacts_notified": 3,
  "therapy_bot_ready": true
}

---

POST /sos/{sos_id}/cancel
Request:
{
  "reason": "False alarm"
}

Response:
{
  "status": "cancelled",
  "message": "SOS cancelled"
}

---

GET /sos/{sos_id}/status
Response:
{
  "sos_id": "uuid",
  "status": "active",
  "duration_seconds": 245,
  "contacts_responses": [
    {
      "contact_id": "uuid",
      "response": "ON_WAY",
      "responded_at": "2024-09-17T10:30:45Z"
    }
  ]
}
```

### **3. Therapy Bot**

```
POST /therapy/send-message
Request:
{
  "sos_id": "uuid",
  "message": "I'm so scared, I don't know what to do",
  "language": "en"
}

Response:
{
  "session_id": "uuid",
  "response": "I hear your fear, and I'm here to help...",
  "sentiment": "supportive",
  "escalation_recommended": false
}

---

GET /therapy/{session_id}/history
Response:
{
  "session_id": "uuid",
  "messages": [
    {
      "role": "user",
      "content": "...",
      "timestamp": "2024-09-17T10:15:00Z"
    },
    {
      "role": "assistant",
      "content": "...",
      "timestamp": "2024-09-17T10:15:30Z"
    }
  ]
}
```

### **4. Legal Bot**

```
POST /legal/ask
Request:
{
  "query": "What can I do about dowry demands?",
  "language": "en"
}

Response:
{
  "response": "The Dowry Prohibition Act, 1961...",
  "sources": [
    {
      "act": "Dowry Prohibition Act, 1961",
      "sections": [3, 4, 5]
    }
  ],
  "resources": [
    {
      "organization": "National Commission for Women",
      "phone": "1800-120-1947"
    }
  ],
  "disclaimer": "Consult a lawyer for your specific case"
}

---

GET /legal/resources
Query Params: state=Maharashtra
Response:
{
  "national_resources": [...],
  "state_resources": [...],
  "local_ngos": [...]
}
```

### **5. Emergency Contacts**

```
POST /contacts/add
Request:
{
  "name": "Aisha (Mom)",
  "phone": "+91-98765-43210",
  "email": "mom@example.com",
  "relationship": "family",
  "priority": 1,
  "notify_immediately": true
}

Response:
{
  "contact_id": "uuid",
  "status": "verification_pending",
  "message": "Verification code sent to contact"
}

---

POST /contacts/{contact_id}/verify
Request:
{
  "verification_code": "123456"
}

Response:
{
  "status": "verified",
  "contact_id": "uuid"
}

---

GET /contacts
Response:
{
  "contacts": [
    {
      "contact_id": "uuid",
      "name": "...",
      "relationship": "...",
      "status": "verified",
      "priority": 1
    }
  ]
}

---

DELETE /contacts/{contact_id}
Response:
{
  "status": "deleted",
  "contact_id": "uuid"
}
```

### **6. User Profile**

```
GET /profile
Response:
{
  "user_id": "uuid",
  "email": "user@example.com",
  "name": "...",
  "language": "en",
  "two_fa_enabled": true,
  "notification_preferences": {...}
}

---

PUT /profile
Request:
{
  "name": "New Name",
  "language": "hi",
  "notification_preferences": {...}
}

Response:
{
  "status": "updated",
  "user_id": "uuid"
}

---

POST /profile/change-password
Request:
{
  "current_password": "...",
  "new_password": "..."
}

Response:
{
  "status": "password_changed"
}
```

### **7. Settings & Preferences**

```
PUT /settings/notification-preferences
Request:
{
  "sms_alerts": true,
  "email_alerts": true,
  "push_notifications": true,
  "vibration": true,
  "sound_enabled": false
}

Response:
{
  "status": "updated"
}

---

PUT /settings/privacy
Request:
{
  "share_location_with_contacts": true,
  "allow_data_sharing": false,
  "data_retention_days": 90
}

Response:
{
  "status": "updated"
}
```

---

# 🎨 FRONTEND COMPONENTS

## **Mobile App Structure (React Native)**

```
App/
├── screens/
│   ├── onboarding/
│   │   ├── SignupScreen.tsx
│   │   ├── LoginScreen.tsx
│   │   └── SetupEmergencyContacts.tsx
│   │
│   ├── home/
│   │   ├── HomeScreen.tsx (dashboard)
│   │   ├── SOS_Button.tsx (main feature)
│   │   └── QuickActions.tsx
│   │
│   ├── therapy/
│   │   ├── TherapyBotScreen.tsx
│   │   ├── ChatInterface.tsx
│   │   └── TherapyHistory.tsx
│   │
│   ├── legal/
│   │   ├── LegalAdviceScreen.tsx
│   │   ├── LegalBotChat.tsx
│   │   └── ResourcesScreen.tsx
│   │
│   ├── contacts/
│   │   ├── EmergencyContactsScreen.tsx
│   │   ├── AddContactFlow.tsx
│   │   └── ContactVerification.tsx
│   │
│   ├── profile/
│   │   ├── ProfileScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   └── PrivacySettings.tsx
│   │
│   └── sos-active/
│       ├── ActiveSOSScreen.tsx
│       ├── TherapyDuringCrisis.tsx
│       └── ContactResponses.tsx
│
├── components/
│   ├── SOSButton.tsx (large, prominent)
│   ├── ChatBubble.tsx
│   ├── LocationMap.tsx
│   ├── Timer.tsx (SOS duration)
│   └── ContactCard.tsx
│
├── services/
│   ├── api/
│   │   ├── auth.ts
│   │   ├── sos.ts
│   │   ├── therapy.ts
│   │   ├── legal.ts
│   │   └── contacts.ts
│   │
│   ├── offline/
│   │   ├── OfflineManager.ts
│   │   ├── LocalStorage.ts
│   │   └── SyncQueue.ts
│   │
│   └── encryption/
│       ├── CryptoService.ts
│       └── KeyManagement.ts
│
├── redux/
│   ├── slices/
│   │   ├── authSlice.ts
│   │   ├── sosSlice.ts
│   │   ├── contactsSlice.ts
│   │   └── settingsSlice.ts
│   └── store.ts
│
└── assets/
    ├── images/
    ├── icons/
    └── translations/
        ├── en.json
        ├── hi.json
        └── [other languages]
```

## **Key Components**

### **SOS Button Component**

```jsx
// SOS_Button.tsx
import React, { useState } from 'react';
import { View, Pressable, Text, Alert } from 'react-native';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle 
} from 'react-native-reanimated';
import * as Location from 'expo-location';

const SOSButton = ({ onPress }) => {
  const [isActive, setIsActive] = useState(false);
  const scale = useSharedValue(1);

  const handlePress = async () => {
    // Get location
    const location = await Location.getCurrentPositionAsync();
    
    // Trigger SOS
    const response = await triggerSOS({
      latitude: location.coords.latitude,
      longitude: location.coords.longitude,
      address: await getAddressFromCoordinates(location.coords)
    });

    if (response.success) {
      setIsActive(true);
      // Show confirmation
      Alert.alert(
        'SOS Activated',
        'Emergency alerts have been sent to your contacts.\nStay on the line for AI support.',
        [{ text: 'I understand', onPress: () => {} }]
      );
      
      // Navigate to active SOS screen
      onPress();
    }
  };

  return (
    <Pressable 
      onPress={handlePress}
      style={styles.button}
    >
      <View style={styles.iconContainer}>
        <Text style={styles.icon}>🆘</Text>
      </View>
      <Text style={styles.text}>
        {isActive ? 'SOS ACTIVE' : 'PRESS FOR HELP'}
      </Text>
    </Pressable>
  );
};

const styles = {
  button: {
    width: '100%',
    height: 120,
    backgroundColor: '#ff4444',
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center'
  },
  iconContainer: {
    fontSize: 48
  },
  text: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 10
  }
};

export default SOSButton;
```

### **Therapy Chat Component**

```jsx
// TherapyBotChat.tsx
import React, { useState, useRef } from 'react';
import { 
  View, 
  FlatList, 
  TextInput, 
  Pressable, 
  Text, 
  ActivityIndicator 
} from 'react-native';
import { sendTherapyMessage } from '../services/api/therapy';

const TherapyChatScreen = ({ sosId }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const flatListRef = useRef();

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: input,
      timestamp: new Date()
    };
    setMessages([...messages, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await sendTherapyMessage(sosId, input);
      
      const botMessage = {
        id: Date.now() + 1,
        role: 'assistant',
        content: response.response,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, botMessage]);

      // Check if escalation needed
      if (response.escalation_recommended) {
        Alert.alert(
          'Need More Help?',
          'Would you like to connect with a human counselor?',
          [
            { text: 'Yes', onPress: () => connectToHumanSupport() },
            { text: 'No, I'm OK', onPress: () => {} }
          ]
        );
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to send message');
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <FlatList
        ref={flatListRef}
        data={messages}
        renderItem={({ item }) => (
          <ChatBubble message={item} />
        )}
        keyExtractor={item => item.id.toString()}
        onContentSizeChange={() => 
          flatListRef.current?.scrollToEnd({ animated: true })
        }
      />

      <View style={styles.inputContainer}>
        <TextInput
          style={styles.input}
          placeholder="What's on your mind?"
          value={input}
          onChangeText={setInput}
          editable={!loading}
          multiline
        />
        <Pressable 
          onPress={handleSendMessage}
          disabled={loading || !input.trim()}
        >
          {loading ? (
            <ActivityIndicator color="blue" />
          ) : (
            <Text style={styles.sendButton}>Send</Text>
          )}
        </Pressable>
      </View>
    </View>
  );
};

export default TherapyChatScreen;
```

---

# 🚀 DEPLOYMENT & DEVOPS

## **AWS Infrastructure Setup**

### **Terraform Configuration**

```hcl
# main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"  # Mumbai region
}

# DynamoDB Tables
resource "aws_dynamodb_table" "users" {
  name           = "haven_users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name            = "email-index"
    hash_key        = "email"
    projection_type = "ALL"
  }

  tags = {
    Name        = "haven-users"
    Environment = "production"
  }
}

resource "aws_dynamodb_table" "sos_events" {
  name           = "haven_sos_events"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "sos_id"
  range_key      = "timestamp"

  attribute {
    name = "sos_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name            = "user_id-timestamp"
    hash_key        = "user_id"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = {
    Name = "haven-sos"
  }
}

# S3 for logs and assets
resource "aws_s3_bucket" "haven_storage" {
  bucket = "haven-secure-storage-${data.aws_caller_identity.current.account_id}"

  tags = {
    Name = "haven-storage"
  }
}

resource "aws_s3_bucket_encryption" "haven_storage" {
  bucket = aws_s3_bucket.haven_storage.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lambda Execution Role
resource "aws_iam_role" "lambda_role" {
  name = "haven-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# Lambda functions
resource "aws_lambda_function" "sos_handler" {
  filename      = "lambda_functions/sos_handler.zip"
  function_name = "haven-sos-handler"
  role          = aws_iam_role.lambda_role.arn
  handler       = "index.lambda_handler"
  runtime       = "python3.11"
  timeout       = 30
  memory_size   = 256

  environment {
    variables = {
      DYNAMODB_SOS_TABLE = aws_dynamodb_table.sos_events.name
      SNS_TOPIC_ARN      = aws_sns_topic.sos_alerts.arn
    }
  }

  depends_on = [
    aws_iam_role.lambda_role,
    aws_iam_role_policy_attachment.lambda_basic
  ]
}

# API Gateway
resource "aws_apigatewayv2_api" "haven_api" {
  name          = "haven-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["https://haven-app.com"]
    allow_methods = ["GET", "POST", "PUT", "DELETE"]
    allow_headers = ["authorization", "content-type"]
  }
}

resource "aws_apigatewayv2_integration" "sos_integration" {
  api_id           = aws_apigatewayv2_api.haven_api.id
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  payload_format_version = "2.0"
  target           = aws_lambda_function.sos_handler.arn
}

resource "aws_apigatewayv2_route" "sos_route" {
  api_id    = aws_apigatewayv2_api.haven_api.id
  route_key = "POST /sos/trigger"
  target    = "integrations/${aws_apigatewayv2_integration.sos_integration.id}"
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "high_sos_volume" {
  alarm_name          = "haven-high-sos-volume"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "SOS Events"
  namespace           = "HAVEN/Metrics"
  period              = "300"
  statistic           = "Sum"
  threshold           = "100"
  alarm_actions       = [aws_sns_topic.alerts.arn]
}
```

### **CI/CD Pipeline (GitHub Actions)**

```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }}
          aws-region: ap-south-1
      
      - name: Build Lambda packages
        run: |
          cd lambda_functions
          for dir in */; do
            cd "$dir"
            pip install -r requirements.txt -t .
            zip -r "../${dir%/}.zip" .
            cd ..
          done
      
      - name: Deploy to AWS Lambda
        run: |
          aws lambda update-function-code \
            --function-name haven-sos-handler \
            --zip-file fileb://lambda_functions/sos_handler.zip
          
          aws lambda update-function-code \
            --function-name haven-therapy-bot \
            --zip-file fileb://lambda_functions/therapy_bot.zip
      
      - name: Deploy frontend
        run: |
          npm run build
          aws s3 sync dist/ s3://haven-frontend/ --delete
          aws cloudfront create-invalidation --distribution-id ${{ secrets.CLOUDFRONT_ID }} --paths "/*"
      
      - name: Notify Slack
        if: success()
        uses: slackapi/slack-github-action@v1
        with:
          webhook-url: ${{ secrets.SLACK_WEBHOOK }}
          payload: |
            {
              "text": "✅ HAVEN deployment successful"
            }
```

---

# 📊 TESTING STRATEGY

## **Unit Tests**

```python
# tests/test_sos_handler.py
import pytest
from unittest.mock import patch, MagicMock
from src.lambdas.sos_handler import lambda_handler

@pytest.fixture
def sos_event():
    return {
        'body': json.dumps({
            'user_id': 'user-123',
            'location': {
                'latitude': 19.0760,
                'longitude': 72.8777,
                'address': 'Mumbai'
            }
        })
    }

@patch('boto3.resource')
def test_sos_creates_record(mock_dynamodb, sos_event):
    """Test SOS trigger creates DynamoDB record"""
    mock_table = MagicMock()
    mock_dynamodb.return_value.Table.return_value = mock_table
    
    response = lambda_handler(sos_event, None)
    
    assert response['statusCode'] == 200
    mock_table.put_item.assert_called_once()

@patch('boto3.client')
def test_sos_sends_alerts(mock_sns, sos_event):
    """Test SOS sends SNS notifications"""
    mock_sns_client = MagicMock()
    mock_sns.return_value = mock_sns_client
    
    response = lambda_handler(sos_event, None)
    
    assert mock_sns_client.publish.called

def test_invalid_location_fails():
    """Test invalid location is rejected"""
    event = {
        'body': json.dumps({
            'user_id': 'user-123',
            'location': {}  # Missing latitude/longitude
        })
    }
    
    response = lambda_handler(event, None)
    assert response['statusCode'] == 400
```

## **Integration Tests**

```python
# tests/test_integration.py
import pytest
import requests
import json

@pytest.fixture
def api_client():
    return requests.Session()

def test_full_sos_flow(api_client):
    """Test complete SOS trigger → alert → therapy flow"""
    
    # 1. Trigger SOS
    response = api_client.post(
        'https://api.haven-dev.com/v1/sos/trigger',
        json={
            'location': {
                'latitude': 19.0760,
                'longitude': 72.8777,
                'address': 'Mumbai'
            }
        },
        headers={'Authorization': f'Bearer {test_token}'}
    )
    
    assert response.status_code == 200
    sos_data = response.json()
    sos_id = sos_data['sos_id']
    
    # 2. Send therapy message
    response = api_client.post(
        f'https://api.haven-dev.com/v1/therapy/send-message',
        json={
            'sos_id': sos_id,
            'message': 'I need help'
        },
        headers={'Authorization': f'Bearer {test_token}'}
    )
    
    assert response.status_code == 200
    therapy_data = response.json()
    assert 'response' in therapy_data
    
    # 3. Check SOS status
    response = api_client.get(
        f'https://api.haven-dev.com/v1/sos/{sos_id}/status',
        headers={'Authorization': f'Bearer {test_token}'}
    )
    
    assert response.status_code == 200
```

## **Load Testing**

```python
# tests/load_test.py
from locust import HttpUser, task, between

class HavenUser(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def trigger_sos(self):
        self.client.post(
            '/v1/sos/trigger',
            json={
                'location': {
                    'latitude': 19.0760,
                    'longitude': 72.8777
                }
            }
        )
    
    @task
    def send_therapy_message(self):
        self.client.post(
            '/v1/therapy/send-message',
            json={
                'sos_id': 'sos-123',
                'message': 'Help me'
            }
        )
```

---

# 📈 ANALYTICS & MONITORING

## **Key Metrics**

```
1. SOS Triggers
   - Total SOS events/day
   - Average resolution time
   - Top locations
   - Time-of-day patterns

2. Therapy Bot Performance
   - Session count
   - Average session duration
   - User satisfaction
   - Escalation rate

3. System Health
   - API latency
   - Error rate
   - Lambda invocation count
   - DynamoDB throttling

4. User Growth
   - Daily active users
   - New signups
   - Retention rate
   - Geographic distribution
```

## **CloudWatch Dashboard**

```json
{
  "widgets": [
    {
      "type": "metric",
      "properties": {
        "metrics": [
          ["HAVEN/Metrics", "SOS_Events", { "stat": "Sum" }],
          ["HAVEN/Metrics", "Therapy_Sessions", { "stat": "Sum" }],
          ["AWS/Lambda", "Invocations", {"dimensions": {"FunctionName": "haven-sos-handler"}}],
          ["AWS/Lambda", "Errors", {"dimensions": {"FunctionName": "haven-sos-handler"}}],
          ["AWS/DynamoDB", "ConsumedWriteCapacityUnits", {"dimensions": {"TableName": "haven_sos_events"}}]
        ],
        "period": 300,
        "stat": "Sum",
        "region": "ap-south-1"
      }
    }
  ]
}
```

---

# 🎬 DEMO FLOW

## **Judging Presentation (3-4 minutes)**

```
MINUTE 0-30 (Problem)
"1 in 3 women in India experience sexual harassment.
Current crisis hotlines have 30+ minute waits.
Women fear calling (abuser might hear).
We built HAVEN."

MINUTE 30-90 (Solution Demo)
1. Open app
2. Press SOS button (large red button)
3. Show instant alert confirmation
4. Show therapy bot responding
5. Show emergency contacts being notified

MINUTE 90-180 (Technical)
"Built on AWS:
- Lambda for instant processing
- Bedrock for AI therapy
- DynamoDB for secure storage
- Amplify for deployment"

MINUTE 180-240 (Impact)
"Users: Women in crisis get support in seconds, not minutes.
Emergency contacts: Know exactly where she is.
Impact: Potentially life-saving."
```

---

This is your complete HAVEN specification. Start building! 🚀

Any questions on specific components?
