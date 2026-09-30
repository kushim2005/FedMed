import { motion } from 'framer-motion'
import { TrendingUp, Shield, Activity, Clock, Users, Target } from 'lucide-react'

const containerVariants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
}

const cardVariants = {
  hidden: { opacity: 0, y: 30 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
}

function StatCard({ icon: Icon, label, value, subtitle, color, bgColor, trend }) {
  return (
    <motion.div variants={cardVariants} className="card-hover p-6 relative overflow-hidden">
      {/* Background gradient */}
      <div className={`absolute inset-0 ${bgColor} opacity-5 pointer-events-none`} />

      <div className="relative flex items-start justify-between">
        <div className="flex-1">
          <p className="text-slate-400 text-sm font-medium mb-2 flex items-center gap-1.5">
            <Icon className={`w-4 h-4 ${color}`} />
            {label}
          </p>
          <p className={`metric-value ${color}`}>{value}</p>
          {subtitle && (
            <p className="text-slate-500 text-xs mt-2 font-mono">{subtitle}</p>
          )}
        </div>
        {trend !== undefined && (
          <div className={`flex items-center gap-1 text-xs font-semibold px-2 py-1 rounded-lg ${
            trend >= 0
              ? 'bg-emerald-500/10 text-emerald-400'
              : 'bg-red-500/10 text-red-400'
          }`}>
            <TrendingUp className={`w-3 h-3 ${trend < 0 ? 'rotate-180' : ''}`} />
            {Math.abs(trend).toFixed(3)}
          </div>
        )}
      </div>
    </motion.div>
  )
}

export default function MetricCards({ metrics = [], privacy = [], hospitals = [] }) {
  const latestMetric = metrics[metrics.length - 1] ?? {}
  const prevMetric = metrics[metrics.length - 2] ?? {}
  const latestPrivacy = privacy[privacy.length - 1] ?? {}

  const diceTrend = latestMetric.dice && prevMetric.dice
    ? latestMetric.dice - prevMetric.dice
    : undefined

  const activeHospitals = hospitals.filter(h => h.status === 'connected').length
  const totalSamples = hospitals.reduce((s, h) => s + (h.samples || 0), 0)

  const avgRoundTime = metrics.length > 0
    ? (metrics.reduce((s, m) => s + (m.round_time || 18.5), 0) / metrics.length).toFixed(1)
    : '--'

  return (
    <motion.div
      variants={containerVariants}
      initial="hidden"
      animate="visible"
      className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4"
    >
      <StatCard
        icon={Target}
        label="Best Dice Score"
        value={latestMetric.dice ? latestMetric.dice.toFixed(4) : '—'}
        subtitle={`ET: ${latestMetric.dice_et?.toFixed(3) ?? '—'} · ED: ${latestMetric.dice_ed?.toFixed(3) ?? '—'} · NCR: ${latestMetric.dice_ncr?.toFixed(3) ?? '—'}`}
        color="text-blue-400"
        bgColor="bg-blue-500"
        trend={diceTrend}
      />

      <StatCard
        icon={Shield}
        label="Privacy Budget (ε)"
        value={latestPrivacy.epsilon ? latestPrivacy.epsilon.toFixed(4) : '—'}
        subtitle={`${latestPrivacy.budget_pct ?? '—'}% used · δ = 1e-5 · σ = 1.1`}
        color="text-purple-400"
        bgColor="bg-purple-500"
      />

      <StatCard
        icon={Users}
        label="Hospital Nodes"
        value={`${activeHospitals} / ${hospitals.length}`}
        subtitle={`${totalSamples} total training samples`}
        color="text-emerald-400"
        bgColor="bg-emerald-500"
      />

      <StatCard
        icon={Clock}
        label="Avg Round Time"
        value={`${avgRoundTime}s`}
        subtitle={`${metrics.length} / 10 rounds complete · HD95: ${latestMetric.hd95?.toFixed(1) ?? '—'}mm`}
        color="text-cyan-400"
        bgColor="bg-cyan-500"
      />
    </motion.div>
  )
}
