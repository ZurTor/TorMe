function logSend() {
  const {PythonShell} = require('python-shell')
  let pyshell = new PythonShell('C:/Users/Kuose/Downloads/electron/resources/app/connect.py');
  pyshell.send("username:" + arguments[0] + ' ' + "password:" + arguments[1]);

  pyshell.on('message', function (message) {
    console.log(message);
  });
  pyshell.end(function (err,code,signal) {
  });
}
