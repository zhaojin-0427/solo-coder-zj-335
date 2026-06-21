export interface Profile {
  id?: number
  elderly_name: string
  age?: number
  gender?: string
  contact_person?: string
  contact_phone?: string
  hearing_aid_model_left?: string
  hearing_aid_model_right?: string
  ear_config_left?: string
  ear_config_right?: string
  fitting_date?: string
  fitting_store?: string
  audiologist?: string
  common_scenarios?: string
  notes?: string
  created_at?: string
  updated_at?: string
}

export interface Feedback {
  id?: number
  profile_id: number
  feedback_date: string
  scenario: string
  scenario_detail?: string
  duration_minutes?: number
  hearing_experience?: string
  hearing_experience_detail?: string
  howling?: string
  howling_detail?: string
  discomfort?: string
  discomfort_detail?: string
  left_ear_rating?: number
  right_ear_rating?: number
  overall_rating?: number
  notes?: string
  created_at?: string
}

export interface Adjustment {
  id?: number
  profile_id: number
  adjustment_date: string
  adjuster?: string
  left_ear_adjustment?: string
  right_ear_adjustment?: string
  program_adjustment?: string
  volume_adjustment?: string
  feedback_suppression?: string
  noise_reduction?: string
  other_adjustments?: string
  reason?: string
  expected_effect?: string
  notes?: string
  created_at?: string
}

export interface Followup {
  id?: number
  profile_id: number
  adjustment_id?: number
  followup_date: string
  followup_type?: string
  hearing_improvement?: string
  howling_improvement?: string
  discomfort_improvement?: string
  adaptation_status?: string
  daily_usage_hours?: number
  left_ear_rating?: number
  right_ear_rating?: number
  overall_rating?: number
  issues_remaining?: string
  suggestions?: string
  next_followup_date?: string
  notes?: string
  created_at?: string
}

export interface BatteryRecord {
  id?: number
  profile_id: number
  change_date: string
  ear: string
  battery_type?: string
  battery_brand?: string
  last_change_date?: string
  usage_days?: number
  notes?: string
  created_at?: string
}

export interface Suggestion {
  scenario: string
  feedback_count: number
  average_rating: number
  issues: string[]
  recommendations: string[]
}

export const SCENARIOS = [
  { value: '菜市场', label: '菜市场', icon: '🛒' },
  { value: '家庭聚餐', label: '家庭聚餐', icon: '👨‍👩‍👧‍👦' },
  { value: '看电视', label: '看电视', icon: '📺' },
  { value: '户外散步', label: '户外散步', icon: '🚶' },
  { value: '打电话', label: '打电话', icon: '📞' },
  { value: '办公室', label: '办公室', icon: '💼' },
  { value: '其他', label: '其他', icon: '📝' }
]

export const HEARING_EXPERIENCE_OPTIONS = [
  { value: '很好', label: '很好' },
  { value: '好', label: '好' },
  { value: '一般', label: '一般' },
  { value: '差', label: '差' },
  { value: '很差', label: '很差' }
]

export const HOWLING_OPTIONS = [
  { value: '无', label: '无' },
  { value: '偶尔', label: '偶尔' },
  { value: '经常', label: '经常' },
  { value: '严重', label: '严重' }
]

export const DISCOMFORT_OPTIONS = [
  { value: '无', label: '无' },
  { value: '轻微', label: '轻微' },
  { value: '有', label: '有' },
  { value: '严重', label: '严重' }
]

export const IMPROVEMENT_OPTIONS = [
  { value: '明显改善', label: '明显改善' },
  { value: '略有改善', label: '略有改善' },
  { value: '无变化', label: '无变化' },
  { value: '略有下降', label: '略有下降' },
  { value: '明显下降', label: '明显下降' }
]
