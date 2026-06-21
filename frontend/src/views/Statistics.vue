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
import { ref, computed, onMounted, h } from 'vue'
import { ElMessage } from 'element-plus'
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
import type { Profile } from '@/types'

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

const loading = ref(false)
const profiles = ref<Profile[]>([])
const selectedProfileId = ref<number>()
const trendDays = ref(90)

const overview = ref<any>()
const discomfortScenarios = ref<any[]>([])
const earDifference = ref<any>()
const batteryCycle = ref<any>()
const improvementRate = ref<any>()
const trends = ref<any[]>([])

const improvementSummary = computed(() => improvementRate.value?.summary || {})
const batteryLeftStats = computed(() => batteryCycle.value?.left_ear?.stats || {})
const batteryRightStats = computed(() => batteryCycle.value?.right_ear?.stats || {})

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

onMounted(loadProfiles)
</script>
