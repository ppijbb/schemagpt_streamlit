
const chartconfig = require('./chart/chartconfig')
const card = require('./chart/gradetochart')

const Render = (function(list, python_data, category_index, result_grades, branch,directions,id){
    const mean_index = python_data[0].length-1;
    const general_index = category_index[0];
    const blood_index = category_index[1];
    const nutrition_index = category_index[2];
    const pattern_index = category_index[3];
    const value_grades = result_grades;
    var user_name=JSON.stringify(list[0][1]);
    var cont_data = python_data[1].slice(12,34);
    var mean_data = python_data[1][mean_index].split(',');
    var reg = /[\{\}\[\]\/?.,;:|\)*~`!^\-_+<>@\#$%&\\\=\(\'\"]/gi
    var branch = branch.map(x=>x.replace(reg,'')).map(x=>x.split(' ')).map(x=>x.map(x=>Number(x)/10-0.7));
    mean_data[0] = mean_data[0].split('[')[1];
    mean_data[32] = mean_data[32].split(']')[0];
    mean_data.splice(0,0,'');
   
    var direction = directions.split(', ').map(x=>x.replace(/[\[\]]/gi,'')[0]).slice(11,34);
    for (var i in direction){
      if(direction[i] ==='-'){
        cont_data[i] = 13-Number(cont_data[i]);
      }
    }
    
    let session;
    if(typeof(id)=='string'){
      session = ``;
    }
    else {
      user_name = '"'+id.id+'"';
      session = `let logon = '${id.id}'`;
      //`sessionStorage.setItem("User", "${id.id}");`
    }

  // public\css\vendor\fontawesome-free\svgs\solid svg파일 위치
    var html =  `
  <script>
    const directions = ${directions};
    var send1 = ${user_name};
    document.getElementById("cont_data1").innerHTML = send1;
    var send2 = ${JSON.stringify(list[2][1])};
    var send3= ${JSON.stringify(list[1][1].split(" ").slice(2,7)[0])[2]};
  //document.getElementById("cont_data2").innerHTML = send3;
    ${session}

    if(send2 === "건강인"){
      document.getElementById("result_section").classList.remove("border-left-success");
      document.getElementById("result_section").classList.add("border-left-primary");
      document.getElementById("result_text").classList.remove("text-success");
      document.getElementById("result_text").classList.add("text-primary");
      document.getElementById("result_icon").classList.add("fa-smile-beam");
      var ctx = document.getElementById('ResultChart').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart = new Chart(ctx, config); 
      SIChart.data.datasets[0].value= 0.5;
      SIChart.data.datasets[0].minValue= 0;
      SIChart.data.datasets[0].data = [1,2,3,4];
      SIChart.options.valueLabel.display=false;
      SIChart.options.title.text= send2;
      SIChart.options.elements.center.text="";
      SIChart.update();
    }
    else if(send2 === "일반인"){
      document.getElementById("result_section").classList.remove("border-left-success");
      document.getElementById("result_section").classList.add("border-left-secondary");
      document.getElementById("result_text").classList.remove("text-success");
      document.getElementById("result_text").classList.add("text-secondary");
      document.getElementById("result_icon").classList.add("fa-smile");
      var ctx = document.getElementById('ResultChart').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart = new Chart(ctx, config); 
      SIChart.data.datasets[0].value= 1.5;
      SIChart.data.datasets[0].minValue= 0;
      SIChart.data.datasets[0].data = [1,2,3,4];
      SIChart.options.valueLabel.display=false;
      SIChart.options.title.text= send2;
      SIChart.options.elements.center.text="";
      SIChart.update();
    }
    else if(send2 === "위험군"){
      document.getElementById("result_section").classList.remove("border-left-success");
      document.getElementById("result_section").classList.add("border-left-warning");
      document.getElementById("result_text").classList.remove("text-success");
      document.getElementById("result_text").classList.add("text-warning");
      document.getElementById("result_icon").classList.add("fa-meh");
      var ctx = document.getElementById('ResultChart').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart = new Chart(ctx, config); 
      SIChart.data.datasets[0].value= 2.5;
      SIChart.data.datasets[0].minValue= 0;
      SIChart.data.datasets[0].data = [1,2,3,4];
      SIChart.options.valueLabel.display=false;
      SIChart.options.title.text= send2;
      SIChart.options.elements.center.text="";
      SIChart.update();
    }
    else if(send2 === "고위험군"){
      document.getElementById("result_section").classList.remove("border-left-success");
      document.getElementById("result_section").classList.add("border-left-danger");
      document.getElementById("result_text").classList.remove("text-success");
      document.getElementById("result_text").classList.add("text-danger");
      document.getElementById("result_icon").classList.add("fa-sad-tear");
      var ctx = document.getElementById('ResultChart').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart = new Chart(ctx, config); 
      SIChart.data.datasets[0].value= 3.5;
      SIChart.data.datasets[0].minValue= 0;
      SIChart.data.datasets[0].data = [1,2,3,4];
      SIChart.options.title.text= send2;
      SIChart.options.valueLabel.display=false;
      SIChart.options.elements.center.text="";
      SIChart.update();
    }

    if(send3 === 0){
      document.getElementById("result_section2").classList.remove("border-left-success");
      document.getElementById("result_section2").classList.add("border-left-primary");
      document.getElementById("result_text2").classList.remove("text-success");
      document.getElementById("result_text2").classList.add("text-primary");
      document.getElementById("result_icon2").classList.add("fa-smile-beam");
      var ctx = document.getElementById('ResultChart2').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart2 = new Chart(ctx, config); 
      SIChart2.data.datasets[0].value= 0.5;
      SIChart2.data.datasets[0].minValue= 0;
      SIChart2.data.datasets[0].data = [1,2,3,4];
      SIChart2.options.title.text= "건강인";
      SIChart2.options.elements.center.text="";
      SIChart2.update();
    }
    else if(send3 === 1){
      document.getElementById("result_section2").classList.remove("border-left-success");
      document.getElementById("result_section2").classList.add("border-left-secondary");
      document.getElementById("result_text2").classList.remove("text-success");
      document.getElementById("result_text2").classList.add("text-secondary");
      document.getElementById("result_icon2").classList.add("fa-smile");
      var ctx = document.getElementById('ResultChart2').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart2 = new Chart(ctx, config); 
      SIChart2.data.datasets[0].value= 1.5;
      SIChart2.data.datasets[0].minValue= 0;
      SIChart2.data.datasets[0].data = [1,2,3,4];
      SIChart2.options.title.text= "일반인";
      SIChart2.options.elements.center.text="";
      SIChart2.update();
    }
    else if(send3 === 2){
      document.getElementById("result_section2").classList.remove("border-left-success");
      document.getElementById("result_section2").classList.add("border-left-warning");
      document.getElementById("result_text2").classList.remove("text-success");
      document.getElementById("result_text2").classList.add("text-warning");
      document.getElementById("result_icon2").classList.add("fa-meh");
      var ctx = document.getElementById('ResultChart2').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart2 = new Chart(ctx, config); 
      SIChart2.data.datasets[0].value= 2.5;
      SIChart2.data.datasets[0].minValue= 0;
      SIChart2.data.datasets[0].data = [1,2,3,4];
      SIChart2.options.title.text= "위험군";
      SIChart2.options.elements.center.text="";
      SIChart2.update();
    }
    else if(send3 === 3){
      document.getElementById("result_section2").classList.remove("border-left-success");
      document.getElementById("result_section2").classList.add("border-left-danger");
      document.getElementById("result_text2").classList.remove("text-success");
      document.getElementById("result_text2").classList.add("text-danger");
      document.getElementById("result_icon2").classList.add("fa-sad-tear");
      var ctx = document.getElementById('ResultChart2').getContext('2d');
      var config = ${chartconfig.generateGaugeChart(cont_data,value_grades,branch)};
      const SIChart2 = new Chart(ctx, config); 
      SIChart2.data.datasets[0].value= 3.5;
      SIChart2.data.datasets[0].minValue= 0;
      SIChart2.data.datasets[0].data = [1,2,3,4];
      SIChart2.options.title.text= "고위험군";
      SIChart2.options.elements.center.text="";
      SIChart2.update();
    }

    const value_grades = ${JSON.stringify(value_grades)};
    const cont_data = [${cont_data}];
    var branch = ${JSON.stringify(branch)};

    for (var i = 11; i < value_grades.length-2; i++){
      var option = '<option value='+i+'>'+value_grades[i][0]+"</option>";
      if(value_grades[i][1].split(" ")[2]=="관심필요" ){
        if(directions[i] < 0)
          $("#coution").append("<p class='btn btn-outline-secondary' onClick={toWarning(this)} id="+i+">"+
                            "<span>"+value_grades[i][0]+ "</span>"+
                            "<span>"+(13-value_grades[i][1].split(" ")[0])+"단계</span>"+
                            "</p>");
        else
          $("#coution").append("<p class='btn btn-outline-secondary' onClick={toWarning(this)} id="+i+">"+
                            "<span>"+value_grades[i][0]+ "</span>"+
                            "<span>"+value_grades[i][1].split(" ")[0]+"단계</span>"+
                            "</p>");
      }
      $("#select_cont_value").append(option);
    }

    var ctx = document.getElementById('generalChart').getContext('2d');
    var config = ${chartconfig.generatePolarChart(python_data,general_index,mean_data,mean_index)};
    const generalChart = new Chart(ctx,config);

    var ctx = document.getElementById('bloodChart').getContext('2d');
    var config = ${chartconfig.generateRadarChart(python_data,blood_index,mean_data,mean_index)};
    const bloodChart = new Chart(ctx, config);

    var ctx = document.getElementById('nutritionChart').getContext('2d');
    var config =  ${chartconfig.generateRadarChart(python_data,nutrition_index,mean_data,mean_index)};
    const nutrirtionChart = new Chart(ctx, config);
    
    var ctx = document.getElementById('patternChart').getContext('2d');
    var config =  ${chartconfig.generateHBarChart(python_data,pattern_index,mean_data,mean_index)};
    const patternChart = new Chart(ctx, config); 
    
    var ctx = document.getElementById('StandardizedIndexChart').getContext('2d');
    var config = ${chartconfig.generateLinearGaugeChart(cont_data,value_grades,branch)};
    config.data.labels[0]= send1;
    config.options.scales.yAxes[0].labels=[send1];
    if(config.options.elements.center.text.split(" ")[2] === "건강") config.data.datasets[0].backgroundColor="deepskyblue";
    else if(config.options.elements.center.text.split(" ")[2] === "일반") config.data.datasets[0].backgroundColor="paleturquoise";
    else if(config.options.elements.center.text.split(" ")[2] === "주의") config.data.datasets[0].backgroundColor="salmon";
    else if(config.options.elements.center.text.split(" ")[2] === "관심필요") config.data.datasets[0].backgroundColor="crimson";
    config.options.tooltips.callbacks=${card.tooltiphbar2} 
    var SIChart = new Chart(ctx, config);
  
    //document.getElementById("about_result").innerHTML=value_grades[11][0];
    
    let fs = new XMLHttpRequest();
    fs.open("GET", "/views/text/blod.txt", false); 
    fs.send();
    if(fs.status == 200 || fs.readyState == fs.DONE) {
        let article = fs.responseText;
        document.getElementById("about_result").innerHTML=article;
          }

    function onChange(e){
      let text_item = [[11,12,13,15,16,17,18,19,22,25,26],
                       [14,20,21,24,27,28,29,30],
                       [23]]
      var index = e.value-11;
      var sendLevel = cont_data[index];
      SIChart.options.title.text= value_grades[e.value][0];
      if(directions[e.value] < 0)
        SIChart.options.elements.center.text=cont_data[index]+" "+value_grades[e.value][1].split(" ")[1]+" "+value_grades[e.value][1].split(" ")[2];
      else
        SIChart.options.elements.center.text=value_grades[e.value][1];
      if(SIChart.options.elements.center.text.split(" ")[2] === "건강") SIChart.data.datasets[0].backgroundColor="deepskyblue";
      else if(SIChart.options.elements.center.text.split(" ")[2] === "일반") SIChart.data.datasets[0].backgroundColor="paleturquoise";
      else if(SIChart.options.elements.center.text.split(" ")[2] === "주의") SIChart.data.datasets[0].backgroundColor="salmon";
      else if(SIChart.options.elements.center.text.split(" ")[2] === "관심필요") SIChart.data.datasets[0].backgroundColor="crimson";
      SIChart.data.datasets[0].data = [cont_data[index],];
      SIChart.data.datasets[1].data = [,branch[index][0]];
      SIChart.data.datasets[2].data = [,branch[index][1]-branch[index][0]];
      SIChart.data.datasets[3].data = [,branch[index][2]-branch[index][1]];
      SIChart.data.datasets[4].data = [,12-branch[index][2]];
      
      SIChart.update();
      for(var i in text_item){
        if(text_item[i].includes(Number(e.value))){
          const fs = new XMLHttpRequest();
          if(i==="0"){
            fs.open("GET", "/views/text/blod.txt", false); 
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) {
                let article = fs.responseText;
                document.getElementById("about_result").innerHTML=article;
                  }
          }
          else if(i==="1"){
            fs.open("GET", "/views/text/nutr.txt", false); 
            fs.send();
            if(fs.status == 200 || fs.readyState == fs.DONE) {
                let article = fs.responseText;
                document.getElementById("about_result").innerHTML=article;
                  }
          }
          else{
            fs.open("GET", "/views/text/obes.txt", false); 
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

    function toWarning(e){
        document.getElementById("select_cont_value").value = e.id;
        onChange(document.getElementById("select_cont_value"));
    }

  $("span:contains('관심필요')").css({color:"red"});
  </script>
  <script type='text/javascript' src="js/chartscript2.js"></script>
  <script type='text/javascript' src="css/js/sb-admin-2.min.js"></script>
  <script type='text/javascript' src="js/signin.js"></script>
`;

return html;
});

module.exports.RenderHtml = Render;
