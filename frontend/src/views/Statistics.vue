<template>
  <div class="statistics-page">
    <div class="page-header">
      <h1 class="page-title">统计分析</h1>
      <el-select v-model="selectedProfileId" placeholder="选择老人" style="width: 200px" @change="loadAllData">
        <el-option v-for="p in profiles" :key="p.id" :label="p.elderly_name" :value="p.id" />
      </el-select>
    </div>

    <div v-loading="loading">
      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value" style="color: #f56c6c">{{ overview?.counts?.feedback || 0 }}</div>
            <div class="stat-label">反馈记录总数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value" style="color: #e6a23c">{{ overview?.counts?.adjustment || 0 }}</div>
            <div class="stat-label">调试次数</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value" style="color: #67c23a">{{ overview?.average_rating || 0 }}</div>
            <div class="stat-label">平均评分</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <div class="stat-value" style="color: #409eff">{{ improvementSummary?.average_improvement || 0 }}%</div>
            <div class="stat-label">平均改善率</div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="24">
          <div class="card">
            <div class="page-header" style="border: none; margin: 0; padding: 0; margin-bottom: 16px">
              <h3 style="font-size: 16px; margin: 0">
                <el-icon color="#f56c6c" style="margin-right: 8px"><BellFilled /></el-icon>
                电池更换提醒汇总
              </h3>
              <div style="font-size: 13px; color: #909399">
                全局预警数据 · 更新于 {{ batteryWarnings?.today || '-' }}
              </div>
            </div>

            <el-row :gutter="16" style="margin-bottom: 16px">
              <el-col :span="4">
                <div class="mini-stat danger">
                  <div class="mini-stat-value">{{ batteryWarnings?.summary?.overdue_count || 0 }}</div>
                  <div class="mini-stat-label">已逾期</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat warning">
                  <div class="mini-stat-value">{{ batteryWarnings?.summary?.soon_due_count || 0 }}</div>
                  <div class="mini-stat-label">即将到期</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat abnormal">
                  <div class="mini-stat-value">{{ batteryWarnings?.summary?.abnormal_count || 0 }}</div>
                  <div class="mini-stat-label">周期异常</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat success">
                  <div class="mini-stat-value">{{ batteryWarnings?.summary?.normal_count || 0 }}</div>
                  <div class="mini-stat-label">状态正常</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat info">
                  <div class="mini-stat-value">{{ batteryWarnings?.summary?.no_data_count || 0 }}</div>
                  <div class="mini-stat-label">暂无数据</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat primary">
                  <div class="mini-stat-value">{{ batteryWarnings?.summary?.total_profiles || 0 }}</div>
                  <div class="mini-stat-label">档案总数</div>
                </div>
              </el-col>
            </el-row>

            <el-tabs v-model="batteryTab" size="small">
              <el-tab-pane label="已逾期" name="overdue">
                <el-empty
                  v-if="!batteryWarnings?.overdue?.length"
                  description="暂无已逾期档案"
                  :image-size="80"
                />
                <el-table
                  v-else
                  :data="batteryWarnings.overdue"
                  size="small"
                  stripe
                  @row-click="goToProfile"
                  style="cursor: pointer"
                >
                  <el-table-column label="老人姓名" width="120">
                    <template #default="{ row }">
                      <strong>{{ row.elderly_name }}</strong>
                    </template>
                  </el-table-column>
                  <el-table-column label="左耳状态" width="180">
                    <template #default="{ row }">
                      <span v-if="row.left_ear.status === 'overdue'">
                        <el-tag type="danger" effect="dark" size="small">
                          逾期 {{ row.left_ear.overdue_days }} 天
                        </el-tag>
                      </span>
                      <el-tag v-else size="small" :type="getEarTagType(row.left_ear.status)">
                        {{ getEarStatusLabel(row.left_ear.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="左耳最近更换" width="130">
                    <template #default="{ row }">{{ row.left_ear.last_change_date || '-' }}</template>
                  </el-table-column>
                  <el-table-column label="左耳预计更换" width="140">
                    <template #default="{ row }">
                      <span class="text-danger">{{ row.left_ear.next_expected_date || '-' }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="右耳状态" width="180">
                    <template #default="{ row }">
                      <span v-if="row.right_ear.status === 'overdue'">
                        <el-tag type="danger" effect="dark" size="small">
                          逾期 {{ row.right_ear.overdue_days }} 天
                        </el-tag>
                      </span>
                      <el-tag v-else size="small" :type="getEarTagType(row.right_ear.status)">
                        {{ getEarStatusLabel(row.right_ear.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="右耳最近更换" width="130">
                    <template #default="{ row }">{{ row.right_ear.last_change_date || '-' }}</template>
                  </el-table-column>
                  <el-table-column label="右耳预计更换" width="140">
                    <template #default="{ row }">
                      <span class="text-danger">{{ row.right_ear.next_expected_date || '-' }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="联系人/门店">
                    <template #default="{ row }">
                      <span v-if="row.contact_person || row.contact_phone">
                        {{ row.contact_person || '-' }} {{ row.contact_phone || '' }}
                      </span>
                      <span v-else-if="row.fitting_store">{{ row.fitting_store }}</span>
                      <span v-else style="color: #909399">-</span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <el-tab-pane label="即将到期" name="soon_due">
                <el-empty
                  v-if="!batteryWarnings?.soon_due?.length"
                  description="暂无即将到期档案"
                  :image-size="80"
                />
                <el-table
                  v-else
                  :data="batteryWarnings.soon_due"
                  size="small"
                  stripe
                  @row-click="goToProfile"
                  style="cursor: pointer"
                >
                  <el-table-column label="老人姓名" width="120">
                    <template #default="{ row }">
                      <strong>{{ row.elderly_name }}</strong>
                    </template>
                  </el-table-column>
                  <el-table-column label="左耳状态" width="180">
                    <template #default="{ row }">
                      <el-tag size="small" :type="getEarTagType(row.left_ear.status)">
                        {{ getEarStatusLabel(row.left_ear.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="左耳最近更换" width="130">
                    <template #default="{ row }">{{ row.left_ear.last_change_date || '-' }}</template>
                  </el-table-column>
                  <el-table-column label="左耳预计更换" width="140">
                    <template #default="{ row }">
                      <span class="text-warning">{{ row.left_ear.next_expected_date || '-' }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="右耳状态" width="180">
                    <template #default="{ row }">
                      <el-tag size="small" :type="getEarTagType(row.right_ear.status)">
                        {{ getEarStatusLabel(row.right_ear.status) }}
                      </el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="右耳最近更换" width="130">
                    <template #default="{ row }">{{ row.right_ear.last_change_date || '-' }}</template>
                  </el-table-column>
                  <el-table-column label="右耳预计更换" width="140">
                    <template #default="{ row }">
                      <span class="text-warning">{{ row.right_ear.next_expected_date || '-' }}</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="联系人/门店">
                    <template #default="{ row }">
                      <span v-if="row.contact_person || row.contact_phone">
                        {{ row.contact_person || '-' }} {{ row.contact_phone || '' }}
                      </span>
                      <span v-else-if="row.fitting_store">{{ row.fitting_store }}</span>
                      <span v-else style="color: #909399">-</span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-tab-pane>

              <el-tab-pane label="周期异常" name="abnormal">
                <el-empty
                  v-if="!batteryWarnings?.abnormal?.length"
                  description="暂无周期异常档案"
                  :image-size="80"
                />
                <div v-for="profile in batteryWarnings?.abnormal" :key="profile.profile_id" class="abnormal-card">
                  <div class="abnormal-header" @click="goToProfile(profile)">
                    <strong style="font-size: 15px">{{ profile.elderly_name }}</strong>
                    <el-tag type="warning" size="small" style="margin-left: 12px">
                      {{ profile.abnormal_cycles.length }} 条异常
                    </el-tag>
                    <el-tag
                      v-if="profile.left_ear.status !== 'normal' && profile.left_ear.status !== 'no_data'"
                      size="small"
                      :type="getEarTagType(profile.left_ear.status)"
                      style="margin-left: 8px"
                    >
                      左耳：{{ getEarStatusLabel(profile.left_ear.status) }}
                    </el-tag>
                    <el-tag
                      v-if="profile.right_ear.status !== 'normal' && profile.right_ear.status !== 'no_data'"
                      size="small"
                      :type="getEarTagType(profile.right_ear.status)"
                      style="margin-left: 8px"
                    >
                      右耳：{{ getEarStatusLabel(profile.right_ear.status) }}
                    </el-tag>
                  </div>
                  <el-table :data="profile.abnormal_cycles" size="small" style="margin-top: 8px">
                    <el-table-column prop="change_date" label="更换日期" width="140" />
                    <el-table-column label="耳朵" width="100">
                      <template #default="{ row }">
                        <el-tag :type="getAbnormalEar(profile, row.id)" size="small">
                          {{ getAbnormalEar(profile, row.id) }}
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="usage_days" label="使用天数" width="100">
                      <template #default="{ row }">
                        <span class="text-warning">{{ row.usage_days }} 天</span>
                      </template>
                    </el-table-column>
                    <el-table-column prop="reason" label="异常原因" />
                  </el-table>
                </div>
              </el-tab-pane>
            </el-tabs>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-bottom: 20px">
        <el-col :span="24">
          <div class="card">
            <div class="page-header" style="border: none; margin: 0; padding: 0; margin-bottom: 16px">
              <h3 style="font-size: 16px; margin: 0">
                <el-icon color="#409eff" style="margin-right: 8px"><Tickets /></el-icon>
                协作任务统计
              </h3>
              <el-button type="primary" size="small" @click="goToTaskCenter">
                <el-icon><ArrowRight /></el-icon>
                前往任务中心
              </el-button>
            </div>

            <el-row :gutter="16" style="margin-bottom: 16px">
              <el-col :span="4">
                <div class="mini-stat primary">
                  <div class="mini-stat-value">{{ taskSummary?.total || 0 }}</div>
                  <div class="mini-stat-label">任务总数</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat success">
                  <div class="mini-stat-value">{{ taskSummary?.completion_rate || 0 }}%</div>
                  <div class="mini-stat-label">完成率</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat danger">
                  <div class="mini-stat-value">{{ taskSummary?.overdue || 0 }}</div>
                  <div class="mini-stat-label">逾期任务</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat warning">
                  <div class="mini-stat-value">{{ taskSummary?.soon_due || 0 }}</div>
                  <div class="mini-stat-label">即将到期</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat info">
                  <div class="mini-stat-value">{{ taskSummary?.pending || 0 }}</div>
                  <div class="mini-stat-label">待处理</div>
                </div>
              </el-col>
              <el-col :span="4">
                <div class="mini-stat abnormal">
                  <div class="mini-stat-value">{{ taskSummary?.in_progress || 0 }}</div>
                  <div class="mini-stat-label">进行中</div>
                </div>
              </el-col>
            </el-row>

            <el-row :gutter="20">
              <el-col :span="12">
                <h4 style="margin-bottom: 12px; font-size: 14px; color: #606266">各类型任务分布</h4>
                <v-chart style="width: 100%; height: 280px" :option="taskTypeChartOption" autoresize />
              </el-col>
              <el-col :span="12">
                <h4 style="margin-bottom: 12px; font-size: 14px; color: #606266">每位老人待办数量（Top 10</h4>
                <v-chart style="width: 100%; height: 280px" :option="taskByProfileChartOption" autoresize />
              </el-col>
            </el-row>

            <el-row :gutter="20" style="margin-top: 16px" v-if="taskByProfile.length > 0">
              <el-col :span="24">
                <h4 style="margin-bottom: 12px; font-size: 14px; color: #606266">老人任务详情一览</h4>
                <el-table :data="taskByProfile" size="small" stripe>
                  <el-table-column label="老人姓名" width="120">
                    <template #default="{ row }">
                      <strong>{{ row.elderly_name }}</strong>
                    </template>
                  </el-table-column>
                  <el-table-column label="任务总数" width="100" align="center">
                    <template #default="{ row }">
                      <el-tag type="primary" size="small">{{ row.total }}</el-tag>
                    </template>
                  </el-table-column>
                  <el-table-column label="待处理" width="100" align="center">
                    <template #default="{ row }">
                      <el-tag v-if="row.pending > 0" type="info" size="small">{{ row.pending }}</el-tag>
                      <span v-else style="color: #909399">-</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="进行中" width="100" align="center">
                    <template #default="{ row }">
                      <el-tag v-if="row.in_progress > 0" type="primary" size="small">{{ row.in_progress }}</el-tag>
                      <span v-else style="color: #909399">-</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="已完成" width="100" align="center">
                    <template #default="{ row }">
                      <el-tag v-if="row.completed > 0" type="success" size="small">{{ row.completed }}</el-tag>
                      <span v-else style="color: #909399">-</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="已逾期" width="100" align="center">
                    <template #default="{ row }">
                      <el-tag v-if="row.overdue > 0" type="danger" effect="dark" size="small">{{ row.overdue }}</el-tag>
                      <span v-else style="color: #909399">-</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="即将到期" width="100" align="center">
                    <template #default="{ row }">
                      <el-tag v-if="row.soon_due > 0" type="warning" size="small">{{ row.soon_due }}</el-tag>
                      <span v-else style="color: #909399">-</span>
                    </template>
                  </el-table-column>
                </el-table>
              </el-col>
            </el-row>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <div class="card">
            <h3 style="margin-bottom: 16px; font-size: 16px">
              <el-icon color="#f56c6c" style="margin-right: 8px"><Warning /></el-icon>
              高频不适场景
            </h3>
            <v-chart class="chart-container" :option="discomfortChartOption" autoresize />
          </div>
        </el-col>
        <el-col :span="12">
          <div class="card">
            <h3 style="margin-bottom: 16px; font-size: 16px">
              <el-icon color="#409eff" style="margin-right: 8px"><Bottom /></el-icon>
              左右耳差异反馈
            </h3>
            <v-chart class="chart-container" :option="earDiffChartOption" autoresize />
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="12">
          <div class="card">
            <h3 style="margin-bottom: 16px; font-size: 16px">
              <el-icon color="#67c23a" style="margin-right: 8px"><Clock /></el-icon>
              电池更换周期
            </h3>
            <v-chart class="chart-container" :option="batteryChartOption" autoresize />
            <div style="margin-top: 16px">
              <el-descriptions :column="2" size="small" border>
                <el-descriptions-item label="左耳平均使用">
                  <span style="font-weight: 600; color: #409eff">{{ batteryLeftStats?.avg || 0 }} 天</span>
                </el-descriptions-item>
                <el-descriptions-item label="右耳平均使用">
                  <span style="font-weight: 600; color: #9c27b0">{{ batteryRightStats?.avg || 0 }} 天</span>
                </el-descriptions-item>
                <el-descriptions-item label="左耳趋势">
                  <el-tag :type="getTrendTagType(batteryLeftStats?.trend)" size="small">
                    {{ getTrendLabel(batteryLeftStats?.trend) }}
                  </el-tag>
                </el-descriptions-item>
                <el-descriptions-item label="右耳趋势">
                  <el-tag :type="getTrendTagType(batteryRightStats?.trend)" size="small">
                    {{ getTrendLabel(batteryRightStats?.trend) }}
                  </el-tag>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-col>
        <el-col :span="12">
          <div class="card">
            <h3 style="margin-bottom: 16px; font-size: 16px">
              <el-icon color="#e6a23c" style="margin-right: 8px"><TrendCharts /></el-icon>
              调试后改善比例
            </h3>
            <v-chart class="chart-container" :option="improvementChartOption" autoresize />
            <div style="margin-top: 16px">
              <el-descriptions :column="3" size="small" border>
                <el-descriptions-item label="改善">
                  <span style="color: #67c23a; font-weight: 600">{{ improvementSummary?.improved_count || 0 }} 次</span>
                </el-descriptions-item>
                <el-descriptions-item label="稳定">
                  <span style="color: #909399; font-weight: 600">{{ improvementSummary?.stable_count || 0 }} 次</span>
                </el-descriptions-item>
                <el-descriptions-item label="下降">
                  <span style="color: #f56c6c; font-weight: 600">{{ improvementSummary?.declined_count || 0 }} 次</span>
                </el-descriptions-item>
              </el-descriptions>
            </div>
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px">
        <el-col :span="24">
          <div class="card">
            <h3 style="margin-bottom: 16px; font-size: 16px">
              <el-icon color="#409eff" style="margin-right: 8px"><DataLine /></el-icon>
              评分趋势（近90天）
            </h3>
            <div style="margin-bottom: 16px">
              <el-radio-group v-model="trendDays" size="small" @change="loadTrends">
                <el-radio-button :value="30">近30天</el-radio-button>
                <el-radio-button :value="60">近60天</el-radio-button>
                <el-radio-button :value="90">近90天</el-radio-button>
              </el-radio-group>
            </div>
            <v-chart style="width: 100%; height: 300px" :option="trendChartOption" autoresize />
          </div>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px" v-if="discomfortScenarios.length > 0">
        <el-col :span="24">
          <div class="card">
            <h3 style="margin-bottom: 16px; font-size: 16px">
              <el-icon color="#f56c6c" style="margin-right: 8px"><WarningFilled /></el-icon>
              场景问题详细分析
            </h3>
            <el-table :data="discomfortScenarios">
              <el-table-column prop="scenario" label="场景" width="120">
                <template #default="{ row }">
                  <el-tag type="warning" size="small">{{ row.scenario }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="total" label="反馈次数" width="100" align="center" />
              <el-table-column label="听力不佳" width="100" align="center">
                <template #default="{ row }">
                  <el-tag v-if="row.poor_hearing > 0" type="danger" size="small">{{ row.poor_hearing }}</el-tag>
                  <span v-else style="color: #909399">-</span>
                </template>
              </el-table-column>
              <el-table-column label="啸叫问题" width="100" align="center">
                <template #default="{ row }">
                  <el-tag v-if="row.howling > 0" type="danger" size="small">{{ row.howling }}</el-tag>
                  <span v-else style="color: #909399">-</span>
                </template>
              </el-table-column>
              <el-table-column label="不适反应" width="100" align="center">
                <template #default="{ row }">
                  <el-tag v-if="row.discomfort > 0" type="warning" size="small">{{ row.discomfort }}</el-tag>
                  <span v-else style="color: #909399">-</span>
                </template>
              </el-table-column>
              <el-table-column label="平均评分" width="120" align="center">
                <template #default="{ row }">
                  <el-rate v-model="row.avg_rating" disabled size="small" />
                </template>
              </el-table-column>
              <el-table-column label="问题总数" width="100" align="center">
                <template #default="{ row }">
                  <el-tag :type="row.issue_count > 2 ? 'danger' : 'warning'" size="small">
                    {{ row.issue_count }}
                  </el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Warning,
  Bottom,
  Clock,
  TrendCharts,
  DataLine,
  WarningFilled,
  BellFilled,
  ArrowRight
} from '@element-plus/icons-vue'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, PieChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent
} from 'echarts/components'
import { profileApi, statisticsApi } from '@/api'
import type { Profile, BatteryWarnings, BatteryWarningProfile, TaskOverview } from '@/types'

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  PieChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DatasetComponent
])

const router = useRouter()
const loading = ref(false)
const profiles = ref<Profile[]>([])
const selectedProfileId = ref<number>()
const trendDays = ref(90)
const batteryTab = ref('overdue')

const overview = ref<any>()
const discomfortScenarios = ref<any[]>([])
const earDifference = ref<any>()
const batteryCycle = ref<any>()
const improvementRate = ref<any>()
const trends = ref<any[]>([])
const batteryWarnings = ref<BatteryWarnings>()
const taskOverview = ref<TaskOverview>()

const improvementSummary = computed(() => improvementRate.value?.summary || {})
const batteryLeftStats = computed(() => batteryCycle.value?.left_ear?.stats || {})
const batteryRightStats = computed(() => batteryCycle.value?.right_ear?.stats || {})
const taskSummary = computed(() => taskOverview.value?.summary || {
  total: 0,
  completed: 0,
  pending: 0,
  in_progress: 0,
  cancelled: 0,
  overdue: 0,
  soon_due: 0,
  completion_rate: 0
})
const taskTypeDistribution = computed(() => taskOverview.value?.type_distribution || [])
const taskByProfile = computed(() => taskOverview.value?.by_profile || [])

const discomfortChartOption = computed(() => {
  const data = discomfortScenarios.value.slice(0, 7)
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['听力不佳', '啸叫问题', '不适反应']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map(d => d.scenario)
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [
      {
        name: '听力不佳',
        type: 'bar',
        stack: 'total',
        data: data.map(d => d.poor_hearing),
        itemStyle: { color: '#f56c6c' }
      },
      {
        name: '啸叫问题',
        type: 'bar',
        stack: 'total',
        data: data.map(d => d.howling),
        itemStyle: { color: '#e6a23c' }
      },
      {
        name: '不适反应',
        type: 'bar',
        stack: 'total',
        data: data.map(d => d.discomfort),
        itemStyle: { color: '#f7ba2a' }
      }
    ]
  }
})

const earDiffChartOption = computed(() => {
  const data = earDifference.value?.by_scenario || []
  return {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['左耳评分', '右耳评分']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.map((d: any) => d.scenario)
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 5,
      minInterval: 1
    },
    series: [
      {
        name: '左耳评分',
        type: 'bar',
        data: data.map((d: any) => d.left_avg),
        itemStyle: { color: '#409eff' },
        barWidth: '30%'
      },
      {
        name: '右耳评分',
        type: 'bar',
        data: data.map((d: any) => d.right_avg),
        itemStyle: { color: '#9c27b0' },
        barWidth: '30%'
      }
    ]
  }
})

const batteryChartOption = computed(() => {
  const leftRecords = batteryCycle.value?.left_ear?.records || []
  const rightRecords = batteryCycle.value?.right_ear?.records || []

  const allDates = Array.from(new Set([
    ...leftRecords.map((r: any) => r.date),
    ...rightRecords.map((r: any) => r.date)
  ])).sort()

  const leftData = allDates.map(date => {
    const r = leftRecords.find((rec: any) => rec.date === date)
    return r ? r.usage_days : null
  })
  const rightData = allDates.map(date => {
    const r = rightRecords.find((rec: any) => rec.date === date)
    return r ? r.usage_days : null
  })

  return {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['左耳使用天数', '右耳使用天数']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: allDates.map(d => d.substring(5))
    },
    yAxis: {
      type: 'value',
      name: '天数'
    },
    series: [
      {
        name: '左耳使用天数',
        type: 'line',
        data: leftData,
        smooth: true,
        itemStyle: { color: '#409eff' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64, 158, 255, 0.4)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
            ]
          }
        }
      },
      {
        name: '右耳使用天数',
        type: 'line',
        data: rightData,
        smooth: true,
        itemStyle: { color: '#9c27b0' },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(156, 39, 176, 0.4)' },
              { offset: 1, color: 'rgba(156, 39, 176, 0.05)' }
            ]
          }
        }
      }
    ]
  }
})

const improvementChartOption = computed(() => {
  const summary = improvementSummary.value
  const data = [
    { value: summary?.improved_count || 0, name: '改善', itemStyle: { color: '#67c23a' } },
    { value: summary?.stable_count || 0, name: '稳定', itemStyle: { color: '#909399' } },
    { value: summary?.declined_count || 0, name: '下降', itemStyle: { color: '#f56c6c' } }
  ]
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%'
        },
        data: data
      }
    ]
  }
})

const trendChartOption = computed(() => {
  const data = trends.value
  return {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['总体评分', '左耳评分', '右耳评分']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: data.map(d => d.date.substring(5))
    },
    yAxis: {
      type: 'value',
      min: 0,
      max: 5
    },
    series: [
      {
        name: '总体评分',
        type: 'line',
        data: data.map(d => d.avg_rating || null),
        smooth: true,
        itemStyle: { color: '#f7ba2a' },
        lineStyle: { width: 3 }
      },
      {
        name: '左耳评分',
        type: 'line',
        data: data.map(d => d.avg_left || null),
        smooth: true,
        itemStyle: { color: '#409eff' }
      },
      {
        name: '右耳评分',
        type: 'line',
        data: data.map(d => d.avg_right || null),
        smooth: true,
        itemStyle: { color: '#9c27b0' }
      }
    ]
  }
})

const taskTypeChartOption = computed(() => {
  const data = taskTypeDistribution.value.map(d => ({
    value: d.count,
    name: d.type,
    percentage: d.percentage
  }))
  const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#9c27b0', '#909399']
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}次 ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    color: colors,
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%'
        },
        data: data
      }
    ]
  }
})

const taskByProfileChartOption = computed(() => {
  const data = taskByProfile.value.slice(0, 10)
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' }
    },
    legend: {
      data: ['待处理', '进行中', '已逾期', '即将到期']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value',
      minInterval: 1
    },
    yAxis: {
      type: 'category',
      data: data.map(d => d.elderly_name)
    },
    series: [
      {
        name: '待处理',
        type: 'bar',
        stack: 'total',
        data: data.map(d => d.pending),
        itemStyle: { color: '#909399' }
      },
      {
        name: '进行中',
        type: 'bar',
        stack: 'total',
        data: data.map(d => d.in_progress),
        itemStyle: { color: '#409eff' }
      },
      {
        name: '即将到期',
        type: 'bar',
        stack: 'total',
        data: data.map(d => d.soon_due),
        itemStyle: { color: '#e6a23c' }
      },
      {
        name: '已逾期',
        type: 'bar',
        stack: 'total',
        data: data.map(d => d.overdue),
        itemStyle: { color: '#f56c6c' }
      }
    ]
  }
})

const getTrendTagType = (trend?: string) => {
  if (trend === 'improving') return 'success'
  if (trend === 'declining') return 'danger'
  return 'info'
}

const getTrendLabel = (trend?: string) => {
  if (trend === 'improving') return '续航提升'
  if (trend === 'declining') return '续航下降'
  return '稳定'
}

const getEarTagType = (status: string) => {
  if (status === 'overdue') return 'danger'
  if (status === 'soon_due') return 'warning'
  if (status === 'normal') return 'success'
  return 'info'
}

const getEarStatusLabel = (status: string) => {
  if (status === 'overdue') return '已逾期'
  if (status === 'soon_due') return '即将到期'
  if (status === 'normal') return '正常'
  return '暂无数据'
}

const getAbnormalEar = (profile: BatteryWarningProfile, recordId: number) => {
  if (profile.left_ear.abnormal_cycles.some(a => a.id === recordId)) return '左耳'
  if (profile.right_ear.abnormal_cycles.some(a => a.id === recordId)) return '右耳'
  return ''
}

const goToProfile = (row: BatteryWarningProfile) => {
  router.push(`/profile/${row.profile_id}`)
}

const loadProfiles = async () => {
  try {
    const res = await profileApi.getAll()
    profiles.value = res.data
    if (res.data.length > 0 && !selectedProfileId.value) {
      selectedProfileId.value = res.data[0].id
      loadAllData()
    }
  } catch (e) {
    ElMessage.error('加载老人列表失败')
  }
}

const loadBatteryWarnings = async () => {
  try {
    const res = await statisticsApi.getBatteryWarnings()
    batteryWarnings.value = res.data
  } catch (e) {
    // non-critical, fail silently
  }
}

const loadTaskOverview = async () => {
  try {
    const res = await statisticsApi.getTaskOverview()
    taskOverview.value = res.data
  } catch (e) {
    // non-critical, fail silently
  }
}

const goToTaskCenter = () => {
  router.push('/tasks')
}

const loadAllData = async () => {
  if (!selectedProfileId.value) return
  loading.value = true
  try {
    const [o, d, e, b, i] = await Promise.all([
      statisticsApi.getOverview(selectedProfileId.value),
      statisticsApi.getDiscomfortScenarios(selectedProfileId.value),
      statisticsApi.getEarDifference(selectedProfileId.value),
      statisticsApi.getBatteryCycle(selectedProfileId.value),
      statisticsApi.getImprovementRate(selectedProfileId.value)
    ])
    overview.value = o.data
    discomfortScenarios.value = d.data
    earDifference.value = e.data
    batteryCycle.value = b.data
    improvementRate.value = i.data
    loadTrends()
  } catch (e) {
    ElMessage.error('加载统计数据失败')
  } finally {
    loading.value = false
  }
}

const loadTrends = async () => {
  if (!selectedProfileId.value) return
  try {
    const res = await statisticsApi.getTrends(selectedProfileId.value, trendDays.value)
    trends.value = res.data
  } catch (e) {
    ElMessage.error('加载趋势数据失败')
  }
}

onMounted(() => {
  loadProfiles()
  loadBatteryWarnings()
  loadTaskOverview()
})
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
.mini-stat {
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  color: #fff;
}
.mini-stat.danger { background: linear-gradient(135deg, #f56c6c, #f78989); }
.mini-stat.warning { background: linear-gradient(135deg, #e6a23c, #f0c78a); }
.mini-stat.abnormal { background: linear-gradient(135deg, #f7ba2a, #fad87a); }
.mini-stat.success { background: linear-gradient(135deg, #67c23a, #95d475); }
.mini-stat.info { background: linear-gradient(135deg, #909399, #b1b3b8); }
.mini-stat.primary { background: linear-gradient(135deg, #409eff, #79bbff); }
.mini-stat-value {
  font-size: 28px;
  font-weight: 700;
  line-height: 1.2;
}
.mini-stat-label {
  font-size: 13px;
  margin-top: 4px;
  opacity: 0.95;
}
.abnormal-card {
  padding: 12px;
  margin-bottom: 12px;
  background: #fdf6ec;
  border: 1px solid #faecd8;
  border-radius: 6px;
}
.abnormal-header {
  cursor: pointer;
  display: flex;
  align-items: center;
}
</style>
