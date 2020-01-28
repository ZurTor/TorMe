const remote = require('electron').remote;
const path = require('path')

var pickle = require('pickle');
async function openTor() {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/tor.py', options);
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}

function logSend(logarg, passaeg, error, callback) {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("login" + ' ' + arguments[0] + ' ' + arguments[1] + '');
  pyshell.on('message', function (message) {
    console.log(message);
    if (message == "token"){
      var xD = remote.getCurrentWindow();
      const BrowserWindow = remote.BrowserWindow;
      const win = new BrowserWindow({
        'minWidth': 940,
        'minHeight': 940,
        height: 1000,
        width: 1000,
        center: true,
        darkTheme: true,
        frame: true,
        webPreferences: {
          preload: path.join(__dirname, 'preload.js'),
          nodeIntegration: true
        }
      });
      win.loadFile("communicator.html");
      xD.close();
    }
    else{
      callback(message);
    }
  });
  pyshell.end(function (err,code,signal) {
    if (err) error(code);
  });
}
function regSend(username, password, error, callback) {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("register" + ' ' + username + ' ' + password + '');
  pyshell.on('message', function (message) {
    if (message == "accex"){
      callback("accex")
    }
  });
  pyshell.end(function (err,code,signal) {
    if (err) error(code);
  });
}
async function sendMsg(data, timestamp, error) {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  data = {"0":"sendMsg", "1":data, "2": timestamp};
  pyshell.send(JSON.stringify(data), { mode: 'json '});
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) error(code);
  });
}
async function getMsg(callback, error) {
  var data;
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("getMsg");
  pyshell.on('message', function (message) {
    if (/^[\],:{}\s]*$/.test(message.replace(/\\["\\\/bfnrtu]/g, '@').
replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').
replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {
message = JSON.parse(message);
    error(":::")
    callback(message.msg, message.user, message.time);
}
  });
  pyshell.end(function (err,code,signal) {
    console.log(err);
    if (err) error(err);
  });
}
async function getPubkey(text, error) {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("getPubkey" + ' ' + text + '');
  pyshell.on('message', function (message) {
    console.log(message)
    error(":::")
  });
  pyshell.end(function (err,code,signal) {
    console.log(err);
    if (err) error(err);
  });
}
