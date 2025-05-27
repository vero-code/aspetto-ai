// components/RemoveImageButton.jsx
import { TrashIcon } from '@heroicons/react/24/solid';
import { motion, AnimatePresence } from 'framer-motion';

export default function RemoveImageButton({ visible, onClick }) {
  return (
    <AnimatePresence>
      {visible && (
        <motion.div
          key="remove-btn"
          initial={{ opacity: 0, x: -10 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <button
            onClick={onClick}
            className="flex items-center gap-1 px-3 py-1.5 text-sm text-red-600 bg-red-100 hover:bg-red-200 rounded-md"
          >
            <TrashIcon className="w-4 h-4" />
            Remove
          </button>
        </motion.div>
      )}
    </AnimatePresence>
  );
}