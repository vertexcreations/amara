// Utility functions
const formatCurrency = (amount) => {
    return 'Bs ' + new Intl.NumberFormat('es-BO', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount);
};

// API calls
const api = {
    getProducts: async () => {
        const res = await fetch('/api/products');
        return await res.json();
    },
    addProduct: async (product) => {
        const res = await fetch('/api/products', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(product)
        });
        return await res.json();
    },
    deleteProduct: async (id) => {
        await fetch(`/api/products/${id}`, { method: 'DELETE' });
    },
    checkout: async (items) => {
        const res = await fetch('/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items })
        });
        if (!res.ok) {
            const err = await res.json();
            throw new Error(err.error);
        }
        return await res.json();
    },
    getSales: async () => {
        const res = await fetch('/api/sales');
        return await res.json();
    },
    getCategories: async () => {
        const res = await fetch('/api/categories');
        return await res.json();
    },
    addCategory: async (category) => {
        const res = await fetch('/api/categories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(category)
        });
        return await res.json();
    },
    deleteCategory: async (id) => {
        await fetch(`/api/categories/${id}`, { method: 'DELETE' });
    },
    getDashboardStats: async () => {
        const res = await fetch('/api/dashboard-stats');
        return await res.json();
    }
};
