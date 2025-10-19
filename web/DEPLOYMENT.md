# 🚀 Vercel Deployment Guide

## Quick Deploy (Recommended)

### Option 1: Deploy with Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy from web directory:**
   ```bash
   cd "/Users/hamdannishad/Desktop/ASL Translator/web"
   vercel --prod
   ```

4. **Follow prompts:**
   - Set up and deploy? `Y`
   - Which scope? Select your account
   - Link to existing project? `N`
   - Project name: `asl-translator` (or your choice)
   - Directory: `./` (default)
   - Override settings? `N`

5. **Done!** Your site will be live at the provided URL.

---

### Option 2: Deploy via GitHub (Automatic Deployments)

1. **Push web folder to GitHub:**
   ```bash
   cd "/Users/hamdannishad/Desktop/ASL Translator"
   git add web/
   git commit -m "Add web application for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel:**
   - Go to https://vercel.com
   - Click "Add New" → "Project"
   - Import your `asl-translator` repository
   - Set **Root Directory** to `web`
   - Click "Deploy"

3. **Automatic Deployments:**
   - Every push to `main` branch auto-deploys!
   - Preview deployments for pull requests

---

## Environment Variables (Optional)

If needed, add in Vercel dashboard:
- Settings → Environment Variables
- Add key-value pairs
- Redeploy to apply

---

## Custom Domain (Optional)

1. Go to your project in Vercel
2. Settings → Domains
3. Add your custom domain
4. Update DNS records as instructed

---

## Build Settings (Already Configured)

These are in `vercel.json`:
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs"
}
```

---

## Testing Locally

Before deploying, test locally:
```bash
cd web
npm run build
npm start
```
Visit http://localhost:3000

---

## Troubleshooting

### Build fails?
- Run `npm install` again
- Check Node.js version (need 18+)
- Clear cache: `rm -rf .next node_modules && npm install`

### Camera not working on deployed site?
- Vercel uses HTTPS automatically (required for camera)
- Check browser permissions
- Test in different browser

### Performance issues?
- Vercel Edge Network handles this automatically
- Consider upgrading Vercel plan for more bandwidth

---

## Post-Deployment

1. **Update README.md** with live URL
2. **Test all features:**
   - Camera access ✓
   - Letter detection ✓
   - Text output ✓
   - Mobile responsive ✓
3. **Share your link!** 🎉

---

## Support

Issues? Check:
- Vercel Dashboard logs
- Browser console
- GitHub Issues: https://github.com/Hamdan772/asl-translator/issues
