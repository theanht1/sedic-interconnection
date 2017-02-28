$(document).ready(function(){
  

  var s = new sigma({
    renderer: {
      container: 'network-container',
      type: 'canvas'
    },
    settings: sigmaSettings
  });

  function clear(s) {
    if (s.graph.nodes().length > 0) s.kill();
  }

  $("#submit").on('ajax:success', function(event, data, status, xhr){
    // console.log(data['geo']);
    // console.log(data['edges']);
    
    // Clear current network
    clear(s);

    var geos = data['geo'];
    var edges = data['edges'];
    var nNode = geos.length;
    var nEdge = edges.length;

    function isNeighbor(x, y) {
      if (!geos[x] || !geos[y]) return true;
      return Math.abs(geos[x][1] - geos[y][1]) + Math.abs(geos[x][2] - geos[y][2]) == 1;
    }
    var g = {
      nodes: [],
      edges: []
    };

    var xSpace = 70;
    var ySpace = 50;
    for (var i = 0; i < nNode; i++) {
      g.nodes.push({
        id: 'n' + geos[i][0],
        label: 'n' + geos[i][0],
        x: geos[i][1] * xSpace,
        y: geos[i][2] * ySpace,
        size: 1,
        color: '#666'
      });
    }


    for (var i = 0; i < nEdge; i++) {
      var x = edges[i][0], y = edges[i][1];
      if (x >= nNode || y >= nNode) continue;
      var type;
      
      var isRandom = false;
      if (isNeighbor(edges[i][0], edges[i][1])) {
        type = 'line';
      }
      else {
        type = 'curve';
        isRandom = true
      }

      g.edges.push({
        id: 'e' + i,
        label: 'e' + edges[i][0] + ':' + edges[i][1],
        source: 'n' + edges[i][0],
        target: 'n' + edges[i][1],
        color: '#ccc',
        size: 2,
        hover_color: '#000',
        type: type,
        is_random: isRandom,
        probility: edges[i][2]
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

    console.log(s.graph);
    s.bind('overNode', function(e){
      console.log(e.data);
    });

    // s.bind('clickNode', function(e){
    //   console.log(e.data);
    //   e.data.node.active;
    // });

    s.bind('clickEdge', function(e){
      console.log(e.data);
      console.log(e.data.edge);

      edge = e.data.edge;
      if (edge.is_random == true) {
        $('#edge-click').empty();
        var formAppend = '<div class="input-group"> <span class="input-group-addon">Source</span><input disabled="true" value=' + edge.source + '></div><div class="input-group"> <span class="input-group-addon">Target</span><input disabled="true" value=' + edge.target + '></div><div class="input-group"> <span class="input-group-addon">Probility</span><input disabled="true" value=' + edge.probility + '></div>';

        // "Source: " + edge.source + "<hr>Target: " + edge.target + 
                         // "<hr>Probility: " + edge.probility;
        $('#edge-click').append(formAppend);
      }
    });
  });
  
  $("#clear").on("click", function(event){
    event.preventDefault();
    console.log("Clear");
    clear(s);
  });

  $("#submit").on("ajax:error", function(event, xhr, status, error){
    console.log("Error occured");
  });
});


function showTorusForm() {
  $("#torus-options").attr("class", "show");
}

function hideTorusForm() {
  $("#torus-options").attr("class", "hide");
}

function topoTypeChange(e) {
  if (e.selectedIndex == 0)
    showTorusForm();
  else
    hideTorusForm();
}

function toggleLinkProb() {
  if ($('#link-prob').attr("class") == "show") {
    $('#link-prob').attr("class", "hide");
  }
  else {
    $('#link-prob').attr("class", "show");
  }
}

function nLinkChange(e) {
  console.log(e.value);
  $("#link-prob").empty();
  var formAppend = "";
  for (var i = 1; i <= e.value; i++) {
    formAppend += "<div class='input-group'> <span class='input-group-addon'>Link " + i + "</span> <input type='number' name='opts[probs][" + i + "]' value='0.2' step='0.01'> </div>";
  }
  $("#link-prob").append(formAppend);
}
