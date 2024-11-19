"const io = require('socket.io-client');

const wsUrl = 'wss://ws-sui.raidenx.io';

// Connect to server
const socket = io(wsUrl, {
  transports: ['websocket'],
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000
});

// Handle connection event
socket.on('connect', () => {
  console.log('Connected to server');
  
  // Subscribe to channels
  socket.emit('SUBSCRIBE_REALTIME_TRANSACTION', {
    pairId: 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356'
  });

  socket.emit('SUBSCRIBE_REALTIME_PAIR_STATS_CHANGED', {
    pairId: 'fd08ebdeb69d67541aa6f0b07cc98a9752516c5667f559367e329de4f5d77356'
  });
});

// Handle data events
socket.on('TRANSACTION', (data) => {
  console.log('Received realtime transaction:', data);
});

socket.on('PAIR_STATS_CHANGED', (data) => {
  console.log('Pair stats changed:', data);
});

// Handle errors
socket.on('connect_error', (error) => {
  console.log('Connection error:', error);
});

socket.on('disconnect', (reason) => {
  console.log('Disconnected:', reason);
});"