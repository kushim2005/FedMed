export default function Footer() {
  return (
    <footer className="border-t border-slate-800/60 mt-16 py-8">
      <div className="max-w-[1600px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-center sm:text-left">
            <div className="text-sm font-semibold text-slate-300 mb-1">
              FedMed — Cross-Silo Federated Learning Engine
            </div>
            <div className="text-xs text-slate-600">
              Brain Tumor Segmentation · BraTS 2021 · MONAI + Flower + TenSEAL + Opacus
            </div>
          </div>
          <div className="flex items-center gap-6 text-xs text-slate-600">
            <span>🏥 AIIMS Delhi · Mayo Clinic · NHS London</span>
            <span className="hidden sm:inline">·</span>
            <a
              href="https://github.com/kushim2005/FedMed"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:text-blue-400 transition-colors"
            >
              github.com/kushim2005/FedMed
            </a>
          </div>
        </div>
        <div className="mt-4 pt-4 border-t border-slate-800/40 flex flex-wrap justify-center gap-4 text-[10px] text-slate-700">
          {['Python 3.10', 'PyTorch 2.1', 'MONAI 1.3', 'Flower 1.6', 'TenSEAL 0.3.14', 'Opacus', 'React 18', 'Vite 5', 'TailwindCSS 3'].map(t => (
            <span key={t} className="px-2 py-0.5 rounded bg-slate-800/60 font-mono">{t}</span>
          ))}
        </div>
      </div>
    </footer>
  )
}
