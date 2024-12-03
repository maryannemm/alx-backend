const express = require('express');
const redis = require('redis');
const kue = require('kue');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Initial state
let reservationEnabled = true;
const queue = kue.createQueue();

// Reserve seats
const reserveSeat = (number) => {
  client.set('available_seats', number);
};

// Get available seats
const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return seats ? parseInt(seats, 10) : 0;
};

// Initialize seats
reserveSeat(50);

// Routes
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (!err) res.json({ status: 'Reservation in process' });
    else res.json({ status: 'Reservation failed' });
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const availableSeats = await getCurrentAvailableSeats();
    if (availableSeats <= 0) {
      reservationEnabled = false;
      done(new Error('Not enough seats available'));
      return;
    }

    reserveSeat(availableSeats - 1);
    if (availableSeats - 1 === 0) reservationEnabled = false;
    done();
  });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

