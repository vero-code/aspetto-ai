import { motion } from "framer-motion";
import { useEffect, useRef } from "react";

const SpotlightButton = ({ onClick, children }) => {
  const btnRef = useRef(null);
  const spanRef = useRef(null);

  useEffect(() => {
    const button = btnRef.current;
    const circle = spanRef.current;

    if (!button || !circle) return;

    const handleMouseMove = (e) => {
      const { width, left } = button.getBoundingClientRect();
      const offsetX = e.clientX - left;
      const leftPercent = `${(offsetX / width) * 100}%`;

      circle.animate({ left: leftPercent }, { duration: 250, fill: "forwards" });
    };

    const handleMouseLeave = () => {
      circle.animate({ left: "50%" }, { duration: 100, fill: "forwards" });
    };

    button.addEventListener("mousemove", handleMouseMove);
    button.addEventListener("mouseleave", handleMouseLeave);

    return () => {
      if (button) {
        button.removeEventListener("mousemove", handleMouseMove);
        button.removeEventListener("mouseleave", handleMouseLeave);
      }
    };
  }, []);

  return (
    <motion.button
      whileTap={{ scale: 0.985 }}
      ref={btnRef}
      onClick={onClick}
      className="relative w-full max-w-xs overflow-hidden rounded-lg bg-slate-950 px-4 py-3 text-lg font-medium text-white"
    >
      <span className="pointer-events-none relative z-10 mix-blend-difference">
        {children || "Hover me"}
      </span>
      <span
        ref={spanRef}
        className="pointer-events-none absolute left-[50%] top-[50%] h-32 w-32 -translate-x-[50%] -translate-y-[50%] rounded-full bg-slate-100"
      />
    </motion.button>
  );
};

export default SpotlightButton;