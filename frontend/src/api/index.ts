import axios from 'axios'
import type { Profile, Feedback, Adjustment, Followup, BatteryRecord } from '@/types'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

export const profileApi = {
  getAll: () => api.get<Profile[]>('/profiles'),
  get: (id: number) => api.get<Profile>(`/profiles/${id}`),
  create: (data: Profile) => api.post<Profile>('/profiles', data),
  update: (id: number, data: Profile) => api.put<Profile>(`/profiles/${id}`, data),
  delete: (id: number) => api.delete(`/profiles/${id}`)
}

export const feedbackApi = {
  getAll: (profileId?: number, scenario?: string) => {
    const params: Record<string, any> = {}
    if (profileId) params.profile_id = profileId
    if (scenario) params.scenario = scenario
    return api.get<Feedback[]>('/feedback', { params })
  },
  get: (id: number) => api.get<Feedback>(`/feedback/${id}`),
  create: (data: Feedback) => api.post<Feedback>('/feedback', data),
  update: (id: number, data: Feedback) => api.put<Feedback>(`/feedback/${id}`, data),
  delete: (id: number) => api.delete(`/feedback/${id}`),
  getSuggestions: (profileId: number) => api.get(`/feedback/suggestions/${profileId}`)
}

export const adjustmentApi = {
  getAll: (profileId?: number) => {
    const params = profileId ? { profile_id: profileId } : {}
    return api.get<Adjustment[]>('/adjustments', { params })
  },
  get: (id: number) => api.get<Adjustment>(`/adjustments/${id}`),
  create: (data: Adjustment) => api.post<Adjustment>('/adjustments', data),
  update: (id: number, data: Adjustment) => api.put<Adjustment>(`/adjustments/${id}`, data),
  delete: (id: number) => api.delete(`/adjustments/${id}`)
}

export const followupApi = {
  getAll: (profileId?: number, adjustmentId?: number) => {
    const params: Record<string, any> = {}
    if (profileId) params.profile_id = profileId
    if (adjustmentId) params.adjustment_id = adjustmentId
    return api.get<Followup[]>('/followups', { params })
  },
  get: (id: number) => api.get<Followup>(`/followups/${id}`),
  create: (data: Followup) => api.post<Followup>('/followups', data),
  update: (id: number, data: Followup) => api.put<Followup>(`/followups/${id}`, data),
  delete: (id: number) => api.delete(`/followups/${id}`)
}

export const batteryApi = {
  getAll: (profileId?: number, ear?: string) => {
    const params: Record<string, any> = {}
    if (profileId) params.profile_id = profileId
    if (ear) params.ear = ear
    return api.get<BatteryRecord[]>('/batteries', { params })
  },
  get: (id: number) => api.get<BatteryRecord>(`/batteries/${id}`),
  create: (data: BatteryRecord) => api.post<BatteryRecord>('/batteries', data),
  update: (id: number, data: BatteryRecord) => api.put<BatteryRecord>(`/batteries/${id}`, data),
  delete: (id: number) => api.delete(`/batteries/${id}`),
  getStats: (profileId: number) => api.get(`/batteries/stats/${profileId}`)
}

export const statisticsApi = {
  getDiscomfortScenarios: (profileId: number) => api.get(`/statistics/discomfort-scenarios/${profileId}`),
  getEarDifference: (profileId: number) => api.get(`/statistics/ear-difference/${profileId}`),
  getBatteryCycle: (profileId: number) => api.get(`/statistics/battery-cycle/${profileId}`),
  getImprovementRate: (profileId: number) => api.get(`/statistics/improvement-rate/${profileId}`),
  getOverview: (profileId: number) => api.get(`/statistics/overview/${profileId}`),
  getTrends: (profileId: number, days?: number) => {
    const params = days ? { days } : {}
    return api.get(`/statistics/trends/${profileId}`, { params })
  }
}

export default api
