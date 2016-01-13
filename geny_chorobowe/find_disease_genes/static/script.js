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
    data=[];
    for (var i in sources){
        data.push({x: new Date(sources[i]), y: 1, indexLabel: i, markerColor : "red"});
    }
    //console.log(sourcesNames);
    var chart = new CanvasJS.Chart("sourcesTimeline",
    {
      title:{
      text: "Sources timeline"
      },
      tooltip:{
        content : "jhfbejrhfv",
      },
      axisX: {
      },
      axisY:{
        maximum : 2,
        interval : 1,
        includeZero: false
      },
      data: [
      {
        type: "line",
        dataPoints: data,
      }
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
}

function updateClinvar() {
    var url = 'update_clinvar';
    $.ajax({
        url: url,
        dataType: 'json',
        type: 'GET',
        success: updateClinvarResponse,
    });
}

function updateClinvarResponse(result,status,xhr){
    if("result" in result && result["result"]=="OK"){
        updateMedgen();
        $("#updateResult").text("Clinvar updated. Updating medgen. It can take a while ...");
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