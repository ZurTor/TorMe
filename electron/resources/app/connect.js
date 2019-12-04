function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
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
async function checkConn(){
  await sleep(10000);
  if(connection==false){
    return false;
  }
  else {
    return true;
  }
}
connection = new Boolean(true);
async function logSend() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('resources/app/connect.py');
  pyshell.send("login" + ' ' + arguments[0] + ' ' + arguments[1]);
  pyshell.on('message', function (message) {
    if (message==="disconnected") {
      connection = false;
    }
    console.log(message);

  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
async function regSend() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('resources/app/connect.py');
  pyshell.send("register" + ' ' + arguments[0] + ' ' + arguments[1] + '');
  pyshell.on('message', function (message) {
    if (message==="disconnected") {
      connection = false;
    }
    console.log(message);

  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
