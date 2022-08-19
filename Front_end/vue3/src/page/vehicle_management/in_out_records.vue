<template>
  <div class="ordering">
    <div class="heading">
        <div>出入记录</div>
        <div class="block">
          <span class="demonstration">选择时间段</span>
          <el-date-picker
            v-model="value1"
            type="datetimerange"
            :shortcuts="shortcuts"
            range-separator="To"
            start-placeholder="Start date"
            end-placeholder="End date"
          />
        </div>
    </div>
    <div class="table">
      <el-table :data="filterTableData" height=700px style="width: 100%">
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

const date = new Date()

const value1 = ref([
  new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0),
  new Date(),
])

//得到停车时长
function getDuration(strDate1:string, strDate2:string){
  const date1 = Date.parse(strDate1);
  const date2 = Date.parse(strDate2);
  const hours = Math.floor((date2-date1)/(60*60*1000))
  const minutes = Math.floor(((date2-date1)/(60*60*1000) - hours) * 60)
  const seconds = Math.floor((((date2-date1)/(60*60*1000) - hours) * 60 - minutes) * 60)
  return(hours + " 时 " + minutes + " 分 " + seconds + " 秒")
}

const tableData: Car[] = [
  {
    in_time: '2022-01-01 01:00:00',
    out_time: '2022-03-05 13:45:45',
    license_plate: '京A88888',
    city: '北京',
    vehicle_model: '蓝牌',
    duration: getDuration("2022-01-01 01:00:00", '2022-03-05 13:45:45')
  },
  {
    in_time: '2022-02-02 02:02:34',
    out_time: '2022-03-05 13:45:56',
    license_plate: '津A666666',
    city: '天津',
    vehicle_model: '绿牌',
    duration: getDuration('2022-02-02 02:02:34', '2022-03-05 13:45:56')
  },
  {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
  {
    in_time: '2022-08-08 08:08:08',
    out_time: '2022-09-05 13:45:09',
    license_plate: '冀A74397',
    city: '石家庄',
    vehicle_model: '黄牌',
    duration: getDuration('2022-08-08 08:08:08', '2022-09-05 13:45:09')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },{
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },
    {
    in_time: '2022-03-03 03:03:03',
    out_time: '2022-03-05 13:45:45',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: getDuration('2022-03-03 03:03:03', '2022-03-05 13:45:45')
  },


]
const shortcuts = [
  {
    text: '过去一周',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
      return [start, end]
    },
  },
  {
    text: '过去一个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
      return [start, end]
    },
  },
  {
    text: '过去三个月',
    value: () => {
      const end = new Date()
      const start = new Date()
      start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
      return [start, end]
    },
  },
]

</script>


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