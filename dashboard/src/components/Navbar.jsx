import { motion } from 'framer-motion'
import { Activity, Shield, Cpu, Github, ExternalLink } from 'lucide-react'

const STATUS_CONFIG = {
  live: { label: 'LIVE', color: 'text-emerald-400', dot: 'bg-emerald-400' },
  loading: { label: 'SYNCING', color: 'text-amber-400', dot: 'bg-amber-400' },
  error: { label: 'OFFLINE', color: 'text-red-400', dot: 'bg-red-400' },
}

export default function Navbar({ lastUpdated, status = 'live' }) {
  const cfg = STATUS_CONFIG[status] || STATUS_CONFIG.live
  const timeStr = lastUpdated
    ? lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
    : '--:--:--'

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="sticky top-0 z-50 border-b border-slate-800/60 bg-slate-950/80 backdrop-blur-xl"
    >
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Logo */}
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center shadow-lg shadow-blue-500/30">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <div className="absolute -top-0.5 -right-0.5 w-3 h-3 rounded-full bg-emerald-400 border-2 border-slate-950" />
          </div>
          <div>
            <span className="text-xl font-bold gradient-text">FedMed</span>
            <span className="ml-2 text-xs text-slate-500 font-medium hidden sm:inline">
              Federated Learning Dashboard
            </span>
          </div>
        </div>

        {/* Center — Tech Stack Badges */}
        <div className="hidden md:flex items-center gap-2">
          <span className="badge badge-blue">
            <Shield className="w-3 h-3" />
            DP-SGD ε=2.79
          </span>
          <span className="badge badge-purple">
            <Cpu className="w-3 h-3" />
            CKKS HE
          </span>
          <span className="badge badge-green">
            3 Hospital Nodes
          </span>
        </div>

        {/* Right — Status + Links */}
        <div className="flex items-center gap-4">
          {/* Live status */}
          <div className="flex items-center gap-2 text-sm">
            <span className={`pulse-dot ${cfg.dot.replace('bg-', 'bg-')}`} />
            <span className={`font-mono text-xs ${cfg.color} font-semibold`}>
              {cfg.label}
            </span>
            <span className="text-slate-600 text-xs font-mono hidden sm:inline">
              {timeStr}
            </span>
          </div>

          {/* GitHub link */}
          <a
            href="https://github.com/kushim2005/FedMed"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1.5 text-slate-400 hover:text-white transition-colors text-sm"
          >
            <Github className="w-4 h-4" />
            <ExternalLink className="w-3 h-3 opacity-60" />
          </a>
        </div>
      </div>
    </motion.nav>
  )
}
