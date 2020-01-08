const remote = require('electron').remote;
const path = require('path')

async function openTor() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('resources/app/tor.py');
  pyshell.on('message', function (message) {
    console.log(message);

  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}

function logSend() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('resources/app/connect.py');
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
  let pyshell = new PythonShell('resources/app/connect.py');
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
  let pyshell = new PythonShell('resources/app/connect.py');
  pyshell.send("checkmsg" + ' ' + arguments[0] + ' ' + arguments[1] + '');
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
async function sendMsg() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('resources/app/connect.py');
  pyshell.send("sendMsg" + ' ' + arguments[0] + ' ' + arguments[1] + '');
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
async function getPubkey() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('resources/app/connect.py');
  pyshell.send("getPubkey" + ' ' + arguments[0] + '');
  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
