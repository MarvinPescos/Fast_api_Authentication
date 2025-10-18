interface TextInputProps {
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder: string;
  rows?: number;
}

export function TextInput({
  label,
  value,
  onChange,
  placeholder,
  rows = 4,
}: TextInputProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {label}
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        rows={rows}
        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amber-500 focus:border-amber-500 resize-none"
      />
    </div>
  );
}
