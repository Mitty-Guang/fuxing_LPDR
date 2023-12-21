<template>
  <div class="ordering">
    <div class="heading">
      <div>车型分析</div>
    </div>
    <div id="main" style="width: 100vh;height:80vh;"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import axios from "axios";

const option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b} : {c} ({d}%)'
      },

      series: [
        {
          name: '车型分析',
          type: 'pie',
          radius: [20, 300],
          center: ['50%', '50%'],
          roseType: 'area',
          itemStyle: {
            borderRadius: 5
          },
          data: []
        }
      ]
    }

export default {
  data() {
    return{};
  },
  methods: {
    drawPieChart() {
      const myChart = echarts.init(document.getElementById('main'))
      myChart.setOption(option);
      myChart.showLoading();
      axios.get("http://127.0.0.1:5000/model").then(res => {
        setTimeout(() => {
          myChart.hideLoading();
          console.log(res.data.results)
          myChart.setOption({
            series: [
              {
                data: res.data.results
              }
            ]
          });
        },500);
      })
          .catch(err => {
            console.log(err)
          });
    }
  },
  mounted() {
    this.drawPieChart();
  }
}
</script>

<style scoped>
.chart {
  height: 1200px;
}
</style>

