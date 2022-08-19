<template>
  <div class="ordering">
    <e-charts class="chart" :option="option"/>
  </div>
</template>

<script setup>
import {ref} from 'vue';
import * as echarts from "echarts";
// import * as cities from '@/store/cities'
// import cardCallerloc from "@/store/cities";
// console.log(cities.cardCallerloc)
//
// const myChart = echarts.init(document.getElementById(doms));
const option = ref({
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      // Use axis to trigger tooltip
      type: 'shadow' // 'shadow' as default; can also be 'line' or 'shadow'
    }
  },
  legend: {},
  grid: {
    left: '3%',
    right: '4%',
    bottom: '10%',
    containLabel: true
  },
  xAxis: {
    type: 'value'
  },
  yAxis: {
    type: 'category',
    data: ["1小时内", "3小时内", "1天内", "超过一天"]
  },
  series: [
    {
      type: 'bar',
      stack: 'total',
      label: {
        show: true
      },
      itemStyle: {
        color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
          { offset: 0, color: '#83bff6' },
          { offset: 0.5, color: '#188df0' },
          { offset: 1, color: '#188df0' }
        ])
      },
        emphasis: {
          focus: 'series',
          itemStyle: {
          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
            { offset: 0, color: '#2378f7' },
            { offset: 0.7, color: '#2378f7' },
            { offset: 1, color: '#83bff6' }
          ])
        }
        },
      data: [320, 302, 301, 334]
    }
  ]
})
// myChart.clear();
// myChart.setOption(option);
// window.addEventListener('resize', function () {myChart.resize();})
// myChart.on('click',function(params){
//   location.href='\'model_analysis\''
// })

</script>

<style scoped>
.chart {
  height: 400px;
}
</style>