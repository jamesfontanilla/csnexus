import { useInView } from "./useInView";
import { useReducedMotion, makeReducedVariants } from "../design-system/motion";

interface ScrollRevealOptions {
  once?: boolean;
  margin?: string;
}

const revealVariants = {
  initial: { opacity: 0, y: 16 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.4, ease: [0, 0, 0.2, 1] },
};

export function useScrollReveal(options?: ScrollRevealOptions) {
  const [ref, isInView] = useInView({
    rootMargin: options?.margin ?? "200px",
  });

  const reducedMotion = useReducedMotion();

  if (reducedMotion) {
    const reduced = makeReducedVariants(revealVariants, true);
    return [ref, reduced] as const;
  }

  const motionProps = {
    initial: revealVariants.initial,
    animate: isInView ? revealVariants.animate : revealVariants.initial,
    transition: revealVariants.transition,
  };

  return [ref, motionProps] as const;
}
