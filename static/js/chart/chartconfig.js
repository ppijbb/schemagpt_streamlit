const generateBarChart = (function(python_data,chart_index,mean_data,mean_index){
    var config ={
    type: 'bar',
    data: {
        labels: extraction(python_data[0],chart_index),
        datasets:[{
        label: python_data[0][mean_index],
        data: extraction(mean_data,chart_index),
        fill:true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        borderWidth:3,
        minBarLength: 20 
            },{
        label: python_data[1][0],
        data: extraction(python_data[1],chart_index),
        fill:true,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        borderWidthL:3,
        minBarLength: 10
            },
        ]},
    options: {
        maintainAspectRatio: false,
        responsive : true,
        elements: {
            line: {
                borderWidth: 3
                }
            },
        scales: {
            yAxes:[{
                display: false,
                type:'logarithmic',
                ticks: {
                    beginAtZero: true,
                    stepSize: 4
                    },
                }]
            }
        }
    };
    return JSON.stringify(config, null, " ");
});

const generateHBarChart = (function(python_data,chart_index,mean_data,mean_index){
    var config ={
    type: 'horizontalBar',
    data: {
        labels: extraction(python_data[0],chart_index),
        datasets:[{
        label: python_data[0][mean_index],
        data: extraction(mean_data,chart_index),
        fill:true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        minBarLength: 20 
            },{
        label: python_data[1][0],
        data: extraction(python_data[1],chart_index),
        fill:true,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        minBarLength: 10
            },
        ]},
    options: {
        maintainAspectRatio: false,
        responsive : true,
        elements: {
            line: {
                borderWidth: 3
                }
        },
        scales: {
            yAxes:[{
                type:"category",
            }],
            xAxes:[{
                type:"logarithmic",
                display: false,
                ticks: {
                    min:0,
                    beginAtZero: true,
                    stepSize: 4,
                    display: true
                    }
                }]
            }
        }
    };
    return JSON.stringify(config, null, " ");
});

const generateRadarChart = (function(python_data,chart_index,mean_data,mean_index){
    var config ={
        type: 'radar',
        data: {
            labels: extraction(python_data[0],chart_index),
            datasets:[{
            label:python_data[0][mean_index],
            lineTension: 0.1,
            data: extraction(mean_data,chart_index),
            fill:true,
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            borderColor: 'rgb(54, 162, 235)',
            pointBackgroundColor: 'rgb(54, 162, 235)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(54, 162, 235)'   
                },{
            label:python_data[1][0],
            lineTension: 0.1,
            data: extraction(python_data[1],chart_index),
            fill:true,
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            borderColor: 'rgb(255, 99, 132)',
            pointBackgroundColor: 'rgb(255, 99, 132)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgb(255, 99, 132)'    
                },]
        },
        options: {
            maintainAspectRatio: false,
            responsive : true,
            elements: {
            line: {
                borderWidth: 3
                }
            },
            layout:{
                padding: 15
            },
            scale: {
                ticks: {
                    display:false,
                    suggestedMin: 0,
                    max: 12,
                    beginAtZero: true,
                    stepSize: 4
                    }
                },
            tooltips:{
                mode:"nearest",
                }
            }
        };
    return JSON.stringify(config, null, " ");
});

const generateDoughnutChart = (function(python_data,value_grades){
    var config ={
        type: 'doughnut',
        data: {
            labels: [python_data[0].slice(12,34)[3]],
            datasets:[{
            label: [python_data[1][0]],
            data: [Number(python_data[1].slice(12,34)[3]), 12-Number(python_data[1].slice(12,34)[3])],
            fill:true,
            backgroundColor: ["tomato","lightgray"],
            weight:1
            },]},
        options: {
            maintainAspectRatio: false,
            rotation: 1* Math.PI,
            circumference: 1*Math.PI,
            responsive : true,
            elements:{
                center :{
                    text : value_grades[14][1],
                    color: '#FF6384', 
                    sidePadding: 60, 
                    minFontSize: 40, 
                    lineHeight: 25 
                    }
                },
            legend:{
                display: true,
                position:"left",
                align:"start"
                },
            }
        };
    return JSON.stringify(config, null, " ");
});
/*
const generateGaugeChart = (function(cont_data,value_grades,branch){
    var index = 0;
    colormap = ['deepskyblue', 'paleturquoise', 'salmon', 'crimson'];
    var config ={
        type: 'gauge',
        data: {
          datasets: [{
            value: Number(cont_data[index]),
            minValue: 0.7,
            data: [branch[index][0],branch[index][1],branch[index][2],12.3],
            backgroundColor: colormap,
          }]
        },
        options: {
          title:{
              display: true,
              text : value_grades[11+index][0],
              position: "top",
              fontSize: 24,
              fontFamily: "Nunito"
          },
          maintainAspectRatio: false,
          needle: {
            radiusPercentage: 1.5,
            widthPercentage: 3.2,
            lengthPercentage: 50,
            color: 'rgba(0, 0, 0, 1)'
          },
          valueLabel: {
            display: false,
            formatter: (value) => {
              return '$' + Math.round(value);
            },
            color: 'rgba(255, 255, 255, 1)',
            backgroundColor: 'rgba(0, 0, 0, 1)',
            borderRadius: 5,
            padding: {
              top: 10,
              bottom: 10,
            }
          },
          elements:{
            center :{
                text : value_grades[11+index][1],
                color: '#FF6384', 
                sidePadding: 60, 
                minFontSize: 40, 
                lineHeight: 15 
                }
            },
        }
      }
    return JSON.stringify(config, null, " ");
});
*/
const generateGaugeChart = (function(value_grades){
    var index = 0;
    colormap = ['deepskyblue', 'paleturquoise', 'salmon', 'crimson'];
    var config ={
        type: 'gauge',
        data: {
          datasets: [{
            value: Number(index),
            minValue: 0,
            data: [1,2,3,4],
            backgroundColor: colormap,
          }]
        },
        options: {  
          title:{
              display: true,
              text : value_grades,
              position: "top",
              fontSize: 24,
              fontFamily: "Nunito"
          },
          maintainAspectRatio: false,
          needle: {
            radiusPercentage: 1.5,
            widthPercentage: 3.2,
            lengthPercentage: 50,
            color: 'rgba(0, 0, 0, 1)'
          },
          valueLabel: {
            display: true,
            formatter: (value) => {
              return '$' + Math.round(value) + '점';
            },
          color: 'rgba(255, 255, 255, 1)',
          backgroundColor: 'rgba(0, 0, 0, 1)',
          borderRadius: 5,
          padding: {
              top: 5,
              bottom: 10,
            }
          },
          elements:{
            center :{
                display:false,
                text : value_grades,
                color: '#FF6384', 
                sidePadding: 60, 
                minFontSize: 40, 
                lineHeight: 15 
                }
            },
        }
      }
    return JSON.stringify(config, null, " ");
});

const generateLinearGaugeChart = (function(cont_data,value_grades,branch){
    var index = 0;
    let colormap = ['deepskyblue', 'paleturquoise', 'salmon', 'crimson'];
    let colormap2 = ['#05ACE705', '#77FEFE05', '#FF5A4705', '#DC153C05'];
    var config ={
        type: 'horizontalBar',
        data: {
            labels:['평가대상자','지수 기준'],
            datasets: [
                {
                    data: [Number(cont_data[index]),],
                    label:["대상자"],
                    backgroundColor:colormap[0],
                    borderWidth:[0,1],
                    stack:"background",
                },{
                    data: [,branch[index][0]],
                    label:[,'건강'],
                    backgroundColor:colormap2[0],
                    borderWidth:[0,1],
                    stack:"background",
                    yAxisID:"y",
                },{
                    data: [,branch[index][1]-branch[index][0]],
                    label:[,'일반'],
                    backgroundColor:colormap2[1],
                    stack:"background",
                    yAxisID:"y",
                },{
                    data: [,branch[index][2]-branch[index][1]],
                    label:[,'주의'],
                    backgroundColor:colormap2[2],
                    stack:"background",
                    yAxisID:"y",
                },{
                    data: [,12-branch[index][2]],
                    label:[,'관심필요'],
                    backgroundColor:colormap2[3],
                    stack:"background",
                    yAxisID:"y",
                }]
            },
        options: {
          title:{
              display: true,
              text : value_grades[11+index][0],
              position: "top",
              fontSize: 24,
              fontFamily: "Nunito"
          },
          layout:{
            padding:{
                right:10,
                left:10,
                bottom:35,
                }
            },
          scales: {
                xAxes: [{
                    display:false,
                    stacked: true,
                    ticks:{
                        stepSize:4,
                        max:12
                    },
                },{
                display:true,
                type:"category",
                labels:['기준','건강','일반','주의','관심필요'],
                ticks:{
                    beginAtZero:true,
                    }
                }],
                yAxes: [{
                    display:true,
                    stacked:false,
                    categoryPercentage: 0.0001,
                    barPercentage: 3* 10000,
                    ticks:{
                        beginAtZero:true,
                    },
                    labels:['평가대상자'],
                },{
                    id:"y",
                    display:false,
                    stacked: true,
                    type:"category",
                    categoryPercentage: 10,
                    barPercentage: 1,
                    ticks:{
                        beginAtZero:true,
                    },gridLines:{
                        lineWidth:2
                    },
                }]
        },
         legend:{
            display:false
        },
         elements:{
            center :{
                text : value_grades[11+index][1],
                fontFamily:"Nunito",
                sidePadding: 60, 
                minFontSize: 40, 
                lineHeight: 15
            }
        },
         tooltips:{
            callbacks:{
                mode:'label',  
                }
            }
        }
      }
    return JSON.stringify(config, null, " ");
});

const generateLinearGaugeChart2 = (function(cont_data,chart_index,mean_data,mean_index){
    var index = 0;
    let colormap = ['deepskyblue', 'paleturquoise', 'salmon', 'crimson'];
    let colormap2 = ['#05ACE705', '#77FEFE05', '#FF5A4705', '#DC153C05'];
    var config={
        type: 'horizontalBar',
        data: {
            labels:['비질환자 평균','평가대상자',"지수"],
            datasets: [
               {
                    data: [mean_data[index+1],,],
                  //label:['2점'],
                    backgroundColor:colormap[Math.floor(mean_data[index+1])],
                    borderWidth:[2,0,0],
                    stack:"background",
                },{
                    data: [,cont_data[1][index+1],],
                  //label:['1점', , '대상자'],
                    backgroundColor:colormap[Math.floor(cont_data[1][index+1])],
                    borderWidth:[0,2,0],
                    stack:"background",
                },{
                    data: [,,1],
                  //label:['0점','비질환자', ],
                    backgroundColor:colormap2[0],
                    stack:"background",
                    yAxisID:"y",
                },{
                    data: [,,1],
                  //label:['0점','비질환자', ],
                    backgroundColor:colormap2[1],
                    stack:"background",
                    yAxisID:"y",
                },{
                    data: [,,1],
                  //label:['0점','비질환자', ],
                    backgroundColor:colormap2[2],
                    stack:"background",
                    yAxisID:"y",
                },{
                    data: [,,1],
                  //label:['0점','비질환자', ],
                    backgroundColor:colormap2[3],
                    stack:"background",
                    yAxisID:"y",
                }]
            },
        options: {
          title:{
              display: true,
              text : cont_data[0][index],
              position: "top",
              fontSize: 24,
              fontFamily: "Nunito"
          },
          layout:{
            padding:{ bottom: 20}
            },
         scales: {   
                grid:{
                    borderWidth:2
                },
                xAxes: [{
                    display:false,
                    stacked:true,
                    ticks:{
                        beginAtZero:true,
                    },
                },{
                display:true,
                type:"category",
                labels:['건강','일반','위험','고위험','[기준점수]'],
                ticks:{
                    beginAtZero:true,
                    }
                }],
                yAxes: [{
                    display:true,
                    stacked:false,
                    categoryPercentage: 0.0001,
                    barPercentage: 4* 10000,
                    ticks:{
                        beginAtZero:true,
                    },
                    labels:['비질환자 평균','평가대상자'],
                },{
                    id:"y",
                    display:false,
                    stacked: true,
                    type:"category",
                    categoryPercentage: 10,
                    barPercentage: 1,
                    ticks:{
                        beginAtZero:true,
                    },
                }]
            },
         legend:{
            display:false
            },
         elements:{
            center :{
                text : "",//cont_data[0][index],
                fontFamily:"Nunito",
                sidePadding: 60, 
                minFontSize: 40, 
                lineHeight: 15
                }
            },
         tooltips:{
            mode:'index',
//          backgroundColor: '#FFF',
            titleFontSize: 16,
//          titleFontColor: '#0066ff',
//          bodyFontColor: '#000',
            bodyFontSize: 14,
            displayColors: false,   
            },
        }
      }
    return JSON.stringify(config, null, " ");
});

const generatePolarChart = (function(python_data,chart_index,mean_data,mean_index){
    const scale=[2,2,5,12,12,12,12];
    var scale_mean = extraction(mean_data,chart_index).map((x,i)=>{return x/scale[i]});
    var scale_data = extraction(python_data[1],chart_index).map((x,i)=>{return x/scale[i]});

    var config ={
    type: 'bar',
    data: {
        labels: extraction(python_data[0],chart_index),
        datasets:[{
        label: python_data[0][mean_index],
        data: scale_mean,
        fill:true,
        backgroundColor: 'rgba(54, 162, 235, 0.2)',
        borderColor: 'rgb(54, 162, 235)',
        minBarLength: 20 
            },{
        label: python_data[1][0],
        data: scale_data,
        fill:true,
        backgroundColor: 'rgba(255, 99, 132, 0.2)',
        borderColor: 'rgb(255, 99, 132)',
        minBarLength: 10
            },
        ]},
    options: {
        maintainAspectRatio: false,
        responsive : true,
        elements: {
        line: {
            borderWidth: 3
                }
            },
        scales: {
            yAxes:[{
                display: false,
                type:'logarithmic',
                ticks: {
                    beginAtZero: true,
                    stepSize: 4
                    },
                }]
            }
        }
    };
    return JSON.stringify(config, null, " ");
});

function extraction (x,index){
    const result = x.filter(function(x,i){return index.includes(i);}); 
    return result;
    }

module.exports.generateBarChart = generateBarChart;
module.exports.generateHBarChart = generateHBarChart;
module.exports.generateRadarChart = generateRadarChart;
module.exports.generateDoughnutChart = generateDoughnutChart;
module.exports.generateGaugeChart = generateGaugeChart;
module.exports.generateLinearGaugeChart = generateLinearGaugeChart;
module.exports.generateLinearGaugeChart2 = generateLinearGaugeChart2;
module.exports.generatePolarChart = generatePolarChart;




