<template>
  <div class="ordering">
    <div id="main" style="width: 100vh;height:150vh;overflow: auto"></div>
      <router-view></router-view>

  </div>
</template>

<script>
// import {onMounted, ref} from 'vue';
import * as echarts from "echarts";
import axios from "axios";

// setTimeout(function (){})
const provinces = new Map();
provinces.set("安徽省", "anhui");
provinces.set("宁夏回族自治区", "ningxia");
provinces.set("海南省", "hainan");
provinces.set("西藏自治区", "xizang");
provinces.set("青海省", "qinghai");
provinces.set("四川省", "sichuan");
provinces.set("广东省", "guangdong");
provinces.set("贵州省", "guizhou");
provinces.set("福建省", "fujian");
provinces.set("吉林省", "jilin");
provinces.set("陕西省", "shaanxi");
provinces.set("内蒙古自治区", "neimenggu");
provinces.set("山西省", "shanxi");
provinces.set("甘肃省", "gansu");
provinces.set("湖北省", "hubei");
provinces.set("江西省", "jiangxi");
provinces.set("浙江省", "zhejiang");
provinces.set("江苏省", "jiangsu");
provinces.set("新疆维吾尔自治区", "xinjiang");
provinces.set("山东省", "shandong");
provinces.set("湖南省", "hunan");
provinces.set("黑龙江省", "heilongjiang");
provinces.set("辽宁省", "liaoning");
provinces.set("云南省", "yunnan");
provinces.set("河南省", "henan");
provinces.set("河北省", "hebei");
provinces.set("重庆市", "chongqing");
provinces.set("天津市", "tianjin");
provinces.set("上海市", "shanghai");
provinces.set("北京市", "beijing");
provinces.set("广西壮族自治区", "guangxi");

const option = {
    legend: {},
    grid: {
      height:750,
      left: '3%',
      right: '4%',
      containLabel: true
    },
    yAxis: {
      data: [],
    },
    xAxis: {},

    series: [
      {
        realtimeSort: true,
        type: 'bar',
        stack: 'total',
        data : [],
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
      }
    ]
}


export default {
  data() {
    return {

    };
  },
  methods: {
    drawBarChart() {
      const myChart = echarts.init(document.getElementById('main'));
      myChart.setOption(option);
      myChart.showLoading();
      axios.get("http://localhost:5000/pros/select").then(res => {
        setTimeout(() => {
          myChart.hideLoading();
          const province = []
          const num = []
          for(let i=0; i<res.data.results.length; i++){
            province.push(res.data.results[i].province)
            num.push(res.data.results[i].num)
          }
          myChart.setOption({
            xAxis: {

              type: 'value'
            },
            yAxis: [
              {
                type: 'category',
                inverse: true,
                data: province
              }
            ],
            series: [
              {
                data:num
              }
            ]
          });

          myChart.on('click', function (param){
            const name=param.name;
            console.log(name);
            const parent_routers = window.location.href.split('/')
            let parent_router = parent_routers[0]
            for(let i = 1; i<parent_routers.length-1; i++){
              parent_router = parent_router + '/' + parent_routers[i]
            }
            window.open(parent_router + '/' + provinces.get(name), '_self');
          });
        }, 500);
      })
          .catch(err => {
            console.log(err);
          });
    }
  },
  mounted() {
    this.drawBarChart();
  }

}

</script>

<style scoped>

</style>