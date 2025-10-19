# ASL Translator Web Application

🤟 **Real-time American Sign Language recognition in your browser!**

This is the web version of ASL Translator, built with Next.js and deployed on Vercel.

## ✨ Features

- 🎯 **24 ASL Letters Recognition** (A-Y, excluding J/Z)
- ⚡ **Real-time Detection** using MediaPipe Hands
- 🎨 **Beautiful Modern UI** with Tailwind CSS
- 🔒 **100% Privacy** - All processing in your browser
- 📱 **Responsive Design** - Works on desktop and mobile
- 🚀 **Ultra-fast** - Powered by Next.js and Vercel

## 🚀 Live Demo

**Visit:** https://web-1j5h4ycct-epokatrandomstuff-4004s-projects.vercel.app

🎉 **Try it now!** No installation required - works in your browser!

## 🛠️ Tech Stack

- **Next.js 14.0.4** - React framework
- **TypeScript** - Type safety
- **MediaPipe Hands** - Hand tracking AI
- **TensorFlow.js** - Machine learning
- **Tailwind CSS** - Modern styling
- **React Webcam** - Camera access

## 💻 Local Development

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Run development server:**
   ```bash
   npm run dev
   ```

3. **Open browser:**
   Navigate to `http://localhost:3000`

## 📦 Build & Deploy

### Build for production:
```bash
npm run build
npm start
```

### Deploy to Vercel:
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
vercel --prod
```

Or connect your GitHub repository to Vercel for automatic deployments!

## 🎯 How to Use

1. **Allow Camera Access** - Grant permission when prompted
2. **Show Your Hand** - Display the back of your hand to camera
3. **Make ASL Letters** - Form letters A-Y
4. **Hold for 1 Second** - Keep gesture steady to add letter
5. **Wait 1.5 Seconds** - Cooldown between letters
6. **Build Words** - Use Space, Backspace, and Clear buttons

## 📝 Supported Letters

**24 Letters:** A, B, C, D, E, F, G, H, I, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y

**Not Supported:** J and Z (require motion)

## 🔧 Configuration

### Adjust Detection Sensitivity

Edit `utils/aslClassifier.ts`:
- `smoothingThreshold` - Frames needed for detection (default: 1/7)
- Confidence thresholds - Minimum confidence (default: 0.40)
- Distance/angle thresholds - Letter pattern tolerances

### Customize UI

Edit `tailwind.config.js` for colors and theme:
```js
colors: {
  primary: '#00D9FF',    // Cyan
  secondary: '#FF00E5',   // Magenta
  accent: '#FFD700',      // Gold
}
```

## 📁 Project Structure

```
web/
├── pages/              # Next.js pages
│   ├── index.tsx       # Main landing page
│   ├── _app.tsx        # App wrapper
│   └── _document.tsx   # HTML document
├── components/         # React components
│   ├── ASLDetector.tsx # Main detection component
│   ├── LetterDisplay.tsx
│   ├── TextOutput.tsx
│   ├── Controls.tsx
│   └── HelpGuide.tsx
├── utils/              # Utilities
│   └── aslClassifier.ts # ASL classification logic
├── styles/             # Global styles
│   └── globals.css
├── package.json        # Dependencies
├── next.config.js      # Next.js config
├── tailwind.config.js  # Tailwind config
└── vercel.json         # Vercel config
```

## 🐛 Troubleshooting

### Camera not working?
- Check browser permissions
- Use HTTPS (required for camera access)
- Try different browser (Chrome/Edge recommended)

### Low detection accuracy?
- Ensure good lighting
- Show back of hand clearly
- Adjust distance from camera
- Check sensitivity settings

### Performance issues?
- Close other tabs
- Use modern browser
- Check system resources

## 📄 License

MIT License - See main repository

## 🔗 Links

- **Main Repository:** https://github.com/Hamdan772/asl-translator
- **Desktop Version:** See main repo README
- **Report Issues:** GitHub Issues

## 👨‍💻 Author

**Hamdan Nishad**
- GitHub: [@Hamdan772](https://github.com/Hamdan772)

---

Built with ❤️ for accessibility and education
