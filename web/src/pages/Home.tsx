import { Link } from "react-router-dom";
import { motion, type Variants } from "framer-motion";
import { isAuthenticated } from "../stores/auth";
import { GlassCard } from "../components/GlassCard";
import { GlassButton } from "../components/GlassButton";
import { GradientText } from "../components/GradientText";
import { PageTransition } from "../components/PageTransition";
import { cardStaggerContainer, cardStaggerItem, useReducedMotion } from "../design-system/motion";
import { useScrollReveal } from "../hooks/useScrollReveal";

export function Home() {
  const reducedMotion = useReducedMotion();
  const [heroRef, heroMotionProps] = useScrollReveal();
  const [featuresRef, featuresMotionProps] = useScrollReveal();
  const [footerRef, footerMotionProps] = useScrollReveal();

  return (
    <PageTransition>
      <main style={{ position: "relative", zIndex: 1 }}>
        {/* Hero with gradient */}
        <motion.div ref={heroRef} {...heroMotionProps}>
          <section
            style={{
              padding: "var(--space-16) var(--space-6) var(--space-12)",
              textAlign: "center",
            }}
          >
            <div style={{ maxWidth: 700, margin: "0 auto" }}>
              <h1
                style={{
                  fontSize: "var(--font-size-5xl)",
                  fontWeight: 800,
                  marginBottom: "var(--space-3)",
                  fontFamily: "var(--font-display)",
                  letterSpacing: "-0.03em",
                }}
              >
                <GradientText variant="accent">CSNexus</GradientText>
              </h1>
              <p
                style={{
                  fontSize: "var(--font-size-lg)",
                  color: "var(--color-text-secondary)",
                  lineHeight: 1.7,
                  maxWidth: 560,
                  margin: "0 auto var(--space-8)",
                }}
              >
                Your free study companion for the Philippine Civil Service Examination.
                Practice lessons, quizzes, and timed mock exams — track your progress
                with XP, streaks, and leaderboards.
              </p>

              {/* CTA Buttons */}
              <div style={{ display: "flex", gap: "var(--space-4)", justifyContent: "center", flexWrap: "wrap" }}>
                {isAuthenticated() ? (
                  <>
                    <Link to="/dashboard" style={{ textDecoration: "none" }} aria-label="Open dashboard">
                      <GlassButton variant="primary" size="lg">
                        Dashboard
                      </GlassButton>
                    </Link>
                    <Link to="/modules" style={{ textDecoration: "none" }} aria-label="Continue studying">
                      <GlassButton variant="secondary" size="lg">
                        Continue Studying →
                      </GlassButton>
                    </Link>
                  </>
                ) : (
                  <>
                    <Link to="/signup" style={{ textDecoration: "none" }} aria-label="Get started for free">
                      <GlassButton variant="primary" size="lg">
                        Get Started — It's Free
                      </GlassButton>
                    </Link>
                    <Link to="/login" style={{ textDecoration: "none" }} aria-label="Log in">
                      <GlassButton variant="secondary" size="lg">
                        Log In
                      </GlassButton>
                    </Link>
                  </>
                )}
              </div>
            </div>
          </section>
        </motion.div>

        {/* Features */}
        <motion.div ref={featuresRef} {...featuresMotionProps}>
          <FeaturesSection reducedMotion={reducedMotion} />
        </motion.div>

        {/* Footer */}
        <motion.div ref={footerRef} {...footerMotionProps}>
          <footer
            style={{
              textAlign: "center",
              padding: "var(--space-6)",
              color: "var(--color-text-muted)",
              fontSize: "var(--font-size-sm)",
            }}
          >
            CSNexus — Your path to passing the Civil Service Exam. Free and open.
          </footer>
        </motion.div>
      </main>
    </PageTransition>
  );
}

function FeaturesSection({ reducedMotion }: { reducedMotion: boolean }) {
  // Stagger configuration is applied regardless of reduced-motion state.
  // Only transforms/opacity are stripped by makeReducedVariants when reducedMotion is true.
  const containerVariants = cardStaggerContainer;
  const itemVariants = reducedMotion
    ? { initial: { opacity: 1 }, animate: { opacity: 1 }, transition: { duration: 0 } }
    : cardStaggerItem;

  return (
    <section style={{ maxWidth: 960, margin: "0 auto", padding: "var(--space-12) var(--space-6)" }}>
      <h2
        style={{
          textAlign: "center",
          marginBottom: "var(--space-8)",
          fontSize: "var(--font-size-2xl)",
          fontWeight: 700,
          fontFamily: "var(--font-display)",
          letterSpacing: "-0.02em",
          color: "var(--color-text)",
        }}
      >
        What You Get
      </h2>
      <motion.div
        variants={containerVariants}
        initial="initial"
        animate="animate"
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
          gap: "var(--space-5)",
        }}
      >
        <FeatureCard variants={itemVariants} emoji="📚" title="Structured Lessons" desc="Modules → Topics → Subtopics with explanations, worked examples, and key takeaways." />
        <FeatureCard variants={itemVariants} emoji="✅" title="Practice Quizzes" desc="20-question subtopic quizzes, 50-question topic quizzes, and 100-question module quizzes." />
        <FeatureCard variants={itemVariants} emoji="⏱️" title="Timed Mock Exams" desc="50-question mock exams with a 3-hour timer matching the real CSE format." />
        <FeatureCard variants={itemVariants} emoji="⚡" title="XP & Levels" desc="Earn XP for every activity. Level up and maintain your daily streak." />
        <FeatureCard variants={itemVariants} emoji="🏆" title="Leaderboards" desc="Compete with other learners on global, weekly, and monthly rankings." />
        <FeatureCard variants={itemVariants} emoji="🏅" title="Achievements" desc="Unlock badges for milestones like first lesson, 7-day streak, and level 10." />
      </motion.div>
    </section>
  );
}

interface FeatureCardProps {
  emoji: string;
  title: string;
  desc: string;
  variants: Variants;
}

function FeatureCard({ emoji, title, desc, variants }: FeatureCardProps) {
  return (
    <motion.div variants={variants}>
      <GlassCard elevation="raised" hoverable>
        <div style={{ fontSize: "1.75rem", marginBottom: "var(--space-3)" }}>{emoji}</div>
        <h3
          style={{
            margin: "0 0 var(--space-2)",
            fontSize: "var(--font-size-base)",
            fontWeight: 600,
            color: "var(--color-text)",
          }}
        >
          {title}
        </h3>
        <p
          style={{
            margin: 0,
            fontSize: "var(--font-size-sm)",
            color: "var(--color-text-secondary)",
            lineHeight: 1.6,
          }}
        >
          {desc}
        </p>
      </GlassCard>
    </motion.div>
  );
}
