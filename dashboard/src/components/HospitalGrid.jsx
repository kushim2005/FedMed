import { motion } from 'framer-motion'
import { Wifi, WifiOff, Server, Activity } from 'lucide-react'

const STATUS_MAP = {
  connected: {
    label: 'Connected',
    icon: Wifi,
    dot: 'bg-emerald-400',
    border: 'border-emerald-500/30',
    glow: 'shadow-emerald-500/10',
    badge: 'badge-green',
  },
  disconnected: {
    label: 'Offline',
    icon: WifiOff,
    dot: 'bg-red-400',
    border: 'border-red-500/30',
    glow: 'shadow-red-500/10',
    badge: 'badge-yellow',
  },
  training: {
    label: 'Training',
    icon: Activity,
    dot: 'bg-blue-400',
    border: 'border-blue-500/30',
    glow: 'shadow-blue-500/10',
    badge: 'badge-blue',
  },
}

function HospitalCard({ hospital, index }) {
  const cfg = STATUS_MAP[hospital.status] || STATUS_MAP.connected
  const StatusIcon = cfg.icon

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5, delay: index * 0.1 }}
      className={`card p-4 border ${cfg.border} shadow-lg ${cfg.glow} transition-all duration-300`}
    >
      <div className="flex items-start gap-3">
        {/* Flag + status dot */}
        <div className="relative flex-shrink-0">
          <div className="w-12 h-12 rounded-xl bg-slate-800 flex items-center justify-center text-2xl">
            {hospital.flag}
          </div>
          <span className={`absolute -top-1 -right-1 w-3.5 h-3.5 rounded-full border-2 border-slate-900 ${cfg.dot}`} />
        </div>

        {/* Info */}
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 mb-0.5">
            <h3 className="font-semibold text-white text-sm truncate">{hospital.name}</h3>
            <span className={`${cfg.badge} text-[10px] py-0.5`}>
              {cfg.label}
            </span>
          </div>
          <p className="text-slate-500 text-xs mb-3 truncate">{hospital.location}</p>

          {/* Stats row */}
          <div className="grid grid-cols-3 gap-2">
            <div>
              <div className="text-[10px] text-slate-600 mb-0.5">Samples</div>
              <div className="text-xs font-mono font-semibold text-slate-300">
                {hospital.samples ?? '—'}
              </div>
            </div>
            <div>
              <div className="text-[10px] text-slate-600 mb-0.5">Last Dice</div>
              <div className="text-xs font-mono font-semibold text-blue-400">
                {hospital.last_round_dice?.toFixed(3) ?? '—'}
              </div>
            </div>
            <div>
              <div className="text-[10px] text-slate-600 mb-0.5">ε spent</div>
              <div className="text-xs font-mono font-semibold text-purple-400">
                {hospital.current_epsilon?.toFixed(3) ?? '—'}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Connection quality bar */}
      <div className="mt-3 pt-3 border-t border-slate-800/60">
        <div className="flex items-center justify-between text-[10px] text-slate-600 mb-1">
          <span>Signal Quality</span>
          <span className="text-emerald-400 font-semibold">Excellent</span>
        </div>
        <div className="h-1 rounded-full bg-slate-800">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: hospital.status === 'connected' ? '92%' : '0%' }}
            transition={{ duration: 1, delay: index * 0.15 }}
            className="h-full rounded-full bg-gradient-to-r from-emerald-500 to-blue-500"
          />
        </div>
      </div>
    </motion.div>
  )
}

export default function HospitalGrid({ hospitals = [] }) {
  const connected = hospitals.filter(h => h.status === 'connected').length

  return (
    <div className="card p-5 h-full">
      <div className="flex items-center justify-between mb-5">
        <h2 className="section-title">
          <Server className="w-5 h-5 text-emerald-400" />
          Hospital Nodes
        </h2>
        <span className="badge badge-green">
          {connected}/{hospitals.length} Online
        </span>
      </div>

      {hospitals.length === 0 ? (
        <div className="flex items-center justify-center h-32 text-slate-600 text-sm">
          No hospital nodes registered
        </div>
      ) : (
        <div className="space-y-3">
          {hospitals.map((h, i) => (
            <HospitalCard key={h.id} hospital={h} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}
