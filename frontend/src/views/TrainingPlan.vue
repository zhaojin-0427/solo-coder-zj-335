<template>
  <div class="training-page">
    <div class="page-header">
      <h1 class="page-title">听力训练与佩戴适应计划</h1>
      <el-button type="primary" @click="openPlanDialog">
        <el-icon><Plus /></el-icon>
        创建训练计划
      </el-button>
    </div>

    <div class="card filter-bar">
      <el-row :gutter="16">
        <el-col :span="5">
          <el-select v-model="filterProfileId" placeholder="选择老人" clearable @change="loadPlans" style="width: 100%">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterStatus" placeholder="计划状态" clearable @change="loadPlans" style="width: 100%">
            <el-option v-for="s in TRAINING_PLAN_STATUSES" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterScenario" placeholder="训练场景" clearable @change="loadPlans" style="width: 100%">
            <el-option v-for="s in TRAINING_SCENARIOS" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterDiscomfort" placeholder="是否不适" clearable @change="loadPlans" style="width: 100%">
            <el-option label="出现不适" value="true" />
          </el-select>
        </el-col>
        <el-col :span="4">
          <el-select v-model="filterCompletion" placeholder="完成情况" clearable @change="loadPlans" style="width: 100%">
            <el-option label="完成率≥80%" value="high" />
            <el-option label="完成率50%-80%" value="mid" />
            <el-option label="完成率<50%" value="low" />
          </el-select>
        </el-col>
      </el-row>
    </div>

    <div v-loading="loading">
      <el-empty v-if="plans.length === 0 && !loading" description="暂无训练计划，点击上方按钮创建" :image-size="100" />

      <div v-for="plan in filteredPlans" :key="plan.id" class="plan-card card">
        <div class="plan-header">
          <div class="plan-title-area">
            <span class="plan-scenario-icon">{{ getScenarioIcon(plan.training_scenario) }}</span>
            <strong class="plan-elderly">{{ plan.elderly_name }}</strong>
            <el-tag :type="getStatusTagType(plan.status)" size="small" effect="dark">
              {{ getStatusLabel(plan.status) }}
            </el-tag>
            <el-tag type="info" size="small">{{ plan.training_scenario }}</el-tag>
            <el-tag v-if="plan.streak_days && plan.streak_days > 0" type="warning" effect="dark" size="small">
              🔥 连续{{ plan.streak_days }}天
            </el-tag>
          </div>
          <div class="plan-actions">
            <el-button size="small" type="success" @click="openRecordDialog(plan)">
              <el-icon><Plus /></el-icon>
              登记训练
            </el-button>
            <el-button size="small" @click="viewPlanDetail(plan)">
              <el-icon><View /></el-icon>
              详情
            </el-button>
            <el-button size="small" @click="openEditPlanDialog(plan)">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
            <el-button size="small" type="danger" @click="deletePlan(plan)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>

        <div class="plan-info">
          <el-descriptions :column="4" size="small" border>
            <el-descriptions-item label="训练目标">{{ plan.goal }}</el-descriptions-item>
            <el-descriptions-item label="训练周期">{{ plan.cycle_days }} 天</el-descriptions-item>
            <el-descriptions-item label="每日佩戴">{{ plan.daily_wear_minutes }} 分钟</el-descriptions-item>
            <el-descriptions-item label="音量等级">{{ plan.volume_level }}</el-descriptions-item>
            <el-descriptions-item label="提醒频率">{{ plan.reminder_frequency }}</el-descriptions-item>
            <el-descriptions-item label="负责人">{{ plan.responsible_person || '-' }}</el-descriptions-item>
            <el-descriptions-item label="开始日期">{{ plan.start_date }}</el-descriptions-item>
            <el-descriptions-item label="结束日期">{{ plan.end_date || '-' }}</el-descriptions-item>
          </el-descriptions>
        </div>

        <div class="plan-progress">
          <div class="progress-header">
            <span>训练进度：{{ plan.completed_days || 0 }} / {{ plan.cycle_days }} 天</span>
            <span :class="{'text-success': (plan.completion_rate || 0) >= 80, 'text-warning': (plan.completion_rate || 0) >= 50 && (plan.completion_rate || 0) < 80, 'text-danger': (plan.completion_rate || 0) < 50}">
              {{ plan.completion_rate || 0 }}%
            </span>
          </div>
          <el-progress :percentage="Math.min(plan.completion_rate || 0, 100)" :color="getProgressColor(plan.completion_rate || 0)" :stroke-width="12" />
        </div>

        <div v-if="plan.recent_7_days && plan.recent_7_days.length > 0" class="plan-7days">
          <h4 style="margin: 0 0 8px 0; font-size: 13px; color: #606266">近 7 天完成情况</h4>
          <div class="day-grid">
            <div v-for="day in plan.recent_7_days" :key="day.date" class="day-cell" :class="{'day-completed': day.completed, 'day-missed': !day.completed, 'day-discomfort': day.has_discomfort}">
              <div class="day-date">{{ day.date.substring(5) }}</div>
              <div class="day-icon">{{ day.completed ? '✅' : '⬜' }}</div>
              <div v-if="day.completed && day.actual_wear_minutes" class="day-wear">{{ day.actual_wear_minutes }}min</div>
              <div v-if="day.has_discomfort" class="day-alert">⚠️</div>
            </div>
          </div>
        </div>

        <el-alert
          v-if="plan.abnormal_alerts && plan.abnormal_alerts.length > 0"
          :title="`近7天有 ${plan.abnormal_alerts.length} 天出现异常`"
          type="warning"
          :closable="false"
          show-icon
          style="margin-top: 12px"
        >
          <div style="margin-top: 4px">
            <div v-for="alert in plan.abnormal_alerts" :key="alert.date" style="font-size: 13px; margin-bottom: 2px">
              <strong>{{ alert.date }}</strong>：{{ alert.issues.join('、') }}
            </div>
          </div>
        </el-alert>
      </div>
    </div>

    <el-dialog v-model="planDialogVisible" :title="isPlanEdit ? '编辑训练计划' : '创建训练计划'" width="700px" :close-on-click-modal="false">
      <el-form :model="planForm" label-width="110px">
        <el-form-item label="老人" required>
          <el-select v-model="planForm.profile_id" placeholder="选择老人" :disabled="isPlanEdit" style="width: 100%">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="训练目标" required>
          <el-input v-model="planForm.goal" placeholder="如：适应菜市场环境正常交流" maxlength="200" show-word-limit />
        </el-form-item>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="训练周期" required>
              <el-input-number v-model="planForm.cycle_days" :min="1" :max="365" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="每日佩戴" required>
              <el-input-number v-model="planForm.daily_wear_minutes" :min="1" :max="1440" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="训练场景" required>
              <el-select v-model="planForm.training_scenario" placeholder="选择训练场景" style="width: 100%">
                <el-option v-for="s in TRAINING_SCENARIOS" :key="s.value" :label="`${s.icon} ${s.label}`" :value="s.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="音量等级">
              <el-select v-model="planForm.volume_level" style="width: 100%">
                <el-option v-for="v in VOLUME_LEVELS" :key="v.value" :label="v.label" :value="v.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="提醒频率">
              <el-select v-model="planForm.reminder_frequency" style="width: 100%">
                <el-option v-for="r in REMINDER_FREQUENCIES" :key="r.value" :label="r.label" :value="r.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="负责人">
              <el-input v-model="planForm.responsible_person" placeholder="家属或验配师姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="开始日期" required>
              <el-date-picker v-model="planForm.start_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束日期">
              <el-date-picker v-model="planForm.end_date" type="date" value-format="YYYY-MM-DD" placeholder="可选" style="width: 100%" clearable />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item v-if="isPlanEdit" label="计划状态">
          <el-select v-model="planForm.status" style="width: 100%">
            <el-option v-for="s in TRAINING_PLAN_STATUSES" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="planForm.notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="planDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="savePlan">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="recordDialogVisible" title="登记训练完成情况" width="600px" :close-on-click-modal="false">
      <el-alert
        v-if="currentRecordPlan"
        :title="`当前计划：${currentRecordPlan.training_scenario} - ${currentRecordPlan.goal}`"
        type="info"
        :closable="false"
        style="margin-bottom: 16px"
      />
      <el-form :model="recordForm" label-width="110px">
        <el-form-item label="训练日期" required>
          <el-date-picker v-model="recordForm.record_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="实际佩戴时长">
          <el-input-number v-model="recordForm.actual_wear_minutes" :min="0" :max="1440" style="width: 100%" />
          <span style="margin-left: 8px; color: #909399; font-size: 13px">分钟（建议：{{ currentRecordPlan?.daily_wear_minutes || '-' }} 分钟）</span>
        </el-form-item>
        <el-form-item label="听清程度">
          <el-select v-model="recordForm.clarity_level" placeholder="选择听清程度" style="width: 100%" clearable>
            <el-option v-for="c in CLARITY_LEVELS" :key="c.value" :label="c.label" :value="c.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="疲劳感">
          <el-select v-model="recordForm.fatigue_level" placeholder="选择疲劳程度" style="width: 100%" clearable>
            <el-option v-for="f in FATIGUE_LEVELS" :key="f.value" :label="f.label" :value="f.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="出现不适">
          <el-switch v-model="recordForm.has_discomfort" />
        </el-form-item>
        <el-form-item v-if="recordForm.has_discomfort" label="不适详情">
          <el-input v-model="recordForm.discomfort_detail" placeholder="描述不适情况" />
        </el-form-item>
        <el-form-item label="是否啸叫">
          <el-select v-model="recordForm.howling" placeholder="选择啸叫情况" style="width: 100%" clearable>
            <el-option v-for="h in HOWLING_OPTIONS" :key="h.value" :label="h.label" :value="h.value" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="recordForm.howling && recordForm.howling !== '无'" label="啸叫详情">
          <el-input v-model="recordForm.howling_detail" placeholder="描述啸叫情况" />
        </el-form-item>
        <el-divider content-position="left">关联记录（可选）</el-divider>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="场景反馈">
              <el-input-number v-model="recordForm.related_feedback_id" :min="0" controls-position="right" style="width: 100%" placeholder="ID" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="调试记录">
              <el-input-number v-model="recordForm.related_adjustment_id" :min="0" controls-position="right" style="width: 100%" placeholder="ID" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="复诊记录">
              <el-input-number v-model="recordForm.related_followup_id" :min="0" controls-position="right" style="width: 100%" placeholder="ID" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="备注">
          <el-input v-model="recordForm.notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="recordDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveRecord">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailDialogVisible" :title="`${detailPlan?.elderly_name} - 训练计划详情`" width="900px">
      <template v-if="detailPlan">
        <el-descriptions :column="3" border size="small" style="margin-bottom: 16px">
          <el-descriptions-item label="训练目标" :span="3">{{ detailPlan.goal }}</el-descriptions-item>
          <el-descriptions-item label="训练场景">{{ detailPlan.training_scenario }}</el-descriptions-item>
          <el-descriptions-item label="训练周期">{{ detailPlan.cycle_days }} 天</el-descriptions-item>
          <el-descriptions-item label="每日佩戴">{{ detailPlan.daily_wear_minutes }} 分钟</el-descriptions-item>
          <el-descriptions-item label="音量等级">{{ detailPlan.volume_level }}</el-descriptions-item>
          <el-descriptions-item label="提醒频率">{{ detailPlan.reminder_frequency }}</el-descriptions-item>
          <el-descriptions-item label="负责人">{{ detailPlan.responsible_person || '-' }}</el-descriptions-item>
          <el-descriptions-item label="开始日期">{{ detailPlan.start_date }}</el-descriptions-item>
          <el-descriptions-item label="结束日期">{{ detailPlan.end_date || '-' }}</el-descriptions-item>
          <el-descriptions-item label="完成进度">{{ detailPlan.completed_days || 0 }} / {{ detailPlan.cycle_days }} 天 ({{ detailPlan.completion_rate || 0 }}%)</el-descriptions-item>
          <el-descriptions-item label="连续打卡">{{ detailPlan.streak_days || 0 }} 天</el-descriptions-item>
          <el-descriptions-item label="备注" :span="3">{{ detailPlan.notes || '-' }}</el-descriptions-item>
        </el-descriptions>

        <h4 style="margin: 16px 0 8px; font-size: 14px; color: #606266">训练记录</h4>
        <el-table :data="detailRecords" size="small" stripe style="width: 100%">
          <el-table-column prop="record_date" label="日期" width="110" />
          <el-table-column label="佩戴时长" width="100" align="center">
            <template #default="{ row }">
              <span :class="{'text-warning': row.actual_wear_minutes < detailPlan.daily_wear_minutes}">{{ row.actual_wear_minutes || 0 }} min</span>
            </template>
          </el-table-column>
          <el-table-column prop="clarity_level" label="听清程度" width="110" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.clarity_level" :type="getClarityTagType(row.clarity_level)" size="small">{{ row.clarity_level }}</el-tag>
              <span v-else style="color: #909399">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="fatigue_level" label="疲劳感" width="80" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.fatigue_level" :type="getFatigueTagType(row.fatigue_level)" size="small">{{ row.fatigue_level }}</el-tag>
              <span v-else style="color: #909399">-</span>
            </template>
          </el-table-column>
          <el-table-column label="不适" width="60" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.has_discomfort" type="danger" size="small">是</el-tag>
              <span v-else style="color: #67c23a">否</span>
            </template>
          </el-table-column>
          <el-table-column label="啸叫" width="80" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.howling && row.howling !== '无'" type="warning" size="small">{{ row.howling }}</el-tag>
              <span v-else style="color: #909399">-</span>
            </template>
          </el-table-column>
          <el-table-column prop="notes" label="备注" show-overflow-tooltip />
          <el-table-column label="操作" width="120" fixed="right">
            <template #default="{ row }">
              <el-button size="small" @click="openEditRecordDialog(row)">编辑</el-button>
              <el-button size="small" type="danger" @click="deleteRecord(row)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, View } from '@element-plus/icons-vue'
import { profileApi, trainingApi } from '@/api'
import { TRAINING_SCENARIOS, VOLUME_LEVELS, REMINDER_FREQUENCIES, TRAINING_PLAN_STATUSES, FATIGUE_LEVELS, CLARITY_LEVELS, HOWLING_OPTIONS } from '@/types'
import type { Profile, TrainingPlan, TrainingRecord } from '@/types'

const router = useRouter()
const loading = ref(false)
const profiles = ref<Profile[]>([])
const plans = ref<TrainingPlan[]>([])

const filterProfileId = ref<number>()
const filterStatus = ref('')
const filterScenario = ref('')
const filterDiscomfort = ref('')
const filterCompletion = ref('')

const planDialogVisible = ref(false)
const isPlanEdit = ref(false)
const currentPlan = ref<TrainingPlan>()
const planForm = ref<Partial<TrainingPlan>>({
  profile_id: undefined,
  goal: '',
  cycle_days: 14,
  daily_wear_minutes: 120,
  training_scenario: '居家安静',
  volume_level: '中',
  reminder_frequency: '每天',
  responsible_person: '',
  status: 'active',
  start_date: new Date().toISOString().split('T')[0],
  end_date: '',
  notes: ''
})

const recordDialogVisible = ref(false)
const isRecordEdit = ref(false)
const currentRecordPlan = ref<TrainingPlan>()
const recordForm = ref<Partial<TrainingRecord>>({
  plan_id: undefined,
  profile_id: undefined,
  record_date: new Date().toISOString().split('T')[0],
  actual_wear_minutes: 120,
  clarity_level: '',
  fatigue_level: '',
  has_discomfort: false,
  discomfort_detail: '',
  howling: '',
  howling_detail: '',
  related_feedback_id: undefined,
  related_adjustment_id: undefined,
  related_followup_id: undefined,
  notes: ''
})

const detailDialogVisible = ref(false)
const detailPlan = ref<TrainingPlan>()
const detailRecords = ref<TrainingRecord[]>([])

const filteredPlans = computed(() => {
  let result = plans.value
  if (filterCompletion.value) {
    result = result.filter(p => {
      const rate = p.completion_rate || 0
      if (filterCompletion.value === 'high') return rate >= 80
      if (filterCompletion.value === 'mid') return rate >= 50 && rate < 80
      if (filterCompletion.value === 'low') return rate < 50
      return true
    })
  }
  return result
})

const getScenarioIcon = (scenario: string) => {
  const item = TRAINING_SCENARIOS.find(s => s.value === scenario)
  return item?.icon || '📝'
}

const getStatusTagType = (status?: string) => {
  if (status === 'active') return 'primary'
  if (status === 'paused') return 'warning'
  if (status === 'completed') return 'success'
  return 'info'
}

const getStatusLabel = (status?: string) => {
  const item = TRAINING_PLAN_STATUSES.find(s => s.value === status)
  return item?.label || status
}

const getProgressColor = (rate: number) => {
  if (rate >= 80) return '#67c23a'
  if (rate >= 50) return '#e6a23c'
  return '#f56c6c'
}

const getClarityTagType = (level: string) => {
  if (level === '完全听清') return 'success'
  if (level === '大部分听清') return 'primary'
  if (level === '部分听清') return 'warning'
  return 'danger'
}

const getFatigueTagType = (level: string) => {
  if (level === '无') return 'success'
  if (level === '轻微') return 'primary'
  if (level === '一般') return 'warning'
  return 'danger'
}

const loadProfiles = async () => {
  try {
    const res = await profileApi.getAll()
    profiles.value = res.data
  } catch (e) {
    ElMessage.error('加载老人列表失败')
  }
}

const loadPlans = async () => {
  loading.value = true
  try {
    const res = await trainingApi.getPlans(
      filterProfileId.value,
      filterStatus.value || undefined,
      filterScenario.value || undefined,
      filterDiscomfort.value === 'true' ? true : undefined
    )
    plans.value = res.data
  } catch (e) {
    ElMessage.error('加载训练计划失败')
  } finally {
    loading.value = false
  }
}

const openPlanDialog = () => {
  isPlanEdit.value = false
  currentPlan.value = undefined
  planForm.value = {
    profile_id: undefined,
    goal: '',
    cycle_days: 14,
    daily_wear_minutes: 120,
    training_scenario: '居家安静',
    volume_level: '中',
    reminder_frequency: '每天',
    responsible_person: '',
    status: 'active',
    start_date: new Date().toISOString().split('T')[0],
    end_date: '',
    notes: ''
  }
  planDialogVisible.value = true
}

const openEditPlanDialog = (plan: TrainingPlan) => {
  isPlanEdit.value = true
  currentPlan.value = plan
  planForm.value = { ...plan }
  planDialogVisible.value = true
}

const savePlan = async () => {
  if (!planForm.value.profile_id || !planForm.value.goal || !planForm.value.cycle_days || !planForm.value.daily_wear_minutes || !planForm.value.training_scenario || !planForm.value.start_date) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    if (isPlanEdit.value && currentPlan.value?.id) {
      await trainingApi.updatePlan(currentPlan.value.id, planForm.value)
      ElMessage.success('更新成功')
    } else {
      await trainingApi.createPlan(planForm.value as TrainingPlan)
      ElMessage.success('创建成功')
    }
    planDialogVisible.value = false
    loadPlans()
  } catch (e: any) {
    const resp = e?.response?.data
    const msg = typeof resp === 'string' ? resp : resp?.error || resp?.message || '保存失败'
    ElMessage.error(msg)
  }
}

const deletePlan = async (plan: TrainingPlan) => {
  try {
    await ElMessageBox.confirm(`确定删除该训练计划？所有训练记录也将被删除。`, '确认删除', { type: 'warning' })
    await trainingApi.deletePlan(plan.id!)
    ElMessage.success('删除成功')
    loadPlans()
  } catch (e) {
    // cancelled
  }
}

const openRecordDialog = (plan: TrainingPlan) => {
  isRecordEdit.value = false
  currentRecordPlan.value = plan
  recordForm.value = {
    plan_id: plan.id,
    profile_id: plan.profile_id,
    record_date: new Date().toISOString().split('T')[0],
    actual_wear_minutes: plan.daily_wear_minutes,
    clarity_level: '',
    fatigue_level: '',
    has_discomfort: false,
    discomfort_detail: '',
    howling: '',
    howling_detail: '',
    related_feedback_id: undefined,
    related_adjustment_id: undefined,
    related_followup_id: undefined,
    notes: ''
  }
  recordDialogVisible.value = true
}

const openEditRecordDialog = async (record: TrainingRecord) => {
  isRecordEdit.value = true
  recordForm.value = { ...record }
  recordDialogVisible.value = true
}

const saveRecord = async () => {
  if (!recordForm.value.plan_id || !recordForm.value.record_date) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    if (isRecordEdit.value && recordForm.value.id) {
      await trainingApi.updateRecord(recordForm.value.id, recordForm.value)
      ElMessage.success('更新成功')
    } else {
      await trainingApi.createRecord(recordForm.value as TrainingRecord)
      ElMessage.success('登记成功')
    }
    recordDialogVisible.value = false
    loadPlans()
    if (detailPlan.value?.id) {
      const res = await trainingApi.getRecords(detailPlan.value.id)
      detailRecords.value = res.data
    }
  } catch (e: any) {
    const resp = e?.response?.data
    const msg = typeof resp === 'string' ? resp : resp?.error || resp?.message || '保存失败'
    ElMessage.error(msg)
  }
}

const deleteRecord = async (record: TrainingRecord) => {
  try {
    await ElMessageBox.confirm('确定删除该训练记录？', '确认删除', { type: 'warning' })
    await trainingApi.deleteRecord(record.id!)
    ElMessage.success('删除成功')
    if (detailPlan.value?.id) {
      const res = await trainingApi.getRecords(detailPlan.value.id)
      detailRecords.value = res.data
    }
    loadPlans()
  } catch (e) {
    // cancelled
  }
}

const viewPlanDetail = async (plan: TrainingPlan) => {
  detailPlan.value = plan
  detailDialogVisible.value = true
  try {
    const res = await trainingApi.getRecords(plan.id)
    detailRecords.value = res.data
  } catch (e) {
    ElMessage.error('加载训练记录失败')
  }
}

onMounted(() => {
  loadProfiles()
  loadPlans()
})
</script>

<style scoped>
.training-page {
  max-width: 1200px;
}
.filter-bar {
  margin-bottom: 20px;
}
.plan-card {
  margin-bottom: 16px;
}
.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.plan-title-area {
  display: flex;
  align-items: center;
  gap: 8px;
}
.plan-scenario-icon {
  font-size: 20px;
}
.plan-elderly {
  font-size: 16px;
}
.plan-actions {
  display: flex;
  gap: 4px;
}
.plan-info {
  margin-bottom: 12px;
}
.plan-progress {
  margin-bottom: 12px;
}
.progress-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 13px;
  color: #606266;
}
.text-success { color: #67c23a; font-weight: 600; }
.text-warning { color: #e6a23c; font-weight: 600; }
.text-danger { color: #f56c6c; font-weight: 600; }
.plan-7days {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #ebeef5;
}
.day-grid {
  display: flex;
  gap: 8px;
}
.day-cell {
  flex: 1;
  text-align: center;
  padding: 8px 4px;
  border-radius: 8px;
  background: #f5f7fa;
  font-size: 12px;
  position: relative;
}
.day-cell.day-completed {
  background: #f0f9eb;
}
.day-cell.day-discomfort {
  background: #fef0f0;
  border: 1px solid #fbc4c4;
}
.day-date {
  color: #909399;
  margin-bottom: 2px;
}
.day-wear {
  color: #409eff;
  font-weight: 600;
}
.day-alert {
  position: absolute;
  top: 2px;
  right: 4px;
  font-size: 12px;
}
</style>
