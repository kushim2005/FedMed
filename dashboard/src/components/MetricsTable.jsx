import { motion } from 'framer-motion'
import { BarChart2, ArrowUp, ArrowDown } from 'lucide-react'

const CLASS_LABELS = {
  dice_et: { label: 'Enhancing Tumor (ET)', color: 'text-blue-400', bg: 'bg-blue-500' },
  dice_ed: { label: 'Edema (ED)', color: 'text-purple-400', bg: 'bg-purple-500' },
  dice_ncr: { label: 'Necrotic Core (NCR)', color: 'text-cyan-400', bg: 'bg-cyan-500' },
}

function DiceBar({ value, color }) {
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 bg-slate-800 rounded-full overflow-hidden">
        <motion.div
          initial={{ width: 0 }}
          animate={{ width: `${(value ?? 0) * 100}%` }}
          transition={{ duration: 1, ease: 'easeOut' }}
          className={`h-full rounded-full ${color}`}
        />
      </div>
      <span className="font-mono text-xs text-slate-400 w-12 text-right">
        {value?.toFixed(4) ?? '—'}
      </span>
    </div>
  )
}

export default function MetricsTable({ data = [] }) {
  const latest = data[data.length - 1] ?? {}
  const prev = data[data.length - 2] ?? {}

  const roundRows = data.slice(-5).reverse()

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.4 }}
      className="card p-6"
    >
      <h2 className="section-title mb-6">
        <BarChart2 className="w-5 h-5 text-cyan-400" />
        Per-Class Segmentation Metrics
      </h2>

      {/* Current round per-class bars */}
      <div className="space-y-4 mb-6">
        {Object.entries(CLASS_LABELS).map(([key, { label, color, bg }]) => (
          <div key={key}>
            <div className="flex justify-between items-center mb-1.5">
              <span className={`text-xs font-medium ${color}`}>{label}</span>
              <span className="text-xs text-slate-500">
                Round {latest.round ?? '—'}
              </span>
            </div>
            <DiceBar value={latest[key]} color={bg} />
          </div>
        ))}

        {/* HD95 */}
        <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
          <span className="text-xs text-slate-400">Hausdorff Distance 95 (HD95)</span>
          <span className="font-mono text-sm font-semibold text-amber-400">
            {latest.hd95?.toFixed(1) ?? '—'} mm
          </span>
        </div>
      </div>

      {/* Recent rounds table */}
      <div>
        <h3 className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-3">
          Recent Rounds
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-xs">
            <thead>
              <tr className="border-b border-slate-800">
                {['Round', 'Dice', 'Loss', 'ET', 'ED', 'NCR', 'HD95'].map(h => (
                  <th key={h} className="text-left py-2 pr-3 text-slate-500 font-medium">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {roundRows.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-6 text-center text-slate-600">
                    No data yet
                  </td>
                </tr>
              ) : (
                roundRows.map((row, i) => {
                  const isLatest = i === 0
                  const diceDelta = row.dice - (data[data.indexOf(row) - 1]?.dice ?? row.dice)
                  return (
                    <tr
                      key={row.round}
                      className={`border-b border-slate-800/40 transition-colors ${isLatest ? 'bg-blue-500/5' : 'hover:bg-slate-800/30'}`}
                    >
                      <td className="py-2 pr-3">
                        <span className={`font-mono font-semibold ${isLatest ? 'text-blue-400' : 'text-slate-400'}`}>
                          {row.round}
                          {isLatest && <span className="ml-1 text-[10px] text-emerald-400">●</span>}
                        </span>
                      </td>
                      <td className="py-2 pr-3">
                        <span className="flex items-center gap-1 font-mono text-white">
                          {row.dice?.toFixed(4)}
                          {diceDelta !== 0 && (
                            <span className={diceDelta > 0 ? 'text-emerald-400' : 'text-red-400'}>
                              {diceDelta > 0 ? <ArrowUp className="w-3 h-3" /> : <ArrowDown className="w-3 h-3" />}
                            </span>
                          )}
                        </span>
                      </td>
                      <td className="py-2 pr-3 font-mono text-red-400">{row.loss?.toFixed(4)}</td>
                      <td className="py-2 pr-3 font-mono text-blue-400">{row.dice_et?.toFixed(3)}</td>
                      <td className="py-2 pr-3 font-mono text-purple-400">{row.dice_ed?.toFixed(3)}</td>
                      <td className="py-2 pr-3 font-mono text-cyan-400">{row.dice_ncr?.toFixed(3)}</td>
                      <td className="py-2 font-mono text-amber-400">{row.hd95?.toFixed(1)}mm</td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  )
}
