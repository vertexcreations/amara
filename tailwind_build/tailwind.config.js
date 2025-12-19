/** @type {import('tailwindcss').Config} */
module.exports = {
    content: ["./templates/**/*.html", "./static/**/*.js"],
    theme: {
        extend: {
            colors: {
                primary: '#6366f1',
                secondary: '#0ea5e9',
                success: '#10b981',
                warning: '#f59e0b',
                danger: '#ef4444',
            }
        },
    },
    plugins: [],
}
