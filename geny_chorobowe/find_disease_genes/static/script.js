function getFilteredDiseases(page) {
    if (page==undefined) {
        page=0;
    }
    window.location.href = 'filterDiseases?diseaseName=' + $("#diseaseName").val() + '&geneSymbol=' + $("#geneSymbol").val()
    + '&fromDate=' + $("#fromDate").val() + '&toDate=' + $("#toDate").val() + '&page=' + page;
    return false;
}

//encodeURIComponent

//draw grph from list [gene, disease]
function drawGraph(geneDiseaseList, genes, diseases) {
    var width = 500;
    var height = 500;
    
    var g = new Graph();
    
    var renderGene = function(r, n) {
            var set = r.set().push(
                r.rect(n.point[0]-30, n.point[1]-13, 60, 44).attr({"fill": "#feb", r : "12px", "stroke-width" : n.distance == 0 ? "3px" : "1px" })).push(
                r.text(n.point[0], n.point[1] + 10, (n.label || genes[n.id])));
            set.click(function(){ window.location.href = 'geneDetails?id=' + n.id});
            return set;
        };
        
    var renderDisease = function(r, n) {
            var set = r.set().push(
                r.rect(n.point[0]-30, n.point[1]-13, 60, 44).attr({"fill": "#bcf", r : "12px", "stroke-width" : n.distance == 0 ? "3px" : "1px" })).push(
                r.text(n.point[0], n.point[1] + 10, (n.label || diseases[n.id])));
                set.click(function(){ window.location.href = 'diseaseDetails?id=' + n.id});
            return set;
        };
    
    /* modify the edge creation to attach random weights */
    g.edgeFactory.build = function(source, target) {
        var e = jQuery.extend(true, {}, this.template);
        e.source = source;
        e.target = target;
        //e.style.label = e.weight = Math.floor(Math.random() * 10) + 1;
        return e;
    }
    
    for(var item in diseases){
        g.addNode(item, {render:renderDisease});
    }
    
    for(var item in genes){
        g.addNode(item, {render:renderGene});
    }

    for (var item in geneDiseaseList) {
        g.addEdge(geneDiseaseList[item][0], geneDiseaseList[item][1]);
    }
    //g.addEdge("Tokyo", "Tel Aviv"/*, {weight:9, directed: true, stroke : "#bfa"}*/); // also supports directed graphs, but currently doesn't look that nice

    /* layout the graph using the Spring layout implementation */
    var layouter = new Graph.Layout.Spring(g);
    
    var renderer = new Graph.Renderer.Raphael('canvasGraph', g, width, height);
    renderer.draw();
}

function getGraphDataForGene(geneID, level) {
    var url = '/getGraphDataForGene';
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'GET',
        data: {
            id: geneID,
            level: level
        },
        success: getGraphDataResponse,
    });
}

function getGraphDataForDisease(diseaseID, level) {
    var url = 'getGraphDataForDisease';
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'GET',
        data: {
            id: diseaseID,
            level: level
        },
        success: getGraphDataResponse,
    });
}

function getGraphDataResponse(result,status,xhr) {
    if (result.error == null) {
        drawGraph(result.data.connections, result.data.genes, result.data.diseases);
    }
}

function drawSourceTimeLine(sources, sourcesNames) {
    var data=[];
    var density = [];
    var dataDensity={};
    if(sources[1]!=undefined){
        var start = (new Date(sources[1])).getTime();
        var stop = (new Date(sources[Object.keys(sources).length])).getTime();
        var interval = (start - stop)/20;
        for(var i=1; i<20; i=i+2){
            dataDensity[start - i*interval] = 0;
        }
        stop = start - 2*interval;
        for (var i in sources){
            var date = new Date(sources[i]);
            data.push({x: date, y: 1, indexLabel: i, markerColor : "red", label: sourcesNames[i]});
            while(!(date.getTime() > stop && date.getTime() <= start)){
                start = stop;
                stop = stop - 2*interval;
            }
            dataDensity[start - interval]+=1;
        }
        for(var i in dataDensity){
            density.push({x: (new Date()).setTime(i), y: dataDensity[i], indexLabel: dataDensity[i], markerColor : "red", label:"hjgjgjug"});
        }
    }
    //console.log(sourcesNames);
    var chart = new CanvasJS.Chart("sourcesTimeline",
    {
      title:{
      text: "Sources timeline"
      },
      tooltip:{
        content : "{label}",
	enabled: true
      },
      axisX: {
      },
      axisY:{
        //maximum : 2,
        //minimum: -1,
        interval : 1,
        includeZero: true,
      },
      data: [
      {
        type: "spline",
        dataPoints: density,
      },
      {
        type: "line",
        dataPoints: data,
      },
      ]
    });

    chart.render();
}

function update_data_base(){
    updateClinvar();
    $("#updateResult").text("Updating clinvar. It can take a while ...");
}

function updateMedgen() {
    var url = 'update_medgen';
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'GET',
        success: updateMedgenResponse,
    });
    $("#updateResult").text("Updating medgen. It can take a while ...");
}

function updateClinvar() {
    var url = 'update_clinvar';
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'GET',
        success: updateClinvarResponse,
    });
    $("#updateResult").text("Updating clinvar. It can take a while ...");
}

function updateClinvarResponse(result,status,xhr){
    if("result" in result && result["result"]=="OK"){
        $("#updateResult").text("Clinvar updated.  Refreshing site ...");
        window.location.href = "/";
        return;
    }
    if("error" in result){
        $("#updateResult").text(result["error"]);
    }
}

function updateMedgenResponse(result,status,xhr){
    if("result" in result && result["result"]=="OK"){
        $("#updateResult").text("Update finished. Refreshing site ...");
        window.location.href = "/";
        return;
    }
    if("error" in result){
        $("#updateResult").text(result["error"]);
    }
}
