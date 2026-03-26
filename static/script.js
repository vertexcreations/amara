// Utility functions
window.formatCurrency = (amount) => {
    return 'Bs ' + new Intl.NumberFormat('es-BO', { minimumFractionDigits: 2, maximumFractionDigits: 2 }).format(amount);
};

// Helper: parse response, throw on error
async function parseResponse(res) {
    if (!res.ok) {
        let msg = `Error ${res.status}`;
        try { const err = await res.json(); msg = err.error || err.message || msg; } catch {}
        throw new Error(msg);
    }
    return await res.json();
}

// API calls
window.api = {
    getProducts: async () => {
        const res = await fetch('/api/products');
        return await parseResponse(res);
    },
    addProduct: async (product) => {
        const res = await fetch('/api/products', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(product)
        });
        return await parseResponse(res);
    },
    updateProduct: async (id, product) => {
        const res = await fetch(`/api/products/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(product)
        });
        return await parseResponse(res);
    },
    deleteProduct: async (id) => {
        const res = await fetch(`/api/products/${id}`, { method: 'DELETE' });
        if (!res.ok) {
            let msg = `Error ${res.status}`;
            try { const err = await res.json(); msg = err.error || msg; } catch {}
            throw new Error(msg);
        }
    },
    checkout: async (items, date) => {
        const res = await fetch('/api/checkout', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items, date })
        });
        return await parseResponse(res);
    },
    getSales: async () => {
        const res = await fetch('/api/sales');
        return await parseResponse(res);
    },
    deleteSale: async (id) => {
        const res = await fetch(`/api/sales/${id}`, { method: 'DELETE' });
        if (!res.ok) {
            let msg = `Error ${res.status}`;
            try { const err = await res.json(); msg = err.error || msg; } catch {}
            throw new Error(msg);
        }
    },
    updateSale: async (id, data) => {
        const res = await fetch(`/api/sales/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        return await parseResponse(res);
    },
    getCategories: async () => {
        const res = await fetch('/api/categories');
        return await parseResponse(res);
    },
    addCategory: async (category) => {
        const res = await fetch('/api/categories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(category)
        });
        return await parseResponse(res);
    },
    updateCategory: async (id, category) => {
        const res = await fetch(`/api/categories/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(category)
        });
        return await parseResponse(res);
    },
    deleteCategory: async (id) => {
        const res = await fetch(`/api/categories/${id}`, { method: 'DELETE' });
        if (!res.ok) {
            let msg = `Error ${res.status}`;
            try { const err = await res.json(); msg = err.error || msg; } catch {}
            throw new Error(msg);
        }
    },
    getDashboardStats: async () => {
        const res = await fetch('/api/dashboard-stats');
        return await parseResponse(res);
    }
};
