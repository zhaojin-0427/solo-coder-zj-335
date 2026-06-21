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

    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #409eff">{{ taskSummary?.summary?.total || 0 }}</div>
          <div class="stat-label">任务总数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #f56c6c">{{ taskSummary?.summary?.overdue || 0 }}</div>
          <div class="stat-label">已逾期任务</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #e6a23c">{{ taskSummary?.summary?.pending || 0 }}</div>
          <div class="stat-label">待处理任务</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #67c23a">{{ taskSummary?.summary?.completion_rate || 0 }}%</div>
          <div class="stat-label">任务完成率</div>
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
            <div style="display: flex; align-items: center; gap: 12px">
              <h3 style="font-size: 18px; margin: 0">电池更换记录</h3>
              <el-tag v-if="batteryStats?.status === 'overdue'" type="danger" effect="dark">
                <el-icon style="margin-right: 4px"><WarningFilled /></el-icon>
                电池已逾期
              </el-tag>
              <el-tag v-else-if="batteryStats?.status === 'soon_due'" type="warning" effect="dark">
                <el-icon style="margin-right: 4px"><Clock /></el-icon>
                即将到期
              </el-tag>
              <el-tag v-else-if="batteryStats?.status === 'abnormal'" type="warning">
                <el-icon style="margin-right: 4px"><Warning /></el-icon>
                周期异常
              </el-tag>
            </div>
            <el-button type="primary" size="small" @click="openBatteryDialog">
              <el-icon><Plus /></el-icon>
              记录更换
            </el-button>
          </div>

          <el-alert
            v-if="allAbnormalCycles.length > 0"
            :title="`检测到 ${allAbnormalCycles.length} 条周期异常记录，请关注`"
            type="warning"
            :closable="false"
            style="margin-bottom: 20px"
            show-icon
          >
            <div style="margin-top: 8px">
              <div v-for="ab in allAbnormalCycles" :key="ab.id" style="font-size: 13px; margin-bottom: 4px">
                <el-tag size="small" type="warning" style="margin-right: 8px">
                  {{ ab.change_date }}
                </el-tag>
                {{ ab.reason }}
              </div>
            </div>
          </el-alert>

          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="12">
              <div class="card ear-card" style="background: linear-gradient(135deg, #e3f2fd; margin: 0">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px">
                  <h4 style="margin: 0">左耳电池</h4>
                  <el-tag
                    v-if="batteryStats?.left_ear?.status === 'overdue'"
                    type="danger"
                    effect="dark"
                    size="small"
                  >
                    已逾期 {{ batteryStats?.left_ear?.overdue_days }} 天
                  </el-tag>
                  <el-tag
                    v-else-if="batteryStats?.left_ear?.status === 'soon_due'"
                    type="warning"
                    effect="dark"
                    size="small"
                  >
                    即将到期
                  </el-tag>
                  <el-tag
                    v-else-if="batteryStats?.left_ear?.status === 'normal'"
                    type="success"
                    size="small"
                  >
                    正常
                  </el-tag>
                  <el-tag v-else type="info" size="small">暂无数据</el-tag>
                </div>
                <el-descriptions :column="2" size="small" border>
                  <el-descriptions-item label="最近更换">
                    {{ batteryStats?.left_ear?.last_change_date || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="平均周期">
                    {{ batteryStats?.left_ear?.avg_cycle_days || 0 }} 天
                  </el-descriptions-item>
                  <el-descriptions-item label="预计下次">
                    <span :class="{ 'text-danger': batteryStats?.left_ear?.status === 'overdue' }">
                      {{ batteryStats?.left_ear?.next_expected_date || '-' }}
                    </span>
                  </el-descriptions-item>
                  <el-descriptions-item label="最短/最长">
                    {{ batteryStats?.left_ear?.min_cycle_days || 0 }} / {{ batteryStats?.left_ear?.max_cycle_days || 0 }} 天
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="card ear-card" style="background: linear-gradient(135deg, #f3e5f5; margin: 0">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px">
                  <h4 style="margin: 0">右耳电池</h4>
                  <el-tag
                    v-if="batteryStats?.right_ear?.status === 'overdue'"
                    type="danger"
                    effect="dark"
                    size="small"
                  >
                    已逾期 {{ batteryStats?.right_ear?.overdue_days }} 天
                  </el-tag>
                  <el-tag
                    v-else-if="batteryStats?.right_ear?.status === 'soon_due'"
                    type="warning"
                    effect="dark"
                    size="small"
                  >
                    即将到期
                  </el-tag>
                  <el-tag
                    v-else-if="batteryStats?.right_ear?.status === 'normal'"
                    type="success"
                    size="small"
                  >
                    正常
                  </el-tag>
                  <el-tag v-else type="info" size="small">暂无数据</el-tag>
                </div>
                <el-descriptions :column="2" size="small" border>
                  <el-descriptions-item label="最近更换">
                    {{ batteryStats?.right_ear?.last_change_date || '-' }}
                  </el-descriptions-item>
                  <el-descriptions-item label="平均周期">
                    {{ batteryStats?.right_ear?.avg_cycle_days || 0 }} 天
                  </el-descriptions-item>
                  <el-descriptions-item label="预计下次">
                    <span :class="{ 'text-danger': batteryStats?.right_ear?.status === 'overdue' }">
                      {{ batteryStats?.right_ear?.next_expected_date || '-' }}
                    </span>
                  </el-descriptions-item>
                  <el-descriptions-item label="最短/最长">
                    {{ batteryStats?.right_ear?.min_cycle_days || 0 }} / {{ batteryStats?.right_ear?.max_cycle_days || 0 }} 天
                  </el-descriptions-item>
                </el-descriptions>
              </div>
            </el-col>
          </el-row>

          <el-table :data="batteryRecords">
            <el-table-column prop="change_date" label="更换日期" width="120">
              <template #default="{ row }">
                <span>{{ row.change_date }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="ear" label="耳朵" width="80">
              <template #default="{ row }">
                <el-tag :type="row.ear === '左耳' ? 'primary' : 'purple'" size="small">{{ row.ear }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="battery_type" label="电池型号" />
            <el-table-column prop="battery_brand" label="品牌" />
            <el-table-column label="使用天数" width="140">
              <template #default="{ row }">
                <span v-if="row.usage_days != null && row.usage_days > 0">
                  <span
                    :class="{
                      'text-warning': isCycleAbnormal(row),
                      'text-danger': row.usage_days < 3
                    }"
                  >
                    {{ row.usage_days }} 天
                  </span>
                  <el-tooltip
                    v-if="isCycleAbnormal(row)"
                    :content="getAbnormalReason(row)"
                    placement="top"
                  >
                    <el-icon class="warn-icon" color="#e6a23c"><WarningFilled /></el-icon>
                  </el-tooltip>
                </span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column prop="notes" label="备注" />
          </el-table>
        </div>
      </el-tab-pane>

      <el-tab-pane label="协作任务" name="tasks">
        <div class="card">
          <div class="page-header" style="border: none; margin: 0; padding: 0; margin-bottom: 20px">
            <div style="display: flex; align-items: center; gap: 12px">
              <h3 style="font-size: 18px; margin: 0">
                <el-icon color="#409eff" style="margin-right: 8px"><Tickets /></el-icon>
                协作任务
              </h3>
              <el-tag v-if="taskSummary?.summary?.overdue && taskSummary.summary.overdue > 0" type="danger" effect="dark">
                {{ taskSummary.summary.overdue }} 项已逾期
              </el-tag>
              <el-tag v-else-if="taskSummary?.summary?.soon_due && taskSummary.summary.soon_due > 0" type="warning" effect="dark">
                {{ taskSummary.summary.soon_due }} 项即将到期
              </el-tag>
            </div>
            <el-button type="primary" size="small" @click="openTaskDialog">
              <el-icon><Plus /></el-icon>
              新建任务
            </el-button>
          </div>

          <el-empty
            v-if="!profileTasks || profileTasks.length === 0"
            description="暂无任务，点击上方按钮创建新任务"
            :image-size="80"
          />

          <div v-else class="task-list">
            <div
              v-for="task in profileTasks"
              :key="task.id"
              class="task-card"
              :class="{ 'task-overdue': task.is_overdue, 'task-completed': task.status === 'completed' }"
            >
              <div class="task-header">
                <div class="task-title">
                  <span class="task-type-icon">{{ getTaskTypeIcon(task.task_type) }}</span>
                  <strong>{{ task.title }}</strong>
                  <el-tag
                    v-if="task.is_overdue && task.status !== 'completed'"
                    type="danger"
                    effect="dark"
                    size="small"
                    style="margin-left: 8px"
                  >
                    逾期 {{ Math.abs(task.days_until_due || 0) }} 天
                  </el-tag>
                  <el-tag
                    v-else-if="task.days_until_due != null && task.days_until_due <= 3 && task.days_until_due >= 0 && task.status !== 'completed'"
                    type="warning"
                    size="small"
                    style="margin-left: 8px"
                  >
                    {{ task.days_until_due === 0 ? '今天到期' : `还有 ${task.days_until_due} 天` }}
                  </el-tag>
                </div>
                <div class="task-actions">
                  <el-button
                    v-if="task.status !== 'completed'"
                    type="success"
                    size="small"
                    @click.stop="openCompleteTaskDialog(task)"
                  >
                    <el-icon><Check /></el-icon>
                    完成
                  </el-button>
                  <el-button size="small" @click.stop="openEditTaskDialog(task)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                </div>
              </div>

              <div class="task-meta">
                <el-tag :type="getTaskPriorityTagType(task.priority)" size="small" effect="dark">
                  {{ getTaskPriorityLabel(task.priority) }}优先级
                </el-tag>
                <el-tag :type="getTaskStatusTagType(task.status)" size="small">
                  {{ getTaskStatusLabel(task.status) }}
                </el-tag>
                <el-tag type="info" size="small">{{ task.task_type }}</el-tag>
                <span v-if="task.assignee" class="meta-item">
                  <el-icon><UserFilled /></el-icon>
                  负责人: {{ task.assignee }}
                </span>
                <span v-if="task.due_date" class="meta-item">
                  <el-icon><Calendar /></el-icon>
                  截止: {{ task.due_date }}
                </span>
              </div>

              <div v-if="task.description" class="task-description">
                {{ task.description }}
              </div>

              <div v-if="task.completion_feedback" class="task-feedback">
                <el-icon color="#67c23a"><ChatDotRound /></el-icon>
                <strong>完成反馈：</strong>{{ task.completion_feedback }}
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="batteryDialogVisible" title="记录电池更换" width="500px">
      <el-form :model="batteryForm" label-width="100px">
        <el-form-item label="更换日期" required>
          <el-date-picker
            v-model="batteryForm.change_date"
            type="date"
            value-format="YYYY-MM-DD"
            :disabled-date="disabledDate"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="耳朵" required>
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

    <el-dialog v-model="taskDialogVisible" :title="isTaskEdit ? '编辑任务' : '新建任务'" width="600px">
      <el-form :model="taskForm" label-width="100px">
        <el-form-item label="任务标题" required>
          <el-input v-model="taskForm.title" placeholder="请输入任务标题" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="任务类型" required>
          <el-select v-model="taskForm.task_type" placeholder="请选择任务类型" style="width: 100%">
            <el-option v-for="t in TASK_TYPES" :key="t.value" :label="`${t.icon} ${t.label}`" :value="t.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="任务描述">
          <el-input v-model="taskForm.description" type="textarea" :rows="3" placeholder="请输入任务详细描述" />
        </el-form-item>
        <el-form-item label="负责人">
          <el-input v-model="taskForm.assignee" placeholder="请输入负责人姓名" />
        </el-form-item>
        <el-form-item label="截止日期">
          <el-date-picker
            v-model="taskForm.due_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择截止日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="优先级">
          <el-radio-group v-model="taskForm.priority">
            <el-radio v-for="p in TASK_PRIORITIES" :key="p.value" :value="p.value" :label="p.value">
              <span :style="{ color: p.color }">{{ p.label }}</span>
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="任务状态">
          <el-select v-model="taskForm.status" style="width: 100%">
            <el-option v-for="s in TASK_STATUSES" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="taskForm.notes" type="textarea" :rows="2" placeholder="请输入备注信息" />
        </el-form-item>
        <el-form-item v-if="taskForm.status === 'completed'" label="完成反馈">
          <el-input v-model="taskForm.completion_feedback" type="textarea" :rows="2" placeholder="请输入完成情况反馈" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="taskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTask">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="completeTaskDialogVisible" title="完成任务" width="500px">
      <div style="margin-bottom: 16px">
        <p><strong>任务：</strong>{{ currentTask?.title }}</p>
      </div>
      <el-form label-width="100px">
        <el-form-item label="完成反馈">
          <el-input v-model="taskCompletionFeedback" type="textarea" :rows="3" placeholder="请描述任务完成情况" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeTaskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCompleteTask">确认完成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  WarningFilled,
  Clock,
  Warning,
  Plus,
  Back,
  Check,
  Edit,
  UserFilled,
  Calendar,
  ChatDotRound
} from '@element-plus/icons-vue'
import { profileApi, feedbackApi, batteryApi, statisticsApi, taskApi } from '@/api'
import { TASK_TYPES, TASK_PRIORITIES, TASK_STATUSES } from '@/types'
import type { Profile, BatteryRecord, Suggestion, BatteryStats, BatteryAbnormalCycle, TaskSummary, Task } from '@/types'

const route = useRoute()
const router = useRouter()
const loading = ref(false)
const activeTab = ref('basic')
const profile = ref<Profile>()
const overview = ref<any>()
const suggestions = ref<Suggestion[]>([])
const batteryRecords = ref<BatteryRecord[]>([])
const batteryStats = ref<BatteryStats>()
const batteryDialogVisible = ref(false)

const taskSummary = ref<TaskSummary>()
const profileTasks = ref<Task[]>([])
const taskDialogVisible = ref(false)
const completeTaskDialogVisible = ref(false)
const isTaskEdit = ref(false)
const currentTask = ref<Task>()
const taskCompletionFeedback = ref('')

const taskForm = ref<Partial<Task>>({
  profile_id: Number(route.params.id),
  title: '',
  task_type: '提醒佩戴',
  description: '',
  assignee: '',
  due_date: '',
  priority: 'medium',
  status: 'pending',
  notes: '',
  completion_feedback: ''
})

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

const allAbnormalCycles = computed<BatteryAbnormalCycle[]>(() => {
  if (!batteryStats.value) return []
  return [
    ...(batteryStats.value.left_ear?.abnormal_cycles || []),
    ...(batteryStats.value.right_ear?.abnormal_cycles || [])
  ]
})

const disabledDate = (time: Date) => {
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  if (time.getTime() > today.getTime()) return true
  if (profile.value?.fitting_date) {
    const fitting = new Date(profile.value.fitting_date)
    fitting.setHours(0, 0, 0, 0)
    if (time.getTime() < fitting.getTime()) return true
  }
  return false
}

const abnormalMap = computed(() => {
  const map = new Map<number, string>()
  allAbnormalCycles.value.forEach(ab => {
    map.set(ab.id, ab.reason)
  })
  return map
})

const isCycleAbnormal = (row: BatteryRecord) => {
  return row.id != null && abnormalMap.value.has(row.id)
}

const getAbnormalReason = (row: BatteryRecord) => {
  return row.id != null ? abnormalMap.value.get(row.id) || '' : ''
}

const loadData = async () => {
  loading.value = true
  const id = Number(route.params.id)
  try {
    const [p, o, s, br, bs, ts, tasks] = await Promise.all([
      profileApi.get(id),
      statisticsApi.getOverview(id),
      feedbackApi.getSuggestions(id),
      batteryApi.getAll(id),
      batteryApi.getStats(id),
      statisticsApi.getTaskSummary(id),
      taskApi.getAll(id)
    ])
    profile.value = p.data
    overview.value = o.data
    suggestions.value = s.data
    batteryRecords.value = br.data
    batteryStats.value = bs.data
    taskSummary.value = ts.data
    profileTasks.value = tasks.data
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

const extractErrorMessage = (err: any) => {
  const resp = err?.response?.data
  if (typeof resp === 'string') return resp
  if (resp?.error) return resp.error
  if (resp?.message) return resp.message
  return '保存失败'
}

const submitBattery = async () => {
  try {
    await batteryApi.create(batteryForm.value as any)
    ElMessage.success('记录成功')
    batteryDialogVisible.value = false
    loadData()
  } catch (e: any) {
    ElMessage.error(extractErrorMessage(e))
  }
}

const getTaskTypeIcon = (type: string) => {
  const item = TASK_TYPES.find(t => t.value === type)
  return item?.icon || '📝'
}

const getTaskPriorityLabel = (priority?: string) => {
  const item = TASK_PRIORITIES.find(p => p.value === priority)
  return item?.label || priority
}

const getTaskPriorityTagType = (priority?: string) => {
  if (priority === 'urgent') return 'danger'
  if (priority === 'high') return 'warning'
  if (priority === 'medium') return 'primary'
  return 'info'
}

const getTaskStatusLabel = (status?: string) => {
  const item = TASK_STATUSES.find(s => s.value === status)
  return item?.label || status
}

const getTaskStatusTagType = (status?: string) => {
  if (status === 'completed') return 'success'
  if (status === 'in_progress') return 'primary'
  if (status === 'cancelled') return 'info'
  return 'warning'
}

const openTaskDialog = () => {
  isTaskEdit.value = false
  taskForm.value = {
    profile_id: Number(route.params.id),
    title: '',
    task_type: '提醒佩戴',
    description: '',
    assignee: '',
    due_date: '',
    priority: 'medium',
    status: 'pending',
    notes: '',
    completion_feedback: ''
  }
  taskDialogVisible.value = true
}

const openEditTaskDialog = (task: Task) => {
  isTaskEdit.value = true
  currentTask.value = task
  taskForm.value = { ...task }
  taskDialogVisible.value = true
}

const openCompleteTaskDialog = (task: Task) => {
  currentTask.value = task
  taskCompletionFeedback.value = ''
  completeTaskDialogVisible.value = true
}

const confirmCompleteTask = async () => {
  if (!currentTask.value?.id) return
  try {
    await taskApi.complete(currentTask.value.id, taskCompletionFeedback.value)
    ElMessage.success('任务已完成')
    completeTaskDialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const saveTask = async () => {
  if (!taskForm.value.title || !taskForm.value.task_type) {
    ElMessage.warning('请填写必填项')
    return
  }

  try {
    if (isTaskEdit.value && currentTask.value?.id) {
      await taskApi.update(currentTask.value.id, taskForm.value)
      ElMessage.success('更新成功')
    } else {
      await taskApi.create(taskForm.value as Task)
      ElMessage.success('创建成功')
    }
    taskDialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

onMounted(loadData)
</script>

<style scoped>
.text-danger {
  color: #f56c6c;
  font-weight: 600;
}
.text-warning {
  color: #e6a23c;
  font-weight: 600;
}
.warn-icon {
  margin-left: 4px;
  vertical-align: middle;
}
.ear-card {
  border-radius: 8px;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.task-card {
  padding: 14px 18px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.2s;
  border-left: 4px solid #dcdfe6;
}

.task-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.task-card.task-overdue {
  border-left-color: #f56c6c;
  background: #fef0f0;
}

.task-card.task-completed {
  border-left-color: #67c23a;
  opacity: 0.8;
}

.task-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 10px;
}

.task-title {
  font-size: 15px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.task-type-icon {
  font-size: 18px;
  margin-right: 4px;
}

.task-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.task-meta {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 10px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
  font-size: 13px;
}

.task-description {
  color: #606266;
  font-size: 13px;
  margin-bottom: 6px;
  padding: 6px 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.task-feedback {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  color: #67c23a;
  font-size: 13px;
  padding: 6px 10px;
  background: #f0f9eb;
  border-radius: 4px;
}
</style>
