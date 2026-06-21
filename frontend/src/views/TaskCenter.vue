<template>
  <div class="task-center">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon color="#409eff" style="margin-right: 8px"><Tickets /></el-icon>
        家庭协作任务中心
      </h1>
      <el-button type="primary" @click="openCreateDialog">
        <el-icon><Plus /></el-icon>
        新建任务
      </el-button>
    </div>

    <div v-loading="loading">
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="6">
          <div class="stat-card pending">
            <div class="stat-icon">⏳</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats?.pending || 0 }}</div>
              <div class="stat-label">待处理</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card soon">
            <div class="stat-icon">🔔</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats?.soon_due || 0 }}</div>
              <div class="stat-label">即将到期 (3天内)</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card overdue">
            <div class="stat-icon">⚠️</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats?.overdue || 0 }}</div>
              <div class="stat-label">已逾期</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card completed">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats?.completed || 0 }}</div>
              <div class="stat-label">已完成</div>
            </div>
          </div>
        </el-col>
      </el-row>

      <div class="card">
        <div class="filter-bar">
          <el-select v-model="filterProfileId" placeholder="选择老人" clearable style="width: 160px" @change="loadTasks">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
          <el-select v-model="filterStatus" placeholder="任务状态" clearable style="width: 140px" @change="loadTasks">
            <el-option v-for="s in TASK_STATUSES" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
          <el-select v-model="filterTaskType" placeholder="任务类型" clearable style="width: 160px" @change="loadTasks">
            <el-option v-for="t in TASK_TYPES" :key="t.value" :label="t.label" :value="t.value" />
          </el-select>
          <el-select v-model="filterOverdue" placeholder="逾期状态" clearable style="width: 140px" @change="loadTasks">
            <el-option label="已逾期" :value="true" />
            <el-option label="未逾期" :value="false" />
          </el-select>
          <el-button @click="resetFilters">
            <el-icon><Refresh /></el-icon>
            重置筛选
          </el-button>
        </div>

        <el-empty
          v-if="filteredTasks.length === 0"
          description="暂无任务，点击右上角按钮创建新任务"
          :image-size="100"
        />

        <div v-else class="task-list">
          <div
            v-for="task in filteredTasks"
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
                  @click.stop="openCompleteDialog(task)"
                >
                  <el-icon><Check /></el-icon>
                  完成
                </el-button>
                <el-button size="small" @click.stop="openEditDialog(task)">
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
                <el-button type="danger" size="small" @click.stop="deleteTask(task)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </div>
            </div>

            <div class="task-meta">
              <el-tag :type="getPriorityTagType(task.priority)" size="small" effect="dark">
                {{ getPriorityLabel(task.priority) }}优先级
              </el-tag>
              <el-tag :type="getStatusTagType(task.status)" size="small">
                {{ getStatusLabel(task.status) }}
              </el-tag>
              <el-tag type="info" size="small">{{ task.task_type }}</el-tag>
              <span class="meta-item">
                <el-icon><User /></el-icon>
                {{ task.elderly_name }}
              </span>
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

            <div v-if="task.notes" class="task-notes">
              <el-icon color="#909399"><Document /></el-icon>
              <span>备注：{{ task.notes }}</span>
            </div>

            <div v-if="task.related_feedback_id || task.related_adjustment_id || task.related_followup_id" class="task-relations">
              <span class="relations-label">关联记录：</span>
              <el-tag v-if="task.related_feedback_id" size="small" type="warning">反馈 #{{ task.related_feedback_id }}</el-tag>
              <el-tag v-if="task.related_adjustment_id" size="small" type="primary">调试 #{{ task.related_adjustment_id }}</el-tag>
              <el-tag v-if="task.related_followup_id" size="small" type="success">复诊 #{{ task.related_followup_id }}</el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <el-dialog v-model="taskDialogVisible" :title="isEdit ? '编辑任务' : '新建任务'" width="600px">
      <el-form :model="taskForm" label-width="100px">
        <el-form-item label="关联老人" required>
          <el-select v-model="taskForm.profile_id" placeholder="请选择老人" style="width: 100%">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-form-item>
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
        <el-form-item label="关联记录">
          <div style="display: flex; gap: 12px; flex-wrap: wrap">
            <el-input
              v-model.number="taskForm.related_feedback_id"
              type="number"
              placeholder="反馈记录ID"
              style="width: 160px"
            />
            <el-input
              v-model.number="taskForm.related_adjustment_id"
              type="number"
              placeholder="调试记录ID"
              style="width: 160px"
            />
            <el-input
              v-model.number="taskForm.related_followup_id"
              type="number"
              placeholder="复诊记录ID"
              style="width: 160px"
            />
          </div>
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

    <el-dialog v-model="completeDialogVisible" title="完成任务" width="500px">
      <div style="margin-bottom: 16px">
        <p><strong>任务：</strong>{{ currentTask?.title }}</p>
        <p><strong>老人：</strong>{{ currentTask?.elderly_name }}</p>
      </div>
      <el-form label-width="100px">
        <el-form-item label="完成反馈">
          <el-input v-model="completionFeedback" type="textarea" :rows="3" placeholder="请描述任务完成情况" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmComplete">确认完成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Refresh,
  Check,
  Edit,
  Delete,
  User,
  UserFilled,
  Calendar,
  Document,
  ChatDotRound
} from '@element-plus/icons-vue'
import { profileApi, taskApi } from '@/api'
import { TASK_TYPES, TASK_PRIORITIES, TASK_STATUSES } from '@/types'
import type { Profile, Task } from '@/types'

const loading = ref(false)
const profiles = ref<Profile[]>([])
const tasks = ref<Task[]>([])

const filterProfileId = ref<number>()
const filterStatus = ref<string>()
const filterTaskType = ref<string>()
const filterOverdue = ref<boolean>()

const taskDialogVisible = ref(false)
const completeDialogVisible = ref(false)
const isEdit = ref(false)
const currentTask = ref<Task>()
const completionFeedback = ref('')

const taskForm = ref<Partial<Task>>({
  profile_id: undefined,
  title: '',
  task_type: '提醒佩戴',
  description: '',
  assignee: '',
  due_date: '',
  priority: 'medium',
  status: 'pending',
  notes: '',
  related_feedback_id: undefined,
  related_adjustment_id: undefined,
  related_followup_id: undefined,
  completion_feedback: ''
})

const stats = computed(() => {
  const pending = tasks.value.filter(t => t.status === 'pending').length
  const completed = tasks.value.filter(t => t.status === 'completed').length
  const overdue = tasks.value.filter(t => t.is_overdue && t.status !== 'completed').length
  const soon_due = tasks.value.filter(t => {
    const days = t.days_until_due
    return days != null && days >= 0 && days <= 3 && t.status !== 'completed'
  }).length
  return { pending, completed, overdue, soon_due }
})

const filteredTasks = computed(() => {
  let result = [...tasks.value]

  if (filterProfileId.value) {
    result = result.filter(t => t.profile_id === filterProfileId.value)
  }
  if (filterStatus.value) {
    result = result.filter(t => t.status === filterStatus.value)
  }
  if (filterTaskType.value) {
    result = result.filter(t => t.task_type === filterTaskType.value)
  }
  if (filterOverdue.value !== undefined) {
    result = result.filter(t => t.is_overdue === filterOverdue.value)
  }

  return result
})

const getTaskTypeIcon = (type: string) => {
  const item = TASK_TYPES.find(t => t.value === type)
  return item?.icon || '📝'
}

const getPriorityLabel = (priority?: string) => {
  const item = TASK_PRIORITIES.find(p => p.value === priority)
  return item?.label || priority
}

const getPriorityTagType = (priority?: string) => {
  if (priority === 'urgent') return 'danger'
  if (priority === 'high') return 'warning'
  if (priority === 'medium') return 'primary'
  return 'info'
}

const getStatusLabel = (status?: string) => {
  const item = TASK_STATUSES.find(s => s.value === status)
  return item?.label || status
}

const getStatusTagType = (status?: string) => {
  if (status === 'completed') return 'success'
  if (status === 'in_progress') return 'primary'
  if (status === 'cancelled') return 'info'
  return 'warning'
}

const resetFilters = () => {
  filterProfileId.value = undefined
  filterStatus.value = undefined
  filterTaskType.value = undefined
  filterOverdue.value = undefined
  loadTasks()
}

const openCreateDialog = () => {
  isEdit.value = false
  taskForm.value = {
    profile_id: profiles.value.length > 0 ? profiles.value[0].id : undefined,
    title: '',
    task_type: '提醒佩戴',
    description: '',
    assignee: '',
    due_date: '',
    priority: 'medium',
    status: 'pending',
    notes: '',
    related_feedback_id: undefined,
    related_adjustment_id: undefined,
    related_followup_id: undefined,
    completion_feedback: ''
  }
  taskDialogVisible.value = true
}

const openEditDialog = (task: Task) => {
  isEdit.value = true
  currentTask.value = task
  taskForm.value = { ...task }
  taskDialogVisible.value = true
}

const openCompleteDialog = (task: Task) => {
  currentTask.value = task
  completionFeedback.value = ''
  completeDialogVisible.value = true
}

const confirmComplete = async () => {
  if (!currentTask.value?.id) return
  try {
    await taskApi.complete(currentTask.value.id, completionFeedback.value)
    ElMessage.success('任务已完成')
    completeDialogVisible.value = false
    loadTasks()
  } catch (e) {
    ElMessage.error('操作失败')
  }
}

const saveTask = async () => {
  if (!taskForm.value.profile_id || !taskForm.value.title || !taskForm.value.task_type) {
    ElMessage.warning('请填写必填项')
    return
  }

  try {
    if (isEdit.value && currentTask.value?.id) {
      await taskApi.update(currentTask.value.id, taskForm.value)
      ElMessage.success('更新成功')
    } else {
      await taskApi.create(taskForm.value as Task)
      ElMessage.success('创建成功')
    }
    taskDialogVisible.value = false
    loadTasks()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

const deleteTask = async (task: Task) => {
  try {
    await ElMessageBox.confirm(`确定要删除任务"${task.title}"吗？`, '确认删除', {
      type: 'warning'
    })
    if (!task.id) return
    await taskApi.delete(task.id)
    ElMessage.success('删除成功')
    loadTasks()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const loadProfiles = async () => {
  try {
    const res = await profileApi.getAll()
    profiles.value = res.data
  } catch (e) {
    ElMessage.error('加载老人列表失败')
  }
}

const loadTasks = async () => {
  loading.value = true
  try {
    const res = await taskApi.getAll(filterProfileId.value, filterStatus.value, filterTaskType.value, filterOverdue.value)
    tasks.value = res.data
  } catch (e) {
    ElMessage.error('加载任务列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfiles()
  loadTasks()
})
</script>

<style scoped>
.task-center {
  padding: 0;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border-radius: 12px;
  color: #fff;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-card.pending {
  background: linear-gradient(135deg, #909399, #b1b3b8);
}

.stat-card.soon {
  background: linear-gradient(135deg, #e6a23c, #f0c78a);
}

.stat-card.overdue {
  background: linear-gradient(135deg, #f56c6c, #f78989);
}

.stat-card.completed {
  background: linear-gradient(135deg, #67c23a, #95d475);
}

.stat-icon {
  font-size: 36px;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  opacity: 0.95;
  margin-top: 4px;
}

.filter-bar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.task-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.task-card {
  padding: 16px 20px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.2s;
  border-left: 4px solid #dcdfe6;
}

.task-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
  margin-bottom: 12px;
}

.task-title {
  font-size: 16px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.task-type-icon {
  font-size: 20px;
  margin-right: 4px;
}

.task-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.task-meta {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 12px;
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
  font-size: 14px;
  margin-bottom: 8px;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.task-feedback {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  color: #67c23a;
  font-size: 14px;
  margin-bottom: 8px;
  padding: 8px 12px;
  background: #f0f9eb;
  border-radius: 4px;
}

.task-notes {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  color: #909399;
  font-size: 13px;
  margin-bottom: 8px;
}

.task-relations {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  padding-top: 12px;
  border-top: 1px dashed #e4e7ed;
  font-size: 13px;
}

.relations-label {
  color: #909399;
}
</style>
