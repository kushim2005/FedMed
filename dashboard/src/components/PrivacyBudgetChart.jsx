import { motion } from 'framer-motion'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, ReferenceLine,
} from 'recharts'
import { Shield, AlertTriangle } from 'lucide-react'

const BUDGET_COLORS = (pct) => {
  if (pct < 50) return '#10b981'
  if (pct < 75) return '#f59e0b'
  return '#f43f5e'
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  const d = payload[0].payload
  return (
    <div className="bg-slate-800/95 border border-slate-700 rounded-xl p-3 shadow-2xl text-sm">
      <p className="text-slate-300 font-semibold mb-2">Round {label}</p>
      <div className="space-y-1">
        <div className="flex justify-between gap-4">
          <span className="text-slate-400">ε (epsilon)</span>
          <span className="font-mono text-purple-400">{d.epsilon?.toFixed(4)}</span>
        </div>
        <div className="flex justify-between gap-4">
          <span className="text-slate-400">Budget used</span>
          <span className="font-mono text-amber-400">{d.budget_pct?.toFixed(1)}%</span>
        </div>
        <div className="flex justify-between gap-4">
          <span className="text-slate-400">δ (delta)</span>
          <span className="font-mono text-slate-400">1e-5</span>
        </div>
        <div className="flex justify-between gap-4">
          <span className="text-slate-400">σ (noise)</span>
          <span className="font-mono text-slate-400">1.1</span>
        </div>
      </div>
    </div>
  )
}

export default function PrivacyBudgetChart({ data = [] }) {
  const latest = data[data.length - 1] ?? {}
  const budgetPct = latest.budget_pct ?? 0
  const isWarning = budgetPct > 70
  const isCritical = budgetPct > 90

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.3 }}
      className="card p-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h2 className="section-title">
            <Shield className="w-5 h-5 text-purple-400" />
            Privacy Budget Tracker
          </h2>
          <p className="text-slate-500 text-sm mt-1">
            Cumulative ε per round (Rényi DP · δ = 1e-5)
          </p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold font-mono text-purple-400">
            {latest.epsilon?.toFixed(4) ?? '—'}
          </div>
          <div className="text-xs text-slate-500">ε / 3.5 max</div>
        </div>
      </div>

      {/* Budget progress bar */}
      <div className="mb-6">
        <div className="flex justify-between text-xs text-slate-500 mb-1.5">
          <span>Budget consumed</span>
          <span className={`font-semibold ${isCritical ? 'text-red-400' : isWarning ? 'text-amber-400' : 'text-emerald-400'}`}>
            {budgetPct.toFixed(1)}%
          </span>
        </div>
        <div className="h-2 rounded-full bg-slate-800 overflow-hidden">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${Math.min(budgetPct, 100)}%` }}
            transition={{ duration: 1, ease: 'easeOut' }}
            className={`h-full rounded-full transition-colors duration-500 ${
              isCritical ? 'bg-red-500' : isWarning ? 'bg-amber-500' : 'bg-emerald-500'
            }`}
          />
        </div>
        {isWarning && (
          <div className="flex items-center gap-1.5 mt-2 text-amber-400 text-xs">
            <AlertTriangle className="w-3.5 h-3.5" />
            {isCritical ? 'Budget nearly exhausted — training will stop soon' : 'Privacy budget running low'}
          </div>
        )}
      </div>

      {/* Bar chart */}
      {data.length === 0 ? (
        <div className="flex items-center justify-center h-40 text-slate-600 text-sm">
          No privacy data yet...
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={180}>
          <BarChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis
              dataKey="round"
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis
              tick={{ fill: '#64748b', fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              domain={[0, 3.5]}
              tickFormatter={v => v.toFixed(1)}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: '#ffffff08' }} />
            <ReferenceLine
              y={3.5}
              stroke="#f43f5e"
              strokeDasharray="5 3"
              strokeOpacity={0.7}
              label={{ value: 'Max ε', fill: '#f43f5e', fontSize: 10, position: 'right' }}
            />
            <Bar dataKey="epsilon" radius={[4, 4, 0, 0]} maxBarSize={40}>
              {data.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={BUDGET_COLORS(entry.budget_pct ?? 0)}
                  fillOpacity={0.85}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      )}

      {/* Legend */}
      <div className="flex items-center justify-center gap-4 mt-3 pt-3 border-t border-slate-800">
        {[
          { color: 'bg-emerald-500', label: '< 50% budget' },
          { color: 'bg-amber-500', label: '50–75%' },
          { color: 'bg-red-500', label: '> 75% budget' },
        ].map(({ color, label }) => (
          <div key={label} className="flex items-center gap-1.5 text-xs text-slate-500">
            <div className={`w-2 h-2 rounded-full ${color}`} />
            {label}
          </div>
        ))}
      </div>
    </motion.div>
  )
}
