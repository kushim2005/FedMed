import { motion } from 'framer-motion'
import { Brain, Lock, Network, TrendingUp } from 'lucide-react'

export default function HeroSection({ totalRounds = 0, currentDice = 0, currentEpsilon = 0 }) {
  return (
    <section className="relative pt-10 pb-6 overflow-hidden">
      {/* Background glow blobs */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-1/4 w-96 h-96 bg-blue-600/10 rounded-full blur-3xl" />
        <div className="absolute top-10 right-1/4 w-80 h-80 bg-purple-600/10 rounded-full blur-3xl" />
        <div className="absolute -bottom-10 left-1/2 w-64 h-64 bg-cyan-600/8 rounded-full blur-3xl" />
      </div>

      <div className="relative flex flex-col lg:flex-row items-center gap-10">
        {/* Left — Text content */}
        <div className="flex-1 text-center lg:text-left">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-blue-500/10 border border-blue-500/30 mb-6">
              <span className="pulse-dot bg-emerald-400" />
              <span className="text-blue-300 text-sm font-medium">
                Active Federated Training Session
              </span>
            </div>

            <h1 className="text-4xl lg:text-6xl font-extrabold leading-tight mb-4">
              <span className="gradient-text">Cross-Silo</span>
              <br />
              <span className="text-white">Federated Learning</span>
              <br />
              <span className="text-slate-400 text-3xl lg:text-4xl font-semibold">
                for Brain Tumor Segmentation
              </span>
            </h1>

            <p className="text-slate-400 text-lg max-w-xl mb-8 leading-relaxed">
              Privacy-preserving collaborative AI across hospital networks.
              Homomorphic Encryption + Differential Privacy ensures patient
              data never leaves institutional boundaries.
            </p>

            {/* Quick stats row */}
            <div className="flex flex-wrap justify-center lg:justify-start gap-6">
              {[
                { icon: TrendingUp, label: 'Rounds Complete', value: totalRounds, color: 'text-blue-400' },
                { icon: Brain, label: 'Best Dice Score', value: currentDice.toFixed(3), color: 'text-purple-400' },
                { icon: Lock, label: 'Privacy ε', value: currentEpsilon.toFixed(3), color: 'text-emerald-400' },
                { icon: Network, label: 'Hospital Nodes', value: '3', color: 'text-cyan-400' },
              ].map(({ icon: Icon, label, value, color }) => (
                <div key={label} className="text-center lg:text-left">
                  <div className={`flex items-center gap-1.5 text-xs text-slate-500 mb-1`}>
                    <Icon className={`w-3.5 h-3.5 ${color}`} />
                    {label}
                  </div>
                  <div className={`text-2xl font-bold font-mono ${color}`}>{value}</div>
                </div>
              ))}
            </div>
          </motion.div>
        </div>

        {/* Right — Animated FL Network SVG */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="flex-shrink-0"
        >
          <FLNetworkDiagram />
        </motion.div>
      </div>
    </section>
  )
}

function FLNetworkDiagram() {
  const hospitals = [
    { x: 80, y: 60, label: 'AIIMS Delhi', flag: '🇮🇳', color: '#3b82f6' },
    { x: 280, y: 40, label: 'Mayo Clinic', flag: '🇺🇸', color: '#8b5cf6' },
    { x: 180, y: 210, label: 'NHS London', flag: '🇬🇧', color: '#10b981' },
  ]
  const center = { x: 180, y: 120 }

  return (
    <div className="card p-6 w-[380px]">
      <div className="text-center mb-4">
        <span className="text-xs text-slate-500 uppercase tracking-widest font-semibold">
          FL Network Topology
        </span>
      </div>
      <svg viewBox="0 0 360 280" className="w-full" style={{ height: 200 }}>
        {/* Connection lines with animated data flow */}
        {hospitals.map((h, i) => (
          <g key={i}>
            <line
              x1={center.x} y1={center.y}
              x2={h.x} y2={h.y}
              stroke={h.color}
              strokeWidth="1.5"
              strokeOpacity="0.3"
            />
            <line
              x1={h.x} y1={h.y}
              x2={center.x} y2={center.y}
              stroke={h.color}
              strokeWidth="2"
              strokeDasharray="8 4"
              strokeOpacity="0.8"
              className="data-flow-line"
              style={{ animationDelay: `${i * 0.7}s` }}
            />
          </g>
        ))}

        {/* Server node */}
        <g>
          <circle cx={center.x} cy={center.y} r="28" fill="#1e293b" stroke="#3b82f6" strokeWidth="2" />
          <circle cx={center.x} cy={center.y} r="20" fill="#3b82f620" />
          <text x={center.x} y={center.y - 4} textAnchor="middle" fontSize="10" fill="#93c5fd" fontWeight="bold">
            FL
          </text>
          <text x={center.x} y={center.y + 8} textAnchor="middle" fontSize="8" fill="#64748b">
            Server
          </text>
        </g>

        {/* Hospital nodes */}
        {hospitals.map((h, i) => (
          <g key={`h-${i}`}>
            <circle cx={h.x} cy={h.y} r="22" fill="#0f172a" stroke={h.color} strokeWidth="2" />
            <circle cx={h.x} cy={h.y} r="14" fill={`${h.color}20`} />
            <text x={h.x} y={h.y + 4} textAnchor="middle" fontSize="14">
              {h.flag}
            </text>
            <text x={h.x} y={h.y + 35} textAnchor="middle" fontSize="8" fill="#94a3b8" fontWeight="500">
              {h.label}
            </text>
          </g>
        ))}

        {/* Legend */}
        <g>
          <circle cx={10} cy={258} r="4" fill="#3b82f6" />
          <text x={18} y={262} fontSize="8" fill="#64748b">Encrypted weights</text>
          <circle cx={130} cy={258} r="4" fill="#10b981" />
          <text x={138} y={262} fontSize="8" fill="#64748b">Global model</text>
          <circle cx={230} cy={258} r="4" fill="#8b5cf6" />
          <text x={238} y={262} fontSize="8" fill="#64748b">DP-SGD noise</text>
        </g>
      </svg>

      <div className="flex items-center justify-center gap-6 mt-2 pt-3 border-t border-slate-800">
        <div className="text-center">
          <div className="text-xs text-slate-500">Protocol</div>
          <div className="text-xs font-semibold text-blue-400">FedProx + HE</div>
        </div>
        <div className="text-center">
          <div className="text-xs text-slate-500">Security</div>
          <div className="text-xs font-semibold text-purple-400">128-bit CKKS</div>
        </div>
        <div className="text-center">
          <div className="text-xs text-slate-500">Privacy</div>
          <div className="text-xs font-semibold text-emerald-400">(ε,δ)-DP</div>
        </div>
      </div>
    </div>
  )
}
