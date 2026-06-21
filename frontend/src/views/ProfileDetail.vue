<template>
  <div class="profile-detail" v-loading="loading">
    <div class="page-header">
      <h1 class="page-title">{{ profile?.elderly_name }} 的佩戴详情</h1>
      <el-button @click="router.back()">
        <el-icon><Back /></el-icon>
        返回列表
      </el-button>
    </div>

    <div class="closed-loop">
      <div class="closed-loop-item">
        <div class="closed-loop-icon">📋</div>
        <div class="closed-loop-title">建档验配</div>
        <div class="closed-loop-desc">记录助听器配置</div>
      </div>
      <div class="closed-loop-item">
        <div class="closed-loop-icon">📝</div>
        <div class="closed-loop-title">场景反馈</div>
        <div class="closed-loop-desc">收集日常佩戴体验</div>
      </div>
      <div class="closed-loop-item">
        <div class="closed-loop-icon">⚙️</div>
        <div class="closed-loop-title">调试复诊</div>
        <div class="closed-loop-desc">调整助听器参数</div>
      </div>
      <div class="closed-loop-item">
        <div class="closed-loop-icon">📊</div>
        <div class="closed-loop-title">效果跟踪</div>
        <div class="closed-loop-desc">跟踪改善效果</div>
      </div>
    </div>

    <el-row :gutter="20">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value">{{ overview?.counts?.feedback || 0 }}</div>
          <div class="stat-label">反馈记录</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value">{{ overview?.counts?.adjustment || 0 }}</div>
          <div class="stat-label">调试记录</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value">{{ overview?.counts?.followup || 0 }}</div>
          <div class="stat-label">复诊记录</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #67c23a">{{ overview?.average_rating || 0 }}</div>
          <div class="stat-label">平均评分</div>
        </div>
      </el-col>
    </el-row>

    <el-tabs v-model="activeTab">
      <el-tab-pane label="基本信息" name="basic">
        <div class="card">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="老人姓名">{{ profile?.elderly_name }}</el-descriptions-item>
            <el-descriptions-item label="年龄">{{ profile?.age }}</el-descriptions-item>
            <el-descriptions-item label="性别">{{ profile?.gender }}</el-descriptions-item>
            <el-descriptions-item label="联系人">{{ profile?.contact_person }}</el-descriptions-item>
            <el-descriptions-item label="联系电话">{{ profile?.contact_phone }}</el-descriptions-item>
            <el-descriptions-item label="验配日期">{{ profile?.fitting_date }}</el-descriptions-item>
            <el-descriptions-item label="验配门店">{{ profile?.fitting_store }}</el-descriptions-item>
            <el-descriptions-item label="验配师">{{ profile?.audiologist }}</el-descriptions-item>
            <el-descriptions-item label="左耳助听器">{{ profile?.hearing_aid_model_left }}</el-descriptions-item>
            <el-descriptions-item label="右耳助听器">{{ profile?.hearing_aid_model_right }}</el-descriptions-item>
            <el-descriptions-item label="左耳配置" :span="2">
              <pre style="white-space: pre-wrap; margin: 0">{{ profile?.ear_config_left }}</pre>
            </el-descriptions-item>
            <el-descriptions-item label="右耳配置" :span="2">
              <pre style="white-space: pre-wrap; margin: 0">{{ profile?.ear_config_right }}</pre>
            </el-descriptions-item>
            <el-descriptions-item label="常用场景" :span="2">
              <div class="tag-list">
                <el-tag v-for="s in scenarios" :key="s" type="info" size="small">{{ s }}</el-tag>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">{{ profile?.notes }}</el-descriptions-item>
          </el-descriptions>
        </div>
      </el-tab-pane>

      <el-tab-pane label="调试建议" name="suggestions">
        <div class="card">
          <div class="page-header" style="border: none; margin: 0; padding: 0">
            <h3 style="font-size: 18px; margin: 0">智能调试建议</h3>
          </div>
          <div v-if="suggestions.length === 0" style="text-align: center; padding: 40px; color: #909399">
            暂无足够数据生成建议，请先收集更多场景反馈
          </div>
          <div v-for="s in suggestions" :key="s.scenario" class="suggestion-card">
            <div class="suggestion-title">
              {{ s.scenario }} - 平均评分: {{ s.average_rating }} ({{ s.feedback_count }}次反馈)
            </div>
            <div class="suggestion-issues">
              <strong>存在问题：</strong>
              <span v-for="(issue, i) in s.issues" :key="i">{{ issue }}{{ i < s.issues.length - 1 ? '、' : '' }}</span>
            </div>
            <div>
              <strong>建议：</strong>
              <div v-for="(rec, i) in s.recommendations" :key="i" class="suggestion-rec">
                {{ i + 1 }}. {{ rec }}
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="电池管理" name="battery">
        <div class="card">
          <div class="page-header" style="border: none; margin: 0; padding: 0; margin-bottom: 20px">
            <h3 style="font-size: 18px; margin: 0">电池更换记录</h3>
            <el-button type="primary" size="small" @click="openBatteryDialog">
              <el-icon><Plus /></el-icon>
              记录更换
            </el-button>
          </div>
          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="12">
              <div class="card" style="background: linear-gradient(135deg, #e3f2fd; margin: 0">
              <h4 style="margin-bottom: 12px">左耳电池</h4>
              <el-descriptions :column="2" size="small">
                <el-descriptions-item label="平均使用天数">{{ batteryStats?.left_ear?.avg || 0 }} 天</el-descriptions-item>
                <el-descriptions-item label="下次预计更换">{{ batteryStats?.next_left_change || '-' }}</el-descriptions-item>
                <el-descriptions-item label="最短使用">{{ batteryStats?.left_ear?.min || 0 }} 天</el-descriptions-item>
                <el-descriptions-item label="最长使用">{{ batteryStats?.left_ear?.max || 0 }} 天</el-descriptions-item>
              </el-descriptions>
            </div>
            </el-col>
            <el-col :span="12">
              <div class="card" style="background: linear-gradient(135deg, #f3e5f5; margin: 0">
              <h4 style="margin-bottom: 12px">右耳电池</h4>
              <el-descriptions :column="2" size="small">
                <el-descriptions-item label="平均使用天数">{{ batteryStats?.right_ear?.avg || 0 }} 天</el-descriptions-item>
                <el-descriptions-item label="下次预计更换">{{ batteryStats?.next_right_change || '-' }}</el-descriptions-item>
                <el-descriptions-item label="最短使用">{{ batteryStats?.right_ear?.min || 0 }} 天</el-descriptions-item>
                <el-descriptions-item label="最长使用">{{ batteryStats?.right_ear?.max || 0 }} 天</el-descriptions-item>
              </el-descriptions>
            </div>
            </el-col>
          </el-row>
          <el-table :data="batteryRecords">
            <el-table-column prop="change_date" label="更换日期" width="120" />
            <el-table-column prop="ear" label="耳朵" width="80">
              <template #default="{ row }">
                <el-tag :type="row.ear === '左耳' ? 'primary' : 'purple'" size="small">{{ row.ear }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="battery_type" label="电池型号" />
            <el-table-column prop="battery_brand" label="品牌" />
            <el-table-column prop="usage_days" label="使用天数" width="100">
              <template #default="{ row }">
                <span v-if="row.usage_days">{{ row.usage_days }} 天</span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column prop="notes" label="备注" />
          </el-table>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="batteryDialogVisible" title="记录电池更换" width="500px">
      <el-form :model="batteryForm" label-width="100px">
        <el-form-item label="更换日期">
          <el-date-picker v-model="batteryForm.change_date" type="date" value-format="YYYY-MM-DD" style="width: 100%" />
        </el-form-item>
        <el-form-item label="耳朵">
          <el-radio-group v-model="batteryForm.ear">
            <el-radio value="左耳">左耳</el-radio>
            <el-radio value="右耳">右耳</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="电池型号">
          <el-input v-model="batteryForm.battery_type" placeholder="如：A13、A312、A10、A675" />
        </el-form-item>
        <el-form-item label="品牌">
          <el-input v-model="batteryForm.battery_brand" placeholder="如：峰力、奥迪康" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="batteryForm.notes" type="textarea" :rows="2" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="batteryDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitBattery">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { profileApi, feedbackApi, batteryApi, statisticsApi } from '@/api'
import type { Profile, BatteryRecord, Suggestion } from '@/types'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const activeTab = ref('basic')
const profile = ref<Profile>()
const overview = ref<any>()
const suggestions = ref<Suggestion[]>([])
const batteryRecords = ref<BatteryRecord[]>([])
const batteryStats = ref<any>()
const batteryDialogVisible = ref(false)

const batteryForm = ref({
  profile_id: Number(route.params.id),
  change_date: new Date().toISOString().split('T')[0],
  ear: '左耳',
  battery_type: '',
  battery_brand: '',
  notes: ''
})

const scenarios = computed(() => {
  if (!profile.value?.common_scenarios) return []
  try {
    return JSON.parse(profile.value.common_scenarios)
  } catch {
    return []
  }
})

const loadData = async () => {
  loading.value = true
  const id = Number(route.params.id)
  try {
    const [p, o, s, br, bs] = await Promise.all([
      profileApi.get(id),
      statisticsApi.getOverview(id),
      feedbackApi.getSuggestions(id),
      batteryApi.getAll(id),
      batteryApi.getStats(id)
    ])
    profile.value = p.data
    overview.value = o.data
    suggestions.value = s.data
    batteryRecords.value = br.data
    batteryStats.value = bs.data
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

const openBatteryDialog = () => {
  batteryForm.value = {
    profile_id: Number(route.params.id),
    change_date: new Date().toISOString().split('T')[0],
    ear: '左耳',
    battery_type: '',
    battery_brand: '',
    notes: ''
  }
  batteryDialogVisible.value = true
}

const submitBattery = async () => {
  try {
    await batteryApi.create(batteryForm.value as any)
    ElMessage.success('记录成功')
    batteryDialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

onMounted(loadData)
</script>
