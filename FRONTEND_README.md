# Legal Evolution Unified - Frontend PWA

## 🎯 Academic Research Platform

Progressive Web App (PWA) for comprehensive legal concept analysis with Reality Filter.

## ✨ Features

### 🎓 **Academic Analysis Wizard**
- Comprehensive analysis workflow for SSRN publications
- Reality Filter (mandatory) - prevents hallucinations
- Export to PDF/LaTeX/JSON
- Step-by-step guided process

### 🌳 **RootFinder - Legal Genealogy Tree**
- Interactive "Tree of Life" for legal principles
- Trace ancestors and descendants of legal concepts
- D3.js visualization with zoom/pan
- Click nodes to re-analyze

### 💼 **My Workspace**
- Save and organize analyses
- Search and filter by type
- Compare multiple analyses
- Export entire workspace

### 📊 **Integrated Tools**
- **JurisRank**: Legal fitness via citation networks
- **RootFinder**: Genealogical tracking
- **Iusmorfos**: Transplant prediction
- **PSM**: Causal inference
- **Peralta**: Bootstrap validation

## 🚀 Quick Start

### Development
```bash
# Install dependencies (already done)
npm install

# Start dev server
npm run dev

# Access at http://localhost:3000
```

### Production Build
```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## 🔧 Architecture

### Tech Stack
- **React 19** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Styling
- **D3.js** - Genealogical tree visualization
- **Recharts** - Charts & graphs
- **React Router** - Navigation
- **Axios** - API communication
- **Lucide React** - Icons

### Project Structure
```
frontend/
├── src/
│   ├── components/      # Reusable components
│   │   └── GenealogicalTree.tsx  # D3 tree visualization
│   ├── pages/          # Route pages
│   │   ├── Dashboard.tsx         # Main dashboard
│   │   ├── AcademicWizard.tsx    # Analysis wizard
│   │   ├── RootFinderPage.tsx    # Genealogy tool
│   │   └── Workspace.tsx         # Saved analyses
│   ├── services/       # API & storage
│   │   ├── api.ts               # FastAPI integration
│   │   └── storage.ts           # LocalStorage wrapper
│   ├── types/          # TypeScript definitions
│   ├── utils/          # Utilities
│   ├── App.tsx         # Root component
│   └── main.tsx        # Entry point
├── public/
│   ├── manifest.json   # PWA manifest
│   └── sw.js          # Service worker
└── index.html         # HTML entry
```

## 🌐 PWA Features

### Installable
- Can be installed as native app on mobile/desktop
- Works offline with service worker caching
- App-like experience with no browser chrome

### Responsive
- Mobile-first design
- Works on phones, tablets, desktops
- Touch-friendly interactions

### Offline Support
- Service worker caches resources
- LocalStorage for data persistence
- Works without internet (after first load)

## 🔌 API Integration

Connects to FastAPI backend at `http://localhost:8000`

### Endpoints Used
- `POST /api/v1/analyze` - Comprehensive analysis
- `POST /api/v1/fitness` - Fitness calculation
- `GET /api/v1/genealogy/ancestors` - Get ancestors
- `GET /api/v1/genealogy/descendants` - Get descendants
- `POST /api/v1/transplant/predict` - Transplant prediction

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to change color scheme:
```js
colors: {
  primary: { ... },    // Main accent color
  academic: { ... },   // Academic theme color
}
```

### Reality Filter
Reality Filter is **mandatory** and cannot be disabled. It's integrated into all analysis workflows to ensure academic accuracy.

## 📱 Mobile Usage

### Install as App
1. Open in mobile browser
2. Tap "Add to Home Screen"
3. Launch like native app

### Offline Mode
1. Visit app once online
2. Service worker caches resources
3. Use offline - data saved locally

## 🔒 Security & Privacy

### Data Storage
- All data stored locally in browser (LocalStorage)
- No external tracking or analytics
- Export/import for backup

### API Communication
- HTTPS in production (configure proxy)
- CORS enabled for API calls
- No sensitive data in URLs

## 📚 Academic Workflow

### Typical Research Flow
1. **Start Wizard** → Configure analysis parameters
2. **Reality Filter** → Automatic verification
3. **View Results** → Comprehensive report
4. **Export** → PDF/LaTeX for publication
5. **Save** → Store in workspace
6. **Compare** → Analyze multiple cases

### RootFinder Workflow
1. **Enter Concept** → Legal principle to trace
2. **Set Depth** → How many generations
3. **Visualize Tree** → Interactive genealogy
4. **Explore** → Click nodes to navigate
5. **Export** → JSON for further analysis

## 🐛 Troubleshooting

### Build Errors
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues
Check `vite.config.ts` proxy configuration:
```ts
proxy: {
  '/api': {
    target: 'http://localhost:8000',
    changeOrigin: true,
  },
}
```

### TypeScript Errors
```bash
# Regenerate TypeScript cache
npx tsc --noEmit
```

## 🚧 Future Enhancements

- [ ] Real-time collaboration
- [ ] Cloud sync for workspace
- [ ] Advanced export templates
- [ ] Batch processing
- [ ] Custom visualization themes
- [ ] Citation management integration
- [ ] Multi-language support

## 📄 License

MIT License - See main repository LICENSE file

## 🤝 Contributing

See main repository CONTRIBUTING.md

---

**Built for academic rigor with Reality Filter verification**
