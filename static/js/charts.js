function ChartInit(){
            // 为echarts对象加载数据
        myLineChart.setOption(lineOption);
//        myLineChart.showLoading();
}
lineOption = {
    tooltip : {
        trigger: 'axis'
    },
    legend: {
        data:['数据']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            dataZoom : {show: true},
            dataView : {show: true},
            saveAsImage: {show: true}
        }
    },
    xAxis : [
        {
            name :'时间',
            type : 'category',
            boundaryGap : false,
            data : []
        }
    ],
    yAxis : [
        {
            type : 'value'
        }
    ],
    series : [
        {
            name:'数据',
            type:'line',
            stack: '总量',
            areaStyle: {normal: {}},
            data:[]
        }
    ]
};
