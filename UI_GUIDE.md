# UI Guide

## Interface Overview

The Advanced RAG Pipeline features a modern, intuitive interface with three main sections accessible via the sidebar.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│  🧠 Advanced RAG Pipeline              [●] Online           │
│  Intelligent Document Retrieval & Generation                │
├──────────┬──────────────────────────────────────────────────┤
│          │                                                   │
│  💬 Chat │                                                   │
│  📤 Upload│              Main Content Area                   │
│  📊 Metrics│                                                  │
│          │                                                   │
│          │                                                   │
└──────────┴──────────────────────────────────────────────────┘
```

## 1. Chat Interface

### Features
- Clean, modern chat layout
- User messages on the right (blue)
- AI responses on the left (white)
- Source citations below each answer
- Processing time display
- Streaming response support

### Visual Elements
- **Empty State**: 
  - Large file icon
  - "Start a Conversation" heading
  - Helpful prompt text

- **Message Bubbles**:
  - Rounded corners
  - Proper spacing
  - Markdown rendering
  - Syntax highlighting for code

- **Sources Section**:
  - Collapsible source cards
  - Relevance scores
  - Document metadata
  - Snippet previews

- **Input Area**:
  - Large text input
  - Send button with icon
  - Disabled state during processing
  - Loading indicator

### Color Scheme
- User messages: Primary blue (#0ea5e9)
- AI messages: White with border
- Background: Gradient slate
- Accents: Primary blue shades

## 2. Upload Interface

### Features
- Drag-and-drop zone
- File browser option
- Upload progress
- Success/error feedback
- Document list with metadata

### Visual Elements
- **Drop Zone**:
  - Dashed border
  - Large upload icon
  - Clear instructions
  - Hover effects
  - Active state when dragging

- **Upload States**:
  - Idle: Blue icon, "Drop files here"
  - Processing: Spinning loader
  - Success: Green checkmark
  - Error: Red X with message

- **Document Cards**:
  - File icon
  - Filename
  - Size and chunk count
  - Upload timestamp
  - Status indicator

### Supported Formats
- PDF documents
- Word documents (DOCX)
- Text files (TXT)
- Markdown files (MD)
- Code files (PY, JS, TS, etc.)

## 3. Metrics Dashboard

### Features
- Real-time statistics
- Service health status
- Performance metrics
- Visual indicators

### Visual Elements
- **Stat Cards**:
  - Large numbers
  - Colored icons
  - Trend indicators
  - Descriptive labels

- **Metrics Displayed**:
  - Total Documents
  - Total Chunks
  - Total Queries
  - Average Response Time

- **Service Status**:
  - Qdrant health
  - OpenAI connectivity
  - System status
  - Color-coded indicators

### Color Coding
- Green: Healthy/Online
- Red: Down/Error
- Orange: Warning
- Blue: Information

## Design System

### Typography
- **Headings**: Bold, gradient text
- **Body**: Clean, readable sans-serif
- **Code**: Monospace font
- **Labels**: Medium weight

### Spacing
- Consistent padding: 1rem, 1.5rem, 2rem
- Card spacing: 1.5rem gaps
- Section spacing: 2rem margins

### Colors
```css
Primary: #0ea5e9 (Sky Blue)
Success: #10b981 (Green)
Error: #ef4444 (Red)
Warning: #f59e0b (Orange)
Background: Gradient from slate-50 to slate-100
Text: slate-800 (dark), slate-600 (medium)
```

### Effects
- **Glass Morphism**: 
  - Semi-transparent backgrounds
  - Backdrop blur
  - Subtle borders
  - Soft shadows

- **Animations**:
  - Smooth transitions
  - Pulse effects
  - Hover states
  - Loading spinners

### Components

#### Buttons
- Primary: Blue background, white text
- Secondary: White background, blue text
- Disabled: Reduced opacity
- Hover: Darker shade

#### Cards
- White/transparent background
- Rounded corners (1rem)
- Subtle shadow
- Border on hover

#### Inputs
- Clean borders
- Focus ring (blue)
- Placeholder text
- Error states

## Responsive Design

### Desktop (1024px+)
- Full sidebar visible
- Multi-column layouts
- Spacious padding
- Large text

### Tablet (768px - 1023px)
- Collapsible sidebar
- Two-column grids
- Medium padding
- Readable text

### Mobile (< 768px)
- Hidden sidebar (menu icon)
- Single column
- Compact padding
- Optimized text size

## Accessibility

### Features
- Semantic HTML
- ARIA labels
- Keyboard navigation
- Focus indicators
- Color contrast (WCAG AA)
- Screen reader support

### Keyboard Shortcuts
- Tab: Navigate elements
- Enter: Submit query
- Escape: Close modals
- Arrow keys: Navigate lists

## User Experience

### Loading States
- Skeleton screens
- Progress indicators
- Spinning loaders
- Disabled buttons

### Error Handling
- Clear error messages
- Retry options
- Helpful suggestions
- Non-blocking alerts

### Success Feedback
- Checkmarks
- Success messages
- Smooth transitions
- Confirmation toasts

## Best Practices

### For Users
1. Upload documents first
2. Wait for processing
3. Ask clear questions
4. Review sources
5. Refine queries as needed

### Visual Hierarchy
1. Most important: Large, bold, colored
2. Secondary: Medium, normal weight
3. Tertiary: Small, lighter color

### Interaction Patterns
- Click to select
- Drag to upload
- Hover for details
- Scroll for more

## Customization

### Theme Colors
Edit `frontend/tailwind.config.js`:
```javascript
colors: {
  primary: {
    500: '#your-color',
    600: '#your-darker-color',
  }
}
```

### Layout
Edit component files in `frontend/src/components/`

### Styling
Modify `frontend/src/index.css` for global styles

## Tips for Best Visual Experience

1. **Use a modern browser**: Chrome, Firefox, Safari, Edge
2. **Enable JavaScript**: Required for functionality
3. **Good internet connection**: For API calls
4. **Adequate screen size**: 1280px+ recommended
5. **Updated graphics drivers**: For smooth animations

## Common UI Issues

### Blurry Text
- Check browser zoom level
- Ensure proper font rendering
- Update graphics drivers

### Slow Animations
- Close other tabs
- Check CPU usage
- Disable animations if needed

### Layout Issues
- Clear browser cache
- Hard refresh (Ctrl+Shift+R)
- Check browser compatibility

## Future UI Enhancements

- [ ] Dark mode toggle
- [ ] Customizable themes
- [ ] Keyboard shortcuts panel
- [ ] Advanced search filters
- [ ] Document preview
- [ ] Query history
- [ ] Saved queries
- [ ] Export results
- [ ] Multi-language UI
- [ ] Accessibility improvements

Enjoy the beautiful interface! ✨
