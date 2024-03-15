const chartconfig = require('./chart/chartconfig')
const card = require('./chart/gradetochart')
const userLog = (function(result, result2, result3){
  const Q16 = {
    "SEQ":	"seq",    "USER_ID":	"id",
    "CB_1":	"general_number-6",    
    "CB_2":	"pattern_number-7",    
    "CB_3":	"pattern_number-3",
    "CB_4":	"pattern_number-8",    
    "CB_5":	"pattern_number-81",    
    "CB_6":	"pattern_number-4",
    "CB_7":	"pattern_number-5",    
    "CB_8":	"pattern_number-9",    
    "CB_9":	"pattern_number-10",
    "CB_10":	"general_number-1",    
    "CB_11":	"general_number-2",    
    "CB_12":	"pattern_number-11",
    "CB_13":	"nutrition_number-15",    
    "CB_14":	"nutrition_number-22",    
    "CB_15":	"nutrition_number-29",
    "CB_16":	"nutrition_number-32",    
    "CB_SUM":	"sum",    "CB_GRADE":	"grade",    "CB_DATE":	"date",
  }
  const Q33 = {
    "SEQ":"seq","USER_ID":"id",
    "CD_1"  : "general_number-1", 
    "CD_2"	: "general_number-2",  
    "CD_3"	: "pattern_number-3",  
    "CD_4"	: "pattern_number-4",
    "CD_5"	: "pattern_number-5",  
    "CD_6"	: "general_number-6",    
    "CD_7"	: "pattern_number-7",  
    "CD_8"	: "pattern_number-8",
    "CD_9"	: "pattern_number-9",  
    "CD_10"	: "pattern_number-10",  
    "CD_11"	: "pattern_number-11",       
    "CD_12"	: "general_number-12",  
    "CD_13"	: "general_number-13",  
    "CD_14"	: "general_number-14", 
    "CD_15"	: "nutrition_number-15",
    "CD_16"	: "blood_number-16",  
    "CD_17"	: "blood_number-17",
    "CD_18"	: "blood_number-18",  
    "CD_19"	: "blood_number-19",  
    "CD_20"	: "blood_number-20",
    "CD_21"	: "nutrition_number-21",
    "CD_22"	: "nutrition_number-22",    
    "CD_23"	: "blood_number-23", 
    "CD_24"	: "general_number-24",   
    "CD_25"	: "nutrition_number-25",
    "CD_26"	: "blood_number-26",  
    "CD_27"	: "blood_number-27", 
    "CD_28"	: "nutrition_number-28",
    "CD_29"	: "nutrition_number-29", 
    "CD_30"	: "nutrition_number-30",  
    "CD_31"	: "nutrition_number-31",
    "CD_32"	: "nutrition_number-32", 
    "CD_33"	: "blood_number-33",    
    "CD_GRADE"	: "grade",  "CD_DATE"	: "date",
  }
  const Q33R = {
    "SEQ":"seq","USER_ID":"id",
    "CR_1"  : "general_number-1", 
    "CR_2"	: "general_number-2", 
    "CR_3"	: "pattern_number-3",  
    "CR_4"	: "pattern_number-4",
    "CR_5"	: "pattern_number-5",    
    "CR_6"	: "general_number-6",
    "CR_7"	: "pattern_number-7",  
    "CR_8"	: "pattern_number-8",
    "CR_9"	: "pattern_number-9",  
    "CR_10"	: "pattern_number-10",  
    "CR_11"	: "pattern_number-11",    
    "CR_12"	: "general_number-12",  
    "CR_13"	: "general_number-13",  
    "CR_14"	: "general_number-14",
    "CR_15"	: "nutrition_number-15",   
    "CR_16"	: "blood_number-16",  
    "CR_17"	: "blood_number-17",
    "CR_18"	: "blood_number-18",  
    "CR_19"	: "blood_number-19",  
    "CR_20"	: "blood_number-20",
    "CR_21"	: "nutrition_number-21",
    "CR_22"	: "nutrition_number-22",
    "CR_23"	: "blood_number-23", 
    "CR_24"	: "general_number-24",
    "CR_25"	: "nutrition_number-25",
    "CR_26"	: "blood_number-26",  
    "CR_27"	: "blood_number-27", 
    "CR_28"	: "nutrition_number-28",
    "CR_29"	: "nutrition_number-29", 
    "CR_30"	: "nutrition_number-30",  
    "CR_31"	: "nutrition_number-31",
    "CR_32"	: "nutrition_number-32",     
    "CR_33"	: "blood_number-33",    
    "CR_DATE"	: "date",
  }
  const label ={
    "general_number-1":"규칙적 운동" ,
    "general_number-2":"보조제 복용", 
    "pattern_number-3":"무기력감"	, 
    "pattern_number-4":"신경질",
    "pattern_number-5":"중강도 신체활동",
    "general_number-6":"자신의 건강",
    "pattern_number-7":"피로",
    "pattern_number-8":"음주"	,
    "pattern_number-81":"음주량",
    "pattern_number-9":"긴장, 불안",
    "pattern_number-10":"대면어려움",
    "pattern_number-11":"시선어려움",
    "general_number-12":"수축기혈압(2차측정치)",
    "general_number-13":"이완기혈압",
    "general_number-14":"수축기혈압(1차측정치)",
    "nutrition_number-15":"Vit E",
    "blood_number-16":"HDL"	, 
    "blood_number-17":"LDL",
    "blood_number-18":"LDL-c",
    "blood_number-19":"HCT",
    "blood_number-20":"CHOL",
    "nutrition_number-21":"회분",
    "nutrition_number-22":"식물성 Fe",
    "blood_number-23":"HGB",
    "general_number-24":"복부지방률",
    "nutrition_number-25":"Mo",
    "blood_number-26":"RBC",
    "blood_number-27":"MONO",
    "nutrition_number-28":"Vit B2",
    "nutrition_number-29":"동물성 단백질",
    "nutrition_number-30":"Cu",
    "nutrition_number-31":"Vit C",
    "nutrition_number-32":"Protein", 
    "blood_number-33":"WBC",    
  }

  let results =[], results2 = [], results3=[];
  for(var key in Q16){
      var temp = [];
      for(let i in result){
         temp.push(String(result[i][key]));
      } results.push(temp);
    }
  for(var key in Q33){
      var temp = [];
      for(let i in result2){
         temp.push(String(result2[i][key]));
      }results2.push(temp);
    }
  for(var key in Q33R){
      var temp = [];
      for(let i in result3){
         temp.push(String(result3[i][key]));
      } results3.push(temp);
    }
    results = JSON.stringify(results);
    results2 = JSON.stringify(results2);
    results3 = JSON.stringify(results3);
    
    var html =  `
  <script>
    const logseq = ${result.length};
    const logseq2 = ${result2.length};
    const label = ${JSON.stringify(label)};

    let results = ${Object(results)};
    let results2 = ${Object(results2)};
    let results3 = ${Object(results3)};

    let results_values = results.slice(2,18);
    let results_values2 = results2.slice(2,35);
    let results_values3 = results3.slice(2,35);

    let Q16 = "${Object.values(Q16)}";
    let Q33 = "${Object.values(Q33)}";
    
    Q16 = Q16.split(',').slice(2,18);
    Q33 = Q33.split(',').slice(2,35);

    let docitem = $("#page-16 .log_result");
    let docitem2 = $("#page-33 .log_result");
    $(".card-header .sidediv")[0].setAttribute('style',"display:flex;position:relative;flex-direction:row;");
    $(".card-header .sidediv")[1].setAttribute('style',"display:flex;position:relative;flex-direction:row;");
    $("input[name=username-0]")[0].value = sessionStorage['User'];
    $("input[name=username-0]")[0].setAttribute('readonly',true);
    $("input[name=username-0]")[1].value = sessionStorage['User'];
    $("input[name=username-0]")[1].setAttribute('readonly',true);
    
    docitem[0].innerHTML = '<table class="logtable16"><thead><tr class="logDate"><th>항목</th><th>평가 기록</th></tr></thead><tbody><tr class="logValue"><td><ul class="chart-select"></ul></td><td><div class="Gchart"></div></td></tr></tbody></table>'
    for(var i in Q16){      
      var logDate = $(".logtable16 .logDate")[i];
      var logValue = $(".logtable16 .logValue")[i];
      let temp = [];
      for(var j=0; j<logseq;j++){
        temp.push([Number(results[0][j]),Number(results_values[i][j])]);
      }
    }

    var multi = $('.logtable16 .logValue .Gchart')[0];
    var chart = new MULTIDATA(results_values, multi, Q16, label);
    for(var i in Q16){
        $(".logtable16 .logValue .chart-select")[0].innerHTML += String("<li><label><input type='checkbox' id='idx"+i+"' onclick={doupdate(results_values,multi,Q16,label)} value='"+ label[Q16[i]] +"'>"+label[Q16[i]]+"</label></li>");
    }
    docitem2[0].innerHTML = '<table class="logtable33"><thead><tr class="logDate"><th>항목</th><th>평가 기록</th></tr></thead><tbody><tr class="logValue1"><td><ul class="chart-select"></ul></td><td><div class="Gchart1"></div><div class="Gchart2 D-NONE"></div></tr></tbody></table>'
    for(var i in Q33){
      var logDate = $(".logtable33 .logDate")[i];
      var logValue1 = $(".logtable33 .logValue1")[i];
      var logValue2 = $(".logtable33 .logValue2")[i];
      let temp = [];
      for(var j=0; j<logseq2;j++){
        temp.push([Number(results2[0][j]),Number(results_values2[i][j]),Number(results_values3[i][j]),]);
      }
    }
    var multi1 = $('.logtable33 .logValue1 .Gchart1')[0];
    var chart1 = new MULTIDATA(results_values2, multi1, Q33, label);
    var multi2 = $('.logtable33 .logValue1 .Gchart2')[0];
    var chart2 = new MULTIDATA(results_values3, multi2, Q33, label);
    for(var i in Q33){
        $(".logtable33 .logValue1 .chart-select")[0].innerHTML += String("<li><label><input type='checkbox' id='idx"+i+"' onclick={doupdate2(results_values2,multi1,results_values3,multi2,Q33,label)} value='"+ label[Q33[i]] +"'>"+label[Q33[i]]+"</label></li>");
    } 
</script>
`;

return html;
});

module.exports = userLog;