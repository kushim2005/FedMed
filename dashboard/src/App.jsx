import { useState, useEffect } from 'react'
import Navbar from './components/Navbar'
import HeroSection from './components/HeroSection'
import MetricCards from './components/MetricCards'
import ConvergenceChart from './components/ConvergenceChart'
import PrivacyBudgetChart from './components/PrivacyBudgetChart'
import HospitalGrid from './components/HospitalGrid'
import MetricsTable from './components/MetricsTable'
import ArchitectureViz from './components/ArchitectureViz'
import Footer from './components/Footer'
import { useFedMedData } from './hooks/useFedMedData'

function App() {
  const { metrics, hospitals, privacy, loading, error, lastUpdated } = useFedMedData()

  return (
    <div className="min-h-screen dark">
      <Navbar lastUpdated={lastUpdated} status={error ? 'error' : loading ? 'loading' : 'live'} />

      <main className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 pb-16">
        {/* Hero Section */}
        <HeroSection
          totalRounds={metrics.length}
          currentDice={metrics[metrics.length - 1]?.dice ?? 0}
          currentEpsilon={privacy[privacy.length - 1]?.epsilon ?? 0}
        />

        {/* Summary Metric Cards */}
        <section className="mt-8">
          <MetricCards metrics={metrics} privacy={privacy} hospitals={hospitals} />
        </section>

        {/* Main Charts Row */}
        <section className="mt-8 grid grid-cols-1 xl:grid-cols-3 gap-6">
          <div className="xl:col-span-2">
            <ConvergenceChart data={metrics} />
          </div>
          <div>
            <HospitalGrid hospitals={hospitals} />
          </div>
        </section>

        {/* Privacy + Metrics Row */}
        <section className="mt-6 grid grid-cols-1 xl:grid-cols-2 gap-6">
          <PrivacyBudgetChart data={privacy} />
          <MetricsTable data={metrics} />
        </section>

        {/* Architecture Visualization */}
        <section className="mt-6">
          <ArchitectureViz hospitals={hospitals} />
        </section>
      </main>

      <Footer />
    </div>
  )
}

export default App
