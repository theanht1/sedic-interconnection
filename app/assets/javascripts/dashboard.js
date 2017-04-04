var geos = [];
var edges = [];
var n_random_links;
var s;
var graph;

function newGraph(graph, settings) {
  return new sigma({
    graph: graph,
    renderer: {
      container: 'network-container',
      type: 'canvas'
    },
    settings: settings
  });
}

function createGraph(data) {
  geos = data['geos'];
  edges = data['edges'];
  n_random_links = data['n_random_links'];
  var nNode = geos.length;
  var nEdge = edges.length;

  function isNeighbor(x, y) {
    if (!geos[x] || !geos[y]) return true;
    return Math.abs(geos[x][1] - geos[y][1]) + Math.abs(geos[x][2] - geos[y][2]) == 1;
  }

  var graph = {
    nodes: [],
    edges: []
  };

  var xSpace = 70;
  var ySpace = 50;
  for (var i = 0; i < nNode; i++) {
    graph.nodes.push({
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
    if (edges[i][2] >= 0) isRandom = true;

    if (isNeighbor(edges[i][0], edges[i][1])) {
      type = 'line';
    }
    else {
      type = 'curve';        
    }

    var color = '#ccc';
    if (edges[i][2]) color = COLORS[edges[i][2]];
    graph.edges.push({
      id: 'e' + i,
      label: 'e' + edges[i][0] + ':' + edges[i][1],
      source: 'n' + edges[i][0],
      target: 'n' + edges[i][1],
      color: color,
      size: 2,
      hover_color: '#000',
      type: type,
      is_random: isRandom,
      nAlpha: edges[i][2],
      alpha: edges[i][3]
    })
  }
  return graph
}

function showResult(data) {
  $('#results').removeClass("hide");
  $('#diameter div input').attr('value', data["diameter"]);
  $('#total-path div input').attr('value', data["total_shortest_path"]);
  $('#average-path div input').attr('value', data["average_shortest_path"]);
  $('#average-path-alpha div input').attr('value', data["average_random_link_path"][0]);
  $('#average-path-alpha2 div input').attr('value', data["average_random_link_path"][1]);
}

function alphaViewToggle(n_random_links) {
  var alphaView = '<div class="input-group"> <span class="input-group-addon">View links</span>'
                  + '<select onchange="linkWithAlpha(this);" class="form-control">';
  for (var i = 0; i <= n_random_links; i++) {
    alphaView += '<option value=' + i + '>' + i + '</option>';

  }
  alphaView += '</select>' + '</div>';
  $("#alpha-view").empty();
  $("#alpha-view").append(alphaView);
}

function clear(s) {
  if (s.graph.nodes().length > 0) s.kill();
}

$(document).ready(function(){
  s = new sigma({
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
    clear(s);

    
    graph = createGraph(data);
    s = newGraph(graph, sigmaSettings);

    s.bind('overNode', function(e){
      console.log(e.data);
    });

    // s.bind('clickNode', function(e){
    //   console.log(e.data);
    //   e.data.node.active;
    // });

    s.bind('clickEdge', function(e){
      // console.log(e.data);
      console.log(e.data.edge);

      // edge = e.data.edge;
      // if (edge.is_random == true) {
      //   $('#edge-click').empty();
      //   var formAppend = '<div class="input-group"> <span class="input-group-addon">Source</span><input disabled="true" value=' + edge.source + '></div><div class="input-group"> <span class="input-group-addon">Target</span><input disabled="true" value=' + edge.target + '></div><div class="input-group"> <span class="input-group-addon">Alpha</span><input disabled="true" value=' + edge.alpha + '></div>';


      //   $('#edge-click').append(formAppend);
      // }
    });

    showResult(data);
    alphaViewToggle(n_random_links);

  });
  
  $("#clear").on("click", function(event){
    event.preventDefault();
    console.log("Clear");
    clear(s);
  });

  $("#submit").on("ajax:error", function(event, xhr, status, error){
    console.log("Error occured");
  });
 
  $("#upload").on("ajax:remotipartComplete", function(e, data){
    e.preventDefault();
    clear(s);
    data_json = eval('('+data.responseText+')');
    graph = createGraph(data_json);
    s = newGraph(graph, sigmaSettings);
    alphaViewToggle(data_json.n_random_links);
    showResult(data_json);
  });
});


function showTorusForm() {
  $("#torus-options").attr("class", "show");
}

function hideTorusForm() {
  $("#torus-options").attr("class", "hide");
}

function topoTypeChange(e) {
  if (e.selectedIndex == 0 || e.selectedIndex == 1)
    showTorusForm();
  else
    hideTorusForm();
}

function toggleLinkAlpha() {
  if ($('#link-alpha').attr("class") == "show") {
    $('#link-alpha').attr("class", "hide");
  }
  else {
    $('#link-alpha').attr("class", "show");
  }
}

function nLinkChange(e) {
  console.log(e.value);
  $("#link-alpha").empty();
  var formAppend = "";
  for (var i = 1; i <= e.value; i++) {
    formAppend += "<div class='input-group'> <span class='input-group-addon'>Link " + i + "</span> <input type='number' class='form-control' name='opts[alphas][" + i + "]' value='2' step='0.01'> </div>";
  }
  $("#link-alpha").append(formAppend);
}

function linkWithAlpha(e) {
  console.log(e.value);
  clear(s);
  s = newGraph(graph, sigmaSettings);
  if (e.value > 0) {
    // console.log(s.graph.edges().length);
    s.graph.edges().forEach(function(edge) {
      if (edge.nAlpha && edge.nAlpha == e.value) {
        // edge.color = COLORS[e.value];
      } else {
        s.graph.dropEdge(edge.id);
      }
    });
  }
  s.refresh();
}

$.ajaxSetup({
  beforeSend: function(xhr) {
    xhr.setRequestHeader('X-CSRF-Token',
   $('meta[name="csrf-token"]').attr('content'));
  }
});
