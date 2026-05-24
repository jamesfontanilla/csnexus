import { useState, useEffect, useRef, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import {
  flashcardsApi,
  Deck,
  ExamSimulation as ExamSimulationType,
  ExamCard,
  ExamResult,
} from "../../api/flashcards";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";

type Phase = "setup" | "loading" | "exam" | "results" | "error";

export function ExamSimulation() {
  const navigate = useNavigate();

  const [phase, setPhase] = useState<Phase>("loading");
  const [decks, setDecks] = useState<Deck[]>([]);
  const [selectedDeckIds, setSelectedDeckIds] = useState<number[]>([]);
  const [cardCount, setCardCount] = useState(30);
  const [timeLimit, setTimeLimit] = useState(15);
  const [error, setError] = useState<string | null>(null);

  // Exam state
  const [exam, setExam] = useState<ExamSimulationType | null>(null);
  const [cards, setCards] = useState<ExamCard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answer, setAnswer] = useState("");
  const [timeRemaining, setTimeRemaining] = useState(0);
  const [result, setResult] = useState<ExamResult | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const timerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const startTimeRef = useRef<number>(0);

  useEffect(() => {
    async function loadDecks() {
      try {
        const userDecks = await flashcardsApi.getDecks();
        setDecks(userDecks);
        setPhase("setup");
      } catch {
        setError("Failed to load decks.");
        setPhase("error");
      }
    }
    loadDecks();
  }, []);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, []);

  const handleDeckToggle = (deckId: number) => {
    setSelectedDeckIds((prev) =>
      prev.includes(deckId)
        ? prev.filter((id) => id !== deckId)
        : [...prev, deckId]
    );
  };

  const handleStartExam = async () => {
    if (selectedDeckIds.length === 0) return;
    setPhase("loading");
    try {
      const examRes = await flashcardsApi.createExam({
        deck_ids: selectedDeckIds,
        card_count: cardCount,
        time_limit_minutes: timeLimit,
      });
      setExam(examRes);

      const examCards = await flashcardsApi.getExamCards(examRes.id);
      setCards(examCards);
      setTimeRemaining(timeLimit * 60);
      startTimeRef.current = Date.now();

      timerRef.current = setInterval(() => {
        setTimeRemaining((prev) => {
          if (prev <= 1) {
            if (timerRef.current) clearInterval(timerRef.current);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);

      setPhase("exam");
    } catch {
      setError("Failed to start exam. Make sure you have enough cards.");
      setPhase("error");
    }
  };

  const handleTimeUp = useCallback(async () => {
    if (timerRef.current) clearInterval(timerRef.current);
    if (!exam) return;
    try {
      const res = await flashcardsApi.completeExam(exam.id);
      setResult(res);
      setPhase("results");
    } catch {
      setError("Failed to complete exam.");
      setPhase("error");
    }
  }, [exam]);

  useEffect(() => {
    if (phase === "exam" && timeRemaining === 0) {
      handleTimeUp();
    }
  }, [timeRemaining, phase, handleTimeUp]);

  const handleSubmitAnswer = async () => {
    if (!exam || submitting) return;
    setSubmitting(true);
    try {
      const card = cards[currentIndex];
      await flashcardsApi.answerExamCard(exam.id, {
        card_id: card.card_id,
        answer: answer,
      });

      if (currentIndex < cards.length - 1) {
        setCurrentIndex((prev) => prev + 1);
        setAnswer("");
      } else {
        // All cards answered
        if (timerRef.current) clearInterval(timerRef.current);
        const res = await flashcardsApi.completeExam(exam.id);
        setResult(res);
        setPhase("results");
      }
    } catch {
      setError("Failed to submit answer.");
      setPhase("error");
    } finally {
      setSubmitting(false);
    }
  };

  const handleComplete = async () => {
    if (!exam) return;
    if (timerRef.current) clearInterval(timerRef.current);
    try {
      const res = await flashcardsApi.completeExam(exam.id);
      setResult(res);
      setPhase("results");
    } catch {
      setError("Failed to complete exam.");
      setPhase("error");
    }
  };

  const formatTime = (seconds: number): string => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
  };

  if (phase === "loading") {
    return (
      <PageTransition>
        <main className="page container">
          <GlassSkeleton height="20rem" />
        </main>
      </PageTransition>
    );
  }

  if (phase === "error") {
    return (
      <PageTransition>
        <main className="page container">
          <GlassCard>
            <p style={{ color: "var(--color-text)", textAlign: "center" }}>
              {error}
            </p>
            <div style={{ textAlign: "center", marginTop: "1rem" }}>
              <GlassButton onClick={() => navigate("/flashcards")}>
                Back to Flashcards
              </GlassButton>
            </div>
          </GlassCard>
        </main>
      </PageTransition>
    );
  }

  if (phase === "setup") {
    return (
      <PageTransition>
        <main className="page container">
          <h1
            style={{
              fontSize: "var(--font-size-2xl)",
              color: "var(--color-text)",
              marginBottom: "1.5rem",
            }}
          >
            Exam Simulation
          </h1>

          <GlassCard style={{ marginBottom: "1.5rem" }}>
            <h2
              style={{
                fontSize: "var(--font-size-lg)",
                color: "var(--color-text)",
                margin: "0 0 1rem",
              }}
            >
              Select Decks
            </h2>
            {decks.length === 0 ? (
              <p style={{ color: "var(--color-text-secondary)" }}>
                No decks available. Create a deck first.
              </p>
            ) : (
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  gap: "0.5rem",
                }}
              >
                {decks.map((deck) => (
                  <label
                    key={deck.id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "0.75rem",
                      padding: "0.5rem",
                      borderRadius: "var(--radius-sm)",
                      cursor: "pointer",
                      background: selectedDeckIds.includes(deck.id)
                        ? "var(--glass-bg-subtle)"
                        : "transparent",
                    }}
                  >
                    <input
                      type="checkbox"
                      checked={selectedDeckIds.includes(deck.id)}
                      onChange={() => handleDeckToggle(deck.id)}
                      style={{ width: "1.25rem", height: "1.25rem" }}
                    />
                    <span style={{ color: "var(--color-text)" }}>
                      {deck.title}
                    </span>
                    <span
                      style={{
                        fontSize: "var(--font-size-sm)",
                        color: "var(--color-text-secondary)",
                        marginLeft: "auto",
                      }}
                    >
                      {deck.card_count} cards
                    </span>
                  </label>
                ))}
              </div>
            )}
          </GlassCard>

          <GlassCard style={{ marginBottom: "1.5rem" }}>
            <h2
              style={{
                fontSize: "var(--font-size-lg)",
                color: "var(--color-text)",
                margin: "0 0 1rem",
              }}
            >
              Settings
            </h2>
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                gap: "1.25rem",
              }}
            >
              <div>
                <label
                  style={{
                    display: "block",
                    color: "var(--color-text)",
                    marginBottom: "0.5rem",
                    fontSize: "var(--font-size-sm)",
                  }}
                >
                  Card Count: {cardCount}
                </label>
                <input
                  type="range"
                  min={10}
                  max={150}
                  step={5}
                  value={cardCount}
                  onChange={(e) => setCardCount(Number(e.target.value))}
                  style={{ width: "100%" }}
                />
                <div
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    fontSize: "var(--font-size-sm)",
                    color: "var(--color-text-secondary)",
                  }}
                >
                  <span>10</span>
                  <span>150</span>
                </div>
              </div>
              <div>
                <label
                  style={{
                    display: "block",
                    color: "var(--color-text)",
                    marginBottom: "0.5rem",
                    fontSize: "var(--font-size-sm)",
                  }}
                >
                  Time Limit (minutes)
                </label>
                <input
                  type="number"
                  min={1}
                  max={180}
                  value={timeLimit}
                  onChange={(e) => setTimeLimit(Number(e.target.value))}
                  style={{
                    width: "100%",
                    padding: "0.5rem 0.75rem",
                    borderRadius: "var(--radius-sm)",
                    border: "1px solid var(--glass-border)",
                    background: "var(--glass-bg)",
                    color: "var(--color-text)",
                    fontSize: "var(--font-size-base)",
                  }}
                />
              </div>
            </div>
          </GlassCard>

          <GlassButton
            variant="primary"
            onClick={handleStartExam}
            disabled={selectedDeckIds.length === 0}
          >
            Start Exam
          </GlassButton>
        </main>
      </PageTransition>
    );
  }

  if (phase === "exam") {
    const currentCard = cards[currentIndex];
    return (
      <PageTransition>
        <main className="page container">
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: "1.5rem",
            }}
          >
            <h1
              style={{
                fontSize: "var(--font-size-lg)",
                color: "var(--color-text)",
                margin: 0,
              }}
            >
              Question {currentIndex + 1} / {cards.length}
            </h1>
            <span
              style={{
                fontSize: "var(--font-size-lg)",
                color:
                  timeRemaining < 60
                    ? "var(--color-error, #ef4444)"
                    : "var(--color-accent)",
                fontWeight: 600,
                fontVariantNumeric: "tabular-nums",
              }}
            >
              {formatTime(timeRemaining)}
            </span>
          </div>

          <GlassCard style={{ marginBottom: "1.5rem" }}>
            <p
              style={{
                fontSize: "var(--font-size-lg)",
                color: "var(--color-text)",
                margin: 0,
                minHeight: "4rem",
                display: "flex",
                alignItems: "center",
              }}
            >
              {currentCard.front}
            </p>
          </GlassCard>

          <div style={{ marginBottom: "1.5rem" }}>
            <input
              type="text"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && answer.trim()) handleSubmitAnswer();
              }}
              placeholder="Type your answer..."
              autoFocus
              style={{
                width: "100%",
                padding: "0.75rem 1rem",
                borderRadius: "var(--radius-sm)",
                border: "1px solid var(--glass-border)",
                background: "var(--glass-bg)",
                color: "var(--color-text)",
                fontSize: "var(--font-size-base)",
              }}
            />
          </div>

          <div style={{ display: "flex", gap: "1rem" }}>
            <GlassButton
              variant="primary"
              onClick={handleSubmitAnswer}
              disabled={!answer.trim() || submitting}
            >
              Submit Answer
            </GlassButton>
            <GlassButton variant="ghost" onClick={handleComplete}>
              Complete
            </GlassButton>
          </div>
        </main>
      </PageTransition>
    );
  }

  if (phase === "results" && result) {
    const timeTaken = result.time_taken_seconds;
    const minutes = Math.floor(timeTaken / 60);
    const seconds = timeTaken % 60;

    return (
      <PageTransition>
        <main className="page container">
          <h1
            style={{
              fontSize: "var(--font-size-2xl)",
              color: "var(--color-text)",
              marginBottom: "1.5rem",
              textAlign: "center",
            }}
          >
            Exam Results
          </h1>

          <GlassCard style={{ textAlign: "center", marginBottom: "2rem" }}>
            <div
              style={{
                fontSize: "3rem",
                fontWeight: 700,
                color: "var(--color-accent)",
                marginBottom: "0.5rem",
              }}
            >
              {result.score} / {result.total}
            </div>
            <div
              style={{
                fontSize: "var(--font-size-lg)",
                color: "var(--color-text-secondary)",
                marginBottom: "1rem",
              }}
            >
              {result.percentage.toFixed(1)}%
            </div>
            <div
              style={{
                fontSize: "var(--font-size-sm)",
                color: "var(--color-text-secondary)",
              }}
            >
              Time taken: {minutes}m {seconds}s
            </div>
            {result.xp_earned > 0 && (
              <div
                style={{
                  fontSize: "var(--font-size-sm)",
                  color: "var(--color-accent)",
                  marginTop: "0.5rem",
                }}
              >
                +{result.xp_earned} XP earned
              </div>
            )}
          </GlassCard>

          <div style={{ textAlign: "center" }}>
            <GlassButton
              variant="primary"
              onClick={() => navigate("/flashcards")}
            >
              Back to Flashcards
            </GlassButton>
          </div>
        </main>
      </PageTransition>
    );
  }

  return null;
}
