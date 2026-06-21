<template>
  <div class="feedback-page">
    <div class="page-header">
      <h1 class="page-title">场景反馈管理</h1>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新增反馈
      </el-button>
    </div>

    <div class="card">
      <el-form :inline="true" :model="filterForm" class="filter-form">
        <el-form-item label="选择老人">
          <el-select v-model="filterForm.profile_id" placeholder="全部" clearable style="width: 200px">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="场景">
          <el-select v-model="filterForm.scenario" placeholder="全部" clearable style="width: 150px">
            <el-option v-for="s in SCENARIOS" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadFeedback">查询</el-button>
          <el-button @click="resetFilter">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="card">
      <el-table :data="feedbackList" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column label="老人" width="120">
          <template #default="{ row }">
            {{ getProfileName(row.profile_id) }}
          </template>
        </el-table-column>
        <el-table-column prop="feedback_date" label="日期" width="120" />
        <el-table-column label="场景" width="120">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ getScenarioLabel(row.scenario) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="scenario_detail" label="场景详情" show-overflow-tooltip />
        <el-table-column label="听感" width="100">
          <template #default="{ row }">
            <el-tag :type="getHearingTagType(row.hearing_experience)" size="small">
              {{ row.hearing_experience || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="啸叫" width="80">
          <template #default="{ row }">
            <el-tag :type="row.howling === '无' ? 'success' : 'danger'" size="small">
              {{ row.howling || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="不适" width="80">
          <template #default="{ row }">
            <el-tag :type="row.discomfort === '无' ? 'success' : 'warning'" size="small">
              {{ row.discomfort || '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="评分" width="150">
          <template #default="{ row }">
            <el-rate v-model="row.overall_rating" disabled show-score text-color="#ff9900" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="openEditDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" link @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑反馈' : '新增反馈'" width="700px">
      <el-form :model="form" label-width="120px" ref="formRef">
        <div class="form-section">
          <div class="form-section-title">基本信息</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="选择老人" prop="profile_id" :rules="[{ required: true, message: '请选择老人' }]">
                <el-select v-model="form.profile_id" placeholder="请选择" style="width: 100%">
                  <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="反馈日期" prop="feedback_date" :rules="[{ required: true, message: '请选择日期' }]">
                <el-date-picker v-model="form.feedback_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="form-section-title">场景信息</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="场景" prop="scenario" :rules="[{ required: true, message: '请选择场景' }]">
                <el-select v-model="form.scenario" placeholder="请选择" style="width: 100%">
                  <el-option v-for="s in SCENARIOS" :key="s.value" :label="s.label" :value="s.value">
                    <span>{{ s.icon }} {{ s.label }}</span>
                  </el-option>
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="持续时长">
                <el-input-number v-model="form.duration_minutes" :min="0" placeholder="分钟" style="width: 100%" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-form-item label="场景详情">
            <el-input v-model="form.scenario_detail" placeholder="请描述具体场景情况" />
          </el-form-item>
        </div>

        <div class="form-section">
          <div class="form-section-title">佩戴感受</div>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="听感">
                <el-select v-model="form.hearing_experience" placeholder="请选择" style="width: 100%">
                  <el-option v-for="o in HEARING_EXPERIENCE_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="啸叫情况">
                <el-select v-model="form.howling" placeholder="请选择" style="width: 100%">
                  <el-option v-for="o in HOWLING_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
                </el-select>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="不适反应">
                <el-select v-model="form.discomfort" placeholder="请选择" style="width: 100%">
                  <el-option v-for="o in DISCOMFORT_OPTIONS" :key="o.value" :label="o.label" :value="o.value" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="听感详情">
                <el-input v-model="form.hearing_experience_detail" type="textarea" :rows="2" placeholder="请详细描述听感" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="啸叫详情">
                <el-input v-model="form.howling_detail" type="textarea" :rows="2" placeholder="请描述啸叫情况" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="不适详情">
                <el-input v-model="form.discomfort_detail" type="textarea" :rows="2" placeholder="请描述不适反应" />
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
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance } from 'element-plus'
import { feedbackApi, profileApi } from '@/api'
import type { Feedback, Profile } from '@/types'
import { SCENARIOS, HEARING_EXPERIENCE_OPTIONS, HOWLING_OPTIONS, DISCOMFORT_OPTIONS } from '@/types'

const loading = ref(false)
const feedbackList = ref<Feedback[]>([])
const profiles = ref<Profile[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()

const filterForm = ref({
  profile_id: undefined as number | undefined,
  scenario: ''
})

const form = ref<Feedback>({
  profile_id: 0,
  feedback_date: new Date().toISOString().split('T')[0],
  scenario: '',
  scenario_detail: '',
  duration_minutes: undefined,
  hearing_experience: '',
  hearing_experience_detail: '',
  howling: '',
  howling_detail: '',
  discomfort: '',
  discomfort_detail: '',
  left_ear_rating: undefined,
  right_ear_rating: undefined,
  overall_rating: undefined,
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

const loadFeedback = async () => {
  loading.value = true
  try {
    const res = await feedbackApi.getAll(filterForm.value.profile_id, filterForm.value.scenario || undefined)
    feedbackList.value = res.data
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const resetFilter = () => {
  filterForm.value = { profile_id: undefined, scenario: '' }
  loadFeedback()
}

const getProfileName = (id: number) => {
  const p = profiles.value.find(p => p.id === id)
  return p ? p.elderly_name : '-'
}

const getScenarioLabel = (value: string) => {
  const s = SCENARIOS.find(s => s.value === value)
  return s ? s.label : value
}

const getHearingTagType = (value?: string) => {
  if (value === '很好' || value === '好') return 'success'
  if (value === '一般') return 'warning'
  if (value === '差' || value === '很差') return 'danger'
  return 'info'
}

const openCreateDialog = () => {
  isEdit.value = false
  form.value = {
    profile_id: 0,
    feedback_date: new Date().toISOString().split('T')[0],
    scenario: '',
    scenario_detail: '',
    duration_minutes: undefined,
    hearing_experience: '',
    hearing_experience_detail: '',
    howling: '',
    howling_detail: '',
    discomfort: '',
    discomfort_detail: '',
    left_ear_rating: undefined,
    right_ear_rating: undefined,
    overall_rating: undefined,
    notes: ''
  }
  dialogVisible.value = true
}

const openEditDialog = (row: Feedback) => {
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
          await feedbackApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await feedbackApi.create(form.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadFeedback()
      } catch (e) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除该反馈吗？', '提示', {
    type: 'warning'
  }).then(async () => {
      await feedbackApi.delete(id)
      ElMessage.success('删除成功')
      loadFeedback()
    }).catch(() => {})
}

onMounted(() => {
  loadProfiles()
  loadFeedback()
})
</script>
