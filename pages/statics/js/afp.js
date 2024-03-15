const Render = require('./render');
const Render16 = require('./render16');
const event = require('./event');

var fs = require('fs');
const views = "public/views"

const afp33 = (function(idex, message, response, list,result_grades,python_data,category_index, id){  //pyshell 데이터 처리 및 출력
    var res = decodeURI(message);
    python_data[0].push(String("'"+idex+"'"));
    python_data[1].push(res);
  //  var id = 'ccccc';//request.body.id;

    for (var i in python_data[1].slice(0,-1)){
      if(i>11 && i<34){
        python_data[1][i] = String(python_data[1][i].split(" ")[0]);
      }
    }
  
   if (['사용자이름','신뢰도','등급'].includes(idex)){  
      list.push([idex,res]);
      return ;
   }
   else if(idex === '방향'){
    console.log('python data : '+'받은 이름 개수 '+ python_data[0].length +' 받은 값 개수 '+ python_data[1].length);
    python_data[0].pop();
    python_data[0].pop();
    directions = python_data[1].pop();
    branch = python_data[1].pop().split('], [')
    console.log('get data from python');
    console.log('Result Rendering...')
    try{
      html =  Render.RenderHtml(list,python_data,category_index,result_grades,branch,directions, id);
      fs.readFile(views+"/chart.html", 'utf8', function(err, description){
        if(err){
          console.log(err);
        } else {
          console.log("@@@@@@@@@@@@@@@@");
          if(typeof(id)=="string") console.log('No insert');
          else event.insertAFP33(python_data, id);
          console.log("Response Send to Client");
          response.send(description+html);
          console.log("#################");
        }
        });
    }
    catch{
      fs.readFile(views+"/500.html", 'utf8', function(err, description){
        if(err){
            console.log(err);
        } else {
            console.log("@@@@@@@@@@@@@@@@");
            console.log(err);
            console.log("Response Crushed");
            response.status(500).send(description);
            console.log("#################");
          }
        });
      }
   }
   else if(idex!="비질환자 평균" && idex!="연속형 분기"){
    result_grades.push([idex,res]);
    return ;
    }
   else return ;
  });


const afp16 = (function(idex, message, response, list,python_data,id){  //pyshell 데이터 처리 및 출력
    var res = decodeURI(message);
    python_data[0].push(String("'"+idex+"'"));
    python_data[1].push(res);

   if (['사용자이름','분류','등급'].includes(idex)){  
      list.push([idex,res]);
      return ;
   }
   else if(idex=="비질환자 평균"){
        console.log('python data : '+'받은 KEY 개수 '+ python_data[0].length +' 받은 VALUE 개수 '+ python_data[1].length);  
        console.log('get data from python');
        console.log('Result Rendering...');
  
    try{
      html = Render16.RenderHtml(list,python_data, id);
      fs.readFile(views+"/chart16.html", 'utf8', function(err, description){
        if(err){
          console.log(err);
        } else {
          console.log("@@@@@@@@@@@@@@@@");
          if(typeof(id)=="string") console.log('No insert');
          else event.insertAFP16(python_data, id);
          console.log("Response Send to Client");
          response.send(description+html);
          console.log("#################");
        }
        });
    }
    catch(e){
      fs.readFile(views+"/500.html", 'utf8', function(err, description){
        if(err){
            console.log(err);
        } else {
          console.log("@@@@@@@@@@@@@@@@");
            console.log(e);
            console.log("Response Crushed");
            response.status(500).send(description);
            console.log("#################");
          }
        });
      }
    }
   else return ;
  });

  module.exports.AFP33 = afp33;
  module.exports.AFP16 = afp16;