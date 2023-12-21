<template>
  <div class="ordering">
    <div class="heading">
        <div>出入记录</div>
        <div class="block">
<!--          <span class="demonstration">选择时间段</span>-->
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
      <el-table :data="cars" height=700px style="width: 100%">
        <el-table-column prop="id" label="编号" sortable min-width="70" />
        <el-table-column prop="license_plate" label="车牌号码" min-width="100" />
        <el-table-column prop="province" label="省份" min-width="100" />
        <el-table-column prop="city" label="地级市" min-width="100" />
        <el-table-column prop="vehicle_model" label="车型" min-width="70" />
        <el-table-column prop="in_time" label="入场时间" sortable min-width="100" />
        <el-table-column prop="out_time" label="出场时间" sortable min-width="100" />
        <el-table-column prop="duration" label="停车时长" sortable min-width="100" />

        <el-table-column align="right" width="180">
          <template #header>
           <div>
              <el-button text @click="add_dialog_visible = true"
                    >添加车辆</el-button
                  >

                  <el-dialog
                    v-model="add_dialog_visible"
                    title="添加车辆"
                    width="30%"
                    :before-close="handleClose"
                    center
                    :append-to-body='true'
                  >
                    <el-form
                      ref="ruleFormRef"
                      :model="car_form"
                      status-icon
                      label-width="120px"
                      class="demo-ruleForm"
                    >
<!--                      <el-form-item label="编号" prop="id">-->
<!--                        <el-input v-model="car_form.id" autocomplete="off"/>-->
<!--                      </el-form-item>-->
                      <el-form-item label="车牌号码" prop="license_plate">
                        <el-input v-model="car_form.license_plate" autocomplete="off"/>
                      </el-form-item>
<!--                      <el-form-item label="省份" prop="province">-->
<!--                        <el-input v-model="car_form.province" autocomplete="off"/>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="地级市" prop="city">-->
<!--                        <el-input v-model="car_form.city" autocomplete="off"/>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="车型" prop="vehicle_model">-->
<!--                        <el-input v-model="car_form.vehicle_model" autocomplete="off"/>-->
<!--                      </el-form-item>-->
                      <el-form-item label="入场时间" prop="in_time">
                        <el-input v-model="car_form.in_time" autocomplete="off"/>
                      </el-form-item>
                      <el-form-item label="出场时间" prop="out_time">
                        <el-input v-model="car_form.out_time" autocomplete="off"/>
                      </el-form-item>
<!--                      <el-form-item label="停车时长" prop="duration">-->
<!--                        <el-input v-model="car_form.duration" autocomplete="off"/>-->
<!--                      </el-form-item>-->
                      <el-form-item>
                        <el-button type="primary" @click="submitForm(ruleFormRef)">提交</el-button>
                        <el-button @click="resetForm(ruleFormRef)">重置</el-button>
                      </el-form-item>
                    </el-form>

                  </el-dialog>
            </div>
          </template>

          <template #default="scope">
            <el-button size="small" @click="handleEdit(scope.$index, scope.row)"
              >Edit</el-button
            >
                  <el-dialog
                    v-model="edit_dialog_visible"
                    title="编辑车辆"
                    width="30%"
                    :before-close="handleClose"
                    center
                    :append-to-body='true'
                  >
                    <el-form
                      ref="editFormRef"
                      :model="car_form"
                      status-icon
                      label-width="120px"
                      class="demo-ruleForm"
                    >
                      <el-form-item label="编号" prop="id">
                        <el-input v-model="car_form.id" autocomplete="off"/>
                      </el-form-item>
                      <el-form-item label="车牌号码" prop="license_plate">
                        <el-input v-model="car_form.license_plate" autocomplete="off"/>
                      </el-form-item>
<!--                      <el-form-item label="省份" prop="province">-->
<!--                        <el-input v-model="car_form.province" autocomplete="off"/>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="地级市" prop="city">-->
<!--                        <el-input v-model="car_form.city" autocomplete="off"/>-->
<!--                      </el-form-item>-->
<!--                      <el-form-item label="车型" prop="vehicle_model">-->
<!--                        <el-input v-model="car_form.vehicle_model" autocomplete="off"/>-->
<!--                      </el-form-item>-->
                      <el-form-item label="入场时间" prop="in_time">
                        <el-input v-model="car_form.in_time" autocomplete="off"/>
                      </el-form-item>
                      <el-form-item label="出场时间" prop="out_time">
                        <el-input v-model="car_form.out_time" autocomplete="off"/>
                      </el-form-item>
                      <el-form-item>
                        <el-button type="primary" @click="editSubmitForm(editFormRef)">编辑提交</el-button>
                        <el-button @click="resetForm(editFormRef)">重置</el-button>
                      </el-form-item>
                    </el-form>
                  </el-dialog>
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

<script setup>
import { computed, ref, onMounted, reactive} from 'vue'
import axios from "axios";
import {ElMessageBox} from "element-plus";

const cars = reactive([])

const getCars = ()=>{
    axios.get("http://localhost:5000/cars/",).then(res => {
    cars.splice(0, cars.length)
    cars.push(...res.data.results)
    console.log('更新数据')
  })
}
onMounted(()=>{
  getCars()
})


const search = ref('')
// const filterTableData = computed(() =>
//   tableData.filter(
//     (data) =>
//       !search.value ||
//       data.license_plate.toLowerCase().includes(search.value.toLowerCase())
//   )
// )

const handleDelete = (index, scope) => {
  console.log(index, scope)
  axios.delete('http://127.0.0.1:5000/cars/' + scope.id).then(()=>{
    getCars()
  })
}

const add_dialog_visible = ref(false)
const ruleFormRef = ref()
const car_form = reactive({
  license_plate: "",
  province: "",
  city: "",
  vehicle_model: "",
  in_time: "",
  out_time: "",
  duration: "",
})
//表单提交事件
const submitForm = (formEl) => {
  axios.post('http://localhost:5000/cars', car_form).then(()=>{
    add_dialog_visible.value = false
    formEl.resetFields()
    getCars()
  })
}
//重置表单
const resetForm = (formEl) => {
  formEl.resetFields()
}

//关闭弹窗前确认
const handleClose = (done) => {
  ElMessageBox.confirm('确认关闭?')
    .then(() => {
      done()
    })
    .catch(() => {
      // catch error
    })
}

// 编辑表单
const editFormRef = ref()
const edit_dialog_visible = ref(false)
const handleEdit = (index, scope) => {
  for (let key in scope) {
    for (let key in scope) {
      car_form[key] = scope[key]
    }
    edit_dialog_visible.value = true
  }
}

//编辑提交按钮
const editSubmitForm = (formEl) => {
  axios.put('http://localhost:5000/cars/' + car_form.id, car_form).then((res) => {
    formEl.resetFields()
    edit_dialog_visible.value = false
    getCars()
  })
}

const date = new Date()

const value1 = ref([
  new Date(date.getFullYear(), date.getMonth(), date.getDate(), 0, 0, 0),
  new Date(),
])

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