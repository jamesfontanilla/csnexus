import { useState, useEffect, useCallback } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  flashcardsApi,
  SessionCard,
  StudySession as StudySessionType,
  SessionSummary,
  ConfidenceLevel,
  ResponseType,
} from "../../api/flashcards";
import { addPendingEvent } from "../../stores/idb";
import { GlassCard } from "../../components/GlassCard";
import { GlassButton } from "../../components/GlassButton";
import { GlassSkeleton } from "../../components/GlassSkeleton";
import { PageTransition } from "../../components/PageTransition";

type Phase = "loading" | "studying" | "summary" | "error";
type StudyModeType = "swipe" | "typing";

const CONFIDENCE_OPTIONS: { level: ConfidenceLevel; label: string; responseType: ResponseType }[] = [
  { level: "guessed", label: "Forgot", responseType: "forgot" },
  { level: "unsure", label: "Unsure", responseType: "remembered" },
  { level: "confident", label: "Confident", responseType: "remembered" },
  { level: "mastered", label: "Mastered", responseType: "remembered" },
];

const CONFIDENCE_COLORS: Record<ConfidenceLevel, string> = {
  guessed: "#ef4444",
  unsure: "#f59e0b",
  confident: "#10b981",
  mastered: "#6366f1",
};

function similarity(a: string, b: string): number {
  const la = a.toLowerCase().trim();
  const lb = b.toLowerCase().trim();
  if (la === lb) return 1;
  const maxLen = Math.max(la.length, lb.length);
  if (maxLen === 0) return 1;
  const matrix: number[][] = [];
  for (let i = 0; i <= la.length; i++) matrix[i] = [i];
  for (let j = 0; j <= lb.length; j++) matrix[0][j] = j;
  for (let i = 1; i <= la.length; i++) {
    for (let j = 1; j <= lb.length; j++) {
      const cost = la[i - 1] === lb[j - 1] ? 0 : 1;
      matrix[i][j] = Math.min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost);
    }
  }
  const dist = matrix[la.length][lb.length];
  return 1 - dist / maxLen;
}

export function StudySession() {
  const navigate = useNavigate();
  const location = useLocation();

  const [phase, setPhase] = useState<Phase>("loading");
  const [session, setSession] = useState<StudySessionType | null>(null);
  const [cards, setCards] = useState<SessionCard[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [summary, setSummary] = useState<SessionSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [responding, setResponding] = useState(false);

  // Typing mode state
  const [studyMode] = useState<StudyModeType>(
    () => (location.state as { mode?: StudyModeType } | null)?.mode || "swipe"
  );
  const [typedAnswer, setTypedAnswer] = useState("");
  const [typingResult, setTypingResult] = useState<{
    correct: boolean;
    correctAnswer: string;
  } | null>(null);

  useEffect(() => {
    async function startSession() {
      try {
        const state = location.state as { deckIds?: number[]; mode?: string } | null;
        const deckIds = state?.deckIds;

        if (!deckIds || deckIds.length === 0) {
          // Default: study from queue
          const queue = await flashcardsApi.getQueue();
          if (queue.length === 0) {
            setError("No cards due for review. You're all caught up!");
            setPhase("error");
            return;
          }
          // Get unique deck IDs from queue
          const uniqueDeckIds = [...new Set(queue.map((c) => parseInt(c.deck_title)))];
          // Fallback: create session with first available deck
          if (uniqueDeckIds.length === 0 || uniqueDeckIds.some(isNaN)) {
            setError("No cards due for review. You're all caught up!");
            setPhase("error");
            return;
          }
        }

        const sessionRes = await flashcardsApi.createSession({
          deck_ids: deckIds || [],
          study_mode: studyMode,
        });
        setSession(sessionRes);

        const sessionCards = await flashcardsApi.getSessionCards(sessionRes.id);
        if (sessionCards.length === 0) {
          setError("No cards available for this study session.");
          setPhase("error");
          return;
        }
        setCards(sessionCards);
        setPhase("studying");
      } catch {
        setError("Failed to start study session. Please try again.");
        setPhase("error");
      }
    }
    startSession();
  }, [location.state, studyMode]);

  const handleReveal = useCallback(() => {
    setRevealed(true);
  }, []);

  const handleConfidence = useCallback(
    async (confidence: ConfidenceLevel, responseType: ResponseType) => {
      if (!session || responding) return;

      setResponding(true);
      const currentCard = cards[currentIndex];

      try {
        await flashcardsApi.respondToCard(session.id, {
          card_id: currentCard.card_id,
          response_type: responseType,
          confidence,
        });

        const nextIndex = currentIndex + 1;
        if (nextIndex >= cards.length) {
          // End session
          const summaryRes = await flashcardsApi.endSession(session.id);
          setSummary(summaryRes);
          setPhase("summary");
        } else {
          setCurrentIndex(nextIndex);
          setRevealed(false);
          setTypedAnswer("");
          setTypingResult(null);
        }
      } catch (err) {
        if (err instanceof TypeError) {
          // Network error — queue for offline sync
          await addPendingEvent({
            client_event_id: `fc-review-${Date.now()}-${currentCard.card_id}`,
            kind: "flashcard_review",
            client_timestamp: new Date().toISOString(),
            payload: {
              card_id: currentCard.card_id,
              response_type: responseType,
              confidence,
            },
          });
          // Continue to next card even offline
          const nextIndex = currentIndex + 1;
          if (nextIndex >= cards.length) {
            // Can't end session offline, show partial summary
            setSummary({ cards_reviewed: cards.length, cards_correct: 0, xp_earned: 0, duration_seconds: 0 });
            setPhase("summary");
          } else {
            setCurrentIndex(nextIndex);
            setRevealed(false);
            setTypedAnswer("");
            setTypingResult(null);
          }
        } else {
          setError("Failed to record response. Please try again.");
        }
      } finally {
        setResponding(false);
      }
    },
    [session, cards, currentIndex, responding]
  );

  const handleTypingCheck = useCallback(() => {
    const currentCard = cards[currentIndex];
    const sim = similarity(typedAnswer, currentCard.back);
    const isCorrect = sim >= 0.8;
    setTypingResult({ correct: isCorrect, correctAnswer: currentCard.back });
  }, [cards, currentIndex, typedAnswer]);

  const handleTypingNext = useCallback(() => {
    if (!typingResult) return;
    const currentCard = cards[currentIndex];
    const sim = similarity(typedAnswer, currentCard.back);

    let confidence: ConfidenceLevel;
    if (sim === 1) {
      confidence = "mastered";
    } else if (sim > 0.8) {
      confidence = "confident";
    } else {
      confidence = "unsure";
    }

    const responseType: ResponseType = typingResult.correct ? "remembered" : "forgot";
    handleConfidence(confidence, responseType);
  }, [typingResult, cards, currentIndex, typedAnswer, handleConfidence]);

  if (phase === "loading") {
    return (
      <PageTransition>
        <main className="page container">
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              gap: "1.5rem",
              paddingTop: "3rem",
            }}
          >
            <GlassSkeleton height="1rem" width="60%" />
            <GlassSkeleton height="16rem" width="100%" />
            <GlassSkeleton height="3rem" width="80%" />
          </div>
        </main>
      </PageTransition>
    );
  }

  if (phase === "error") {
    return (
      <PageTransition>
        <main className="page container">
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              minHeight: "50vh",
            }}
          >
            <GlassCard style={{ maxWidth: "400px", textAlign: "center" }}>
              <p
                style={{
                  color: "var(--color-text)",
                  fontSize: "var(--font-size-base)",
                  margin: "0 0 1.5rem",
                }}
              >
                {error}
              </p>
              <GlassButton variant="primary" onClick={() => navigate("/flashcards")}>
                Back to Flashcards
              </GlassButton>
            </GlassCard>
          </div>
        </main>
      </PageTransition>
    );
  }

  if (phase === "summary" && summary) {
    return (
      <PageTransition>
        <main className="page container">
          <div
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              minHeight: "50vh",
            }}
          >
            <GlassCard style={{ maxWidth: "420px", textAlign: "center" }}>
              <h2
                style={{
                  fontSize: "var(--font-size-xl)",
                  color: "var(--color-text)",
                  margin: "0 0 1.5rem",
                }}
              >
                Session Complete
              </h2>
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: "1.5rem",
                  marginBottom: "2rem",
                }}
              >
                <div>
                  <p
                    style={{
                      fontSize: "var(--font-size-2xl)",
                      color: "var(--color-accent)",
                      fontWeight: 700,
                      margin: 0,
                    }}
                  >
                    {summary.cards_reviewed}
                  </p>
                  <p
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                      margin: 0,
                    }}
                  >
                    Cards Reviewed
                  </p>
                </div>
                <div>
                  <p
                    style={{
                      fontSize: "var(--font-size-2xl)",
                      color: "#10b981",
                      fontWeight: 700,
                      margin: 0,
                    }}
                  >
                    {summary.cards_correct}
                  </p>
                  <p
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                      margin: 0,
                    }}
                  >
                    Correct
                  </p>
                </div>
                <div>
                  <p
                    style={{
                      fontSize: "var(--font-size-2xl)",
                      color: "#6366f1",
                      fontWeight: 700,
                      margin: 0,
                    }}
                  >
                    +{summary.xp_earned}
                  </p>
                  <p
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                      margin: 0,
                    }}
                  >
                    XP Earned
                  </p>
                </div>
                <div>
                  <p
                    style={{
                      fontSize: "var(--font-size-2xl)",
                      color: "var(--color-text)",
                      fontWeight: 700,
                      margin: 0,
                    }}
                  >
                    {Math.round(summary.duration_seconds / 60)}m
                  </p>
                  <p
                    style={{
                      fontSize: "var(--font-size-sm)",
                      color: "var(--color-text-secondary)",
                      margin: 0,
                    }}
                  >
                    Duration
                  </p>
                </div>
              </div>
              <div style={{ display: "flex", gap: "1rem", justifyContent: "center" }}>
                <GlassButton variant="primary" onClick={() => navigate("/flashcards")}>
                  Done
                </GlassButton>
                <GlassButton
                  variant="secondary"
                  onClick={() => window.location.reload()}
                >
                  Study Again
                </GlassButton>
              </div>
            </GlassCard>
          </div>
        </main>
      </PageTransition>
    );
  }

  // Studying phase
  const currentCard = cards[currentIndex];
  const progress = ((currentIndex + 1) / cards.length) * 100;

  return (
    <PageTransition>
      <main className="page container">
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            maxWidth: "600px",
            margin: "0 auto",
            paddingTop: "1rem",
          }}
        >
          {/* Progress bar */}
          <div
            style={{
              width: "100%",
              marginBottom: "1.5rem",
              display: "flex",
              alignItems: "center",
              gap: "1rem",
            }}
          >
            <div
              style={{
                flex: 1,
                height: "6px",
                background: "var(--glass-bg-subtle)",
                borderRadius: "var(--radius-sm)",
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${progress}%`,
                  height: "100%",
                  background: "var(--color-accent)",
                  borderRadius: "var(--radius-sm)",
                  transition: "width 0.3s ease",
                }}
              />
            </div>
            <span
              style={{
                fontSize: "var(--font-size-sm)",
                color: "var(--color-text-secondary)",
                whiteSpace: "nowrap",
              }}
            >
              {currentIndex + 1} / {cards.length}
            </span>
          </div>

          {/* Card */}
          <AnimatePresence mode="wait">
            <motion.div
              key={`${currentCard.id}-${revealed}-${typingResult ? "checked" : "pending"}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              style={{ width: "100%" }}
            >
              <GlassCard
                style={{
                  minHeight: "14rem",
                  display: "flex",
                  flexDirection: "column",
                  alignItems: "center",
                  justifyContent: "center",
                  textAlign: "center",
                  cursor: studyMode === "swipe" && !revealed ? "pointer" : "default",
                }}
                hoverable={studyMode === "swipe" && !revealed}
                onClick={studyMode === "swipe" && !revealed ? handleReveal : undefined}
              >
                {studyMode === "swipe" && !revealed && (
                  <>
                    <p
                      style={{
                        fontSize: "var(--font-size-xl)",
                        color: "var(--color-text)",
                        margin: "0 0 1rem",
                        lineHeight: 1.4,
                      }}
                    >
                      {currentCard.front}
                    </p>
                    <p
                      style={{
                        fontSize: "var(--font-size-sm)",
                        color: "var(--color-text-secondary)",
                        margin: 0,
                      }}
                    >
                      Tap to reveal answer
                    </p>
                  </>
                )}

                {studyMode === "swipe" && revealed && (
                  <>
                    <p
                      style={{
                        fontSize: "var(--font-size-sm)",
                        color: "var(--color-text-secondary)",
                        margin: "0 0 0.5rem",
                        textTransform: "uppercase",
                        letterSpacing: "0.05em",
                      }}
                    >
                      Answer
                    </p>
                    <p
                      style={{
                        fontSize: "var(--font-size-xl)",
                        color: "var(--color-text)",
                        margin: 0,
                        lineHeight: 1.4,
                      }}
                    >
                      {currentCard.back}
                    </p>
                  </>
                )}

                {studyMode === "typing" && !typingResult && (
                  <>
                    <p
                      style={{
                        fontSize: "var(--font-size-xl)",
                        color: "var(--color-text)",
                        margin: "0 0 1.5rem",
                        lineHeight: 1.4,
                      }}
                    >
                      {currentCard.front}
                    </p>
                    <div style={{ width: "100%", maxWidth: "360px" }}>
                      <input
                        type="text"
                        value={typedAnswer}
                        onChange={(e) => setTypedAnswer(e.target.value)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" && typedAnswer.trim()) {
                            handleTypingCheck();
                          }
                        }}
                        placeholder="Type your answer..."
                        style={{
                          width: "100%",
                          padding: "0.75rem 1rem",
                          fontSize: "var(--font-size-base)",
                          background: "var(--glass-bg-subtle)",
                          border: "1px solid var(--glass-border)",
                          borderRadius: "var(--radius-sm)",
                          color: "var(--color-text)",
                          outline: "none",
                          boxSizing: "border-box",
                        }}
                        autoFocus
                      />
                      <div style={{ marginTop: "1rem" }}>
                        <GlassButton
                          variant="primary"
                          size="sm"
                          disabled={!typedAnswer.trim()}
                          onClick={handleTypingCheck}
                        >
                          Check
                        </GlassButton>
                      </div>
                    </div>
                  </>
                )}

                {studyMode === "typing" && typingResult && (
                  <>
                    <p
                      style={{
                        fontSize: "var(--font-size-xl)",
                        color: "var(--color-text)",
                        margin: "0 0 1rem",
                        lineHeight: 1.4,
                      }}
                    >
                      {currentCard.front}
                    </p>
                    <p
                      style={{
                        fontSize: "var(--font-size-lg)",
                        fontWeight: 700,
                        color: typingResult.correct ? "#10b981" : "#ef4444",
                        margin: "0 0 0.5rem",
                      }}
                    >
                      {typingResult.correct ? "Correct!" : "Incorrect"}
                    </p>
                    {!typingResult.correct && (
                      <p
                        style={{
                          fontSize: "var(--font-size-base)",
                          color: "var(--color-text-secondary)",
                          margin: "0 0 0.5rem",
                        }}
                      >
                        Correct answer: <strong style={{ color: "var(--color-text)" }}>{typingResult.correctAnswer}</strong>
                      </p>
                    )}
                    <p
                      style={{
                        fontSize: "var(--font-size-sm)",
                        color: "var(--color-text-secondary)",
                        margin: "0 0 1rem",
                      }}
                    >
                      Your answer: {typedAnswer}
                    </p>
                  </>
                )}
              </GlassCard>
            </motion.div>
          </AnimatePresence>

          {/* Swipe mode: Confidence buttons */}
          {studyMode === "swipe" && revealed && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: 0.1 }}
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(4, 1fr)",
                gap: "0.75rem",
                width: "100%",
                marginTop: "1.5rem",
              }}
            >
              {CONFIDENCE_OPTIONS.map((opt) => (
                <GlassButton
                  key={opt.level}
                  variant="secondary"
                  size="sm"
                  disabled={responding}
                  onClick={() => handleConfidence(opt.level, opt.responseType)}
                  style={{
                    borderColor: CONFIDENCE_COLORS[opt.level],
                    color: CONFIDENCE_COLORS[opt.level],
                  }}
                >
                  {opt.label}
                </GlassButton>
              ))}
            </motion.div>
          )}

          {/* Typing mode: Next button */}
          {studyMode === "typing" && typingResult && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.2, delay: 0.1 }}
              style={{ marginTop: "1.5rem" }}
            >
              <GlassButton
                variant="primary"
                disabled={responding}
                onClick={handleTypingNext}
              >
                Next
              </GlassButton>
            </motion.div>
          )}

          {/* Error inline */}
          {error && (
            <p
              style={{
                color: "#ef4444",
                fontSize: "var(--font-size-sm)",
                marginTop: "1rem",
              }}
            >
              {error}
            </p>
          )}
        </div>
      </main>
    </PageTransition>
  );
}
