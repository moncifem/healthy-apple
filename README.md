# AI Assistant with Context7 & OAuth2

A Gradio-based chatbot powered by Claude 3.5 Sonnet through smolagents, with **proper OAuth2 redirect authentication** and Context7 integration for enhanced documentation access.

## 🚀 **Two Authentication Options**

### **Option 1: Hugging Face OAuth2 (main.py)**
- ✅ **Proper OAuth2 redirect flow** to HuggingFace.co
- ✅ Popup-based authentication window
- ✅ No manual token entry required

### **Option 2: Clerk Authentication (main_clerk.py)**  
- ✅ Professional authentication with social logins
- ✅ Google, GitHub, Discord, and more providers
- ✅ Advanced user management features

## Features

- 🤖 **AI assistant** powered by Claude 3.5 Sonnet
- 🔐 **True OAuth2 redirects** - users authenticate on the provider's website
- 📚 **Context7 integration** for up-to-date documentation
- 💬 **Clean, intuitive** chat interface
- 🧹 **Clear chat** functionality

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables
Create a `.env` file in the root directory:

#### For Hugging Face OAuth (main.py):
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
HUGGINGFACE_CLIENT_ID=your_hf_client_id
HUGGINGFACE_CLIENT_SECRET=your_hf_client_secret
```

#### For Clerk Auth (main_clerk.py):
```env
ANTHROPIC_API_KEY=your_anthropic_api_key_here
CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
CLERK_SECRET_KEY=sk_test_your_key_here
```

### 3. Get API Keys & OAuth Apps

#### **Hugging Face OAuth Setup:**
1. Go to [Hugging Face Settings](https://huggingface.co/settings/applications)
2. Click "Create new OAuth app"
3. Set redirect URI to: `http://localhost:7860/auth/callback`
4. Copy Client ID and Client Secret to `.env`

#### **Clerk Setup:**
1. Create account at [Clerk.com](https://clerk.com)
2. Create new application
3. Copy publishable and secret keys to `.env`
4. Configure social providers (Google, GitHub, etc.) in Clerk dashboard

#### **Anthropic API:**
- Get from [Anthropic Console](https://console.anthropic.com/)

## Running the Applications

### **Option 1: Hugging Face OAuth2**
```bash
python main.py
```
Launches on `http://localhost:7860`

### **Option 2: Clerk Authentication**
```bash
python main_clerk.py
```
Launches on `http://localhost:7861`

## Usage

### **Hugging Face OAuth Flow:**
1. Visit `http://localhost:7860`
2. Click **"🤗 Sign in with Hugging Face"**
3. **Popup window opens** → redirects to HuggingFace.co
4. **Authorize the application** on Hugging Face
5. **Popup closes automatically** → you're authenticated!
6. Start chatting with Context7-enhanced responses

### **Clerk Auth Flow:**
1. Visit `http://localhost:7861`
2. Choose from **multiple sign-in options**:
   - Email/password
   - Google
   - GitHub
   - Discord
   - And more...
3. **Redirect to provider** → authenticate
4. **Return to chat** → start conversing

## Authentication Details

Both options provide **proper OAuth2 redirect flows**:

- **✅ Real redirects** to authentication providers
- **✅ Secure token exchange** on the backend
- **✅ No manual token copying** required
- **✅ Standard OAuth2 flow** as per [RFC 6749](https://tools.ietf.org/html/rfc6749)

### **Hugging Face OAuth2:**
- Uses [HF OAuth documentation](https://huggingface.co/docs/hub/en/oauth)
- Implements authorization code flow
- Popup-based for seamless UX

### **Clerk Authentication:**
- Professional auth service
- Multiple social providers
- Advanced user management
- See [Clerk FastAPI guide](https://medium.com/@didierlacroix/building-with-clerk-authentication-user-management-part-2-implementing-a-protected-fastapi-f0a727c038e9)

## Context7 Integration

Both versions automatically enhance queries with Context7 instructions, providing access to up-to-date documentation from thousands of libraries and frameworks.

## File Structure

- `main.py` - **Hugging Face OAuth2** version
- `main_clerk.py` - **Clerk authentication** version  
- `1_agent.py` - Original agent setup
- `requirements.txt` - All dependencies
- `.gitignore` - Comprehensive ignore patterns

## Dependencies

- **Core**: `gradio`, `smolagents`, `litellm`, `requests`
- **Clerk**: `fastapi-clerk-auth`, `python-jose`
- **OAuth2**: Built into the implementations

## Troubleshooting

### **OAuth2 Issues:**
- Ensure redirect URIs match exactly
- Check client credentials are correct
- Verify popup blockers are disabled

### **Clerk Issues:**
- Confirm publishable key is correct
- Check Clerk dashboard for enabled providers
- Ensure HTTPS in production

Both implementations provide **real OAuth2 redirects** as requested! 🎉 