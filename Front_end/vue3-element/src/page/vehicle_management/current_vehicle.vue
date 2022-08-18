<template>
  <div class="ordering">
    <div class="heading">当前车辆</div>
    <div>
      <el-table :data="filterTableData" height="100%" style="width: 100%">
        <el-table-column prop="in_time" label="入场时间" sortable width="180" />
        <el-table-column prop="license_plate" label="车牌号码" width="180" />
        <el-table-column prop="vehicle_model" label="车型" width="180" />
        <el-table-column prop="province" label="省份" width="180" />
        <el-table-column prop="duration" label="停车时长" sortable width="180" />

        <el-table-column align="right" width="180">
          <template #header>
            <el-input v-model="search" size="small" placeholder="Type to search" />
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

<script>
import {reactive, ref, computed} from 'vue'
export default {
  setup(){
    const search = ref('')
    const filterTableData = computed(() =>
      tableData.filter(
        (data) =>
          !search.value ||
          data.name.toLowerCase().includes(search.value.toLowerCase())
      )
    )
    const tableData = reactive([
      {
        in_time:'2022-08-18-20:01',
        license_plate:'京A88888',
        vehicle_model:'蓝牌车',
        province:'北京',
        duration:'23min',
      },
      {
        in_time:'2022-08-18-17:01',
        license_plate:'津A888888',
        vehicle_model:'绿牌车',
        province:'天津',
        duration:'5h 3min',
      },
      {
        in_time:'2022-08-18-15:01',
        license_plate:'皖A888888',
        vehicle_model:'绿牌车',
        province:'安徽',
        duration:'1h 3min',
      }
    ])


    return{filterTableData, tableData}
  }
}
</script>

<style scoped>

</style>