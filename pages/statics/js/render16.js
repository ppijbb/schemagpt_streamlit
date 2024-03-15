const chartconfig = require('./chart/chartconfig')
const card = require('./chart/gradetochart')
const scoref = require('./about_score')

function range(start, stop, step) {
  if (typeof stop == 'undefined') {
      // one param defined
      stop = start;
      start = 0;
  }

  if (typeof step == 'undefined') {
      step = 1;
  }

  if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
      return [];
  }

  var result = [];
  for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
      result.push(i);
  }

  return result;
};

function data_trans(arr){
  return arr.slice(1,17).map(x=>Number(x));
}

const Render = (function(list, python_data, id){
    const mean_index = python_data[0].length-1;
    var mean_data = python_data[1][mean_index].replace(/[\[\]]/gi,'').split(',');
    var reg = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi
    mean_data.splice(0,0,'');
    mean_data.pop(); mean_data.pop();
    var user_name =JSON.stringify(list[0][1]);
    var grade = JSON.stringify(list[2][1]).replace(reg,'');
    var result = JSON.stringify(list[1][1].split(" ")[1]).replace(reg,'');
    var score = JSON.stringify(list[1][1].split(" ")[2]).replace(reg,'');
    var card1 ='', card2 ='';
    [card1, card2]= card.generateCard(grade, result);
    var blood_index = range(1,17), nutrition_index= [];
  //var blood_index = [1,2,3,4,5,6,8,9,12] , nutrition_index = [7,10,11,13,14,15,16];
    var personal = [];
    for(var i in data_trans(mean_data)){
      let mean_gap = data_trans(mean_data)[i]-data_trans(python_data[1])[i];
      personal.push({"value":Math.abs(mean_gap),
                     "lowover":mean_gap,
                      "index":i});
    }
    personal.sort(function(a,b){
      return b.value - a.value;
    }).slice(0,3).forEach(element => {
      nutrition_index.push(Number(element.index));
    });

    let session;
    if(typeof(id)=='string'){
      session = ``;
    }
    else {
      user_name = '"'+id.id+'"';
      session = `let logon = '${id.id}';`
      //`sessionStorage.setItem("User", "${id.id}");`
    }

    var html = 
    ` <script>
    var user_name = ${user_name};
    var grade = "${grade}";
    var result = ${result};
    var columns = [${python_data[0].slice(1,17)}];
    var values = [${python_data[1].slice(1,17)}];
    var mean = [${mean_data.slice(1,17)}];
    ${session}
    document.getElementById("cont_data1").innerHTML = user_name;
    document.getElementById("about_Score").innerHTML = ${scoref.about_Score(user_name, result, score, python_data[0].slice(1,17), python_data[1].slice(1,17), personal[0].index)};
    ${card1}
    ${card2}
    SIChart2.options.valueLabel.formatter= ()=>{return "${score}점"};
    SIChart2.options.tooltips.enabled = true;
    SIChart2.options.tooltips.callbacks=${card.tooltipgauge}
    SIChart2.update();

    var ctx = document.getElementById('bloodChart').getContext('2d');
    var config = ${chartconfig.generateRadarChart(python_data,blood_index,mean_data,mean_index)};
    const bloodChart = new Chart(ctx, config);

    bloodChart.options.tooltips.callbacks = ${card.tooltipradar}
    bloodChart.options.scale.ticks.max= 3;
    bloodChart.options.scale.ticks.stepSize= 1;
    bloodChart.update();

    var ctx = document.getElementById('StandardizedIndexChart').getContext('2d');
    var config =  ${chartconfig.generateLinearGaugeChart2(python_data,nutrition_index,mean_data,mean_index)};
    config.data.labels[1]=user_name;
    config.options.tooltips.callbacks = ${card.tooltiphbar}
    const indivChart = new Chart(ctx, config);

    
    for (var i in columns){
      var option = '<option value='+i+'>'+columns[i]+"</option>";
      $("#select_cont_value").append(option);
    }
    onChange(document.getElementById("select_cont_value"));

//$("span:contains('관심필요')").css({color:"red"});

  function onChange(e){
    let text_item =[[0],[1,2,5,7,8,11],[3,4],[6,9],[10],[12,13,14,15]];
    let colormap = ['deepskyblue', 'paleturquoise', 'salmon', 'crimson'];
    indivChart.data.datasets[0].data = [mean[Number(e.value)],,];
    indivChart.data.datasets[0].backgroundColor = colormap[Math.floor(mean[Number(e.value)])];
    indivChart.data.datasets[1].data = [,values[Number(e.value)],];
    indivChart.data.datasets[1].backgroundColor = colormap[Math.floor(values[Number(e.value)])];
    indivChart.options.title.text = columns[Number(e.value)];
  //indivChart.options.elements.center.text = values[Number(e.value)];
    indivChart.update();
    for (var i in text_item){
        if( text_item[i].includes(Number(e.value)) ){
          const fs = new XMLHttpRequest();
          if(i==0){
            fs.open("GET", "./views/text/selfcheck.txt", false); 
          //  fs.responseType = 'text';
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) {
                let article = fs.responseText;
                document.getElementById("about_result").innerHTML=article;
                }
              }
          else if(i==1){
            fs.open("GET", "/views/text/stress.txt", false); 
          //fs.responseType = 'text';
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) { 
              let article = fs.responseText;
              document.getElementById("about_result").innerHTML=article;
                }
              }
          else if(i==2){
            fs.open("GET", "/views/text/alchol.txt", false);
          //fs.responseType = 'text';
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) {
              let article = fs.response;
              document.getElementById("about_result").innerHTML=article; 
                }
              }
          else if(i==3){
            fs.open("GET", "/views/text/physical.txt", false); 
          //fs.responseType = 'text';
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) {
              let article = fs.responseText;
              document.getElementById("about_result").innerHTML=article;
                }
              }
          else if(i==4){
            fs.open("GET", "/views/text/medicine.txt", false); 
          //fs.responseType = 'text';
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) {
              let article = fs.responseText;
              document.getElementById("about_result").innerHTML=article;
                }
              }
          else if(i==5){
            fs.open("GET", "/views/text/nutr.txt", false); 
          //fs.responseType = 'text';
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) {
              let article = fs.responseText;
              document.getElementById("about_result").innerHTML=article;
                }
              }
        }
    }
    //document.getElementById("about_result").innerHTML=value_grades[e.value][0];
  } 
    </script>
    <script type='text/javascript' src="js/chartscript.js"></script>
    <script type='text/javascript' src="css/js/sb-admin-2.min.js"></script>
    <script type='text/javascript' src="js/signin.js"></script>
    `;
return html;
});

module.exports.RenderHtml = Render;