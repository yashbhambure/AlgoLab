import { BrowserRouter, Routes, Route } from "react-router-dom";
import DashboardPage from "./pages/DashboardPage";
import CurriculumHubPage from "./pages/CurriculumHubPage";
import ModuleDetailPage from "./pages/ModuleDetailPage";
import ProblemsHubPage from "./pages/ProblemsHubPage";
import ProblemDetailPage from "./pages/ProblemDetailPage";
import AlgorithmDetailPage from "./pages/AlgorithmDetailPage";
import CatalogPage from "./pages/CatalogPage";
import BenchmarkArenaPage from "./pages/BenchmarkArenaPage";
import VisualizerPage from "./pages/VisualizerPage";
import ComplexityPage from "./pages/ComplexityPage";
import RecommendationPage from "./pages/RecommendationPage";
import DecisionTreePage from "./pages/DecisionTreePage";
import ExperimentsPage from "./pages/ExperimentsPage";

import { ThemeProvider } from "./context/ThemeContext";

export function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<DashboardPage />} />
          <Route path="/curriculum" element={<CurriculumHubPage />} />
          <Route path="/curriculum/:moduleId" element={<ModuleDetailPage />} />
          <Route path="/problems" element={<ProblemsHubPage />} />
          <Route path="/problems/:slug" element={<ProblemDetailPage />} />
          <Route path="/algorithms/:slug" element={<AlgorithmDetailPage />} />
          <Route path="/catalog" element={<CatalogPage />} />
          <Route path="/benchmark" element={<BenchmarkArenaPage />} />
          <Route path="/visualizer" element={<VisualizerPage />} />
          <Route path="/complexity" element={<ComplexityPage />} />
          <Route path="/recommend" element={<RecommendationPage />} />
          <Route path="/decision-tree" element={<DecisionTreePage />} />
          <Route path="/experiments" element={<ExperimentsPage />} />
        </Routes>
      </BrowserRouter>
    </ThemeProvider>
  );
}

export default App;