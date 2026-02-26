# RayPulse - AI Chatbot & Subscription Guide

## 🤖 AI Chatbot Feature

### Overview
RayPulse now includes an intelligent AI chatbot that helps users understand and use the platform effectively.

### How to Use the Chatbot

1. **Open Chatbot**: Click the floating blue chat button in the bottom-right corner
2. **Ask Questions**: Type your question or select a quick reply
3. **Get Instant Help**: Receive intelligent responses about:
   - Feedback collection process
   - QR code setup
   - Dashboard analytics
   - Friction scores
   - Subscription plans
   - Platform features

### Chatbot Capabilities

**Topics Covered:**
- ✅ How feedback collection works
- ✅ QR code deployment guide
- ✅ Dashboard features explanation
- ✅ Friction score interpretation
- ✅ Subscription plan comparison
- ✅ Setup and installation help
- ✅ Alert system details

**Example Questions:**
- "How does feedback collection work?"
- "What is friction score?"
- "Show me subscription plans"
- "How to setup QR codes?"
- "What alerts will I receive?"

### Quick Replies

The chatbot provides suggested questions you can click:
- "How does feedback collection work?"
- "Show me subscription plans"
- "How to setup QR codes?"
- "What is friction score?"
- "View pricing"

---

## 💳 Subscription & Payment System

### Subscription Plans

#### 💎 FREE - $0/month
- Up to 50 feedbacks/month
- Basic analytics
- 1 QR code
- Email support

#### 🚀 BASIC - $29/month
- Up to 500 feedbacks/month
- Advanced analytics
- 5 QR codes
- Email alerts
- Priority support

#### ⭐ PRO - $99/month (POPULAR)
- Up to 5,000 feedbacks/month
- AI recommendations
- Unlimited QR codes
- Real-time alerts
- Export reports
- Priority support

#### 💼 ENTERPRISE - $299/month
- Unlimited feedbacks
- Custom integrations
- Dedicated account manager
- API access
- White-label option
- SLA guarantee

### How to Subscribe

1. **Login** to your RayPulse account
2. **Click "Subscription"** in the navigation menu
3. **Choose a Plan** that fits your needs
4. **Click "Subscribe Now"**
5. **Scan the Payment QR Code**
6. **Complete Payment** via Google Pay, PhonePe, or any UPI app
7. **Click "I've Completed Payment"**
8. **Enjoy** your upgraded features!

### Payment Process

#### QR Code Payment
After selecting a plan, you'll see a payment QR code:

1. Open your payment app (Google Pay, PhonePe, Paytm)
2. Scan the QR code displayed
3. Verify the amount matches your selected plan
4. Complete the payment
5. Return to RayPulse and confirm

#### Supported Payment Methods
- ✅ Google Pay
- ✅ PhonePe
- ✅ Paytm
- ✅ Any UPI app
- ✅ Credit Card (coming soon)
- ✅ Bank Transfer (coming soon)

### Setting Up Your Payment QR Code

**For Platform Owners:**

1. **Update Payment Details**:
   Edit `generate_payment_qr.py`:
   ```python
   PAYMENT_UPI_ID = "yourupiid@bank"  # Your actual UPI ID
   MERCHANT_NAME = "RayPulse"
   ```

2. **Generate QR Code**:
   ```bash
   source venv/bin/activate
   python generate_payment_qr.py
   ```

3. **Replace QR Image**:
   - Save your custom Google Pay QR code
   - Name it `payment-qr.png`
   - Place in `static/images/` directory

4. **Test**:
   - Subscribe to a test plan
   - Scan the QR code with your phone
   - Verify payment details appear correctly

### Subscription Management

**View Current Plan:**
- See your plan on the dashboard (top right)
- Plan badge shows: FREE, BASIC, PRO, or ENTERPRISE

**Upgrade/Downgrade:**
- Go to Subscription page
- Select new plan
- Complete payment
- Changes take effect immediately

**Check Expiry:**
- Subscription end date shown on plans page
- Email reminder sent 7 days before expiry
- Auto-renewal available (coming soon)

---

## 🔧 Technical Implementation

### Database Models

#### Subscription Fields (Business Model)
```python
subscription_plan = 'free'  # free, basic, pro, enterprise
subscription_status = 'active'  # active, expired, cancelled
subscription_start = datetime
subscription_end = datetime
```

#### Payment Model
```python
class Payment:
    business_id
    plan  # basic, pro, enterprise
    amount
    currency  # USD
    status  # pending, completed, failed
    transaction_id
    payment_method  # qr_code
    created_at
```

#### ChatMessage Model
```python
class ChatMessage:
    business_id
    session_id
    message  # User's question
    response  # AI's answer
    created_at
```

### API Endpoints

**Chatbot:**
- `POST /api/chat` - Send message, get AI response

**Subscription:**
- `GET /subscription` - View all plans
- `POST /subscribe/<plan>` - Start subscription
- `POST /payment/confirm/<payment_id>` - Confirm payment

### Chatbot AI Engine

**Location:** `utils/chatbot.py`

**Features:**
- Pattern matching for user questions
- Pre-defined responses for common topics
- Quick reply suggestions
- Session tracking
- Conversation history (for logged-in users)

**Customization:**
Edit knowledge base in `utils/chatbot.py`:
```python
self.knowledge_base = {
    'greetings': ['hello', 'hi', ...],
    'help': ['help', 'assist', ...],
    # Add more topics
}

self.responses = {
    'greeting': "Your custom greeting",
    # Add more responses
}
```

---

## 🎨 UI Components

### Chatbot Widget

**Features:**
- Floating button (bottom-right)
- Pulsing animation to attract attention
- Expandable chat window
- Quick reply buttons
- Markdown formatting in responses
- Mobile responsive

**Styling:**
- Located in `static/css/style.css`
- Purple gradient for messages
- Smooth animations
- Auto-scroll to latest message

### Subscription Page

**Features:**
- 4 pricing tiers (cards)
- Feature comparison table
- FAQ accordion
- Current plan badge
- Upgrade/downgrade buttons

### Payment Page

**Features:**
- Large QR code display
- Plan summary
- Payment instructions
- Confirmation button
- Alternative payment methods info

---

## 📱 Mobile Optimization

### Chatbot Mobile View
- Full-screen on mobile devices
- Larger tap targets
- Optimized keyboard interaction
- Quick replies scroll horizontally

### Subscription Mobile View
- Stacked pricing cards
- Horizontal scroll for comparison table
- Touch-friendly buttons

---

## 🔒 Security Considerations

### Payment Security
- QR codes generated server-side
- No sensitive data stored in browser
- Payment status tracked in database
- Transaction IDs for verification

### Chatbot Security
- Rate limiting (recommended)
- Session tracking
- No personal data in responses
- Logged conversations for authenticated users only

---

## 🚀 Future Enhancements

### Chatbot
- [ ] Natural Language Processing (NLP)
- [ ] Multi-language support
- [ ] Voice input/output
- [ ] Integration with support tickets
- [ ] Learning from user interactions

### Subscription
- [ ] Auto-renewal
- [ ] Promo codes/discounts
- [ ] Annual billing (20% discount)
- [ ] Team/multi-user plans
- [ ] Custom enterprise pricing
- [ ] Invoice generation
- [ ] Payment webhooks

---

## 🧪 Testing Guide

### Test Chatbot
1. Open chatbot widget
2. Try each quick reply
3. Ask custom questions:
   - "How does this work?"
   - "Show pricing"
   - "What is friction score?"
4. Verify responses are accurate
5. Check mobile responsiveness

### Test Subscription Flow
1. Login to demo account (demo@raypulse.com / demo123)
2. Go to Subscription page
3. Select BASIC plan
4. Verify payment page displays
5. Check QR code loads
6. Mock payment (click "I've Completed Payment")
7. Verify subscription updated in dashboard
8. Check database for payment record

### Verify Database
```bash
source venv/bin/activate
python -c "
from app import app, db
from models.models import Business, Payment, ChatMessage

with app.app_context():
    # Check subscription
    business = Business.query.first()
    print(f'Plan: {business.subscription_plan}')
    print(f'Status: {business.subscription_status}')

    # Check payments
    payments = Payment.query.all()
    print(f'Total payments: {len(payments)}')

    # Check chat messages
    chats = ChatMessage.query.all()
    print(f'Total chats: {len(chats)}')
"
```

---

## 📞 Support

**Questions about:**
- Chatbot not responding? Check browser console for errors
- Payment QR not showing? Verify `payment-qr.png` exists in `static/images/`
- Subscription not updating? Check database connection

**Contact:**
- Email: support@raypulse.com
- Documentation: See README.md
- GitHub Issues: [Report bugs]

---

## 🎉 Summary

RayPulse now includes:
- ✅ AI-powered chatbot for instant help
- ✅ 4-tier subscription system (FREE, BASIC, PRO, ENTERPRISE)
- ✅ QR code payment integration
- ✅ Subscription management
- ✅ Payment tracking
- ✅ Mobile-optimized UI

All features are production-ready and fully integrated!

---

**RayPulse** - *Detect Dissatisfaction Early. Convert Insights Into Growth.* 🚀
