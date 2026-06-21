<template>
  <div class="adjustments-page">
    <div class="page-header">
      <h1 class="page-title">调试记录管理</h1>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新增调试
      </el-button>
    </div>

    <div class="card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="选择老人">
          <el-select v-model="filterForm.profile_id" placeholder="全部" clearable style="width: 200px">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadAdjustments">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card">
      <el-table :data="adjustments" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="老人" width="120">
          <template #default="{ row }">
            {{ getProfileName(row.profile_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="adjustment_date" label="调试日期" width="120" />
        <el-table-column prop="adjuster" label="调试人员" width="120" />
        <el-table-column label="左耳调整" show-overflow-tooltip>
          <template #default="{ row }">{{ row.left_ear_adjustment || '-' }}</template>
        </el-table-column>
        <el-table-column label="右耳调整" show-overflow-tooltip>
          <template #default="{ row }">{{ row.right_ear_adjustment || '-' }}</template>
        </el-table-column>
        <el-table-column prop="reason" label="调试原因" show-overflow-tooltip />
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="viewFollowups(row)">
              复诊记录
            </el-button>
            <el-button size="small" type="success" link @click="openEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑调试' : '新增调试'" width="800px">
      <el-form :model="form" label-width="120px" ref="formRef">
        <div class="form-section">
          <div class="form-section-title">基本信息</div>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="选择老人" prop="profile_id" :rules="[{ required: true, message: '请选择老人' }]">
                <el-select v-model="form.profile_id" placeholder="请选择" style="width: 100%">
                  <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="调试日期" prop="adjustment_date" :rules="[{ required: true, message: '请选择日期' }]">
                <el-date-picker v-model="form.adjustment_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="调试人员">
                <el-input v-model="form.adjuster" placeholder="验配师姓名" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="调试原因">
            <el-input v-model="form.reason" type="textarea" :rows="2" placeholder="请描述调试原因" />
          </el-form-item>
        </div>

        <div class="form-section">
          <div class="form-section-title">参数调整</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="左耳调整">
                <el-input v-model="form.left_ear_adjustment" type="textarea" :rows="3" placeholder="如：增益+5dB，降噪级别2" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="右耳调整">
                <el-input v-model="form.right_ear_adjustment" type="textarea" :rows="3" placeholder="如：增益+5dB，降噪级别2" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="程序调整">
                <el-input v-model="form.program_adjustment" placeholder="如：切换到多人对话模式" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="音量调整">
                <el-input v-model="form.volume_adjustment" placeholder="如：整体音量+2" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="反馈抑制">
                <el-input v-model="form.feedback_suppression" placeholder="如：开启自适应反馈抑制" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="降噪功能">
                <el-input v-model="form.noise_reduction" placeholder="如：开启强降噪" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="其他调整">
                <el-input v-model="form.other_adjustments" type="textarea" :rows="2" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="form-section-title">预期效果</div>
          <el-form-item label="预期效果">
            <el-input v-model="form.expected_effect" type="textarea" :rows="2" placeholder="请描述预期改善效果" />
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="form.notes" type="textarea" :rows="2" />
          </el-form-item>
        </div>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="followupDialogVisible" title="复诊记录" width="900px">
      <div style="margin-bottom: 15px">
        <el-button type="primary" size="small" @click="openFollowupCreate">
          <el-icon><Plus /></el-icon>
          新增复诊
        </el-button>
      </div>
      <el-table :data="followups" size="small">
        <el-table-column prop="followup_date" label="复诊日期" width="120" />
        <el-table-column prop="followup_type" label="复诊类型" width="100" />
        <el-table-column label="听力改善" width="100">
          <template #default="{ row }">
            <el-tag :type="getImprovementTagType(row.hearing_improvement)" size="small">
              {{ row.hearing_improvement || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="啸叫改善" width="100">
          <template #default="{ row }">
            <el-tag :type="getImprovementTagType(row.howling_improvement)" size="small">
              {{ row.howling_improvement || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="不适改善" width="100">
          <template #default="{ row }">
            <el-tag :type="getImprovementTagType(row.discomfort_improvement)" size="small">
              {{ row.discomfort_improvement || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="总体评分" width="120">
          <template #default="{ row }">
            <el-rate v-model="row.overall_rating" disabled show-score text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column prop="next_followup_date" label="下次复诊" width="120" />
      </el-table>
    </el-dialog>

    <el-dialog v-model="followupCreateVisible" title="新增复诊记录" width="700px">
      <el-form :model="followupForm" label-width="120px" ref="followupFormRef">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="复诊日期" prop="followup_date" :rules="[{ required: true }]">
              <el-date-picker v-model="followupForm.followup_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="复诊类型">
              <el-select v-model="followupForm.followup_type" style="width: 100%">
                <el-option label="电话随访" value="电话随访" />
                <el-option label="门店复诊" value="门店复诊" />
                <el-option label="上门服务" value="上门服务" />
                <el-option label="线上咨询" value="线上咨询" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="听力改善">
              <el-select v-model="followupForm.hearing_improvement" style="width: 100%">
                <el-option v-for="o in IMPROVEMENT_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="啸叫改善">
              <el-select v-model="followupForm.howling_improvement" style="width: 100%">
                <el-option v-for="o in IMPROVEMENT_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="不适改善">
              <el-select v-model="followupForm.discomfort_improvement" style="width: 100%">
                <el-option v-for="o in IMPROVEMENT_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="适应状态">
              <el-select v-model="followupForm.adaptation_status" style="width: 100%">
                <el-option label="完全适应" value="完全适应" />
                <el-option label="基本适应" value="基本适应" />
                <el-option label="部分适应" value="部分适应" />
                <el-option label="尚未适应" value="尚未适应" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="日均佩戴时长">
              <el-input-number v-model="followupForm.daily_usage_hours" :min="0" :max="24" :step="0.5" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-form-item label="左耳评分">
              <el-rate v-model="followupForm.left_ear_rating" show-score text-color="#ff9900" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="右耳评分">
              <el-rate v-model="followupForm.right_ear_rating" show-score text-color="#ff9900" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="总体评分">
              <el-rate v-model="followupForm.overall_rating" show-score text-color="#ff9900" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-form-item label="剩余问题">
          <el-input v-model="followupForm.issues_remaining" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="建议">
          <el-input v-model="followupForm.suggestions" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="下次复诊">
          <el-date-picker v-model="followupForm.next_followup_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="followupCreateVisible = false">取消</el-button>
        <el-button type="primary" @click="submitFollowup">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { adjustmentApi, profileApi, followupApi } from '@/api'
import type { Adjustment, Profile, Followup } from '@/types'
import { IMPROVEMENT_OPTIONS } from '@/types'

const loading = ref(false)
const adjustments = ref<Adjustment[]>([])
const profiles = ref<Profile[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const followupDialogVisible = ref(false)
const followupCreateVisible = ref(false)
const followupFormRef = ref<FormInstance>()
const followups = ref<Followup[]>([])
const currentAdjustment = ref<Adjustment>()

const filterForm = ref({
  profile_id: undefined as number | undefined
})

const form = ref<Adjustment>({
  profile_id: 0,
  adjustment_date: new Date().toISOString().split('T')[0],
  adjuster: '',
  left_ear_adjustment: '',
  right_ear_adjustment: '',
  program_adjustment: '',
  volume_adjustment: '',
  feedback_suppression: '',
  noise_reduction: '',
  other_adjustments: '',
  reason: '',
  expected_effect: '',
  notes: ''
})

const followupForm = ref<Followup>({
  profile_id: 0,
  adjustment_id: 0,
  followup_date: new Date().toISOString().split('T')[0],
  followup_type: '',
  hearing_improvement: '',
  howling_improvement: '',
  discomfort_improvement: '',
  adaptation_status: '',
  daily_usage_hours: undefined,
  left_ear_rating: undefined,
  right_ear_rating: undefined,
  overall_rating: undefined,
  issues_remaining: '',
  suggestions: '',
  next_followup_date: '',
  notes: ''
})

const loadProfiles = async () => {
  try {
    const res = await profileApi.getAll()
    profiles.value = res.data
  } catch (e) {
    ElMessage.error('加载老人列表失败')
  }
}

const loadAdjustments = async () => {
  loading.value = true
  try {
    const res = await adjustmentApi.getAll(filterForm.value.profile_id)
    adjustments.value = res.data
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.value = { profile_id: undefined }
  loadAdjustments()
}

const getProfileName = (id: number) => {
  const p = profiles.value.find(p => p.id === id)
  return p ? p.elderly_name : '-'
}

const getImprovementTagType = (value?: string) => {
  if (value === '明显改善') return 'success'
  if (value === '略有改善') return 'primary'
  if (value === '无变化') return 'info'
  if (value === '略有下降' || value === '明显下降') return 'danger'
  return 'warning'
}

const openCreateDialog = () => {
  isEdit.value = false
  form.value = {
    profile_id: 0,
    adjustment_date: new Date().toISOString().split('T')[0],
    adjuster: '',
    left_ear_adjustment: '',
    right_ear_adjustment: '',
    program_adjustment: '',
    volume_adjustment: '',
    feedback_suppression: '',
    noise_reduction: '',
    other_adjustments: '',
    reason: '',
    expected_effect: '',
    notes: ''
  }
  dialogVisible.value = true
}

const openEditDialog = (row: Adjustment) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value && form.value.id) {
          await adjustmentApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await adjustmentApi.create(form.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadAdjustments()
      } catch (e) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除该调试记录吗？', '提示', {
    type: 'warning'
  }).then(async () => {
      await adjustmentApi.delete(id)
      ElMessage.success('删除成功')
      loadAdjustments()
    }).catch(() => {})
}

const viewFollowups = async (row: Adjustment) => {
  currentAdjustment.value = row
  try {
    const res = await followupApi.getAll(row.profile_id, row.id)
    followups.value = res.data
    followupDialogVisible.value = true
  } catch (e) {
    ElMessage.error('加载复诊记录失败')
  }
}

const openFollowupCreate = () => {
  if (!currentAdjustment.value) return
  followupForm.value = {
    profile_id: currentAdjustment.value.profile_id,
    adjustment_id: currentAdjustment.value.id,
    followup_date: new Date().toISOString().split('T')[0],
    followup_type: '',
    hearing_improvement: '',
    howling_improvement: '',
    discomfort_improvement: '',
    adaptation_status: '',
    daily_usage_hours: undefined,
    left_ear_rating: undefined,
    right_ear_rating: undefined,
    overall_rating: undefined,
    issues_remaining: '',
    suggestions: '',
    next_followup_date: '',
    notes: ''
  }
  followupCreateVisible.value = true
}

const submitFollowup = async () => {
  if (!followupFormRef.value) return
  await followupFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await followupApi.create(followupForm.value)
        ElMessage.success('创建成功')
        followupCreateVisible.value = false
        if (currentAdjustment.value) {
          const res = await followupApi.getAll(currentAdjustment.value.profile_id, currentAdjustment.value.id)
          followups.value = res.data
        }
      } catch (e) {
        ElMessage.error('保存失败')
      }
    }
  })
}

onMounted(() => {
  loadProfiles()
  loadAdjustments()
})
</script>
