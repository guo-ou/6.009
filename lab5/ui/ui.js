"use strict";

// RPC wrapper
function invoke_rpc(method, args, timeout, on_done) {
  hide($("#crash"));
  hide($("#timeout"));
  show($("#rpc_spinner"));
  //send RPC with whatever data is appropriate. Display an error message on crash or timeout
  var xhr = new XMLHttpRequest();
  xhr.open("POST", method, true);
  xhr.setRequestHeader('Content-Type', 'application/json; charset=UTF-8');
  xhr.timeout = timeout;
  xhr.send(JSON.stringify(args));
  xhr.ontimeout = function () {
    show($("#timeout"));
    hide($("#rpc_spinner"));
    hide($("#crash"));
  };
  xhr.onloadend = function () {
    if (xhr.status === 200) {
      hide($("#rpc_spinner"));
      var result = JSON.parse(xhr.responseText);
      hide($("#timeout"));
      if (typeof (on_done) != "undefined") {
        on_done(result);
      }
    } else {
      show($("#crash"));
    }
  };
}

// Resource load wrapper
function load_resource(name, on_done) {
  var xhr = new XMLHttpRequest();
  xhr.open("GET", name, true);
  xhr.onloadend = function () {
    if (xhr.status === 200) {
      var result = JSON.parse(xhr.responseText);
      on_done(result);
    }
  };
  xhr.send();
}


function hide($object) {
  $object.css({
    display: 'none'
  });
}

function show($object) {
  $object.css({
    display: 'inline-block'
  });
}

// Code that runs first
$(document).ready(function(){
    invoke_rpc( "/restart", {}, 0, function() { init(); } );
});

function restart(){
  invoke_rpc( "/restart", {} );
}

//  LAB CODE

function message_out(text, bad){
  var elt = $("#message_out");
  elt.text(text);
  if (bad) {
    elt.addClass("bad");
  } else {
    elt.removeClass("bad");
  }
}

function find_assignment(){
  // gracefully choose 0 if K is not a number
  var K = Math.max(parseInt(document.getElementById("K").value) || 0, 0);

  var assignment_handler = function( assignment ){
    generateColors(assignment);
    updateGraph(assignment);

    var text = "";
    if (assignment){
      text = "Okay! Your assignment uses " +
        Object.keys(managerColors).length +
        " managers!";
    } else {
      text = "We don't seem to have enough managers! :(";
    }

    message_out(text, !assignment);
  };

  var args = { "K": K, "db_name": selected_db_name };
  invoke_rpc( "/ui_assign", args, 0, assignment_handler);
}

var name_mappings = {};
var selected_db_name;
var graphs = {};
var managerColors = {};

function set_db(db_name) {
  $("#db").html(db_name);
  selected_db_name = db_name;
  setGraph();
  message_out("", false);
}

function init(){
  var list_db_names = function (db_names_list) {
    db_names_list.forEach(function(db_name) {
      $("#dbs")
        .append(
          $("<li class=\"mdl-menu__item\"" +
          " onclick=\"set_db('" + db_name + "')\">" +
          db_name +
          "</li>"));
    });

    selected_db_name = db_names_list[0];
  };

  invoke_rpc("/ui_list_db_names", {}, 0, list_db_names);

  // actual data for d3graph
  var dbs_callback = function( dbs ) {
    graphs = {};
    for (var name in dbs) {
      graphs[name] = convert_to_d3graph(get_actor_to_coactors(dbs[name]));
    }
    set_db(selected_db_name);
  };

  invoke_rpc( "/ui_list_dbs", {}, 0, dbs_callback);
}

function setGraph() {
  var graph = graphs[selected_db_name];
  window.graph = graph;
  drawForce(graph);
}

function get_actor_to_coactors(database) {
  var a_to_c = {};
  database.forEach(function(datum) {
    var actor1 = datum[0];
    var actor2 = datum[1];
    if (!(actor1 in a_to_c)) {
      a_to_c[actor1] = [];
    }
    if (!(actor2 in a_to_c)) {
      a_to_c[actor2] = [];
    }

    a_to_c[actor1].push(actor2);
    a_to_c[actor2].push(actor1);
  });

  return a_to_c;
}

function convert_to_d3graph(graph) {
  var order = {};

  var d3graph = {
    "nodes": [],
    "links": []
  };

  var counter = 0;
  for (var actorid in graph){
    d3graph["nodes"].push({
      "value": actorid,
      "manager": -1
    })
    order[actorid] = counter
    counter += 1
  }

  for (var actorid in graph) {
    graph[actorid].forEach(function(coactorid) {
      d3graph["links"].push({
        "source": order[actorid],
        "target": order[coactorid],
        "value": 1,
        "edge_color": "#999"
      });
    });
  }

  return d3graph
}

// =================================================================
// D3-related code
// =================================================================

function generateColors(assignment){
  // algorithm from https://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors
  var colors = {};
  if (!assignment) {
    managerColors = colors;
    return;
  }

  for (var actor in assignment) {
    colors[assignment[actor]] = "#000000";
  }

  var numColors = Object.keys(colors).length;

  var i = 0;
  for (var actor in assignment) {
    i += (360 / numColors)

    var h = i;
    var s = 0.4 + Math.random() * 0.2;
    var l = 0.4 + Math.random() * 0.2;

    colors[assignment[actor]] = d3.hsl(h, s, l).toString();
  }

  managerColors = colors;
}

function getColor(managerNum){
  if (managerNum == -1) {
    return "#aec7e8";
  }
  return managerColors[managerNum];
}

function getValuebyId(val){
  if (window.graph) {
    return window.graph.nodes[val].value;
  } else { return null; }
}

var force;

function handle_resize(){
  var width = document.getElementById('graph').offsetWidth;
  var height = document.getElementById('graph').offsetHeight;
  force.size([width, height]).resume();
}
window.onresize = handle_resize;

function drawForce(graph) {
  var svg = d3.select("#graph")
              .html('')
              .append("svg")
              .attr("width", "100%")
              .attr("height", "80ex");

  force = d3.layout.force()
                    .charge(-120)
                    .linkDistance(50);

  handle_resize();

  force.nodes(graph.nodes)
       .links(graph.links)
       .start();

  var link = svg.selectAll(".link")
                .data(graph.links)
                .enter().append("line")
                .attr("class", "link")
                .attr('stroke', function (d) {
                  return d.edge_color;
                })
                .style("stroke-width", function (d) {
                  return Math.sqrt(d.value);
                });

  var node = svg.selectAll(".node")
                .data(graph.nodes)
                .enter().append("circle")
                .attr("class", "node")
                .attr("r", 8)
                .style("fill", function (d) {
                  return getColor(d.manager);
                })
                .call(force.drag);

  node.append("title") .text(
    function (d) {
      var text = d.value + ": ";
      if (d.manager >= 0) {
        return text + "Manager " + d.manager;
      }
      return text + "No manager";
    });

  force.on("tick", function () {
          link.attr("x1", function (d) {
              return d.source.x;
          })
       .attr("y1", function (d) {
          return d.source.y;
       })
       .attr("x2", function (d) {
          return d.target.x;
       })
       .attr("y2", function (d) {
          return d.target.y;
       });

       node.attr("cx", function (d) { return d.x; })
           .attr("cy", function (d) { return d.y; });
  });
}

function updateGraph(assignment) {
  if (window.graph) {
    var graph = window.graph;

    // reset the graph
    // clear selected nodes
    for (var i = 0; i < graph.nodes.length; i++) {
      graph.nodes[i].manager = -1;
    }

    if (assignment) {
      // color the nodes with their managers
      for (var i = 0; i < graph.nodes.length; i++) {
        var g_val = graph.nodes[i].value;
        graph.nodes[i].manager = assignment[g_val];
      }
    }

    drawForce(graph);
  }
}

