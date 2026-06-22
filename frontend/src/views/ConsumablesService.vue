<template>
  <div class="consumables-service">
    <div class="page-header">
      <h1 class="page-title">
        <el-icon color="#409eff" style="margin-right: 8px"><Box /></el-icon>
        耗材与服务管理
      </h1>
    </div>

    <div v-loading="loading">
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="6">
          <div class="stat-card normal">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats?.normal || 0 }}</div>
              <div class="stat-label">正常耗材</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card soon">
            <div class="stat-icon">🔔</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats?.soon_due || 0 }}</div>
              <div class="stat-label">即将更换</div>
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
          <div class="stat-card low-stock">
            <div class="stat-icon">📦</div>
            <div class="stat-content">
              <div class="stat-value">{{ stats?.low_stock || 0 }}</div>
              <div class="stat-label">库存不足</div>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="6">
          <div class="stat-card ticket-pending">
            <div class="stat-icon">⏳</div>
            <div class="stat-content">
              <div class="stat-value">{{ ticketStats?.pending || 0 }}</div>
              <div class="stat-label">待处理工单</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card ticket-progress">
            <div class="stat-icon">🔧</div>
            <div class="stat-content">
              <div class="stat-value">{{ ticketStats?.in_progress || 0 }}</div>
              <div class="stat-label">处理中工单</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card ticket-completed">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-value">{{ ticketStats?.completed || 0 }}</div>
              <div class="stat-label">已完成工单</div>
            </div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card ticket-total">
            <div class="stat-icon">📋</div>
            <div class="stat-content">
              <div class="stat-value">{{ ticketStats?.total || 0 }}</div>
              <div class="stat-label">工单总数</div>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="耗材管理" name="consumables">
          <div class="card">
            <div class="filter-bar">
              <el-select v-model="filterProfileId" placeholder="选择老人" clearable style="width: 160px" @change="loadConsumables">
                <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
              </el-select>
              <el-select v-model="filterConsumableType" placeholder="耗材类型" clearable style="width: 140px" @change="loadConsumables">
                <el-option v-for="t in CONSUMABLE_TYPES" :key="t.value" :label="t.label" :value="t.value" />
              </el-select>
              <el-select v-model="filterEar" placeholder="适配耳别" clearable style="width: 140px" @change="loadConsumables">
                <el-option v-for="e in EAR_OPTIONS" :key="e.value" :label="e.label" :value="e.value" />
              </el-select>
              <el-select v-model="filterLowStock" placeholder="库存状态" clearable style="width: 140px" @change="loadConsumables">
                <el-option label="库存不足" :value="true" />
                <el-option label="库存充足" :value="false" />
              </el-select>
              <el-select v-model="filterNeedsReplacement" placeholder="更换状态" clearable style="width: 140px" @change="loadConsumables">
                <el-option label="待更换(含逾期)" :value="true" />
                <el-option label="正常" :value="false" />
              </el-select>
              <el-button @click="resetConsumableFilters">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
              <el-button type="primary" @click="openConsumableDialog">
                <el-icon><Plus /></el-icon>
                登记耗材
              </el-button>
            </div>

            <el-empty
              v-if="filteredConsumables.length === 0"
              description="暂无耗材记录，点击上方按钮登记"
              :image-size="80"
            />

            <el-table v-else :data="filteredConsumables" style="width: 100%">
              <el-table-column prop="elderly_name" label="老人" width="100" />
              <el-table-column label="耗材名称" width="140">
                <template #default="{ row }">
                  <span style="font-weight: 600">{{ getConsumableTypeIcon(row.consumable_type) }} {{ row.name }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="consumable_type" label="类型" width="100">
                <template #default="{ row }">
                  <el-tag size="small">{{ row.consumable_type }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="ear" label="耳别" width="80">
                <template #default="{ row }">
                  <el-tag v-if="row.ear" :type="row.ear === '左耳' ? 'primary' : row.ear === '右耳' ? 'success' : 'info'" size="small">
                    {{ row.ear }}
                  </el-tag>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column prop="start_date" label="启用日期" width="110" />
              <el-table-column label="更换周期" width="100">
                <template #default="{ row }">
                  <span v-if="row.replacement_cycle_days">{{ row.replacement_cycle_days }} 天</span>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column prop="last_replacement_date" label="最近更换" width="110">
                <template #default="{ row }">
                  <span>{{ row.last_replacement_date || '-' }}</span>
                </template>
              </el-table-column>
              <el-table-column label="预计下次更换" width="130">
                <template #default="{ row }">
                  <span v-if="row.next_replacement_date" :class="{ 'text-danger': row.is_overdue, 'text-warning': row.is_soon_due }">
                    {{ row.next_replacement_date }}
                    <el-tag v-if="row.is_overdue" type="danger" size="small" effect="dark" style="margin-left: 4px">
                      逾期 {{ Math.abs(row.days_until_replacement || 0) }} 天
                    </el-tag>
                    <el-tag v-else-if="row.is_soon_due" type="warning" size="small" style="margin-left: 4px">
                      {{ row.days_until_replacement === 0 ? '今天' : `${row.days_until_replacement} 天` }}
                    </el-tag>
                  </span>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column label="库存数量" width="100">
                <template #default="{ row }">
                  <span :class="{ 'text-danger': row.is_low_stock }">
                    {{ row.stock_quantity ?? 0 }} 个
                    <el-tag v-if="row.is_low_stock" type="danger" size="small" effect="dark" style="margin-left: 4px">不足</el-tag>
                  </span>
                </template>
              </el-table-column>
              <el-table-column label="状态" width="100">
                <template #default="{ row }">
                  <el-tag :type="getConsumableStatusTagType(row.status)" size="small" effect="dark">
                    {{ getConsumableStatusLabel(row.status) }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="notes" label="备注" min-width="120" show-overflow-tooltip />
              <el-table-column label="操作" width="160" fixed="right">
                <template #default="{ row }">
                  <el-button size="small" @click="openEditConsumableDialog(row)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="deleteConsumable(row)">
                    <el-icon><Delete /></el-icon>
                  </el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="服务工单" name="tickets">
          <div class="card">
            <div class="filter-bar">
              <el-select v-model="filterTicketProfileId" placeholder="选择老人" clearable style="width: 160px" @change="loadTickets">
                <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
              </el-select>
              <el-select v-model="filterTicketStatus" placeholder="工单状态" clearable style="width: 140px" @change="loadTickets">
                <el-option v-for="s in SERVICE_TICKET_STATUSES" :key="s.value" :label="s.label" :value="s.value" />
              </el-select>
              <el-select v-model="filterIssueType" placeholder="问题类型" clearable style="width: 140px" @change="loadTickets">
                <el-option v-for="t in SERVICE_TICKET_TYPES" :key="t.value" :label="t.label" :value="t.value" />
              </el-select>
              <el-select v-model="filterServiceMethod" placeholder="服务方式" clearable style="width: 140px" @change="loadTickets">
                <el-option v-for="m in SERVICE_METHODS" :key="m.value" :label="m.label" :value="m.value" />
              </el-select>
              <el-button @click="resetTicketFilters">
                <el-icon><Refresh /></el-icon>
                重置
              </el-button>
              <el-button type="primary" @click="openTicketDialog">
                <el-icon><Plus /></el-icon>
                发起工单
              </el-button>
            </div>

            <el-empty
              v-if="filteredTickets.length === 0"
              description="暂无服务工单，点击上方按钮发起"
              :image-size="80"
            />

            <div v-else class="ticket-list">
              <div
                v-for="ticket in filteredTickets"
                :key="ticket.id"
                class="ticket-card"
                :class="{
                  'ticket-pending': ticket.status === 'pending',
                  'ticket-progress': ticket.status === 'in_progress',
                  'ticket-completed': ticket.status === 'completed'
                }"
              >
                <div class="ticket-header">
                  <div class="ticket-title">
                    <span class="ticket-type-icon">{{ getIssueTypeIcon(ticket.issue_type) }}</span>
                    <strong>{{ ticket.issue_type }}</strong>
                    <el-tag
                      :type="getTicketStatusTagType(ticket.status)"
                      size="small"
                      effect="dark"
                      style="margin-left: 8px"
                    >
                      {{ getTicketStatusLabel(ticket.status) }}
                    </el-tag>
                  </div>
                  <div class="ticket-actions">
                    <el-button
                      v-if="ticket.status !== 'completed' && ticket.status !== 'cancelled'"
                      type="success"
                      size="small"
                      @click.stop="openCompleteTicketDialog(ticket)"
                    >
                      <el-icon><Check /></el-icon>
                      完成
                    </el-button>
                    <el-button size="small" @click.stop="openEditTicketDialog(ticket)">
                      <el-icon><Edit /></el-icon>
                      编辑
                    </el-button>
                    <el-button type="danger" size="small" @click.stop="deleteTicket(ticket)">
                      <el-icon><Delete /></el-icon>
                    </el-button>
                  </div>
                </div>

                <div class="ticket-meta">
                  <el-tag type="info" size="small">{{ ticket.elderly_name }}</el-tag>
                  <el-tag v-if="ticket.consumable_name" type="warning" size="small">
                    关联耗材：{{ ticket.consumable_name }}
                  </el-tag>
                  <el-tag v-if="ticket.service_method" size="small">
                    {{ getServiceMethodIcon(ticket.service_method) }} {{ ticket.service_method }}
                  </el-tag>
                  <span v-if="ticket.handler" class="meta-item">
                    <el-icon><UserFilled /></el-icon>
                    处理人员：{{ ticket.handler }}
                  </span>
                  <span v-if="ticket.appointment_time" class="meta-item">
                    <el-icon><Calendar /></el-icon>
                    预约：{{ formatDateTime(ticket.appointment_time) }}
                  </span>
                  <span class="meta-item">
                    <el-icon><Clock /></el-icon>
                    创建：{{ formatDateTime(ticket.created_at) }}
                  </span>
                </div>

                <div v-if="ticket.description" class="ticket-description">
                  <strong>问题描述：</strong>{{ ticket.description }}
                </div>

                <div v-if="ticket.result" class="ticket-result">
                  <el-icon color="#67c23a"><ChatDotRound /></el-icon>
                  <strong>处理结果：</strong>{{ ticket.result }}
                </div>

                <div v-if="ticket.photo_urls && ticket.photo_urls.length > 0" class="ticket-photos">
                  <strong style="margin-right: 8px">照片：</strong>
                  <el-image
                    v-for="(url, idx) in ticket.photo_urls"
                    :key="idx"
                    :src="url"
                    :preview-src-list="ticket.photo_urls"
                    :initial-index="idx"
                    fit="cover"
                    style="width: 80px; height: 80px; border-radius: 4px; margin-right: 8px"
                  />
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-dialog v-model="consumableDialogVisible" :title="isConsumableEdit ? '编辑耗材' : '登记耗材'" width="600px">
      <el-form :model="consumableForm" label-width="110px">
        <el-form-item label="关联老人" required>
          <el-select v-model="consumableForm.profile_id" placeholder="请选择老人" style="width: 100%">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="耗材名称" required>
          <el-input v-model="consumableForm.name" placeholder="请输入耗材名称" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="耗材类型" required>
          <el-select v-model="consumableForm.consumable_type" placeholder="请选择耗材类型" style="width: 100%">
            <el-option v-for="t in CONSUMABLE_TYPES" :key="t.value" :label="`${t.icon} ${t.label}`" :value="t.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="适配耳别">
          <el-select v-model="consumableForm.ear" placeholder="请选择耳别" clearable style="width: 100%">
            <el-option v-for="e in EAR_OPTIONS" :key="e.value" :label="e.label" :value="e.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="启用日期">
          <el-date-picker
            v-model="consumableForm.start_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择启用日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="建议更换周期">
          <el-input-number v-model="consumableForm.replacement_cycle_days" :min="1" :max="3650" style="width: 100%">
            <template #default="{ value }">
              <span>{{ value }} 天</span>
            </template>
          </el-input-number>
        </el-form-item>
        <el-form-item label="最近更换日期">
          <el-date-picker
            v-model="consumableForm.last_replacement_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择最近更换日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="库存数量">
          <el-input-number v-model="consumableForm.stock_quantity" :min="0" :max="9999" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="consumableForm.notes" type="textarea" :rows="2" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="consumableDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveConsumable">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="ticketDialogVisible" :title="isTicketEdit ? '编辑工单' : '发起服务工单'" width="600px">
      <el-form :model="ticketForm" label-width="110px">
        <el-form-item label="关联老人" required>
          <el-select v-model="ticketForm.profile_id" placeholder="请选择老人" style="width: 100%" @change="loadProfileConsumables">
            <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="问题类型" required>
          <el-select v-model="ticketForm.issue_type" placeholder="请选择问题类型" style="width: 100%">
            <el-option v-for="t in SERVICE_TICKET_TYPES" :key="t.value" :label="`${t.icon} ${t.label}`" :value="t.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联耗材">
          <el-select v-model="ticketForm.consumable_id" placeholder="选择关联的耗材(可选)" clearable style="width: 100%">
            <el-option v-for="c in profileConsumables" :key="c.id" :label="`${c.name} (${c.consumable_type})`" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="服务方式">
          <el-radio-group v-model="ticketForm.service_method">
            <el-radio v-for="m in SERVICE_METHODS" :key="m.value" :value="m.value">
              {{ m.icon }} {{ m.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="预约时间">
          <el-date-picker
            v-model="ticketForm.appointment_time"
            type="datetime"
            value-format="YYYY-MM-DDTHH:mm:ss"
            placeholder="选择预约时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="处理人员">
          <el-input v-model="ticketForm.handler" placeholder="请输入处理人员姓名" />
        </el-form-item>
        <el-form-item label="工单状态">
          <el-select v-model="ticketForm.status" style="width: 100%">
            <el-option v-for="s in SERVICE_TICKET_STATUSES" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="问题描述">
          <el-input v-model="ticketForm.description" type="textarea" :rows="3" placeholder="请详细描述问题情况" />
        </el-form-item>
        <el-form-item v-if="ticketForm.status === 'completed'" label="处理结果">
          <el-input v-model="ticketForm.result" type="textarea" :rows="2" placeholder="请输入处理结果" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="ticketDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveTicket">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="completeTicketDialogVisible" title="完成工单" width="500px">
      <div style="margin-bottom: 16px">
        <p><strong>问题类型：</strong>{{ currentTicket?.issue_type }}</p>
        <p><strong>老人：</strong>{{ currentTicket?.elderly_name }}</p>
      </div>
      <el-form label-width="100px">
        <el-form-item label="处理结果">
          <el-input v-model="ticketResultFeedback" type="textarea" :rows="3" placeholder="请描述处理结果" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="completeTicketDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmCompleteTicket">确认完成</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Box,
  Refresh,
  Plus,
  Edit,
  Delete,
  UserFilled,
  Calendar,
  Clock,
  ChatDotRound,
  Check
} from '@element-plus/icons-vue'
import { profileApi, consumableApi, serviceTicketApi } from '@/api'
import {
  CONSUMABLE_TYPES,
  EAR_OPTIONS,
  CONSUMABLE_STATUSES,
  SERVICE_TICKET_TYPES,
  SERVICE_METHODS,
  SERVICE_TICKET_STATUSES
} from '@/types'
import type { Profile, Consumable, ServiceTicket } from '@/types'

const loading = ref(false)
const activeTab = ref('consumables')
const profiles = ref<Profile[]>([])
const consumables = ref<Consumable[]>([])
const tickets = ref<ServiceTicket[]>([])
const profileConsumables = ref<Consumable[]>([])

const filterProfileId = ref<number>()
const filterConsumableType = ref<string>()
const filterEar = ref<string>()
const filterLowStock = ref<boolean>()
const filterNeedsReplacement = ref<boolean>()

const filterTicketProfileId = ref<number>()
const filterTicketStatus = ref<string>()
const filterIssueType = ref<string>()
const filterServiceMethod = ref<string>()

const consumableDialogVisible = ref(false)
const ticketDialogVisible = ref(false)
const completeTicketDialogVisible = ref(false)
const isConsumableEdit = ref(false)
const isTicketEdit = ref(false)
const currentConsumable = ref<Consumable>()
const currentTicket = ref<ServiceTicket>()
const ticketResultFeedback = ref('')

const consumableForm = ref<Partial<Consumable>>({
  profile_id: undefined,
  name: '',
  consumable_type: '耳塞',
  ear: '',
  start_date: '',
  replacement_cycle_days: 90,
  stock_quantity: 0,
  last_replacement_date: '',
  notes: ''
})

const ticketForm = ref<Partial<ServiceTicket>>({
  profile_id: undefined,
  consumable_id: undefined,
  issue_type: '耗材损坏',
  service_method: '上门服务',
  appointment_time: '',
  handler: '',
  status: 'pending',
  result: '',
  description: '',
  photo_urls: []
})

const stats = computed(() => {
  const normal = consumables.value.filter(c => c.status === 'normal').length
  const soon_due = consumables.value.filter(c => c.status === 'soon_due').length
  const overdue = consumables.value.filter(c => c.status === 'overdue').length
  const low_stock = consumables.value.filter(c => c.status === 'low_stock').length
  return { normal, soon_due, overdue, low_stock }
})

const ticketStats = computed(() => {
  const pending = tickets.value.filter(t => t.status === 'pending').length
  const in_progress = tickets.value.filter(t => t.status === 'in_progress').length
  const completed = tickets.value.filter(t => t.status === 'completed').length
  const total = tickets.value.length
  return { pending, in_progress, completed, total }
})

const filteredConsumables = computed(() => {
  let result = [...consumables.value]
  if (filterProfileId.value) result = result.filter(c => c.profile_id === filterProfileId.value)
  if (filterConsumableType.value) result = result.filter(c => c.consumable_type === filterConsumableType.value)
  if (filterEar.value) result = result.filter(c => c.ear === filterEar.value)
  if (filterLowStock.value !== undefined) result = result.filter(c => c.is_low_stock === filterLowStock.value)
  if (filterNeedsReplacement.value !== undefined) {
    result = result.filter(c => (c.is_overdue || c.is_soon_due) === filterNeedsReplacement.value)
  }
  return result
})

const filteredTickets = computed(() => {
  let result = [...tickets.value]
  if (filterTicketProfileId.value) result = result.filter(t => t.profile_id === filterTicketProfileId.value)
  if (filterTicketStatus.value) result = result.filter(t => t.status === filterTicketStatus.value)
  if (filterIssueType.value) result = result.filter(t => t.issue_type === filterIssueType.value)
  if (filterServiceMethod.value) result = result.filter(t => t.service_method === filterServiceMethod.value)
  return result
})

const getConsumableTypeIcon = (type: string) => {
  const item = CONSUMABLE_TYPES.find(t => t.value === type)
  return item?.icon || '📦'
}

const getConsumableStatusLabel = (status?: string) => {
  const item = CONSUMABLE_STATUSES.find(s => s.value === status)
  return item?.label || status
}

const getConsumableStatusTagType = (status?: string) => {
  if (status === 'overdue' || status === 'low_stock') return 'danger'
  if (status === 'soon_due') return 'warning'
  return 'success'
}

const getIssueTypeIcon = (type: string) => {
  const item = SERVICE_TICKET_TYPES.find(t => t.value === type)
  return item?.icon || '📝'
}

const getServiceMethodIcon = (method: string) => {
  const item = SERVICE_METHODS.find(m => m.value === method)
  return item?.icon || ''
}

const getTicketStatusLabel = (status?: string) => {
  const item = SERVICE_TICKET_STATUSES.find(s => s.value === status)
  return item?.label || status
}

const getTicketStatusTagType = (status?: string) => {
  if (status === 'completed') return 'success'
  if (status === 'in_progress') return 'primary'
  if (status === 'cancelled') return 'info'
  return 'warning'
}

const formatDateTime = (str?: string) => {
  if (!str) return '-'
  return str.replace('T', ' ').slice(0, 16)
}

const resetConsumableFilters = () => {
  filterProfileId.value = undefined
  filterConsumableType.value = undefined
  filterEar.value = undefined
  filterLowStock.value = undefined
  filterNeedsReplacement.value = undefined
  loadConsumables()
}

const resetTicketFilters = () => {
  filterTicketProfileId.value = undefined
  filterTicketStatus.value = undefined
  filterIssueType.value = undefined
  filterServiceMethod.value = undefined
  loadTickets()
}

const extractErrorMessage = (err: any) => {
  const resp = err?.response?.data
  if (typeof resp === 'string') return resp
  if (resp?.error) return resp.error
  if (resp?.message) return resp.message
  return '操作失败'
}

const openConsumableDialog = () => {
  isConsumableEdit.value = false
  consumableForm.value = {
    profile_id: profiles.value.length > 0 ? profiles.value[0].id : undefined,
    name: '',
    consumable_type: '耳塞',
    ear: '',
    start_date: new Date().toISOString().split('T')[0],
    replacement_cycle_days: 90,
    stock_quantity: 0,
    last_replacement_date: '',
    notes: ''
  }
  consumableDialogVisible.value = true
}

const openEditConsumableDialog = (c: Consumable) => {
  isConsumableEdit.value = true
  currentConsumable.value = c
  consumableForm.value = { ...c }
  consumableDialogVisible.value = true
}

const saveConsumable = async () => {
  if (!consumableForm.value.profile_id || !consumableForm.value.name || !consumableForm.value.consumable_type) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    if (isConsumableEdit.value && currentConsumable.value?.id) {
      await consumableApi.update(currentConsumable.value.id, consumableForm.value)
      ElMessage.success('更新成功')
    } else {
      await consumableApi.create(consumableForm.value as Consumable)
      ElMessage.success('登记成功')
    }
    consumableDialogVisible.value = false
    loadConsumables()
  } catch (e) {
    ElMessage.error(extractErrorMessage(e))
  }
}

const deleteConsumable = async (c: Consumable) => {
  try {
    await ElMessageBox.confirm(`确定要删除耗材"${c.name}"吗？`, '确认删除', { type: 'warning' })
    if (!c.id) return
    await consumableApi.delete(c.id)
    ElMessage.success('删除成功')
    loadConsumables()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

const openTicketDialog = () => {
  isTicketEdit.value = false
  ticketForm.value = {
    profile_id: profiles.value.length > 0 ? profiles.value[0].id : undefined,
    consumable_id: undefined,
    issue_type: '耗材损坏',
    service_method: '上门服务',
    appointment_time: '',
    handler: '',
    status: 'pending',
    result: '',
    description: '',
    photo_urls: []
  }
  loadProfileConsumables()
  ticketDialogVisible.value = true
}

const openEditTicketDialog = (t: ServiceTicket) => {
  isTicketEdit.value = true
  currentTicket.value = t
  ticketForm.value = { ...t }
  loadProfileConsumables()
  ticketDialogVisible.value = true
}

const openCompleteTicketDialog = (t: ServiceTicket) => {
  currentTicket.value = t
  ticketResultFeedback.value = ''
  completeTicketDialogVisible.value = true
}

const confirmCompleteTicket = async () => {
  if (!currentTicket.value?.id) return
  try {
    await serviceTicketApi.update(currentTicket.value.id, {
      status: 'completed',
      result: ticketResultFeedback.value
    })
    ElMessage.success('工单已完成')
    completeTicketDialogVisible.value = false
    loadTickets()
  } catch (e) {
    ElMessage.error(extractErrorMessage(e))
  }
}

const saveTicket = async () => {
  if (!ticketForm.value.profile_id || !ticketForm.value.issue_type) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    if (isTicketEdit.value && currentTicket.value?.id) {
      await serviceTicketApi.update(currentTicket.value.id, ticketForm.value)
      ElMessage.success('更新成功')
    } else {
      await serviceTicketApi.create(ticketForm.value as ServiceTicket)
      ElMessage.success('工单已发起')
    }
    ticketDialogVisible.value = false
    loadTickets()
  } catch (e) {
    ElMessage.error(extractErrorMessage(e))
  }
}

const deleteTicket = async (t: ServiceTicket) => {
  try {
    await ElMessageBox.confirm(`确定要删除该工单吗？`, '确认删除', { type: 'warning' })
    if (!t.id) return
    await serviceTicketApi.delete(t.id)
    ElMessage.success('删除成功')
    loadTickets()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

const loadProfileConsumables = async () => {
  if (!ticketForm.value.profile_id) {
    profileConsumables.value = []
    return
  }
  try {
    const res = await consumableApi.getAll(ticketForm.value.profile_id)
    profileConsumables.value = res.data
  } catch (e) {
    profileConsumables.value = []
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

const loadConsumables = async () => {
  loading.value = true
  try {
    const res = await consumableApi.getAll(
      filterProfileId.value,
      filterConsumableType.value,
      filterEar.value,
      filterLowStock.value,
      filterNeedsReplacement.value
    )
    consumables.value = res.data
  } catch (e) {
    ElMessage.error('加载耗材列表失败')
  } finally {
    loading.value = false
  }
}

const loadTickets = async () => {
  loading.value = true
  try {
    const res = await serviceTicketApi.getAll(
      filterTicketProfileId.value,
      filterTicketStatus.value,
      filterIssueType.value,
      filterServiceMethod.value
    )
    tickets.value = res.data
  } catch (e) {
    ElMessage.error('加载工单列表失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadProfiles()
  loadConsumables()
  loadTickets()
})
</script>

<style scoped>
.consumables-service {
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

.stat-card.normal {
  background: linear-gradient(135deg, #67c23a, #95d475);
}

.stat-card.soon {
  background: linear-gradient(135deg, #e6a23c, #f0c78a);
}

.stat-card.overdue {
  background: linear-gradient(135deg, #f56c6c, #f78989);
}

.stat-card.low-stock {
  background: linear-gradient(135deg, #f56c6c, #f89898);
}

.stat-card.ticket-pending {
  background: linear-gradient(135deg, #909399, #b1b3b8);
}

.stat-card.ticket-progress {
  background: linear-gradient(135deg, #409eff, #79bbff);
}

.stat-card.ticket-completed {
  background: linear-gradient(135deg, #67c23a, #95d475);
}

.stat-card.ticket-total {
  background: linear-gradient(135deg, #8e44ad, #a569bd);
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

.text-danger {
  color: #f56c6c;
  font-weight: 600;
}

.text-warning {
  color: #e6a23c;
  font-weight: 600;
}

.ticket-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.ticket-card {
  padding: 16px 20px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.2s;
  border-left: 4px solid #dcdfe6;
}

.ticket-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.ticket-card.ticket-pending {
  border-left-color: #e6a23c;
  background: #fdf6ec;
}

.ticket-card.ticket-progress {
  border-left-color: #409eff;
  background: #ecf5ff;
}

.ticket-card.ticket-completed {
  border-left-color: #67c23a;
  opacity: 0.85;
}

.ticket-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.ticket-title {
  font-size: 16px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.ticket-type-icon {
  font-size: 20px;
  margin-right: 4px;
}

.ticket-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.ticket-meta {
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

.ticket-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 8px;
  padding: 8px 12px;
  background: #f5f7fa;
  border-radius: 4px;
}

.ticket-result {
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

.ticket-photos {
  display: flex;
  align-items: center;
  margin-top: 8px;
  padding-top: 12px;
  border-top: 1px dashed #e4e7ed;
}
</style>
