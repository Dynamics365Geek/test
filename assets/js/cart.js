(() => {
  const STORAGE_KEY = 'shoppingCart';

  const readCart = () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) {
        return [];
      }
      const parsed = JSON.parse(raw);
      return Array.isArray(parsed) ? parsed : [];
    } catch (err) {
      console.warn('Unable to read cart from storage', err);
      return [];
    }
  };

  const writeCart = (cart) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    renderCartCount();
  };

  const normalizeProduct = ({ id, name, price, image }) => ({
    id: String(id),
    name,
    price: Number(price),
    image: image || '',
  });

  const addItem = (product, quantity = 1) => {
    const cart = readCart();
    const normalized = normalizeProduct(product);
    const existing = cart.find((item) => item.id === normalized.id);

    if (existing) {
      existing.quantity += quantity;
    } else {
      cart.push({ ...normalized, quantity });
    }

    writeCart(cart);
  };

  const updateQuantity = (productId, quantity) => {
    const cart = readCart();
    const item = cart.find((entry) => entry.id === String(productId));

    if (!item) {
      return;
    }

    item.quantity = Math.max(0, quantity);

    const filtered = item.quantity === 0 ? cart.filter((entry) => entry.id !== item.id) : cart;
    writeCart(filtered);
  };

  const removeItem = (productId) => {
    const cart = readCart().filter((entry) => entry.id !== String(productId));
    writeCart(cart);
  };

  const clearCart = () => {
    localStorage.removeItem(STORAGE_KEY);
    renderCartCount();
  };

  const getCart = () => readCart();

  const getItemCount = () => readCart().reduce((sum, item) => sum + (item.quantity || 0), 0);

  const getCartTotal = () =>
    readCart().reduce((sum, item) => sum + (item.price || 0) * (item.quantity || 0), 0);

  const renderCartCount = () => {
    const badge = document.querySelector('[data-cart-count]');
    if (!badge) {
      return;
    }
    badge.textContent = getItemCount();
  };

  window.Cart = {
    addItem,
    updateQuantity,
    removeItem,
    clearCart,
    getCart,
    getItemCount,
    getCartTotal,
    renderCartCount,
  };

  document.addEventListener('DOMContentLoaded', () => {
    renderCartCount();
  });
})();
