interface LoadingSpinnerProps {
  size?: "sm" | "md" | "lg" | "xl";
  fullScreen?: boolean;
  text?: string;
}

const sizeMap = {
  sm: "h-4 w-4",
  md: "h-8 w-8",
  lg: "h-12 w-12",
  xl: "h-16 w-16",
};

export function LoadingSpinner({
  size = "md",
  fullScreen = false,
  text,
}: LoadingSpinnerProps) {
  const spinner = (
    <div className="flex flex-col items-center justify-center gap-3">
      {/* Modern spinning ring */}
      <div className="relative">
        <div
          className={`${sizeMap[size]} rounded-full border-2 border-gray-200`}
        ></div>
        <div
          className={`${sizeMap[size]} absolute top-0 left-0 rounded-full border-2 border-transparent border-t-amber-500 animate-spin`}
        ></div>
      </div>

      {text && <p className="text-gray-600 text-sm font-medium">{text}</p>}
    </div>
  );

  if (fullScreen) {
    return (
      <div className="flex justify-center items-center min-h-screen bg-gray-50">
        {spinner}
      </div>
    );
  }

  return spinner;
}
