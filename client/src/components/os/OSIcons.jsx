export function CaughtIn4KIcon({ size = 32 }) {
  return (
    <svg width={size} height={size} viewBox="0 0 32 32" fill="none">
      <rect x="3" y="8" width="18" height="15" fill="#c0c0c0" stroke="#000000" strokeWidth="1.5" />
      <line x1="4" y1="9" x2="20" y2="9" stroke="#ffffff" strokeWidth="1.5" />
      <polygon points="21,12 28,7 28,24 21,19" fill="#808080" stroke="#000000" strokeWidth="1.5" />
      <circle cx="7" cy="12" r="2" fill="#ff0000" stroke="#000000" strokeWidth="0.5" />
      <line x1="24" y1="12" x2="26" y2="10" stroke="#ffffff" strokeWidth="1" />
      <rect x="7" y="16" width="10" height="5" fill="#808080" stroke="#000000" strokeWidth="1" />
      <rect x="20" y="23" width="11" height="7" fill="#ffff00" stroke="#000000" strokeWidth="1" />
      <text x="21" y="29" fontSize="6" fontWeight="bold" fill="#000000" fontFamily="monospace">4K</text>
    </svg>
  );
}