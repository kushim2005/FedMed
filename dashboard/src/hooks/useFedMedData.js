import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || ''

// Simulated data for offline / demo mode
const DEMO_METRICS = Array.from({ length: 10 }, (_, i) => ({
  round: i + 1,
  dice: parseFloat((0.42 + i * 0.028 + Math.random() * 0.005).toFixed(4)),
  loss: parseFloat((0.72 - i * 0.055 + Math.random() * 0.01).toFixed(4)),
  dice_et: parseFloat((0.41 + i * 0.030).toFixed(4)),
  dice_ed: parseFloat((0.48 + i * 0.027).toFixed(4)),
  dice_ncr: parseFloat((0.30 + i * 0.027).toFixed(4)),
  hd95: parseFloat((22.0 - i * 0.78).toFixed(2)),
  clients: 3,
  round_time: parseFloat((18.2 + Math.random() * 2).toFixed(1)),
}))

const DEMO_PRIVACY = Array.from({ length: 10 }, (_, i) => ({
  round: i + 1,
  epsilon: parseFloat(((i + 1) * 0.279).toFixed(4)),
  delta: 1e-5,
  noise_multiplier: 1.1,
  clip_norm: 1.0,
  budget_pct: parseFloat((((i + 1) * 0.279) / 3.5 * 100).toFixed(1)),
}))

const DEMO_HOSPITALS = [
  {
    id: 'aiims_delhi',
    name: 'AIIMS Delhi',
    location: 'New Delhi, India',
    status: 'connected',
    samples: 187,
    last_round_dice: 0.681,
    current_epsilon: 2.79,
    flag: '🇮🇳',
  },
  {
    id: 'mayo_clinic',
    name: 'Mayo Clinic',
    location: 'Rochester, USA',
    status: 'connected',
    samples: 224,
    last_round_dice: 0.689,
    current_epsilon: 2.79,
    flag: '🇺🇸',
  },
  {
    id: 'nhs_london',
    name: 'NHS London',
    location: 'London, UK',
    status: 'connected',
    samples: 163,
    last_round_dice: 0.678,
    current_epsilon: 2.79,
    flag: '🇬🇧',
  },
]

export function useFedMedData(pollInterval = 5000) {
  const [metrics, setMetrics] = useState(DEMO_METRICS)
  const [hospitals, setHospitals] = useState(DEMO_HOSPITALS)
  const [privacy, setPrivacy] = useState(DEMO_PRIVACY)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [lastUpdated, setLastUpdated] = useState(new Date())

  const fetchData = useCallback(async () => {
    try {
      setLoading(true)
      const [metricsRes, hospitalsRes, privacyRes] = await Promise.all([
        axios.get(`${API_BASE}/api/metrics`, { timeout: 3000 }),
        axios.get(`${API_BASE}/api/hospitals`, { timeout: 3000 }),
        axios.get(`${API_BASE}/api/privacy`, { timeout: 3000 }),
      ])
      setMetrics(metricsRes.data)
      setHospitals(hospitalsRes.data)
      setPrivacy(privacyRes.data)
      setError(null)
      setLastUpdated(new Date())
    } catch {
      // Fall back to demo data silently — API may not be running locally
      setMetrics(DEMO_METRICS)
      setHospitals(DEMO_HOSPITALS)
      setPrivacy(DEMO_PRIVACY)
      setLastUpdated(new Date())
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    fetchData()
    const interval = setInterval(fetchData, pollInterval)
    return () => clearInterval(interval)
  }, [fetchData, pollInterval])

  return { metrics, hospitals, privacy, loading, error, lastUpdated }
}
