function getFilteredDiseases(page) {
    if (page==undefined) {
        page=0;
    }
    window.location.href = 'filterDiseases?diseaseName=' + $("#diseaseName").val() + '&geneSymbol=' + $("#geneSymbol").val()
    + '&fromDate=' + $("#fromDate").val() + '&toDate=' + $("#toDate").val() + '&page=' + page;
    return false;
}

//encodeURIComponent

var renderGene = function(r, n) {
            var set = r.set().push(
                r.rect(n.point[0]-30, n.point[1]-13, 60, 44).attr({"fill": "#feb", r : "12px", "stroke-width" : n.distance == 0 ? "3px" : "1px" })).push(
                r.text(n.point[0], n.point[1] + 10, (n.label || n.id)));
            set.click(function(){console.log(n.id)});
            return set;
        };
        
var renderDisease = function(r, n) {
            var set = r.set().push(
                r.rect(n.point[0]-30, n.point[1]-13, 60, 44).attr({"fill": "#bcf", r : "12px", "stroke-width" : n.distance == 0 ? "3px" : "1px" })).push(
                r.text(n.point[0], n.point[1] + 10, (n.label || n.id)));
            return set;
        };

//draw grph from list [gene, disease]
function drawGraph(geneDiseaseList) {
    var width = 500;
    var height = 500;
    
    var g = new Graph();
    
    /* modify the edge creation to attach random weights */
    g.edgeFactory.build = function(source, target) {
        var e = jQuery.extend(true, {}, this.template);
        e.source = source;
        e.target = target;
        //e.style.label = e.weight = Math.floor(Math.random() * 10) + 1;
        return e;
    }
    
    for (var item in geneDiseaseList) {
        g.addNode(geneDiseaseList[item][0], {render:renderGene});
        g.addNode(geneDiseaseList[item][1], {render:renderDisease});
    }

    for (var item in geneDiseaseList) {
        g.addEdge(geneDiseaseList[item][0], geneDiseaseList[item][1]);
    }
    //g.addEdge("Tokyo", "Tel Aviv"/*, {weight:9, directed: true, stroke : "#bfa"}*/); // also supports directed graphs, but currently doesn't look that nice

    /* layout the graph using the Spring layout implementation */
    var layouter = new Graph.Layout.Spring(g);
    
    var renderer = new Graph.Renderer.Raphael('canvas', g, width, height);
    renderer.draw();
}