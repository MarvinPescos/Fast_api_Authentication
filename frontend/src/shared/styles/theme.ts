// Modern Design System - Purple & Yellow Theme
// Inspired by your logo's gradient aesthetic

export const theme = {
  // Color Palette
  colors: {
    // Primary Purple Gradient
    primary: {
      50: "#faf5ff",
      100: "#f3e8ff",
      200: "#e9d5ff",
      300: "#d8b4fe",
      400: "#c084fc",
      500: "#a855f7", // Main purple
      600: "#9333ea",
      700: "#7e22ce",
      800: "#6b21a8",
      900: "#581c87",
    },
    // Accent Yellow
    accent: {
      50: "#fefce8",
      100: "#fef9c3",
      200: "#fef08a",
      300: "#fde047",
      400: "#facc15", // Main yellow
      500: "#eab308",
      600: "#ca8a04",
      700: "#a16207",
      800: "#854d0e",
      900: "#713f12",
    },
    // Neutrals
    gray: {
      50: "#f9fafb",
      100: "#f3f4f6",
      200: "#e5e7eb",
      300: "#d1d5db",
      400: "#9ca3af",
      500: "#6b7280",
      600: "#4b5563",
      700: "#374151",
      800: "#1f2937",
      900: "#111827",
    },
    // Semantic Colors
    success: "#10b981",
    error: "#ef4444",
    warning: "#f59e0b",
    info: "#3b82f6",

    // Dark Theme
    dark: {
      bg: "#0a0a0a",
      surface: "#1a1a1a",
      border: "rgba(255, 255, 255, 0.1)",
    },
  },

  // Gradients
  gradients: {
    primary: "linear-gradient(135deg, #a855f7 0%, #7e22ce 100%)",
    accent: "linear-gradient(135deg, #fde047 0%, #facc15 100%)",
    hero: "linear-gradient(135deg, #a855f7 0%, #7e22ce 50%, #facc15 100%)",
    subtle:
      "linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(250, 204, 21, 0.1) 100%)",
    glass:
      "linear-gradient(135deg, rgba(255, 255, 255, 0.1) 0%, rgba(255, 255, 255, 0.05) 100%)",
  },

  // Shadows
  shadows: {
    sm: "0 1px 2px 0 rgba(0, 0, 0, 0.05)",
    md: "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
    lg: "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
    xl: "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
    glow: "0 0 20px rgba(168, 85, 247, 0.3), 0 0 40px rgba(250, 204, 21, 0.2)",
    glowPurple: "0 0 30px rgba(168, 85, 247, 0.5)",
    glowYellow: "0 0 30px rgba(250, 204, 21, 0.5)",
  },

  // Spacing
  spacing: {
    xs: "0.5rem", // 8px
    sm: "0.75rem", // 12px
    md: "1rem", // 16px
    lg: "1.5rem", // 24px
    xl: "2rem", // 32px
    "2xl": "3rem", // 48px
    "3xl": "4rem", // 64px
  },

  // Border Radius
  radius: {
    sm: "0.375rem", // 6px
    md: "0.5rem", // 8px
    lg: "0.75rem", // 12px
    xl: "1rem", // 16px
    "2xl": "1.5rem", // 24px
    full: "9999px",
  },

  // Typography
  fonts: {
    sans: "Inter, system-ui, -apple-system, sans-serif",
    mono: "JetBrains Mono, monospace",
  },

  // Animations
  transitions: {
    fast: "150ms ease-in-out",
    normal: "300ms ease-in-out",
    slow: "500ms ease-in-out",
  },

  // Blur Effects (Glassmorphism)
  blur: {
    sm: "blur(8px)",
    md: "blur(12px)",
    lg: "blur(16px)",
    xl: "blur(24px)",
  },
} as const;

// Utility function to get color
export const getColor = (path: string) => {
  const keys = path.split(".");
  let value: any = theme.colors;
  for (const key of keys) {
    value = value[key];
  }
  return value;
};
