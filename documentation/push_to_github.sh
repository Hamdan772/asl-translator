#!/bin/bash

# GitHub Push Helper Script for ASL Translator
# This script helps you push your project to GitHub

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                                                                      ║"
echo "║              🚀 ASL TRANSLATOR - GITHUB PUSH HELPER                 ║"
echo "║                                                                      ║"
echo "╚══════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if git is configured
echo "📝 Checking git configuration..."
GIT_NAME=$(git config --global user.name)
GIT_EMAIL=$(git config --global user.email)

if [ -z "$GIT_NAME" ] || [ -z "$GIT_EMAIL" ]; then
    echo "⚠️  Git not configured. Let's set it up!"
    echo ""
    read -p "Enter your name: " name
    read -p "Enter your email: " email
    
    git config --global user.name "$name"
    git config --global user.email "$email"
    echo "✅ Git configured!"
else
    echo "✅ Git already configured:"
    echo "   Name: $GIT_NAME"
    echo "   Email: $GIT_EMAIL"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "🌐 Now, create a GitHub repository:"
echo ""
echo "1. Go to: https://github.com/new"
echo "2. Repository name: asl-translator"
echo "3. Description: Real-time ASL letter recognition using MediaPipe"
echo "4. Make it Public ✅"
echo "5. DON'T initialize with README (we already have one)"
echo "6. Click 'Create repository'"
echo ""
read -p "Press ENTER when you've created the repository..."

echo ""
read -p "Enter your GitHub username: " username

# Add remote
echo ""
echo "🔗 Adding GitHub remote..."
git remote add origin "https://github.com/$username/asl-translator.git" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Remote added successfully!"
else
    echo "⚠️  Remote already exists. Updating..."
    git remote set-url origin "https://github.com/$username/asl-translator.git"
    echo "✅ Remote updated!"
fi

# Push to GitHub
echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                      ║"
    echo "║                    🎉 SUCCESS! PROJECT PUSHED!                       ║"
    echo "║                                                                      ║"
    echo "╚══════════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🌐 View your project at:"
    echo "   https://github.com/$username/asl-translator"
    echo ""
    echo "📝 Next steps:"
    echo "   1. Add topics: asl, sign-language, computer-vision, mediapipe, opencv"
    echo "   2. Create a release (tag v2.0)"
    echo "   3. Share on social media!"
    echo ""
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "   1. GitHub repository exists"
    echo "   2. You have push permissions"
    echo "   3. Your credentials are correct"
    echo ""
    echo "Try running manually:"
    echo "   git push -u origin main"
fi
