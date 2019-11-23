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

async function logSend() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('resources/app/connect.py');
  pyshell.send("username:" + arguments[0] + ' ' + "password:" + arguments[1]);
  await sleep(1000);
  pyshell.on('message', function (message) {
    console.log(message);

  });
  pyshell.end(function (err,code,signal) {
    if (err) throw err;
  });
}
