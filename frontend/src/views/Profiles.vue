<template>
  <div class="profiles-page">
    <div class="page-header">
      <h1 class="page-title">佩戴档案管理</h1>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新建档案
      </el-button>
    </div>

    <div class="card">
      <el-table :data="profiles" v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="elderly_name" label="老人姓名" width="120" />
        <el-table-column prop="age" label="年龄" width="80" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column label="助听器型号">
          <template #default="{ row }">
            <div>左耳: {{ row.hearing_aid_model_left || '-' }}</div>
            <div>右耳: {{ row.hearing_aid_model_right || '-' }}</div>
          </template>
        </el-table-column>
        <el-table-column prop="fitting_date" label="验配日期" width="120" />
        <el-table-column prop="fitting_store" label="验配门店" width="150" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" link @click="viewDetail(row.id)">
              查看详情
            </el-button>
            <el-button size="small" type="success" link @click="openEditDialog(row)">
              编辑
            </el-button>
            <el-button size="small" type="danger" link @click="handleDelete(row.id)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑档案' : '新建档案'"
      width="800px"
    >
      <el-form :model="form" label-width="120px" ref="formRef">
        <div class="form-section">
          <div class="form-section-title">基本信息</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="老人姓名" prop="elderly_name" :rules="[{ required: true, message: '请输入老人姓名' }]">
                <el-input v-model="form.elderly_name" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="年龄">
                <el-input-number v-model="form.age" :min="0" :max="120" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="6">
              <el-form-item label="性别">
                <el-select v-model="form.gender" placeholder="请选择">
                  <el-option label="男" value="男" />
                  <el-option label="女" value="女" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="联系人">
                <el-input v-model="form.contact_person" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="联系电话">
                <el-input v-model="form.contact_phone" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="form-section-title">助听器配置</div>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="左耳型号">
                <el-input v-model="form.hearing_aid_model_left" placeholder="如：峰力 Phonak Audeo P90" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="右耳型号">
                <el-input v-model="form.hearing_aid_model_right" placeholder="如：峰力 Phonak Audeo P90" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="左耳配置">
                <el-input v-model="form.ear_config_left" type="textarea" :rows="2" placeholder="如：开放式耳塞，增益设置等" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="右耳配置">
                <el-input v-model="form.ear_config_right" type="textarea" :rows="2" placeholder="如：开放式耳塞，增益设置等" />
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="验配日期">
                <el-date-picker v-model="form.fitting_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="验配门店">
                <el-input v-model="form.fitting_store" />
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="验配师">
                <el-input v-model="form.audiologist" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>

        <div class="form-section">
          <div class="form-section-title">常用场景</div>
          <el-form-item label="常用场景">
            <el-checkbox-group v-model="scenarioChecks">
              <el-checkbox label="菜市场" />
              <el-checkbox label="家庭聚餐" />
              <el-checkbox label="看电视" />
              <el-checkbox label="户外散步" />
              <el-checkbox label="打电话" />
              <el-checkbox label="办公室" />
              <el-checkbox label="其他" />
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="备注">
            <el-input v-model="form.notes" type="textarea" :rows="3" />
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
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { profileApi } from '@/api'
import type { Profile } from '@/types'

const router = useRouter()
const loading = ref(false)
const profiles = ref<Profile[]>([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref<FormInstance>()
const scenarioChecks = ref<string[]>([])

const form = ref<Profile>({
  elderly_name: '',
  age: undefined,
  gender: '',
  contact_person: '',
  contact_phone: '',
  hearing_aid_model_left: '',
  hearing_aid_model_right: '',
  ear_config_left: '',
  ear_config_right: '',
  fitting_date: '',
  fitting_store: '',
  audiologist: '',
  common_scenarios: '',
  notes: ''
})

const loadProfiles = async () => {
  loading.value = true
  try {
    const res = await profileApi.getAll()
    profiles.value = res.data
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  isEdit.value = false
  form.value = {
    elderly_name: '',
    age: undefined,
    gender: '',
    contact_person: '',
    contact_phone: '',
    hearing_aid_model_left: '',
    hearing_aid_model_right: '',
    ear_config_left: '',
    ear_config_right: '',
    fitting_date: '',
    fitting_store: '',
    audiologist: '',
    common_scenarios: '',
    notes: ''
  }
  scenarioChecks.value = []
  dialogVisible.value = true
}

const openEditDialog = (row: Profile) => {
  isEdit.value = true
  form.value = { ...row }
  scenarioChecks.value = row.common_scenarios ? JSON.parse(row.common_scenarios || '[]') : []
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate(async (valid) => {
    if (valid) {
      form.value.common_scenarios = JSON.stringify(scenarioChecks.value)
      try {
        if (isEdit.value && form.value.id) {
          await profileApi.update(form.value.id, form.value)
          ElMessage.success('更新成功')
        } else {
          await profileApi.create(form.value)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadProfiles()
      } catch (e) {
        ElMessage.error('保存失败')
      }
    }
  })
}

const handleDelete = (id: number) => {
  ElMessageBox.confirm('确定要删除该档案吗？', '提示', {
    type: 'warning'
  }).then(async () => {
      await profileApi.delete(id)
      ElMessage.success('删除成功')
      loadProfiles()
    }).catch(() => {})
}

const viewDetail = (id: number) => {
  router.push(`/profiles/${id}`)
}

const formatDate = (date?: string) => {
  return date ? new Date(date).toLocaleString('zh-CN') : ''
}

onMounted(loadProfiles)
</script>
