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

var step = 50;

var ghosting = false;
var debug = false;

var busy = false;
var emoji;
var pressed_keys = [];
var scale = 4;
var svg_width;
var svg_height;
var last_data;

var tile_size = 64;

var intervalId = null;

var DIRECTION_BUTTONS = [37,38,39,40];
var BUTTON_ON = "mdl-button--colored button-on";

// convert game data into svg
function display(data) {
    init_svg();
    var states = data[0];
    var state = states[0];
    var ref_state = states[1];
    $('#game-state').text(state).removeClass("warning");
    enable_forward_buttons();

    if (ghosting) {  
      if (ref_state) { 
        if (state != ref_state) {
          $('#game-state').text("should be " + ref_state + ", but is " + state + "!").addClass("warning");
        }
      } else {
        // ghost mode must be over
        disable_forward_buttons();
        if (intervalId) { // if it's running, pause it
          handle_pause_button();
        }
      }
    } 

    var blobs = data[1];

    var showGhosts = $('#show-ghosts').prop('checked');
    var showMain = $('#show-main').prop('checked');
    blobs = blobs.filter(function(blob) {
      // if it's a ghost and we're showing ghosts or
      // if it's not a ghost and we're showing normals
      return (!!blob.ghost && showGhosts) || (!blob.ghost && showMain);
    });

    // build list of svg for emoji
    var blist = [];
    blobs.forEach(function(blob) {
        // blob attributes: texture, rect
        var svg = emoji[blob.texture];
        if (svg === undefined) {
            console.log('no emoji for '+JSON.stringify(blob));
        } else {
            var x = blob.rect[0].toString();
            var y = (scale*svg_height - blob.rect[3] - blob.rect[1]).toString();
            var g = '<g transform="translate('+x+' '+y+')';
            var scalex = blob.rect[2]/tile_size;
            var scaley = blob.rect[3]/tile_size;
            if (scalex != 1 || scaley != 1) {
                g += 'scale('+scalex.toString()+' '+scaley.toString()+')';
            }
            g += '"';
            if (blob.ghost) {
                g += ' opacity="0.5"';
            }
            g += '>';
            g += svg;
            if (debug) {
                g += '<rect x="0" y="0" width="64" height="64" stroke="red" stroke-width="2" fill="none"/>';
                g += '<text x="-5" y="-5" text-anchor="end" stroke="red" fill="red">'+x.toString()+","+y.toString()+'</text>';
            }
            g += '</g>';
            blist.push(g);
        }
    });

    // update visualization
    var svg = '<svg width="' + 
            svg_width.toString() +
            '" height="' +
            svg_height.toString() +
            '" viewbox="0 0 ' +
            (scale*svg_width).toString() +
            ' ' +
            (scale*svg_height).toString() +
            '">' +
            blist.join('') +
            '</svg>';
    $('#wrapper').html(svg);
}

function init_svg() {
    var w = $('#wrapper');
    svg_width = w.width();
    svg_height = 3*svg_width/4;   // 4:3 aspect ratio
}

function debug_render() {
  if (last_data) {
    display(last_data);
  }
}

function disable_ghost_button(){
  $("#ghost").prop('disabled', true).css('visibility', 'hidden');
}

function enable_ghost_button(){
  $("#ghost").prop('disabled', false).css('visibility', 'visible');
}

function disable_forward_buttons(){
  $("#step_simulation").prop('disabled', true);
  $("#run_simulation").prop('disabled', true);
}

function enable_forward_buttons(){
  $("#step_simulation").prop('disabled', false);
  $("#run_simulation").prop('disabled', false);
}

function hide_all_simulate_buttons() {
  $("#step_simulation").css('display','none');
  $("#run_simulation").css('display','none');
  $("#pause_simulation").css('display','none');
}

function show_forward_buttons() {
  $("#pause_simulation").css('display','none');
  $("#run_simulation").css('display','inline-block');
  if (ghosting) {
    $("#step_simulation").css('display','inline-block');
  }
}

function show_pause_button() {
  $("#pause_simulation").css('display','inline-block');
  $("#run_simulation").css('display','none');
  $("#step_simulation").css('display','none');
}

function timestep(actions) {
    busy = true;

    init_svg();

    // translate pressed keys into action string
    if (actions === undefined) {
        actions = [];
        pressed_keys.forEach(function(keycode) {
            if (keycode >= 65 && keycode <= 90) actions.push(String.fromCharCode(keycode));
            else if (keycode == 8) actions.push('delete');        // del
            else if (keycode == 9) actions.push('tab');        // tab
            else if (keycode == 13) actions.push('enter');       // enter/return
            else if (keycode == 32) actions.push('space');        // space
            else if (keycode == 37) actions.push('left');   // left arrow
            else if (keycode == 38) actions.push('up');   // up arrow
            else if (keycode == 39) actions.push('right');   // right arrow
            else if (keycode == 40) actions.push('down');   // down arrow
        });
    }

    invoke_rpc('/timestep', [actions, ghosting, scale*svg_width, scale*svg_height], 500, function (data) {
        last_data = data;
        if (emoji) display(data);
        busy = false;
    });
}

// like timestep, but don't advance game state
function render() {
    busy = true;
    init_svg();

    invoke_rpc('/render', [ghosting,scale*svg_width,scale*svg_height], 500, function (data) {
        last_data = data;
        if (emoji) display(data);
        busy = false;
    });
}

function init_gui() {
    // add key listeners to game board
    pressed_keys = [];
    $(document).on('keydown',function(event) {
        var key = event.which;
        if (DIRECTION_BUTTONS.indexOf(key)!= -1) {
          // TODO other keys might have undesirable side-effects 
          event.preventDefault();
        }
        if (pressed_keys.indexOf(key) == -1) pressed_keys.push(key);
    });
    $(document).on('keyup',function(event) {
        var key = event.which;
        if (DIRECTION_BUTTONS.indexOf(key)!= -1) {
          // TODO other keys might have undesirable side-effects
          event.preventDefault();
        }
        var i = pressed_keys.indexOf(key);
        if (i != -1) pressed_keys.splice(i,1);
    });

    $('#show-main').on('change', debug_render);
    $('#show-ghosts').on('change', debug_render);

    // load SVG for all the emoji
    load_resource('/resources/emoji.json',function (data) {
        emoji = {};
        var re = new RegExp('\<svg.*?\>(.*)\</svg\>');
        $.each(data,function(codepoint,svg) {
            svg = svg.replace(re,'$1');
            emoji[codepoint] = svg;
        });
        if (last_data) display(last_data);
    });

    // hide controls until we have a map
    hide_all_simulate_buttons();

    // getting around a material bug where the menu doesn't close on click?
    $('#map_list').click(function () {
      $('.is-visible').removeClass('is-visible');
    });

    // set up map selection
    invoke_rpc("/ls", {"path":"resources/maps/"}, 0, function(loaded) {
        loaded.sort();
        for (var i in loaded) {
            $("#map_list").append(
                "<li class=\"mdl-menu__item\" onclick=\"handle_map_select('" +
                    loaded[i] +
                    "')\">" +
                    loaded[i] +
                    "</li>");
        }
        // start by selecting a map
        // if a valid one is stored, us it
        var map = sessionStorage.getItem('map');
        if (!map || loaded.indexOf(map)<0) {
          map = loaded[0];
        }
        handle_map_select(map);
    });
}

function handle_map_select(value){
    pause();
    ghosting = false;
    update_ghost_button_display();

    hide_all_simulate_buttons();

    invoke_rpc('/init_game',value,500,function (ghost_enabled) {
        $('#current_map').text(value);
        show_forward_buttons();
        $('#')        
        sessionStorage.setItem('map', value);
        if (ghost_enabled) {
          enable_ghost_button();
        } else {
          disable_ghost_button();
        }
        render();
    });
}

function handle_reset_button() {
    pause();
    handle_map_select($('#current_map').text());
}

function handle_simulate_button(){
  // start simulation
  if(!intervalId){
    // show / hide GUI elements
    show_pause_button();

    start();
  }
}

function handle_step_button(){
  timestep();
}

function handle_ghost_button(){
    ghosting = !ghosting;
    update_ghost_button_display();
    render();
}

function update_ghost_button_display() {
    var button = $('#ghost');
    var toggles = $('.view-toggle');
    var step_button = $('#step_simulation');
    if (ghosting) {
        button.addClass(BUTTON_ON);
        toggles.css('visibility', 'visible');
        step_button.css('display','inline-block');
    } else {
        button.removeClass(BUTTON_ON);
        toggles.css('visibility', 'hidden');
        step_button.css('display','none');
    }
  
}

function handle_pause_button(){
  if(intervalId){
    // show / hide GUI elements
    show_forward_buttons();
    pause();
  }
}

function handle_bigger_button() {
    if (scale > 1) scale -= 1;
    if (!busy) render();
}

function handle_smaller_button() {
    if (scale < 8) scale += 1;
    if (!busy) render();
}

function handle_debug_button() {
    debug = !debug;
    var button = $('#debug');
    if (debug) {
        button.addClass(BUTTON_ON);
    } else {
        button.removeClass(BUTTON_ON)
    }

    if (last_data) display(last_data);
}

function start() {
    timestep();
    intervalId = setInterval(function() {
      if (!busy) timestep()
    }, step);
}

function pause() {
    clearInterval(intervalId);
    intervalId = null;
}

function init(){
    init_gui();
}


