function randomColor() {
  var letters = '0123456789ABCDEF';
  var color = '#';
  for (var i = 0; i < 6; i++) {
    color += letters[Math.floor(Math.random() * 16)];
  }
  return color;
};

function hexToRgb(hex) {
  var bigint = parseInt(parseInt(hex.replace(/^#/, ''), 16), 16);
  var r = (bigint >> 16) & 255;
  var g = (bigint >> 8) & 255;
  var b = bigint & 255;

  return r + ',' + g + ',' + b;
};

$(document).ready(function() {
  var username;
  var token;
  var active_users = [];

  var form_login = $('form#login');
  var form_msg = $('form#msg');
  var button_logout = $('p#logout');
  var ul_active_users = $('ul#active_users');
  var ul_messages = $('ul#messages');
  var input_msg = $('form#msg > div.field > div.control > input[name="text"]');

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port + '/notification');
  console.log(location.protocol + '//' + document.domain + ':' + location.port + '/notification');

  socket.on('connect', function() {
    console.log('socketio connected');
  });

  socket.on('push_users', function(msg) {
    refreshActiveUsers(msg['data']);
  });

  socket.on('push_messages', function(msg) {
    refreshMessages(msg['data']);
  });

  ul_active_users.children('li').each(function(index, object) {
    var color = randomColor();
    active_users.push({
      'user': object.innerText,
      'color': color,
      'refreshed_at': new Date()
    });
    object.style.color = color;
  });

  ul_messages.children('li').each(function(index, object) {
    var [msg, user] = object.innerText.split('-');
    msg = msg.trim();
    user = user.trim();
    var color = '#000000';
    for (var i = 0; i < active_users.length; i++) {
      if (active_users[i]['user'] === user) {
        color = active_users[i]['color'];
        break;
      }
    }
    object.innerText = msg;
    object.style.color = color;
  });


  form_login.submit(function() {
    username = $(this).serialize().split('&')[0].split('=')[1];
    $.post($(this).attr('action'), $(this).serialize(), function(response) {
      if (typeof response !== 'undefined' && 'token' in response) {
        token = response['token'];
        form_login.attr('style', 'display: none');
        button_logout.attr('style', 'display: block');
      }
    }, 'json');
    return false;
  });

  form_msg.submit(function() {
    $.post($(this).attr('action'), $(this).serialize() + '&token=' + token, function(response) {}, 'json');
    input_msg.val('');
    return false;
  });

  button_logout.click(function() {
    $.ajax({
      url: '/user/logout',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify({
        'user': username,
        'token': token
      }),
      success: function(response) {
        username = undefined;
        token = undefined;
        button_logout.attr('style', 'display: none');
        form_login.attr('style', 'display: block');
      }
    });
  });

  function refreshActiveUsers(data) {
    var now = new Date();
    for (var i = 0; i < data.length; i++) {
      var found = false;
      for (var j = 0; j < active_users.length; j++) {
        if (active_users[j]['user'] === data[i]['user']) {
          active_users[j]['refreshed_at'] = now;
          found = true;
          break;
        }
      }
      if (!found) {
        active_users.push({
          'user': data[i]['user'],
          'color': randomColor(),
          'refreshed_at': now
        });
      }
    }
    ul_active_users.empty();
    for (var i = active_users.length - 1; i >= 0; i--) {
      if (active_users[i]['refreshed_at'].getTime() !== now.getTime()) {
        active_users.splice(i, 1);
      } else {
        ul_active_users.append('<li style="color: rgb(' + hexToRgb(active_users[i]['color']) + ');">' + active_users[i]['user'] + '</li>');
      }
    }
  };

  function refreshMessages(data) {
    ul_messages.empty();
    for (var i = 0; i < data.length; i++) {
      msg = data[i]['text'];
      user = data[i]['user'];
      var color = '#000000';
      for (var i = 0; i < active_users.length; i++) {
        if (active_users[i]['user'] === user) {
          color = active_users[i]['color'];
          break;
        }
      }
      ul_messages.append('<li style="color: rgb(' + hexToRgb(color) + ');">' + msg + '</li>');
    }
  };
});
