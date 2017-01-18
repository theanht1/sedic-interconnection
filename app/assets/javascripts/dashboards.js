$(document).ready(function(){

  var s = new sigma({
    renderer: {
      container: 'network-container',
      type: 'canvas'
    },
    settings: sigmaSettings
  });

  $("#submit").on('ajax:success', function(event, data, status, xhr){
    // console.log(data['geo']);
    // console.log(data['edges']);
    
    // Clear current network
    s.kill();

    var geos = data['geo'];
    var edges = data['edges'];
    var nNode = geos.length;
    var nEdge = edges.length;

    function isNeighbor(x, y) {
      return Math.abs(geos[x][1] - geos[y][1]) + Math.abs(geos[x][2] - geos[y][2]) == 1;
    }
    var g = {
      nodes: [],
      edges: []
    };

    var xSpace = 100;
    var ySpace = 100;
    for (var i = 0; i < nNode; i++) {
      g.nodes.push({
        id: 'n' + geos[i][0],
        label: 'node ' + geos[i][0],
        x: geos[i][1] * xSpace,
        y: geos[i][2] * ySpace,
        size: 1,
        color: '#666'
      });
    }


    for (var i = 0; i < nEdge; i++) {
      var x = edges[i][0], y = edges[i][1];
      var type;
      
      if (isNeighbor(edges[i][0], edges[i][1]))
        type = 'line';
      else
        type = 'curve';
      g.edges.push({
        id: 'e' + i,
        // label: 'edge ' + edges[i][0] + ' : ' + edges[i][1],
        source: 'n' + edges[i][0],
        target: 'n' + edges[i][1],
        color: '#ccc',
        size: 2,
        hover_color: '#000',
        type: type
      })
    }

    s = new sigma({
      graph: g,
      renderer: {
        container: 'network-container',
        type: 'canvas'
      },
      settings: sigmaSettings
    });

    // s.bind('overNode', function(e){
    //   console.log(e.data);
    // });
  });
  
  $("#submit").on("ajax:error", function(event, xhr, status, error){
    console.log("Error occured");
  });

});
