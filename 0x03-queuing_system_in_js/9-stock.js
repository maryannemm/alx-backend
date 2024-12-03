const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Redis client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);

// Product list
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 },
];

// Get product by ID
const getItemById = (id) => listProducts.find((product) => product.itemId === id);

// Reserve stock in Redis
const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock);
};

// Get reserved stock
const getCurrentReservedStockById = async (itemId) => {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock, 10) : null;
};

// Routes
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.initialAvailableQuantity - (reservedStock || 0);

  res.json({ ...product, currentQuantity });
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }

  const reservedStock = await getCurrentReservedStockById(itemId);
  const currentQuantity = product.initialAvailableQuantity - (reservedStock || 0);

  if (currentQuantity <= 0) {
    res.json({ status: 'Not enough stock available', itemId });
    return;
  }

  reserveStockById(itemId, (reservedStock || 0) + 1);
  res.json({ status: 'Reservation confirmed', itemId });
});

// Start server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});

