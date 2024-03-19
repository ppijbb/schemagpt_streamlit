const chartconfig = require('./chartconfig')

const generateCard = (function(send2,send3){
    var card1 ='', card2 = '';

    if(send2 === "건강인"){
        card1 =
       `document.getElementById("result_section").classList.remove("border-left-success");
        document.getElementById("result_section").classList.add("border-left-primary");
        document.getElementById("result_text").classList.remove("text-success");
        document.getElementById("result_text").classList.add("text-primary");
        document.getElementById("result_icon").classList.add("fa-smile-beam");
        var ctx = document.getElementById('ResultChart').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send2)};
        const SIChart = new Chart(ctx, config); 
        SIChart.data.datasets[0].value= 0.5;
        SIChart.options.title.text= "${send2}";
        SIChart.options.elements.center.text="";
        SIChart.update();
        `;
    }
    else if(send2 === "일반인"){
        card1 =`
        document.getElementById("result_section").classList.remove("border-left-success");
        document.getElementById("result_section").classList.add("border-left-secondary");
        document.getElementById("result_text").classList.remove("text-success");
        document.getElementById("result_text").classList.add("text-secondary");
        document.getElementById("result_icon").classList.add("fa-smile");
        var ctx = document.getElementById('ResultChart').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send2)};
        const SIChart = new Chart(ctx, config); 
        SIChart.data.datasets[0].value= 1.5;        
        SIChart.options.title.text= "${send2}";
        SIChart.options.elements.center.text="";
        SIChart.update();
        `;
    }
    else if(send2 === "위험군"){
        card1 =`
        document.getElementById("result_section").classList.remove("border-left-success");
        document.getElementById("result_section").classList.add("border-left-warning");
        document.getElementById("result_text").classList.remove("text-success");
        document.getElementById("result_text").classList.add("text-warning");
        document.getElementById("result_icon").classList.add("fa-meh");
        var ctx = document.getElementById('ResultChart').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send2)};
        const SIChart = new Chart(ctx, config); 
        SIChart.data.datasets[0].value= 2.5;        
        SIChart.options.title.text= "${send2}";
        SIChart.options.elements.center.text="";
        SIChart.update();
        `;
    }
    else if(send2 === "고위험군"){
        card1=`
        document.getElementById("result_section").classList.remove("border-left-success");
        document.getElementById("result_section").classList.add("border-left-danger");
        document.getElementById("result_text").classList.remove("text-success");
        document.getElementById("result_text").classList.add("text-danger");
        document.getElementById("result_icon").classList.add("fa-sad-tear");
        var ctx = document.getElementById('ResultChart').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send2)};
        const SIChart = new Chart(ctx, config); 
        SIChart.data.datasets[0].value= 3.5;        
        SIChart.options.title.text= "${send2}";
        SIChart.options.elements.center.text="";
        SIChart.update();
        `;
    }

    if(send3 === "0"){
        card2 =`
        document.getElementById("result_section2").classList.remove("border-left-success");
        document.getElementById("result_section2").classList.add("border-left-primary");
        document.getElementById("result_text2").classList.remove("text-success");
        document.getElementById("result_text2").classList.add("text-primary");
        document.getElementById("result_icon2").classList.add("fa-smile-beam");
        var ctx = document.getElementById('ResultChart2').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send3)};
        const SIChart2 = new Chart(ctx, config); 
        SIChart2.data.datasets[0].value= 0.5;        
        SIChart2.options.title.text= "건강인";
        SIChart2.options.elements.center.text="";
        SIChart2.update();
        `;
    }
    else if(send3 === "1"){
        card2 =`
        document.getElementById("result_section2").classList.remove("border-left-success");
        document.getElementById("result_section2").classList.add("border-left-secondary");
        document.getElementById("result_text2").classList.remove("text-success");
        document.getElementById("result_text2").classList.add("text-secondary");
        document.getElementById("result_icon2").classList.add("fa-smile");
        var ctx = document.getElementById('ResultChart2').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send3)};
        const SIChart2 = new Chart(ctx, config); 
        SIChart2.data.datasets[0].value= 1.5;        
        SIChart2.options.title.text= "일반인";
        SIChart2.options.elements.center.text="";
        SIChart2.update();
        `;
    }
    else if(send3 === "2"){
        card2 = `
        document.getElementById("result_section2").classList.remove("border-left-success");
        document.getElementById("result_section2").classList.add("border-left-warning");
        document.getElementById("result_text2").classList.remove("text-success");
        document.getElementById("result_text2").classList.add("text-warning");
        document.getElementById("result_icon2").classList.add("fa-meh");
        var ctx = document.getElementById('ResultChart2').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send3)};
        const SIChart2 = new Chart(ctx, config); 
        SIChart2.data.datasets[0].value= 2.5;        
        SIChart2.options.title.text= "위험군";
        SIChart2.options.elements.center.text="";
        SIChart2.update();
        `;
    }
    else if(send3 === "3"){
        card2 =`
        document.getElementById("result_section2").classList.remove("border-left-success");
        document.getElementById("result_section2").classList.add("border-left-danger");
        document.getElementById("result_text2").classList.remove("text-success");
        document.getElementById("result_text2").classList.add("text-danger");
        document.getElementById("result_icon2").classList.add("fa-sad-tear");
        var ctx = document.getElementById('ResultChart2').getContext('2d');
        var config = ${chartconfig.generateGaugeChart(send3)};
        const SIChart2 = new Chart(ctx, config); 
        SIChart2.data.datasets[0].value= 3.5;        
        SIChart2.options.title.text= "고위험군";
        SIChart2.options.elements.center.text="";
        SIChart2.update();
        `;
    }

    return [card1, card2];
});
module.exports.generateCard = generateCard;

const tooltiphbar =`{
    label:function(tooltipItem,data){
        if(tooltipItem.yLabel === "지수"){if(tooltipItem.x<206) return "0점~3점";}
        else if(tooltipItem.label === "비질환자 평균") {
            if(!isNaN(tooltipItem.x))
                return String(data.datasets[0].data[tooltipItem.index].toFixed(2) + '점');
            }
        else{
            if(!isNaN(tooltipItem.x)){
                return String(
                    '해당항목의' +
                    '점수는 '+ data.datasets[1].data[tooltipItem.index] + '점으로 평균과 '+
                    (data.datasets[1].data[tooltipItem.index] - data.datasets[0].data[tooltipItem.index-1]).toFixed(2)+
                    '점 차이가 있습니다.');}
        }
    }
}`
module.exports.tooltiphbar = tooltiphbar;

const tooltipgauge = `{
    title:function(tooltipItem,data){
        if(data.datasets[0].data[tooltipItem[0].index]===1) return "건강인";
        else if(data.datasets[0].data[tooltipItem[0].index]===2) return "일반인";
        else if(data.datasets[0].data[tooltipItem[0].index]===3) return "위험군";
        else if(data.datasets[0].data[tooltipItem[0].index]===4) return "고위험군";
        },
    label:function(tooltipItem,data){
        if(data.datasets[0].data[tooltipItem.index]===1) return "~15점";
        else if(data.datasets[0].data[tooltipItem.index]===2) return "16~20점";
        else if(data.datasets[0].data[tooltipItem.index]===3) return "21~24점";
        else if(data.datasets[0].data[tooltipItem.index]===4) return "24~점";
    }
}`
module.exports.tooltipgauge = tooltipgauge;

const tooltipradar = `{
    title:function(tooltipItem,data){
        if(data.datasets[0].data[tooltipItem[0].index]===1) return "건강인";
        else if(data.datasets[0].data[tooltipItem[0].index]===2) return "일반인";
        else if(data.datasets[0].data[tooltipItem[0].index]===3) return "위험군";
        else if(data.datasets[0].data[tooltipItem[0].index]===4) return "고위험군";
        },
    label:function(tooltipItem,data){
        return data.datasets[0].data[tooltipItem.index];
    }
}`
module.exports.tooltipradar = tooltipradar;

const tooltiphbar2 =`{
    title:function(tooltipItem,data){
        return data.labels[tooltipItem[0].index];
    },
    label:function(tooltipItem,data){
        if(tooltipItem.index <1 ){
            if(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index] != null)
            return String(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]
                          +" 단계");
        }
        else {
            function recur(data, index){
                if(index === 1)
                    return data[index].data[1];
                else
                    return data[index].data[1]+recur(data,index-1);
            }
            if(data.datasets[tooltipItem.datasetIndex].label[tooltipItem.index] === '건강') 
                return String(data.datasets[tooltipItem.datasetIndex].label[tooltipItem.index]
                            + " : 1~" +
                            Math.floor(data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index]));
            else 
                return String(data.datasets[tooltipItem.datasetIndex].label[tooltipItem.index]
                            + " : " +
                            Math.floor(recur(data.datasets,tooltipItem.datasetIndex-1))
                            + "~" +
                            Math.floor(recur(data.datasets,tooltipItem.datasetIndex))
                            );
        }
    }
}`
module.exports.tooltiphbar2 = tooltiphbar2;