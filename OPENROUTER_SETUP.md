# OpenRouter Setup Guide 🚀

## Why OpenRouter?

- **100% FREE** - No credit card required
- **Multiple Models** - Access to Llama 2, OpenChat, Mistral, and more
- **Fast & Reliable** - Community-run inference service
- **No Quotas** - Reasonable free tier with no artificial limits
- **Easy Integration** - Simple REST API

## Step-by-Step Setup

### Step 1: Create OpenRouter Account

1. Go to https://openrouter.ai
2. Click "Sign Up"
3. Choose either:
   - Sign up with email
   - Sign up with GitHub
4. **No credit card needed!**

### Step 2: Get Your API Key

1. After account creation, go to https://openrouter.ai/keys
2. Click "Create Key"
3. Give it a name (e.g., "LearnSphere")
4. Copy the generated key (looks like: `sk-...`)
5. **Keep this safe!** Don't share it publicly

### Step 3: Add to LearnSphere

1. Open your `.env` file (created from `.env.example`)
2. Replace the placeholder with your actual key:
   ```
   OPENROUTER_API_KEY=sk_your_actual_key_here
   ```
3. Save the file

### Step 4: Verify Setup

Run LearnSphere and check that it prints:
```
✓ OpenRouter API configured successfully
  Using model: google/gemma-3-27b-it:free
```

## Available Free Models

LearnSphere uses **Google Gemma 3.27B** by default - the most powerful free option available!

| Model | Speed | Quality | ID |
|-------|-------|---------|-----|
| Google Gemma 3.27B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | `google/gemma-3-27b-it:free` |
| Llama 2 7B | ⭐⭐⭐ | ⭐⭐⭐ | `meta-llama/llama-2-7b-chat` |
| OpenChat 7B | ⭐⭐⭐⭐ | ⭐⭐⭐ | `openchat/openchat-7b` |
| Mistral 7B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | `mistralai/mistral-7b-instruct` |

Check https://openrouter.ai/models for more free models and their IDs.

## First Generation Test

1. Start LearnSphere: `python app.py`
2. Open http://localhost:5000
3. Try generating: 
   - Topic: "Machine Learning"
   - Level: "Beginner"
   - Mode: "Text"
4. Click "Generate Content"

First request takes 5-10 seconds (model warming up), then responses are faster!

## Troubleshooting

### "OpenRouter API error: 401"
- Check your API key in `.env`
- Make sure it starts with `sk-`
- Go to https://openrouter.ai/keys to verify it's still active

### "Connection timeout"
- Check your internet connection
- OpenRouter servers might be temporarily busy
- Wait a minute and try again

### "Invalid model"
- Make sure the model ID is exactly correct
- Copy from the [models page](https://openrouter.ai/models)
- Some models may be temporarily unavailable

### Slow Responses
- Llama 2 is slower (~10-15 seconds) but free and reliable
- Try OpenChat or Mistral for faster responses
- First request of the day is usually slower

## API Documentation

For more details, see:
- OpenRouter Docs: https://openrouter.ai/docs
- Models List: https://openrouter.ai/models
- API Status: https://openrouter.ai/status

## Features Working with OpenRouter

✅ Text explanations  
✅ Python code generation  
✅ Audio conversion (gTTS)  
✅ Visual diagram prompts  
✅ All learning levels  
✅ Multiple content modes  

## Cost

**FREE!** 🎉

- No payment method required
- No hidden charges
- No quota restrictions (reasonable limits)
- Community-supported

---

Happy learning with LearnSphere! 📚
