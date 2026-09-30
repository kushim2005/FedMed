import { motion } from 'framer-motion'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip,
  Legend, ResponsiveContainer, ReferenceLine, Area, ComposedChart,
} from 'recharts'
import { TrendingUp } from 'lucide-react'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-slate-800/95 border border-slate-700 rounded-xl p-3 shadow-2xl text-sm">
      <p className="text-slate-300 font-semibold mb-2">Round {label}</p>
      {payload.map((entry) => (
        <div key={entry.name} className="flex items-center justify-between gap-6 mb-1">
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 rounded-full" style={{ background: entry.color }} />
            <span className="text-slate-400">{entry.name}</span>
          </span>
          <span className="font-mono font-semibold" style={{ color: entry.color }}>
            {entry.value?.toFixed(4)}
          </span>
        </div>
      ))}
    </div>
  )
}

export default function ConvergenceChart({ data = [] }) {
  const maxDice = data.length > 0 ? Math.max(...data.map(d => d.dice)) : 0

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6, delay: 0.2 }}
      className="card p-6 h-full"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="section-title">
            <TrendingUp className="w-5 h-5 text-blue-400" />
            Training Convergence
          </h2>
          <p className="text-slate-500 text-sm mt-1">
            Dice coefficient and loss per federated round
          </p>
        </div>
        <div className="flex items-center gap-2">
          {maxDice > 0 && (
            <span className="badge badge-blue">
              Peak Dice: {maxDice.toFixed(4)}
            </span>
          )}
        </div>
      </div>

      {data.length === 0 ? (
        <div className="flex items-center justify-center h-64 text-slate-600">
          Waiting for training data...
        </div>
      ) : (
        <ResponsiveContainer width="100%" height={300}>
          <ComposedChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
            <defs>
              <linearGradient id="diceGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0.0} />
              </linearGradient>
              <linearGradient id="lossGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#f43f5e" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#f43f5e" stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="round"
              tick={{ fill: '#64748b', fontSize: 12 }}
              axisLine={{ stroke: '#334155' }}
              tickLine={false}
              label={{ value: 'Round', position: 'insideBottom', offset: -2, fill: '#64748b', fontSize: 11 }}
            />
            <YAxis
              yAxisId="dice"
              domain={[0, 1]}
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={v => v.toFixed(2)}
              width={40}
            />
            <YAxis
              yAxisId="loss"
              orientation="right"
              tick={{ fill: '#64748b', fontSize: 11 }}
              axisLine={false}
              tickLine={false}
              tickFormatter={v => v.toFixed(2)}
              width={40}
            />
            <Tooltip content={<CustomTooltip />} />
            <Legend
              wrapperStyle={{ paddingTop: '16px' }}
              formatter={(value) => (
                <span className="text-slate-400 text-xs">{value}</span>
              )}
            />
            <ReferenceLine
              yAxisId="dice"
              y={0.72}
              stroke="#10b981"
              strokeDasharray="5 3"
              strokeOpacity={0.5}
              label={{ value: 'Centralised 0.72', fill: '#10b981', fontSize: 10, position: 'right' }}
            />
            <Area
              yAxisId="dice"
              type="monotone"
              dataKey="dice"
              name="Dice Score"
              stroke="#3b82f6"
              strokeWidth={2.5}
              fill="url(#diceGradient)"
              dot={{ fill: '#3b82f6', r: 4, strokeWidth: 2, stroke: '#1e3a8a' }}
              activeDot={{ r: 6, stroke: '#3b82f6', strokeWidth: 2, fill: '#fff' }}
            />
            <Area
              yAxisId="loss"
              type="monotone"
              dataKey="loss"
              name="Loss"
              stroke="#f43f5e"
              strokeWidth={2}
              fill="url(#lossGradient)"
              strokeDasharray="5 3"
              dot={{ fill: '#f43f5e', r: 3 }}
              activeDot={{ r: 5, stroke: '#f43f5e', strokeWidth: 2, fill: '#fff' }}
            />
            <Line
              yAxisId="dice"
              type="monotone"
              dataKey="dice_et"
              name="Dice ET"
              stroke="#8b5cf6"
              strokeWidth={1.5}
              dot={false}
              strokeDasharray="4 2"
            />
            <Line
              yAxisId="dice"
              type="monotone"
              dataKey="dice_ed"
              name="Dice ED"
              stroke="#06b6d4"
              strokeWidth={1.5}
              dot={false}
              strokeDasharray="4 2"
            />
          </ComposedChart>
        </ResponsiveContainer>
      )}
    </motion.div>
  )
}
