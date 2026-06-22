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

    <el-row :gutter="20" style="margin-bottom: 20px">
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #67c23a">{{ consumables.length }}</div>
          <div class="stat-label">耗材总数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #f56c6c">{{ consumableAlerts.overdue }}</div>
          <div class="stat-label">已逾期耗材</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #e6a23c">{{ consumableAlerts.soon_due + consumableAlerts.low_stock }}</div>
          <div class="stat-label">待关注耗材</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card">
          <div class="stat-value" style="color: #409eff">{{ serviceTickets.length }}</div>
          <div class="stat-label">服务工单总数</div>
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

      <el-tab-pane label="耗材与服务" name="consumables-service">
        <div class="card">
          <div class="page-header" style="border: none; margin: 0; padding: 0; margin-bottom: 20px">
            <div style="display: flex; align-items: center; gap: 12px">
              <h3 style="font-size: 18px; margin: 0">
                <el-icon color="#409eff" style="margin-right: 8px"><Box /></el-icon>
                耗材状态与服务工单
              </h3>
              <el-tag v-if="consumableAlerts.overdue > 0" type="danger" effect="dark">
                {{ consumableAlerts.overdue }} 项已逾期
              </el-tag>
              <el-tag v-if="consumableAlerts.soon_due > 0" type="warning" effect="dark">
                {{ consumableAlerts.soon_due }} 项即将更换
              </el-tag>
              <el-tag v-if="consumableAlerts.low_stock > 0" type="warning">
                {{ consumableAlerts.low_stock }} 项库存不足
              </el-tag>
            </div>
            <div style="display: flex; gap: 8px">
              <el-button type="primary" size="small" @click="openDetailConsumableDialog">
                <el-icon><Plus /></el-icon>
                登记耗材
              </el-button>
              <el-button type="success" size="small" @click="openDetailTicketDialog">
                <el-icon><Plus /></el-icon>
                发起工单
              </el-button>
            </div>
          </div>

          <el-divider content-position="left">耗材清单</el-divider>

          <el-empty
            v-if="consumables.length === 0"
            description="暂无耗材记录，点击上方按钮登记"
            :image-size="60"
          />

          <el-table v-else :data="consumables" style="width: 100%; margin-bottom: 24px">
            <el-table-column label="耗材名称" width="140">
              <template #default="{ row }">
                <span style="font-weight: 600">{{ getDetailConsumableTypeIcon(row.consumable_type) }} {{ row.name }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="consumable_type" label="类型" width="90">
              <template #default="{ row }">
                <el-tag size="small">{{ row.consumable_type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="ear" label="耳别" width="70">
              <template #default="{ row }">
                <el-tag v-if="row.ear" :type="row.ear === '左耳' ? 'primary' : row.ear === '右耳' ? 'success' : 'info'" size="small">
                  {{ row.ear }}
                </el-tag>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column label="更换周期" width="90">
              <template #default="{ row }">
                <span v-if="row.replacement_cycle_days">{{ row.replacement_cycle_days }} 天</span>
                <span v-else>-</span>
              </template>
            </el-table-column>
            <el-table-column prop="last_replacement_date" label="最近更换" width="100">
              <template #default="{ row }">
                <span>{{ row.last_replacement_date || '-' }}</span>
              </template>
            </el-table-column>
            <el-table-column label="预计下次更换" width="160">
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
            <el-table-column label="库存" width="90">
              <template #default="{ row }">
                <span :class="{ 'text-danger': row.is_low_stock }">
                  {{ row.stock_quantity ?? 0 }}
                  <el-tag v-if="row.is_low_stock" type="danger" size="small" effect="dark" style="margin-left: 4px">不足</el-tag>
                </span>
              </template>
            </el-table-column>
            <el-table-column label="状态" width="90">
              <template #default="{ row }">
                <el-tag :type="getDetailConsumableStatusTagType(row.status)" size="small" effect="dark">
                  {{ getDetailConsumableStatusLabel(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="notes" label="备注" min-width="100" show-overflow-tooltip />
            <el-table-column label="操作" width="120" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="openDetailEditConsumableDialog(row)">
                  <el-icon><Edit /></el-icon>
                  编辑
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <el-divider content-position="left">最近服务工单</el-divider>

          <el-empty
            v-if="serviceTickets.length === 0"
            description="暂无服务工单，点击上方按钮发起"
            :image-size="60"
          />

          <div v-else class="ticket-list">
            <div
              v-for="ticket in recentServiceTickets"
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
                  <span class="ticket-type-icon">{{ getDetailIssueTypeIcon(ticket.issue_type) }}</span>
                  <strong>{{ ticket.issue_type }}</strong>
                  <el-tag
                    :type="getDetailTicketStatusTagType(ticket.status)"
                    size="small"
                    effect="dark"
                    style="margin-left: 8px"
                  >
                    {{ getDetailTicketStatusLabel(ticket.status) }}
                  </el-tag>
                </div>
                <div class="ticket-actions">
                  <el-button
                    v-if="ticket.status !== 'completed' && ticket.status !== 'cancelled'"
                    type="success"
                    size="small"
                    @click.stop="openDetailCompleteTicketDialog(ticket)"
                  >
                    <el-icon><Check /></el-icon>
                    完成
                  </el-button>
                  <el-button size="small" @click.stop="openDetailEditTicketDialog(ticket)">
                    <el-icon><Edit /></el-icon>
                    编辑
                  </el-button>
                </div>
              </div>

              <div class="ticket-meta">
                <el-tag v-if="ticket.consumable_name" type="warning" size="small">
                  关联耗材：{{ ticket.consumable_name }}
                </el-tag>
                <el-tag v-if="ticket.service_method" size="small">
                  {{ getDetailServiceMethodIcon(ticket.service_method) }} {{ ticket.service_method }}
                </el-tag>
                <span v-if="ticket.handler" class="meta-item">
                  <el-icon><UserFilled /></el-icon>
                  处理人员：{{ ticket.handler }}
                </span>
                <span v-if="ticket.appointment_time" class="meta-item">
                  <el-icon><Calendar /></el-icon>
                  预约：{{ formatDetailDateTime(ticket.appointment_time) }}
                </span>
                <span class="meta-item">
                  <el-icon><Clock /></el-icon>
                  创建：{{ formatDetailDateTime(ticket.created_at) }}
                </span>
              </div>

              <div v-if="ticket.description" class="ticket-description">
                <strong>问题描述：</strong>{{ ticket.description }}
              </div>

              <div v-if="ticket.result" class="ticket-result">
                <el-icon color="#67c23a"><ChatDotRound /></el-icon>
                <strong>处理结果：</strong>{{ ticket.result }}
              </div>
            </div>
          </div>
        </div>
      </el-tab-pane>

      <el-tab-pane label="适应训练" name="training">
        <div class="card">
          <div class="page-header" style="border: none; margin: 0; padding: 0; margin-bottom: 20px">
            <h3 style="font-size: 18px; margin: 0">
              🎧 听力训练与佩戴适应计划
            </h3>
            <el-button type="primary" size="small" @click="router.push('/training')">
              <el-icon><ArrowRight /></el-icon>
              前往训练管理
            </el-button>
          </div>

          <el-empty v-if="trainingPlans.length === 0" description="暂无训练计划" :image-size="60" />

          <div v-for="plan in trainingPlans" :key="plan.id" class="detail-training-card">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px">
              <div style="display: flex; align-items: center; gap: 8px">
                <strong>{{ plan.training_scenario }}</strong>
                <el-tag :type="plan.status === 'active' ? 'primary' : plan.status === 'completed' ? 'success' : 'warning'" size="small" effect="dark">
                  {{ plan.status === 'active' ? '进行中' : plan.status === 'completed' ? '已完成' : plan.status === 'paused' ? '已暂停' : '已取消' }}
                </el-tag>
                <el-tag v-if="plan.streak_days && plan.streak_days > 0" type="warning" size="small">🔥 连续{{ plan.streak_days }}天</el-tag>
              </div>
              <span style="font-size: 13px; color: #606266">
                进度：{{ plan.completed_days || 0 }}/{{ plan.cycle_days }}天 ({{ plan.completion_rate || 0 }}%)
              </span>
            </div>
            <el-progress :percentage="Math.min(plan.completion_rate || 0, 100)" :stroke-width="8" :color="plan.completion_rate && plan.completion_rate >= 80 ? '#67c23a' : plan.completion_rate && plan.completion_rate >= 50 ? '#e6a23c' : '#f56c6c'" style="margin-bottom: 8px" />
            <el-descriptions :column="4" size="small" border>
              <el-descriptions-item label="训练目标">{{ plan.goal }}</el-descriptions-item>
              <el-descriptions-item label="每日佩戴">{{ plan.daily_wear_minutes }} 分钟</el-descriptions-item>
              <el-descriptions-item label="音量等级">{{ plan.volume_level }}</el-descriptions-item>
              <el-descriptions-item label="负责人">{{ plan.responsible_person || '-' }}</el-descriptions-item>
            </el-descriptions>

            <div v-if="plan.recent_7_days && plan.recent_7_days.length > 0" style="margin-top: 8px">
              <span style="font-size: 12px; color: #909399">近7天：</span>
              <span v-for="day in plan.recent_7_days" :key="day.date" style="margin-right: 6px; font-size: 12px">
                <span :style="{ color: day.completed ? '#67c23a' : '#c0c4cc' }">{{ day.date.substring(5) }} {{ day.completed ? '✅' : '⬜' }}</span>
                <span v-if="day.has_discomfort" style="color: #f56c6c">⚠️</span>
              </span>
            </div>

            <el-alert
              v-if="plan.abnormal_alerts && plan.abnormal_alerts.length > 0"
              :title="`异常提醒：近7天有${plan.abnormal_alerts.length}天出现不适/啸叫/明显疲劳`"
              type="warning"
              :closable="false"
              show-icon
              style="margin-top: 8px"
            />
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

    <el-dialog v-model="detailConsumableDialogVisible" :title="isDetailConsumableEdit ? '编辑耗材' : '登记耗材'" width="600px">
      <el-form :model="detailConsumableForm" label-width="110px">
        <el-form-item label="耗材名称" required>
          <el-input v-model="detailConsumableForm.name" placeholder="请输入耗材名称" maxlength="200" show-word-limit />
        </el-form-item>
        <el-form-item label="耗材类型" required>
          <el-select v-model="detailConsumableForm.consumable_type" placeholder="请选择耗材类型" style="width: 100%">
            <el-option v-for="t in CONSUMABLE_TYPES" :key="t.value" :label="`${t.icon} ${t.label}`" :value="t.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="适配耳别">
          <el-select v-model="detailConsumableForm.ear" placeholder="请选择耳别" clearable style="width: 100%">
            <el-option v-for="e in EAR_OPTIONS" :key="e.value" :label="e.label" :value="e.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="启用日期">
          <el-date-picker
            v-model="detailConsumableForm.start_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择启用日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="建议更换周期">
          <el-input-number v-model="detailConsumableForm.replacement_cycle_days" :min="1" :max="3650" style="width: 100%" />
        </el-form-item>
        <el-form-item label="最近更换日期">
          <el-date-picker
            v-model="detailConsumableForm.last_replacement_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="选择最近更换日期"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="库存数量">
          <el-input-number v-model="detailConsumableForm.stock_quantity" :min="0" :max="9999" style="width: 100%" />
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="detailConsumableForm.notes" type="textarea" :rows="2" placeholder="请输入备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="detailConsumableDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDetailConsumable">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailTicketDialogVisible" :title="isDetailTicketEdit ? '编辑工单' : '发起服务工单'" width="600px">
      <el-form :model="detailTicketForm" label-width="110px">
        <el-form-item label="问题类型" required>
          <el-select v-model="detailTicketForm.issue_type" placeholder="请选择问题类型" style="width: 100%">
            <el-option v-for="t in SERVICE_TICKET_TYPES" :key="t.value" :label="`${t.icon} ${t.label}`" :value="t.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="关联耗材">
          <el-select v-model="detailTicketForm.consumable_id" placeholder="选择关联的耗材(可选)" clearable style="width: 100%">
            <el-option v-for="c in consumables" :key="c.id" :label="`${c.name} (${c.consumable_type})`" :value="c.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="服务方式">
          <el-radio-group v-model="detailTicketForm.service_method">
            <el-radio v-for="m in SERVICE_METHODS" :key="m.value" :value="m.value">
              {{ m.icon }} {{ m.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="预约时间">
          <el-date-picker
            v-model="detailTicketForm.appointment_time"
            type="datetime"
            value-format="YYYY-MM-DDTHH:mm:ss"
            placeholder="选择预约时间"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="处理人员">
          <el-input v-model="detailTicketForm.handler" placeholder="请输入处理人员姓名" />
        </el-form-item>
        <el-form-item label="工单状态">
          <el-select v-model="detailTicketForm.status" style="width: 100%">
            <el-option v-for="s in SERVICE_TICKET_STATUSES" :key="s.value" :label="s.label" :value="s.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="问题描述">
          <el-input v-model="detailTicketForm.description" type="textarea" :rows="3" placeholder="请详细描述问题情况" />
        </el-form-item>
        <el-form-item label="照片说明">
          <div style="width: 100%">
            <div style="display: flex; gap: 8px; margin-bottom: 8px">
              <el-input v-model="newDetailPhotoUrl" placeholder="输入照片URL，按回车添加" @keyup.enter="addDetailPhotoUrl" />
              <el-button type="primary" @click="addDetailPhotoUrl">添加</el-button>
            </div>
            <div v-if="detailTicketForm.photo_urls && detailTicketForm.photo_urls.length > 0" style="display: flex; flex-wrap: wrap; gap: 8px">
              <div v-for="(url, idx) in detailTicketForm.photo_urls" :key="idx" style="position: relative">
                <el-image :src="url" :preview-src-list="detailTicketForm.photo_urls" :initial-index="idx" fit="cover" style="width: 80px; height: 80px; border-radius: 4px" />
                <el-button type="danger" size="small" circle style="position: absolute; top: -8px; right: -8px; padding: 0" @click="removeDetailPhotoUrl(idx)">
                  <el-icon><Close /></el-icon>
                </el-button>
              </div>
            </div>
            <div v-else style="color: #909399; font-size: 13px">暂无照片，可在上方输入URL添加</div>
          </div>
        </el-form-item>
        <el-form-item v-if="detailTicketForm.status === 'completed'" label="处理结果">
          <el-input v-model="detailTicketForm.result" type="textarea" :rows="2" placeholder="请输入处理结果" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="detailTicketDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDetailTicket">确定</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="detailCompleteTicketDialogVisible" title="完成工单" width="500px">
      <div style="margin-bottom: 16px">
        <p><strong>问题类型：</strong>{{ currentDetailTicket?.issue_type }}</p>
      </div>
      <el-form label-width="100px">
        <el-form-item label="处理结果">
          <el-input v-model="detailTicketResultFeedback" type="textarea" :rows="3" placeholder="请描述处理结果" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="detailCompleteTicketDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmDetailCompleteTicket">确认完成</el-button>
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
  ChatDotRound,
  Box,
  Close,
  ArrowRight
} from '@element-plus/icons-vue'
import { profileApi, feedbackApi, batteryApi, statisticsApi, taskApi, consumableApi, serviceTicketApi, trainingApi } from '@/api'
import { TASK_TYPES, TASK_PRIORITIES, TASK_STATUSES, CONSUMABLE_TYPES, EAR_OPTIONS, CONSUMABLE_STATUSES, SERVICE_TICKET_TYPES, SERVICE_METHODS, SERVICE_TICKET_STATUSES } from '@/types'
import type { Profile, BatteryRecord, Suggestion, BatteryStats, BatteryAbnormalCycle, TaskSummary, Task, Consumable, ServiceTicket, TrainingPlan } from '@/types'

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

const consumables = ref<Consumable[]>([])
const serviceTickets = ref<ServiceTicket[]>([])
const trainingPlans = ref<TrainingPlan[]>([])

const detailConsumableDialogVisible = ref(false)
const detailTicketDialogVisible = ref(false)
const detailCompleteTicketDialogVisible = ref(false)
const isDetailConsumableEdit = ref(false)
const isDetailTicketEdit = ref(false)
const currentDetailConsumable = ref<Consumable>()
const currentDetailTicket = ref<ServiceTicket>()
const detailTicketResultFeedback = ref('')
const newDetailPhotoUrl = ref('')

const detailConsumableForm = ref<Partial<Consumable>>({
  profile_id: Number(route.params.id),
  name: '',
  consumable_type: '耳塞',
  ear: '',
  start_date: '',
  replacement_cycle_days: 90,
  stock_quantity: 0,
  last_replacement_date: '',
  notes: ''
})

const detailTicketForm = ref<Partial<ServiceTicket>>({
  profile_id: Number(route.params.id),
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

const consumableAlerts = computed(() => {
  const overdue = consumables.value.filter(c => c.is_overdue).length
  const soon_due = consumables.value.filter(c => c.is_soon_due && !c.is_overdue).length
  const low_stock = consumables.value.filter(c => c.is_low_stock).length
  return { overdue, soon_due, low_stock }
})

const recentServiceTickets = computed(() => {
  return [...serviceTickets.value]
    .sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime())
    .slice(0, 5)
})

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
    const [p, o, s, br, bs, ts, tasks, cs, st, tp] = await Promise.all([
      profileApi.get(id),
      statisticsApi.getOverview(id),
      feedbackApi.getSuggestions(id),
      batteryApi.getAll(id),
      batteryApi.getStats(id),
      statisticsApi.getTaskSummary(id),
      taskApi.getAll(id),
      consumableApi.getAll(id),
      serviceTicketApi.getAll(id),
      trainingApi.getPlans(id)
    ])
    profile.value = p.data
    overview.value = o.data
    suggestions.value = s.data
    batteryRecords.value = br.data
    batteryStats.value = bs.data
    taskSummary.value = ts.data
    profileTasks.value = tasks.data
    consumables.value = cs.data
    serviceTickets.value = st.data
    trainingPlans.value = tp.data
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

const getDetailConsumableTypeIcon = (type: string) => {
  const item = CONSUMABLE_TYPES.find(t => t.value === type)
  return item?.icon || '📦'
}

const getDetailConsumableStatusLabel = (status?: string) => {
  const item = CONSUMABLE_STATUSES.find(s => s.value === status)
  return item?.label || status
}

const getDetailConsumableStatusTagType = (status?: string) => {
  if (status === 'overdue' || status === 'low_stock') return 'danger'
  if (status === 'soon_due') return 'warning'
  return 'success'
}

const getDetailIssueTypeIcon = (type: string) => {
  const item = SERVICE_TICKET_TYPES.find(t => t.value === type)
  return item?.icon || '📝'
}

const getDetailServiceMethodIcon = (method: string) => {
  const item = SERVICE_METHODS.find(m => m.value === method)
  return item?.icon || ''
}

const getDetailTicketStatusLabel = (status?: string) => {
  const item = SERVICE_TICKET_STATUSES.find(s => s.value === status)
  return item?.label || status
}

const getDetailTicketStatusTagType = (status?: string) => {
  if (status === 'completed') return 'success'
  if (status === 'in_progress') return 'primary'
  if (status === 'cancelled') return 'info'
  return 'warning'
}

const formatDetailDateTime = (str?: string) => {
  if (!str) return '-'
  return str.replace('T', ' ').slice(0, 16)
}

const extractDetailErrorMessage = (err: any) => {
  const resp = err?.response?.data
  if (typeof resp === 'string') return resp
  if (resp?.error) return resp.error
  if (resp?.message) return resp.message
  return '操作失败'
}

const openDetailConsumableDialog = () => {
  isDetailConsumableEdit.value = false
  detailConsumableForm.value = {
    profile_id: Number(route.params.id),
    name: '',
    consumable_type: '耳塞',
    ear: '',
    start_date: new Date().toISOString().split('T')[0],
    replacement_cycle_days: 90,
    stock_quantity: 0,
    last_replacement_date: '',
    notes: ''
  }
  detailConsumableDialogVisible.value = true
}

const openDetailEditConsumableDialog = (c: Consumable) => {
  isDetailConsumableEdit.value = true
  currentDetailConsumable.value = c
  detailConsumableForm.value = { ...c }
  detailConsumableDialogVisible.value = true
}

const saveDetailConsumable = async () => {
  if (!detailConsumableForm.value.name || !detailConsumableForm.value.consumable_type) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    if (isDetailConsumableEdit.value && currentDetailConsumable.value?.id) {
      await consumableApi.update(currentDetailConsumable.value.id, detailConsumableForm.value)
      ElMessage.success('更新成功')
    } else {
      await consumableApi.create(detailConsumableForm.value as Consumable)
      ElMessage.success('登记成功')
    }
    detailConsumableDialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error(extractDetailErrorMessage(e))
  }
}

const openDetailTicketDialog = () => {
  isDetailTicketEdit.value = false
  detailTicketForm.value = {
    profile_id: Number(route.params.id),
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
  detailTicketDialogVisible.value = true
}

const openDetailEditTicketDialog = (t: ServiceTicket) => {
  isDetailTicketEdit.value = true
  currentDetailTicket.value = t
  detailTicketForm.value = { ...t }
  detailTicketDialogVisible.value = true
}

const openDetailCompleteTicketDialog = (t: ServiceTicket) => {
  currentDetailTicket.value = t
  detailTicketResultFeedback.value = ''
  detailCompleteTicketDialogVisible.value = true
}

const confirmDetailCompleteTicket = async () => {
  if (!currentDetailTicket.value?.id) return
  try {
    await serviceTicketApi.update(currentDetailTicket.value.id, {
      status: 'completed',
      result: detailTicketResultFeedback.value
    })
    ElMessage.success('工单已完成')
    detailCompleteTicketDialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error(extractDetailErrorMessage(e))
  }
}

const saveDetailTicket = async () => {
  if (!detailTicketForm.value.issue_type) {
    ElMessage.warning('请填写必填项')
    return
  }
  try {
    if (isDetailTicketEdit.value && currentDetailTicket.value?.id) {
      await serviceTicketApi.update(currentDetailTicket.value.id, detailTicketForm.value)
      ElMessage.success('更新成功')
    } else {
      await serviceTicketApi.create(detailTicketForm.value as ServiceTicket)
      ElMessage.success('工单已发起')
    }
    detailTicketDialogVisible.value = false
    loadData()
  } catch (e) {
    ElMessage.error(extractDetailErrorMessage(e))
  }
}

const addDetailPhotoUrl = () => {
  const url = newDetailPhotoUrl.value.trim()
  if (!url) return
  if (!detailTicketForm.value.photo_urls) {
    detailTicketForm.value.photo_urls = []
  }
  if (detailTicketForm.value.photo_urls.includes(url)) {
    ElMessage.warning('该照片URL已添加')
    return
  }
  detailTicketForm.value.photo_urls.push(url)
  newDetailPhotoUrl.value = ''
}

const removeDetailPhotoUrl = (index: number) => {
  if (detailTicketForm.value.photo_urls) {
    detailTicketForm.value.photo_urls.splice(index, 1)
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
.detail-training-card {
  padding: 12px;
  margin-bottom: 12px;
  background: #f5f7fa;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}
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
  gap: 12px;
}

.ticket-card {
  padding: 14px 18px;
  background: #fff;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.2s;
  border-left: 4px solid #dcdfe6;
}

.ticket-card:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
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
  margin-bottom: 10px;
}

.ticket-title {
  font-size: 15px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
}

.ticket-type-icon {
  font-size: 18px;
  margin-right: 4px;
}

.ticket-actions {
  display: flex;
  gap: 6px;
  flex-shrink: 0;
}

.ticket-meta {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  align-items: center;
  margin-bottom: 10px;
}

.ticket-description {
  color: #606266;
  font-size: 13px;
  margin-bottom: 6px;
  padding: 6px 10px;
  background: #f5f7fa;
  border-radius: 4px;
}

.ticket-result {
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
