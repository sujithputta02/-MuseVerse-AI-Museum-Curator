# 🔒 Security Policy

## API Key Management

### ⚠️ Important Security Notice

**NEVER commit your actual Google API key to the repository!**

### ✅ Secure Setup

1. **Get Your Own API Key**
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Keep it private

2. **Configure Locally**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your key
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. **Verify .gitignore**
   - The `.env` file is already in `.gitignore`
   - This prevents accidental commits
   - Never remove `.env` from `.gitignore`

### 🚫 What NOT to Do

❌ Don't hardcode API keys in code
❌ Don't commit `.env` file
❌ Don't share API keys in documentation
❌ Don't post API keys in issues/PRs
❌ Don't include keys in screenshots

### ✅ What TO Do

✅ Use environment variables (`.env` file)
✅ Use `.env.example` as template
✅ Keep `.env` in `.gitignore`
✅ Rotate keys if exposed
✅ Use separate keys for dev/prod

## If You Accidentally Expose a Key

1. **Immediately revoke the key** at [Google AI Studio](https://makersuite.google.com/app/apikey)
2. **Generate a new key**
3. **Update your local `.env` file**
4. **Never reuse the exposed key**

## Repository Security

### Protected Files

These files should NEVER contain real API keys:
- `README.md`
- `INSTALLATION.md`
- `kaggle_notebook.ipynb`
- Any `.py` files
- Any `.md` files

### Safe Files

Only these files should contain your actual key:
- `.env` (local only, never committed)

### Example Files

These files show the format but use placeholders:
- `.env.example` - Template with `your_api_key_here`

## Best Practices

### For Development

```bash
# Good: Use environment variable
import os
api_key = os.getenv('GOOGLE_API_KEY')

# Bad: Hardcoded key
api_key = 'AIzaSy...'  # NEVER DO THIS
```

### For Deployment

- Use secret management services (Google Secret Manager, AWS Secrets Manager)
- Set environment variables in deployment platform
- Never include keys in Docker images
- Use separate keys for different environments

### For Collaboration

- Share `.env.example` (with placeholders)
- Document how to get API keys
- Never share actual keys via email/chat
- Use secure key sharing tools if needed

## Reporting Security Issues

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: your.email@example.com
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

## Security Checklist

Before committing:
- [ ] No API keys in code
- [ ] `.env` is in `.gitignore`
- [ ] Only placeholders in documentation
- [ ] No keys in notebooks
- [ ] No keys in config files

Before pushing:
- [ ] Run `git diff` to review changes
- [ ] Check for accidental key exposure
- [ ] Verify `.env` is not staged

Before sharing:
- [ ] Remove any test keys
- [ ] Clear output cells in notebooks
- [ ] Review all documentation

## Additional Resources

- [Google API Key Best Practices](https://cloud.google.com/docs/authentication/api-keys)
- [GitHub Security Best Practices](https://docs.github.com/en/code-security)
- [OWASP API Security](https://owasp.org/www-project-api-security/)

---

**Remember: Security is everyone's responsibility!** 🔒

**Last Updated:** November 21, 2025
