<template>
  <div class="ordering">
    <div class="heading">
        <div>出入记录</div>
        <div class="block">
          <span class="demonstration">选择时间段</span>
          <el-date-picker
            v-model="value1"
            type="datetimerange"
            range-separator="To"
            start-placeholder="Start date"
            end-placeholder="End date"
          />
        </div>
    </div>
    <div class="table">
      <el-table :data="filterTableData" height="100%" style="width: 100%">
        <el-table-column prop="license_plate" label="车牌号码" min-width="100" />
        <el-table-column prop="city" label="地级市" min-width="100" />
        <el-table-column prop="vehicle_model" label="车型" min-width="100" />
        <el-table-column prop="in_time" label="入场时间" sortable min-width="100" />
        <el-table-column prop="out_time" label="出场时间" sortable min-width="100" />
        <el-table-column prop="duration" label="停车时长" sortable min-width="100" />

        <el-table-column align="right" width="180">
          <template #header>
            <el-input v-model="search" size="small" placeholder="输入关键字搜索车牌" />
          </template>
          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
              >Edit</el-button
            >
            <el-button
              size="small"
              type="danger"
              @click="handleDelete(scope.$index, scope.row)"
              >Delete</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { computed, ref } from 'vue'

interface Car {
  in_time: string
  out_time: string
  license_plate: string
  city:string
  vehicle_model: string
  duration:string
}

const search = ref('')
const filterTableData = computed(() =>
  tableData.filter(
    (data) =>
      !search.value ||
      data.license_plate.toLowerCase().includes(search.value.toLowerCase())
  )
)
const handleEdit = (index: number, row: Car) => {
  console.log(index, row)
}
const handleDelete = (index: number, row: Car) => {
  console.log(index, row)
}

const value1 = ref([
  new Date(2000, 10, 10, 10, 10),
  new Date(2000, 10, 11, 10, 10),
])

const tableData: Car[] = [
  {
    in_time: '2022-01-01 00:00',
    out_time: '2022-03-05 13:45',
    license_plate: '京A88888',
    city: '北京',
    vehicle_model: '蓝牌',
    duration: '9999 h 13 min'
  },
  {
    in_time: '2022-02-02-02:02',
    out_time: '2022-03-05 13:45',
    license_plate: '津A666666',
    city: '天津',
    vehicle_model: '绿牌',
    duration: '6666 h 34 min'
  },
  {
    in_time: '2022-03-03-03:03',
    out_time: '2022-03-05 13:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: '7777 h 12 min'
  },
  {
    in_time: '2022-08-08-08:08',
    out_time: '2022-09-05 13:45',
    license_plate: '冀A74397',
    city: '石家庄',
    vehicle_model: '黄牌',
    duration: '0 h 35 min'
  },
]
</script>

<!--<script>-->
<!--import {reactive, ref, computed} from 'vue'-->
<!--export default {-->
<!--  setup(){-->
<!--    const search = ref('')-->
<!--    const filterTableData = computed(() =>-->
<!--      tableData.filter(-->
<!--        (data) =>-->
<!--          !search.value ||-->
<!--          data.name.toLowerCase().includes(search.value.toLowerCase())-->
<!--      )-->
<!--    )-->
<!--    const tableData = reactive([-->
<!--      {-->
<!--        in_time:'2022-08-18-20:01',-->
<!--        license_plate:'京A88888',-->
<!--        vehicle_model:'蓝牌车',-->
<!--        province:'北京',-->
<!--        duration:'23min',-->
<!--      },-->
<!--      {-->
<!--        in_time:'2022-08-18-17:01',-->
<!--        license_plate:'津A888888',-->
<!--        vehicle_model:'绿牌车',-->
<!--        province:'天津',-->
<!--        duration:'5h 3min',-->
<!--      },-->
<!--      {-->
<!--        in_time:'2022-08-18-15:01',-->
<!--        license_plate:'皖A888888',-->
<!--        vehicle_model:'绿牌车',-->
<!--        province:'安徽',-->
<!--        duration:'1h 3min',-->
<!--      }-->
<!--    ])-->


<!--    return{filterTableData, tableData}-->
<!--  }-->
<!--}-->
<!--</script>-->

<style scoped>
.block {
  padding: 0 30px;
  text-align: center;
  border-right: solid 1px var(--el-border-color);
  flex: 1;
}
.block:last-child {
  border-right: none;
}
.block .demonstration {
  display: block;
  color: var(--el-text-color-secondary);
  font-size: 14px;
  margin-bottom: 20px;
}
</style>