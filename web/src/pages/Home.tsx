import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { isAuthenticated } from "../stores/auth";
import { GlassCard } from "../components/GlassCard";
import { GlassButton } from "../components/GlassButton";
import { GradientText } from "../components/GradientText";
import { PageTransition } from "../components/PageTransition";
import { staggerContainer, staggerItem } from "../design-system";
import { useInView } from "../hooks/useInView";

export function Home() {
  return (
    <PageTransition>
      <main style={{ position: "relative", zIndex: 1 }}>
        {/* Hero with gradient */}
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
                <Link to="/modules" style={{ textDecoration: "none" }} aria-label="Continue studying">
                  <GlassButton variant="primary" size="lg">
                    Continue Studying →
                  </GlassButton>
                </Link>
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

        {/* Features */}
        <FeaturesSection />

        {/* Social proof */}
        <section
          style={{
            textAlign: "center",
            padding: "var(--space-10) var(--space-6)",
            borderTop: "1px solid var(--glass-border-light)",
          }}
        >
          <p style={{ fontSize: "var(--font-size-lg)", color: "var(--color-text-secondary)", margin: 0 }}>
            Join learners preparing for the Civil Service Exam
          </p>
        </section>

        {/* Footer */}
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
      </main>
    </PageTransition>
  );
}

function FeaturesSection() {
  const [sectionRef, isInView] = useInView();

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
      <div ref={sectionRef}>
        {isInView ? (
          <motion.div
            variants={staggerContainer}
            initial="initial"
            animate="animate"
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fill, minmax(260px, 1fr))",
              gap: "var(--space-5)",
            }}
          >
            <FeatureCard emoji="📚" title="Structured Lessons" desc="Modules → Topics → Subtopics with explanations, worked examples, and key takeaways." />
            <FeatureCard emoji="✅" title="Practice Quizzes" desc="20-question subtopic quizzes, 50-question topic quizzes, and 100-question module quizzes." />
            <FeatureCard emoji="⏱️" title="Timed Mock Exams" desc="50-question mock exams with a 3-hour timer matching the real CSE format." />
            <FeatureCard emoji="⚡" title="XP & Levels" desc="Earn XP for every activity. Level up and maintain your daily streak." />
            <FeatureCard emoji="🏆" title="Leaderboards" desc="Compete with other learners on global, weekly, and monthly rankings." />
            <FeatureCard emoji="🏅" title="Achievements" desc="Unlock badges for milestones like first lesson, 7-day streak, and level 10." />
          </motion.div>
        ) : (
          <div style={{ minHeight: "300px" }} />
        )}
      </div>
    </section>
  );
}

function FeatureCard({ emoji, title, desc }: { emoji: string; title: string; desc: string }) {
  return (
    <motion.div variants={staggerItem}>
      <GlassCard hoverable>
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
