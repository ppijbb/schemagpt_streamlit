function BASIC_CHART(arr, target){
    function drawBackgroundColor() {
         var data = new google.visualization.DataTable();
             data.addColumn('number', 'seq');
             data.addColumn('number', 'value');
             data.addRows(arr);
             var options = {
                 hAxis: {
                     title: '회차',
                 },
                 vAxis: {
                     //   title: '점수'
                     ticks : [1,2,3,4]
                 },
                 backgroundColor: '#f1f8e9',
                 height: 400,
                 width: 700,
                 chartArea: { width: '80%', left: 20, height: '75%' },
                 trendlines: {
                     0: {
                         type: 'linear',
                         color: 'green',
                         lineWidth: 3,
                         opacity: 0.3,
                         visibleInLegend: true
                     },
                 },
                 annotations: { 'column_id': { style: 'line' } }
             };
             var chart = new google.visualization.LineChart(target);
             chart.draw(data, options);
         }
     function chart(){
     google.charts.load('current', { packages: ['corechart', 'line'] });
     google.charts.setOnLoadCallback(drawBackgroundColor);
     }
     return chart();
 }


function DETAIL_CHART(arr, target){
   function drawBackgroundColor() {
        var data = new google.visualization.DataTable();
            data.addColumn('number', 'seq');
            data.addColumn('number', 'value');
            data.addColumn('number', 'value2');
            data.addRows(arr);

            var options = {
                hAxis: {
                    title: '회차',
                },
                vAxis: {
                    //   title: '점수'
                },
                backgroundColor: '#f1f8e9',
                height: 400,
                width: 700,
                chartArea: { width: '80%', left: 20, height: '75%' },
                trendlines: {
                    // 0: {
                    //     type: 'linear',
                    //     color: 'green',
                    //     lineWidth: 3,
                    //     opacity: 0.3,
                    //     visibleInLegend: true
                    // },
                    // 1: {
                    //     type: 'linear',
                    //     color: 'black',
                    //     lineWidth: 3,
                    //     opacity: 1,
                    //     visibleInLegend: false
                    // }
                },
                annotations: { 'column_id': { style: 'line' } }
            };
            var chart = new google.visualization.LineChart(target);
            chart.draw(data, options);
        }
    function chart(){
    google.charts.load('current', { packages: ['corechart', 'line'] });
    google.charts.setOnLoadCallback(drawBackgroundColor);
    }
    return chart();
}

function MULTIDATA(values, target, Q, label){
    function drawBackgroundColor() {
        var data = new google.visualization.DataTable();
        let seq = values[0];
        data.addColumn("string", "X");
        for(let i=0; i<seq.length; i++)
           data.addColumn("number", `seq${i+1}`);

        // data.addColumn("number", "Cats");
        data.addRows(Object.keys(values).length);
        let g = seq.length-3;
        let absseq={}
        for (let i = g; i < seq.length; i++) {
          let absdata = {}
          for(let n=0; n<values.length; n++){
            absdata[label[Q[n]]] = Math.abs(values[n][i]-values[n][i-1]);
          }
          absseq[i-g] = absdata;
        }

        for(let as in absseq){
          absseq[as] = Object.entries(absseq[as])
                      .sort(([,a],[,b])=>a-b)
                        .reduce((r,[k,v])=>({...r,[k]:v}),{});
          }
        
        // for (let i = 0; i < Object.keys(absseq).length; i++) {
        //   // data.setCell(i, 0, i+1);
        //   for(let n = Object.keys(absseq[i]).length-5  ; n < Object.keys(absseq[i]).length; n++){
        //     console.log(i,"/",Object.keys(absseq[i])[n]);
        //     data.setCell(i,0,Object.keys(absseq[i])[n]);
        //     data.setCell(i,1,Object.values(absseq[i])[n]);
        //   }
        // }
        console.log(values);
        for (let i = 0 ; i < Object.keys(values).length; i++) {
          for(let n=0; n<seq.length; n++){
            data.setCell(i,0,label[Q[i]]);
            data.setCell(i,n+1,values[i][n]);
          }
        }
        console.log(data)
        var len = seq.length+1;
        var htick = [];
        for(let h = 1; h<=seq.length; h++){
          htick.push(h);
        }
        var options = {
          // isStacked:'percent',
          // hAxis: {
          //   title: "회차",
          //   // ticks : htick,
          // },
          // vAxis: {
          //   title: '수치'
          // },
          seriesType: 'candlesticks',
          series: {len: {type: 'line'}},
          backgroundColor: "white",//"#f1f8e9",
          height: 430,
          width: 700,
          // lineWidth:5,
          // bar:{
          //   groupWidth:"95%"
          // },
          orientation:"horizontal",
          chartArea: { width: "75%", left: 40, height: "75%" },
          // trendlines: {
          //   0: {
          //     type: "linear",
          //     color: "green",
          //     lineWidth: 3,
          //     opacity: 0.3,
          //     visibleInLegend: true,
          //   },
          //   1: {
          //     type: "linear",
          //     color: "black",
          //     lineWidth: 3,
          //     opacity: 1,
          //     visibleInLegend: false,
          //   },
          // },
          legend:'none',
          // annotations: { column_id: { style: "bar" } },
        };
      
        var chart = new google.visualization.CandlestickChart(
          target
        );
        chart.draw(data, options);
      }     
      
      function chart(){
        google.charts.load('current', { packages: ['corechart', 'bar'] });
        google.charts.setOnLoadCallback(drawBackgroundColor);
      }
      return chart();
}

function CHARTUPDATE(func){
  function chart(){
  google.charts.load("current", { packages: ["corechart", "bar"] });
  google.charts.setOnLoadCallback(func);
  }
  return chart();
}

function doupdate(values, target, Q, label) {
  function drawBackgroundColor() {
    var data = new google.visualization.DataTable();
    data.addColumn("number", "X");
    for(var i in values)
      data.addColumn("number", label[Q[i]]);
    let seq = values[0];
    data.addRows(seq.length);

    for (let i = 0; i < seq.length; i++) {
      for(let n=0; n<values.length; n++){
      if ($(`input:checkbox[id="idx${n}"]`).is(":checked") == true) {
        data.setCell(i, 0, i+1);
        data.setCell(i, n+1, values[n][i]);
        } 
      else{
          data.setCell(i, n+1, 0);
        }
      }
    }
    var htick = [];
        for(let h = 1; h<seq.length; h++){
          htick.push(h);
        }
    var options = {
      hAxis: {
        title: "회차",
        ticks : htick
      },
      vAxis: {
        title: '수치',
      },
      backgroundColor: "white",//"#f1f8e9",
      height: 430,
      width: 700,
      lineWidth:5,
      chartArea: { width: "70%", left: 40, height: "75%" },
      trendlines: {
        // 0: {
        //   type: "linear",
        //   color: "green",
        //   lineWidth: 3,
        //   opacity: 0.3,
        //   visibleInLegend: true,
        // },
      },
      annotations: { column_id: { style: "bar" } },
    };

    var chart = new google.visualization.BarChart(
      target
    );
    chart.draw(data, options);
  }
  return CHARTUPDATE(drawBackgroundColor);
}

function doupdate2(values1, target1, values2, target2, Q, label) {
  return doupdate(values1,target1,Q,label), 
          doupdate(values2,target2,Q,label);
}