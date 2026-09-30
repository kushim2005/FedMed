import { motion } from 'framer-motion'
import { Layers } from 'lucide-react'

const STEPS = [
  {
    id: 1,
    phase: 'Local Training',
    desc: 'Hospital trains on local BraTS data with DP-SGD (σ=1.1, C=1.0)',
    color: '#3b82f6',
    icon: '🏥',
    detail: 'FedProx + Opacus',
  },
  {
    id: 2,
    phase: 'HE Encryption',
    desc: 'Weight updates encrypted with CKKS (128-bit, poly_n=8192)',
    color: '#8b5cf6',
    icon: '🔐',
    detail: 'TenSEAL CKKS',
  },
  {
    id: 3,
    phase: 'Secure Aggregation',
    desc: 'Server computes FedAvg over ciphertexts — never sees plaintext',
    color: '#10b981',
    icon: '⚡',
    detail: 'HE FedAvg',
  },
  {
    id: 4,
    phase: 'Global Broadcast',
    desc: 'Decrypted global model distributed back to all hospital nodes',
    color: '#f59e0b',
    icon: '📡',
    detail: 'gRPC + TLS',
  },
]

function StepCard({ step, index }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: index * 0.15 }}
      className="relative"
    >
      {/* Connector line */}
      {index < STEPS.length - 1 && (
        <div
          className="absolute top-8 left-[calc(50%+2rem)] right-0 h-0.5 hidden xl:block"
          style={{
            background: `linear-gradient(90deg, ${step.color}60, ${STEPS[index + 1].color}60)`,
          }}
        />
      )}

      <div
        className="card p-5 relative border transition-all duration-300 hover:scale-105"
        style={{ borderColor: `${step.color}30` }}
      >
        {/* Step number */}
        <div
          className="absolute -top-3 left-4 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold text-white"
          style={{ background: step.color }}
        >
          {step.id}
        </div>

        <div className="flex items-center gap-3 mb-3 mt-1">
          <span className="text-2xl">{step.icon}</span>
          <div>
            <h3 className="font-semibold text-white text-sm">{step.phase}</h3>
            <span
              className="text-[10px] font-mono font-medium px-2 py-0.5 rounded"
              style={{ background: `${step.color}20`, color: step.color }}
            >
              {step.detail}
            </span>
          </div>
        </div>

        <p className="text-slate-400 text-xs leading-relaxed">{step.desc}</p>
      </div>
    </motion.div>
  )
}

export default function ArchitectureViz({ hospitals = [] }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6, delay: 0.5 }}
      className="card p-6"
    >
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="section-title">
            <Layers className="w-5 h-5 text-amber-400" />
            Federated Learning Pipeline
          </h2>
          <p className="text-slate-500 text-sm mt-1">
            End-to-end secure training cycle — Week 3 + Week 4 stack
          </p>
        </div>
        <div className="flex gap-2">
          <span className="badge badge-blue">HE Week 3</span>
          <span className="badge badge-purple">DP-SGD Week 4</span>
        </div>
      </div>

      {/* Pipeline steps */}
      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-6 relative">
        {STEPS.map((step, i) => (
          <StepCard key={step.id} step={step} index={i} />
        ))}
      </div>

      {/* Security guarantees footer */}
      <div className="mt-6 pt-5 border-t border-slate-800 grid grid-cols-1 sm:grid-cols-3 gap-4">
        {[
          {
            title: 'Data Privacy',
            value: '(ε=2.79, δ=1e-5)-DP',
            desc: 'Rényi DP via Opacus DP-SGD',
            color: 'text-purple-400',
          },
          {
            title: 'Weight Confidentiality',
            value: '128-bit IND-CPA',
            desc: 'CKKS under RLWE assumption',
            color: 'text-blue-400',
          },
          {
            title: 'Transport Security',
            value: 'TLS 1.3 + mTLS',
            desc: 'RSA-2048 mutual authentication',
            color: 'text-emerald-400',
          },
        ].map(({ title, value, desc, color }) => (
          <div key={title} className="bg-slate-800/40 rounded-xl p-4">
            <div className="text-xs text-slate-500 mb-1">{title}</div>
            <div className={`font-mono font-semibold text-sm ${color}`}>{value}</div>
            <div className="text-xs text-slate-600 mt-0.5">{desc}</div>
          </div>
        ))}
      </div>
    </motion.div>
  )
}
