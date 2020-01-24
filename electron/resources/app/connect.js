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

function logSend() {
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
        'minWidth': 500,
        'minHeight': 500,
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
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
function regSend() {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("register" + ' ' + arguments[0] + ' ' + arguments[1] + '');
  pyshell.on('message', function (message) {
    console.log(message);

  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
async function checkMsg() {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("checkmsg" + ' ' + arguments[0] + ' ' + arguments[1] + '');
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
async function sendMsg(data) {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  data = {"0":"sendMsg", "1":data};
  pyshell.send(JSON.stringify(data), { mode: 'json '});
  console.log(data);
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
async function getMsg(callback) {
  var data;
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("getMsg");
  var count = 0;
  var who = "";
  var message = "";
  pyshell.on('message', function (message) {
    console.log(message);
    if (/^[\],:{}\s]*$/.test(message.replace(/\\["\\\/bfnrtu]/g, '@').
replace(/"[^"\\\n\r]*"|true|false|null|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, ']').
replace(/(?:^|:|,)(?:\s*\[)+/g, ''))) {
message = JSON.parse(message);
    callback(message.msg, message.user);
}
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
async function getPubkey() {
  const {PythonShell} = require('python-shell')
  let options = {
  pythonPath: 'pyloc/python.exe'
  };
  let pyshell = new PythonShell('resources/app/connect.py', options);
  pyshell.send("getPubkey" + ' ' + arguments[0] + '');
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
