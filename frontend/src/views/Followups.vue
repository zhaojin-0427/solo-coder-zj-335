<template>
  <div class="followups-page">
    <div class="page-header">
      <h1 class="page-title">复诊跟踪管理</h1>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新增复诊
      </el-button>
    </div>

    <div class="card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="选择老人">
          <el-select v-model="filterForm.profile_id" placeholder="全部" clearable style="width: 200px">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="复诊类型">
          <el-select v-model="filterForm.followup_type" placeholder="全部" clearable style="width: 150px">
            <el-option label="电话随访" value="电话随访" />
            <el-option label="门店复诊" value="门店复诊" />
            <el-option label="上门服务" value="上门服务" />
            <el-option label="线上咨询" value="线上咨询" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadFollowups">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card">
      <el-table :data="followups" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="老人" width="120">
          <template #default="{ row }">
            {{ getProfileName(row.profile_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="followup_date" label="复诊日期" width="120" />
        <el-table-column prop="followup_type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ row.followup_type || '-' }}</el-tag>
          </template>
        </el-table-column>
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
        <el-table-column label="评分" width="120">
          <template #default="{ row }">
            <el-rate v-model="row.overall_rating" disabled show-score text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column prop="next_followup_date" label="下次复诊" width="120" />
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="openEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <div class="card">
      <h3 style="margin-bottom: 20px; font-size: 18px">复诊时间线</h3>
      <div v-for="item in timeline" :key="item.id" class="timeline-item">
        <div class="timeline-date">
          {{ item.followup_date }} - {{ getProfileName(item.profile_id) }}
          <el-tag size="small" style="margin-left: 10px">{{ item.followup_type }}</el-tag>
        </div>
        <div class="timeline-content">
          <el-row :gutter="20">
            <el-col :span="6">
              <div><strong>听力改善:</strong> {{ item.hearing_improvement || '-' }}</div>
            </el-col>
            <el-col :span="6">
              <div><strong>啸叫改善:</strong> {{ item.howling_improvement || '-' }}</div>
            </el-col>
            <el-col :span="6">
              <div><strong>不适改善:</strong> {{ item.discomfort_improvement || '-' }}</div>
            </el-col>
            <el-col :span="6">
              <el-rate v-model="item.overall_rating" disabled size="small" />
            </el-col>
          </el-row>
          <el-divider style="margin: 10px 0" />
          <div v-if="item.issues_remaining" style="margin-bottom: 8px">
            <strong>剩余问题:</strong> {{ item.issues_remaining }}
          </div>
          <div v-if="item.suggestions" style="margin-bottom: 8px">
            <strong>建议:</strong> {{ item.suggestions }}
          </div>
          <div v-if="item.notes">
            <strong>备注:</strong> {{ item.notes }}
          </div>
        </div>
      </div>
      <div v-if="timeline.length === 0" style="text-align: center; padding: 40px; color: #909399">
        暂无复诊记录
      </div>
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑复诊' : '新增复诊'" width="700px">
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
              <el-form-item label="复诊日期" prop="followup_date" :rules="[{ required: true, message: '请选择日期' }]">
                <el-date-picker v-model="form.followup_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="关联调试">
                <el-select v-model="form.adjustment_id" placeholder="可选" style="width: 100%" clearable>
                  <el-option
                    v-for="a in profileAdjustments"
                    :key="a.id"
                    :label="`${a.adjustment_date} - ${a.reason}`"
                    :value="a.id"
                  />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="复诊类型">
            <el-select v-model="form.followup_type" style="width: 100%">
              <el-option label="电话随访" value="电话随访" />
              <el-option label="门店复诊" value="门店复诊" />
              <el-option label="上门服务" value="上门服务" />
              <el-option label="线上咨询" value="线上咨询" />
            </el-select>
          </el-form-item>
        </div>

        <div class="form-section">
          <div class="form-section-title">改善情况</div>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="听力改善">
                <el-select v-model="form.hearing_improvement" style="width: 100%">
                  <el-option v-for="o in IMPROVEMENT_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="啸叫改善">
                <el-select v-model="form.howling_improvement" style="width: 100%">
                  <el-option v-for="o in IMPROVEMENT_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="不适改善">
                <el-select v-model="form.discomfort_improvement" style="width: 100%">
                  <el-option v-for="o in IMPROVEMENT_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="适应状态">
                <el-select v-model="form.adaptation_status" style="width: 100%">
                  <el-option label="完全适应" value="完全适应" />
                  <el-option label="基本适应" value="基本适应" />
                  <el-option label="部分适应" value="部分适应" />
                  <el-option label="尚未适应" value="尚未适应" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="日均佩戴时长(小时)">
                <el-input-number v-model="form.daily_usage_hours" :min="0" :max="24" :step="0.5" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="form-section-title">评分</div>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="左耳评分">
                <el-rate v-model="form.left_ear_rating" show-score text-color="#ff9900" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="右耳评分">
                <el-rate v-model="form.right_ear_rating" show-score text-color="#ff9900" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="总体评分">
                <el-rate v-model="form.overall_rating" show-score text-color="#ff9900" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="form-section-title">其他信息</div>
          <el-form-item label="剩余问题">
            <el-input v-model="form.issues_remaining" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item label="建议">
            <el-input v-model="form.suggestions" type="textarea" :rows="2" />
          </el-form-item>
          <el-form-item label="下次复诊">
            <el-date-picker v-model="form.next_followup_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { followupApi, profileApi, adjustmentApi } from '@/api'
import type { Followup, Profile, Adjustment } from '@/types'
import { IMPROVEMENT_OPTIONS } from '@/types'

const loading = ref(false)
const followups = ref<Followup[]>([])
const profiles = ref<Profile[]>([])
const adjustments = ref<Adjustment[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const filterForm = ref({
  profile_id: undefined as number | undefined,
  followup_type: ''
})

const form = ref<Followup>({
  profile_id: 0,
  adjustment_id: undefined,
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

const profileAdjustments = ref<Adjustment[]>([])

const timeline = computed(() => {
  return [...followups.value].sort((a, b) => 
    new Date(b.followup_date).getTime() - new Date(a.followup_date).getTime()
  )
})

import { computed } from 'vue'

const loadProfiles = async () => {
  try {
    const res = await profileApi.getAll()
    profiles.value = res.data
  } catch (e) {
    ElMessage.error('加载老人列表失败')
  }
}

const loadAdjustments = async () => {
  try {
    const res = await adjustmentApi.getAll()
    adjustments.value = res.data
  } catch (e) {
    ElMessage.error('加载调试记录失败')
  }
}

const loadFollowups = async () => {
  loading.value = true
  try {
    const res = await followupApi.getAll(filterForm.value.profile_id)
    let data = res.data
    if (filterForm.value.followup_type) {
      data = data.filter(f => f.followup_type === filterForm.value.followup_type)
    }
    followups.value = data
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.value = { profile_id: undefined, followup_type: '' }
  loadFollowups()
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

watch(() => form.value.profile_id, (newId) => {
  if (newId) {
    profileAdjustments.value = adjustments.value.filter(a => a.profile_id === newId)
  } else {
    profileAdjustments.value = []
  }
})

const openCreateDialog = () => {
  isEdit.value = false
  form.value = {
    profile_id: 0,
    adjustment_id: undefined,
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
  dialogVisible.value = true
}

const openEditDialog = (row: Followup) => {
  isEdit.value = true
  form.value = { ...row }
  profileAdjustments.value = adjustments.value.filter(a => a.profile_id === row.profile_id)
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value && form.value.id) {
          await followupApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await followupApi.create(form.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadFollowups()
      } catch (e) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除该复诊记录吗？', '提示', {
    type: 'warning'
  }).then(async () => {
      await followupApi.delete(id)
      ElMessage.success('删除成功')
      loadFollowups()
    }).catch(() => {})
}

onMounted(() => {
  loadProfiles()
  loadAdjustments()
  loadFollowups()
})
</script>
