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

export interface BatteryAbnormalCycle {
  id: number
  change_date: string
  usage_days: number
  reason: string
}

export interface BatteryEarMetrics {
  count: number
  last_change_date: string | null
  avg_cycle_days: number
  min_cycle_days: number
  max_cycle_days: number
  next_expected_date: string | null
  overdue_days: number
  status: 'normal' | 'soon_due' | 'overdue' | 'no_data'
  abnormal_cycles: BatteryAbnormalCycle[]
}

export interface BatteryStats {
  profile_id: number
  today: string
  warn_days_before: number
  status: 'normal' | 'soon_due' | 'overdue' | 'abnormal' | 'no_data'
  left_ear: BatteryEarMetrics
  right_ear: BatteryEarMetrics
  recent_records: BatteryRecord[]
}

export interface BatteryEarSummary {
  status: 'normal' | 'soon_due' | 'overdue' | 'no_data'
  last_change_date: string | null
  next_expected_date: string | null
  overdue_days: number
  avg_cycle_days: number
  abnormal_cycles: BatteryAbnormalCycle[]
}

export interface BatteryWarningProfile {
  profile_id: number
  elderly_name: string
  contact_person?: string
  contact_phone?: string
  fitting_store?: string
  status: 'normal' | 'soon_due' | 'overdue' | 'abnormal' | 'no_data'
  left_ear: BatteryEarSummary
  right_ear: BatteryEarSummary
  abnormal_cycles: BatteryAbnormalCycle[]
}

export interface BatteryWarnings {
  today: string
  warn_days_before: number
  summary: {
    total_profiles: number
    overdue_count: number
    soon_due_count: number
    abnormal_count: number
    normal_count: number
    no_data_count: number
  }
  overdue: BatteryWarningProfile[]
  soon_due: BatteryWarningProfile[]
  abnormal: BatteryWarningProfile[]
}

export interface Task {
  id?: number
  profile_id: number
  elderly_name?: string
  title: string
  task_type: string
  description?: string
  assignee?: string
  due_date?: string
  priority?: 'low' | 'medium' | 'high' | 'urgent'
  status?: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  notes?: string
  completion_feedback?: string
  completed_at?: string
  related_feedback_id?: number
  related_adjustment_id?: number
  related_followup_id?: number
  is_overdue?: boolean
  days_until_due?: number
  created_at?: string
  updated_at?: string
}

export interface TaskMeta {
  task_types: string[]
  statuses: string[]
  priorities: string[]
  status_labels: Record<string, string>
  priority_labels: Record<string, string>
}

export interface TaskTypeDistribution {
  type: string
  count: number
  percentage: number
}

export interface TaskProfileSummary {
  profile_id: number
  elderly_name: string
  total: number
  pending: number
  in_progress: number
  completed: number
  cancelled: number
  overdue: number
  soon_due: number
}

export interface TaskOverview {
  today: string
  summary: {
    total: number
    completed: number
    pending: number
    in_progress: number
    cancelled: number
    overdue: number
    soon_due: number
    completion_rate: number
  }
  type_distribution: TaskTypeDistribution[]
  by_profile: TaskProfileSummary[]
}

export interface TaskSummary {
  profile_id: number
  summary: {
    total: number
    completed: number
    pending: number
    in_progress: number
    cancelled: number
    overdue: number
    soon_due: number
    completion_rate: number
  }
  recent_tasks: Task[]
}

export const TASK_TYPES = [
  { value: '提醒佩戴', label: '提醒佩戴', icon: '👂' },
  { value: '提醒清洁耳塞', label: '提醒清洁耳塞', icon: '🧹' },
  { value: '预约复诊', label: '预约复诊', icon: '📅' },
  { value: '购买电池', label: '购买电池', icon: '🔋' },
  { value: '观察特定场景听感', label: '观察特定场景听感', icon: '👀' },
  { value: '其他', label: '其他', icon: '📝' }
]

export const TASK_PRIORITIES = [
  { value: 'low', label: '低', color: '#909399' },
  { value: 'medium', label: '中', color: '#409eff' },
  { value: 'high', label: '高', color: '#e6a23c' },
  { value: 'urgent', label: '紧急', color: '#f56c6c' }
]

export const TASK_STATUSES = [
  { value: 'pending', label: '待处理', color: '#909399' },
  { value: 'in_progress', label: '进行中', color: '#409eff' },
  { value: 'completed', label: '已完成', color: '#67c23a' },
  { value: 'cancelled', label: '已取消', color: '#c0c4cc' }
]

export interface Consumable {
  id?: number
  profile_id: number
  elderly_name?: string
  name: string
  consumable_type: string
  ear?: string
  start_date?: string
  replacement_cycle_days?: number
  stock_quantity?: number
  last_replacement_date?: string
  next_replacement_date?: string
  days_until_replacement?: number
  notes?: string
  is_overdue?: boolean
  is_soon_due?: boolean
  is_low_stock?: boolean
  status?: 'normal' | 'soon_due' | 'overdue' | 'low_stock'
  created_at?: string
  updated_at?: string
}

export const CONSUMABLE_TYPES = [
  { value: '耳塞', label: '耳塞', icon: '👂' },
  { value: '导声管', label: '导声管', icon: '🔌' },
  { value: '干燥盒', label: '干燥盒', icon: '📦' },
  { value: '电池', label: '电池', icon: '🔋' },
  { value: '清洁刷', label: '清洁刷', icon: '🧹' },
  { value: '其他', label: '其他', icon: '📦' }
]

export const EAR_OPTIONS = [
  { value: '左耳', label: '左耳' },
  { value: '右耳', label: '右耳' },
  { value: '双耳', label: '双耳' },
  { value: '不适用', label: '不适用' }
]

export const CONSUMABLE_STATUSES = [
  { value: 'normal', label: '正常', color: '#67c23a' },
  { value: 'soon_due', label: '即将更换', color: '#e6a23c' },
  { value: 'overdue', label: '已逾期', color: '#f56c6c' },
  { value: 'low_stock', label: '库存不足', color: '#f56c6c' }
]

export interface ServiceTicket {
  id?: number
  profile_id: number
  elderly_name?: string
  consumable_id?: number
  consumable_name?: string
  issue_type: string
  service_method?: string
  appointment_time?: string
  handler?: string
  status?: 'pending' | 'in_progress' | 'completed' | 'cancelled'
  result?: string
  description?: string
  photo_urls?: string[]
  created_at?: string
  updated_at?: string
}

export const SERVICE_TICKET_TYPES = [
  { value: '耗材损坏', label: '耗材损坏', icon: '💥' },
  { value: '佩戴不稳', label: '佩戴不稳', icon: '⚠️' },
  { value: '声音变闷', label: '声音变闷', icon: '🔇' },
  { value: '清洁困难', label: '清洁困难', icon: '🧼' },
  { value: '其他', label: '其他', icon: '📝' }
]

export const SERVICE_METHODS = [
  { value: '上门服务', label: '上门服务', icon: '🚗' },
  { value: '到店服务', label: '到店服务', icon: '🏪' }
]

export const SERVICE_TICKET_STATUSES = [
  { value: 'pending', label: '待处理', color: '#909399' },
  { value: 'in_progress', label: '处理中', color: '#409eff' },
  { value: 'completed', label: '已完成', color: '#67c23a' },
  { value: 'cancelled', label: '已取消', color: '#c0c4cc' }
]

export interface ConsumableMeta {
  consumable_types: string[]
  ear_options: string[]
  status_labels: Record<string, string>
}

export interface ServiceTicketMeta {
  issue_types: string[]
  service_methods: string[]
  statuses: string[]
  status_labels: Record<string, string>
}

export interface TrainingPlan {
  id?: number
  profile_id: number
  elderly_name?: string
  goal: string
  cycle_days: number
  daily_wear_minutes: number
  training_scenario: string
  volume_level?: string
  reminder_frequency?: string
  responsible_person?: string
  notes?: string
  status?: 'active' | 'paused' | 'completed' | 'cancelled'
  start_date: string
  end_date?: string
  completed_days?: number
  completion_rate?: number
  streak_days?: number
  recent_7_days?: TrainingDayStatus[]
  abnormal_alerts?: TrainingAbnormalAlert[]
  created_at?: string
  updated_at?: string
}

export interface TrainingDayStatus {
  date: string
  completed: boolean
  actual_wear_minutes?: number | null
  clarity_level?: string | null
  fatigue_level?: string | null
  has_discomfort?: boolean | null
}

export interface TrainingAbnormalAlert {
  date: string
  issues: string[]
}

export interface TrainingRecord {
  id?: number
  plan_id: number
  profile_id: number
  elderly_name?: string
  training_scenario?: string
  record_date: string
  actual_wear_minutes?: number
  clarity_level?: string
  fatigue_level?: string
  has_discomfort?: boolean
  discomfort_detail?: string
  howling?: string
  howling_detail?: string
  related_feedback_id?: number
  related_adjustment_id?: number
  related_followup_id?: number
  notes?: string
  created_at?: string
}

export interface TrainingMeta {
  training_scenarios: string[]
  plan_statuses: string[]
  volume_levels: string[]
  reminder_frequencies: string[]
  fatigue_levels: string[]
  clarity_levels: string[]
  status_labels: Record<string, string>
}

export interface TrainingOverview {
  total_plans: number
  active_plans: number
  completed_plans: number
  total_records: number
  avg_daily_wear_minutes: number
  overall_completion_rate: number
}

export interface TrainingProfileStats {
  total_plans: number
  active_plans: number
  completed_plans: number
  completion_rate: number
  avg_daily_wear_minutes: number
  streak_days: number
  clarity_change: number
  clarity_trend: { date: string; score: number; level: string }[]
  high_discomfort_scenarios: {
    scenario: string
    total_records: number
    discomfort_count: number
    howling_count: number
    fatigue_count: number
    issue_total: number
  }[]
}

export const TRAINING_SCENARIOS = [
  { value: '居家安静', label: '居家安静', icon: '🏠' },
  { value: '一对一对话', label: '一对一对话', icon: '🗣️' },
  { value: '家庭聚餐', label: '家庭聚餐', icon: '👨‍👩‍👧‍👦' },
  { value: '菜市场', label: '菜市场', icon: '🛒' },
  { value: '户外散步', label: '户外散步', icon: '🚶' },
  { value: '看电视', label: '看电视', icon: '📺' },
  { value: '打电话', label: '打电话', icon: '📞' },
  { value: '会议室', label: '会议室', icon: '💼' },
  { value: '其他', label: '其他', icon: '📝' }
]

export const VOLUME_LEVELS = [
  { value: '低', label: '低' },
  { value: '中低', label: '中低' },
  { value: '中', label: '中' },
  { value: '中高', label: '中高' },
  { value: '高', label: '高' }
]

export const REMINDER_FREQUENCIES = [
  { value: '每天', label: '每天' },
  { value: '每2天', label: '每2天' },
  { value: '每3天', label: '每3天' },
  { value: '每周', label: '每周' }
]

export const TRAINING_PLAN_STATUSES = [
  { value: 'active', label: '进行中', color: '#409eff' },
  { value: 'paused', label: '已暂停', color: '#e6a23c' },
  { value: 'completed', label: '已完成', color: '#67c23a' },
  { value: 'cancelled', label: '已取消', color: '#909399' }
]

export const FATIGUE_LEVELS = [
  { value: '无', label: '无' },
  { value: '轻微', label: '轻微' },
  { value: '一般', label: '一般' },
  { value: '明显', label: '明显' },
  { value: '严重', label: '严重' }
]

export const CLARITY_LEVELS = [
  { value: '完全听不清', label: '完全听不清' },
  { value: '勉强听清', label: '勉强听清' },
  { value: '部分听清', label: '部分听清' },
  { value: '大部分听清', label: '大部分听清' },
  { value: '完全听清', label: '完全听清' }
]
