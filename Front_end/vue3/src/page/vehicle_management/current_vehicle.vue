<template>
  <div class="ordering">
    <div class="heading">
      <div>当前车辆</div>
    </div>
    <div>
      <el-table :data="filterTableData" height="100%" style="width: 100%">
        <el-table-column prop="in_time" label="入场时间" sortable min-width="100" />
        <el-table-column prop="license_plate" label="车牌号码" min-width="100" />
        <el-table-column prop="city" label="地级市" min-width="100" />
        <el-table-column prop="vehicle_model" label="车型" min-width="100" />
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
  license_plate: string
  city:string
  vehicle_model: string
  duration:string
}

//时间相减
// function get_duration(time: string){
//   const t = new Date(time);
//   const date = new Date();
//   console.log(t);
//   console.log(date - t)
// }
//
// get_duration('2022-01-01 00:00')

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

// 将字符串转换为时间

const tableData: Car[] = [
  {
    in_time: '2022-01-01 00:00',
    license_plate: '京A88888',
    city: '北京',
    vehicle_model: '蓝牌',
    duration: '9999 h 59 min'
  },
  {
    in_time: '2022-02-02 02:02',
    license_plate: '津A666666',
    city: '天津',
    vehicle_model: '绿牌',
    duration: '6666 h 46 min'
  },
  {
    in_time: '2022-03-03 03:03',
    license_plate: '皖H12345警',
    city: '安庆',
    vehicle_model: '白牌',
    duration: '7777 h 37 min'
  },
  {
    in_time: '2022-08-08 08:08',
    license_plate: '冀A74397',
    city: '石家庄',
    vehicle_model: '黄牌',
    duration: '0 h 35 min'
  },
]
</script>


<style scoped>

</style>