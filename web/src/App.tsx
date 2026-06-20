import { BrowserRouter, Routes, Route, Navigate, useLocation } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { Login } from "./pages/auth/Login";
import { Signup } from "./pages/auth/Signup";
import { ForgotPassword } from "./pages/auth/ForgotPassword";
import { OTPVerification } from "./pages/auth/OTPVerification";
import { Home } from "./pages/Home";
import { Dashboard } from "./pages/Dashboard";
import { ModuleList } from "./pages/content/ModuleList";
import { TopicList } from "./pages/content/TopicList";
import { SubtopicList } from "./pages/content/SubtopicList";
import { LessonReader } from "./pages/content/LessonReader";
import { QuizPlayer } from "./pages/quiz/QuizPlayer";
import { MockExamPlayer } from "./pages/mock-exam/MockExamPlayer";
import { Leaderboard } from "./pages/Leaderboard";
import { Mastery } from "./pages/Mastery";
import { Goals } from "./pages/Goals";
import { Tournaments } from "./pages/Tournaments";
import { Profile } from "./pages/Profile";
import { Settings } from "./pages/Settings";
import { Analytics } from "./pages/Analytics";
import { AdminDashboard } from "./pages/AdminDashboard";
import { GlassNavbar } from "./components/GlassNavbar";
import { AmbientBackground } from "./components/AmbientBackground";
import { AuthGuard } from "./components/AuthGuard";
import { ToastProvider } from "./context/ToastContext";
import { Tutor } from "./pages/Tutor";
import { StudyPlan } from "./pages/StudyPlan";
import { Readiness } from "./pages/Readiness";
import { Focus } from "./pages/Focus";
import { Flashcards } from "./pages/flashcards/Flashcards";
import { DeckDetail } from "./pages/flashcards/DeckDetail";
import { CreateDeck } from "./pages/flashcards/CreateDeck";
import { StudySession } from "./pages/flashcards/StudySession";
import { Marketplace } from "./pages/flashcards/Marketplace";
import { FlashcardAnalytics } from "./pages/flashcards/FlashcardAnalytics";
import { ExamSimulation } from "./pages/flashcards/ExamSimulation";
import { Social } from "./pages/flashcards/Social";
import { GenerateCards } from "./pages/flashcards/GenerateCards";
import { FlashcardAdmin } from "./pages/flashcards/FlashcardAdmin";
import { Onboarding } from "./pages/onboarding/Onboarding";
import { DailyQueue } from "./pages/queue/DailyQueue";
import { MockExamResults } from "./pages/mock-exam/MockExamResults";
import { Milestones } from "./pages/milestones/Milestones";
import { DesktopAppShell } from "./components/shell/DesktopAppShell";
import { useBreakpoint } from "./hooks/useBreakpoint";

/** Crossfade transition variants for layout switching (250ms) */
const layoutTransition = {
  initial: { opacity: 0 },
  animate: { opacity: 1 },
  exit: { opacity: 0 },
  transition: { duration: 0.25, ease: "easeInOut" },
};

function AppRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait" initial={false}>
      <Routes location={location} key={location.pathname}>
        {/* Public auth routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/verify-otp" element={<OTPVerification />} />

        {/* Protected routes */}
        <Route
          path="/dashboard"
          element={
            <AuthGuard>
              <Dashboard />
            </AuthGuard>
          }
        />
        <Route
          path="/modules"
          element={
            <AuthGuard>
              <ModuleList />
            </AuthGuard>
          }
        />
        <Route
          path="/modules/:moduleId/topics"
          element={
            <AuthGuard>
              <TopicList />
            </AuthGuard>
          }
        />
        <Route
          path="/topics/:topicId/subtopics"
          element={
            <AuthGuard>
              <SubtopicList />
            </AuthGuard>
          }
        />
        <Route
          path="/subtopics/:subtopicId/lesson"
          element={
            <AuthGuard>
              <LessonReader />
            </AuthGuard>
          }
        />
        <Route
          path="/quiz/:scope/:scopeId"
          element={
            <AuthGuard>
              <QuizPlayer />
            </AuthGuard>
          }
        />
        <Route
          path="/mock-exam"
          element={
            <AuthGuard>
              <MockExamPlayer />
            </AuthGuard>
          }
        />
        <Route
          path="/leaderboard"
          element={
            <AuthGuard>
              <Leaderboard />
            </AuthGuard>
          }
        />
        <Route
          path="/mastery"
          element={
            <AuthGuard>
              <Mastery />
            </AuthGuard>
          }
        />
        <Route
          path="/analytics"
          element={
            <AuthGuard>
              <Analytics />
            </AuthGuard>
          }
        />
        <Route
          path="/goals"
          element={
            <AuthGuard>
              <Goals />
            </AuthGuard>
          }
        />
        <Route
          path="/tournaments"
          element={
            <AuthGuard>
              <Tournaments />
            </AuthGuard>
          }
        />
        <Route
          path="/profile"
          element={
            <AuthGuard>
              <Profile />
            </AuthGuard>
          }
        />
        <Route
          path="/settings"
          element={
            <AuthGuard>
              <Settings />
            </AuthGuard>
          }
        />
        <Route
          path="/admin"
          element={
            <AuthGuard>
              <AdminDashboard />
            </AuthGuard>
          }
        />
        <Route
          path="/tutor"
          element={
            <AuthGuard>
              <Tutor />
            </AuthGuard>
          }
        />
        <Route
          path="/study-plan"
          element={
            <AuthGuard>
              <StudyPlan />
            </AuthGuard>
          }
        />
        <Route
          path="/readiness"
          element={
            <AuthGuard>
              <Readiness />
            </AuthGuard>
          }
        />
        <Route
          path="/focus"
          element={
            <AuthGuard>
              <Focus />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards"
          element={
            <AuthGuard>
              <Flashcards />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/decks/new"
          element={
            <AuthGuard>
              <CreateDeck />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/decks/:deckId"
          element={
            <AuthGuard>
              <DeckDetail />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/study"
          element={
            <AuthGuard>
              <StudySession />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/marketplace"
          element={
            <AuthGuard>
              <Marketplace />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/analytics"
          element={
            <AuthGuard>
              <FlashcardAnalytics />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/exam"
          element={
            <AuthGuard>
              <ExamSimulation />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/social"
          element={
            <AuthGuard>
              <Social />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/generate"
          element={
            <AuthGuard>
              <GenerateCards />
            </AuthGuard>
          }
        />
        <Route
          path="/flashcards/admin"
          element={
            <AuthGuard>
              <FlashcardAdmin />
            </AuthGuard>
          }
        />

        {/* Onboarding */}
        <Route
          path="/onboarding"
          element={
            <AuthGuard>
              <Onboarding />
            </AuthGuard>
          }
        />

        {/* Daily Queue */}
        <Route
          path="/queue"
          element={
            <AuthGuard>
              <DailyQueue />
            </AuthGuard>
          }
        />

        {/* Mock Exam Results */}
        <Route
          path="/mock-exam/:attemptId/results"
          element={
            <AuthGuard>
              <MockExamResults />
            </AuthGuard>
          }
        />

        {/* Milestones */}
        <Route
          path="/milestones"
          element={
            <AuthGuard>
              <Milestones />
            </AuthGuard>
          }
        />

        {/* Homepage */}
        <Route path="/" element={<Home />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnimatePresence>
  );
}

function AppContent() {
  const { isDesktop } = useBreakpoint();

  return (
    <>
      <AmbientBackground />
      <AnimatePresence mode="wait" initial={false}>
        {isDesktop ? (
          <motion.div
            key="desktop-shell"
            {...layoutTransition}
            style={{ height: "100vh", overflow: "hidden" }}
          >
            <DesktopAppShell>
              <AppRoutes />
            </DesktopAppShell>
          </motion.div>
        ) : (
          <motion.div key="mobile-layout" {...layoutTransition}>
            <GlassNavbar />
            <AppRoutes />
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}

export function App() {
  return (
    <BrowserRouter>
      <ToastProvider>
        <AppContent />
      </ToastProvider>
    </BrowserRouter>
  );
}
