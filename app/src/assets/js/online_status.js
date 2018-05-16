const ElectronOnline = require('electron-online')
const connection = new ElectronOnline()

connection.on('online', () => {
  console.log('App is online!')
  require('./update_json_db');
})

connection.on('offline', () => {
  console.log('App is offline!')
})

console.log(connection.status) // 'PENDING'
