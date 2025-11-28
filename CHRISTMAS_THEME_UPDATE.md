# Christmas Theme Update Instructions

## Changes to Make for v1.1.0

### 1. Update `frontend/src/index.css`

Add this at the top of the file:

```css
/* 🎄 Christmas Theme 🎄 */
:root {
  --christmas-red: #c41e3a;
  --christmas-green: #165b33;
  --christmas-gold: #ffd700;
  --christmas-white: #f8f9fa;
  --snow-white: #ffffff;
}

body {
  background: linear-gradient(135deg, var(--christmas-red) 0%, var(--christmas-green) 100%);
  background-attachment: fixed;
}

/* Snowflake animation */
@keyframes snowfall {
  0% {
    transform: translateY(-10vh) rotate(0deg);
    opacity: 1;
  }
  100% {
    transform: translateY(100vh) rotate(360deg);
    opacity: 0.3;
  }
}

.snowflake {
  position: fixed;
  top: -10vh;
  color: white;
  font-size: 1.5em;
  animation: snowfall linear infinite;
  pointer-events: none;
  z-index: 9999;
}
```

### 2. Update `frontend/src/App.jsx`

Add snowflakes and Christmas styling. Find the main return statement and add:

```jsx
// Add this function before the return statement
const Snowflakes = () => {
  return (
    <>
      {[...Array(20)].map((_, i) => (
        <div
          key={i}
          className="snowflake"
          style={{
            left: `${Math.random() * 100}%`,
            animationDuration: `${5 + Math.random() * 10}s`,
            animationDelay: `${Math.random() * 5}s`,
            fontSize: `${0.5 + Math.random() * 1}em`,
          }}
        >
          ❄
        </div>
      ))}
    </>
  );
};

// Then in the return, add <Snowflakes /> at the top
return (
  <div className="min-h-screen bg-gradient-to-br from-red-900 via-green-900 to-red-900">
    <Snowflakes />
    {/* rest of your JSX */}
```

### 3. Update Colors Throughout

Replace blue colors with Christmas colors:
- `bg-blue-500` → `bg-red-600` (Christmas red)
- `bg-blue-600` → `bg-green-700` (Christmas green)
- `text-blue-600` → `text-red-600`
- `hover:bg-blue-700` → `hover:bg-red-700`

### 4. Add Christmas Message

In the header or welcome section, add:

```jsx
<div className="text-center mb-4">
  <h2 className="text-2xl font-bold text-yellow-300">
    🎄 Happy Holidays! 🎅
  </h2>
  <p className="text-white">Special Christmas Edition</p>
</div>
```

### 5. Update VERSION

```bash
echo "1.1.0" > VERSION
```

### 6. Commit and Push

```bash
git add -A
git commit -m "v1.1.0: Christmas Theme 🎄

- Added festive red and green color scheme
- Animated snowflakes
- Christmas holiday message
- Updated to version 1.1.0"

git push origin main
```

### 7. Create Package

```bash
chmod +x create-package.sh && ./create-package.sh
```

### 8. Create v1.1.0 Release

1. Go to: https://github.com/Vexalabs/AIP-Notebook/releases
2. Click "Create a new release"
3. Tag: `v1.1.0`
4. Title: "AIP Notebooks v1.1.0 - 🎄 Christmas Edition"
5. Description:
   ```markdown
   ## 🎄 What's New
   
   - ❄️ Festive Christmas theme with red and green colors
   - ⛄ Animated snowflakes
   - 🎅 Holiday greetings
   - 🎁 Improved user experience
   
   Happy Holidays from the AIP Notebooks team!
   ```
6. Upload: `dist/AIP-Model-Builder-Installer.tar.gz`
7. Publish release

### 9. Test the Update

1. Go back to your v1.0.0 installation
2. Launch the app
3. Should see "Update Available: v1.1.0"
4. Click "Update Now"
5. After update and restart, you should see:
   - ✅ Christmas red/green theme
   - ✅ Snowflakes falling
   - ✅ Holiday message
   - ✅ Version shows 1.1.0

---

## Quick Commands Summary

```bash
# In new clone directory
cd C:\Temp\AIP-Notebook

# Make the changes above, then:
echo "1.1.0" > VERSION
git add -A
git commit -m "v1.1.0: Christmas Theme 🎄"
git push origin main
wsl -d Ubuntu bash -c "cd $(pwd) && chmod +x create-package.sh && ./create-package.sh"

# Then create release on GitHub with the package
```
