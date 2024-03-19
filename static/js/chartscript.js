Chart.pluginService.register({
    beforeDraw: function (chart) {
        if (chart.config.options.elements.center) {
    //Get ctx from string
    var ctx = chart.chart.ctx;

    //Get options from the center object in options
    var centerConfig = chart.config.options.elements.center;
      var fontStyle = centerConfig.fontStyle || 'Arial';
    var txt = centerConfig.text;
    var color = centerConfig.color || '#000';
    var sidePadding = centerConfig.sidePadding || 20;
    var sidePaddingCalculated = (sidePadding/100) * (chart.innerRadius * 2)
    //Start with a base font of 30px
    ctx.font = "20px " + fontStyle;

    //Get the width of the string and also the width of the element minus 10 to give it 5px side padding
    var stringWidth = ctx.measureText(txt).width;
    var elementWidth = (chart.innerRadius * 2) - sidePaddingCalculated;

    // Find out how much the font can grow in width.
    var widthRatio = elementWidth / stringWidth;
    var newFontSize = Math.floor(30 * widthRatio);
    var elementHeight = (chart.innerRadius * 0.5);

    // Pick a new font size so it will not be larger than the height of label.
    var fontSizeToUse = Math.min(newFontSize, elementHeight);

    //Set font settings to draw it correctly.
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    
    var centerX = ((chart.chartArea.left + chart.chartArea.right) /1.9);
    var centerY = ((chart.chartArea.top + chart.chartArea.bottom)/1.4);
    ctx.font = fontSizeToUse+"px " + fontStyle;
    ctx.fillStyle = color;

    //Draw text in center
    ctx.fillText(txt, centerX, centerY);
        }
    }
});

if (sessionStorage.key('User')){
  console.log("Login User:"+sessionStorage['User']);
  $("#menu-section")[0].setAttribute('include-html', "views/topbar-login.html");
  }
else{
  console.log("No Login");
}

includeHTML( function () {
    if (sessionStorage.key('User')){
        $("#Login-Section").text("환영합니다. " + sessionStorage['User']);
    }
    else{

    }
    includeRouter( function () {
// do something in the future
        });
    });

function getBoxWidth(labelOpts, fontSize) {
  return labelOpts.usePointStyle ?
    fontSize * Math.SQRT2 :
  labelOpts.boxWidth;
};

Chart.NewLegend = Chart.Legend.extend({
  afterFit: function() {
    this.height = this.height + 15;
  },
});

function createNewLegendAndAttach(chartInstance, legendOpts) {
  var legend = new Chart.NewLegend({
    ctx: chartInstance.chart.ctx,
    options: legendOpts,
    chart: chartInstance
  });
  
  if (chartInstance.legend) {
    Chart.layoutService.removeBox(chartInstance, chartInstance.legend);
    delete chartInstance.newLegend;
  }
  
  chartInstance.newLegend = legend;
  Chart.layoutService.addBox(chartInstance, legend);
}

// Register the legend plugin
Chart.plugins.register({
  beforeInit: function(chartInstance) {
    var legendOpts = chartInstance.options.legend;

    if (legendOpts) {
      createNewLegendAndAttach(chartInstance, legendOpts);
    }
  },
  beforeUpdate: function(chartInstance) {
    var legendOpts = chartInstance.options.legend;

    if (legendOpts) {
      legendOpts = Chart.helpers.configMerge(Chart.defaults.global.legend, legendOpts);

      if (chartInstance.newLegend) {
        chartInstance.newLegend.options = legendOpts;
      } else {
        createNewLegendAndAttach(chartInstance, legendOpts);
      }
    } else {
      Chart.layoutService.removeBox(chartInstance, chartInstance.newLegend);
      delete chartInstance.newLegend;
    }
  },
  afterEvent: function(chartInstance, e) {
    var legend = chartInstance.newLegend;
    if (legend) {
      legend.handleEvent(e);
    }
  }
});