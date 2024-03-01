<template>
    <div>
        <div class="filters-container">
            <label for="searchQuery" class="filter-label">Search:</label>
            <input type="text" id="searchQuery" v-model="searchQuery" @input="fetchProducts" placeholder="Search products..." class="search-input" />
            <label for="sortKey" class="filter-label">Sort By:</label>
            <select v-model="sortKey" id="sortKey" class="sort-dropdown">
                <option value="name">Name</option>
                <option value="inventory">Inventory</option>
                <option value="last_modified">Last Updated</option>
            </select>
            <label for="sortOrder" class="filter-label">Sort Order:</label>
            <button @click="sortOrder = sortOrder === 'asc' ? 'desc' : 'asc'" id="sortOrder" class="sort-order-button">{{ sortOrder === 'asc' ? 'Desc ↓' : 'Asc ↑' }}</button>
            <label for="limit" class="filter-label">Results Per Page:</label>
            <select v-model="limit" id="limit" class="limit-dropdown">
                <option value="10">10</option>
                <option value="20">20</option>
                <option value="50">50</option>
                <option value="100">100</option>
            </select>
        </div>
        <table>
            <thead>
                <tr>
                    <th>Product Name</th>
                    <th>Inventory Count</th>
                    <th>Description</th>
                    <th>Last Updated</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="product in products" :key="product.id">
                    <td>{{ product.name }}</td>
                    <td>{{ product.inventory }}</td>
                    <td>{{ product.description }}</td>
                    <td>{{ formatDate(product.last_modified) }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
import { ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import moment from 'moment' // Assuming moment.js is added as a dependency

export default {
    setup() {
        const products = ref([])
        const searchQuery = ref('')
        const sortKey = ref('name') // Default sort key
        const sortOrder = ref('asc') // Default sort order
        const limit = ref('10') // Default limit
        const route = useRoute()
        const router = useRouter()

        watchEffect(() => {
            //   searchQuery.value = route.query.q || ''
            fetchProducts()
        })

        async function fetchProducts() {
            const backendUrl = import.meta.env.VITE_API_ENDPOINT
            try {
                const response = await fetch(`${backendUrl}/api/products?s=${searchQuery.value}&sort=${sortKey.value}&order=${sortOrder.value}&limit=${limit.value}`)
                if (response.ok) {
                    const product_data = await response.json()
                    products.value = product_data.products;
                } else {
                    console.error('Failed to fetch products')
                }
            } catch (error) {
                console.error('Error fetching products:', error)
            }
            if (searchQuery.value) {
                router.push({ path: '/', query: { q: searchQuery.value } }).catch((err) => { })
            } else {
                router.push({ path: '/' }).catch((err) => { })
            }
        }

        function formatDate(dateString) {
            return moment.unix(dateString).format('MMMM Do, YYYY @ h:mmA') // Converts epoch to "February 18th, 2024 @ 2:23PM" format
        }

        return {
            products,
            searchQuery,
            fetchProducts,
            formatDate,
            sortKey,
            limit,
            sortOrder // Make the function available in the template
        }
    }
}
</script>

<style scoped>
.filters-container {
    display: flex;
    justify-content: space-between;
    padding-top: 20px;
    gap: 10px; /* Added to create more space between filter items */
}

.filter-label {
    margin-right: 5px; /* Reduced margin */
    align-self: center;
}

.search-input {
    flex-grow: 2; /* Increased flex-grow for search input */
    padding: 8px; /* Reduced padding */
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-right: 5px; /* Reduced margin */
}

.sort-dropdown,
.limit-dropdown {
    flex-grow: 0.5; /* Reduced width of dropdowns */
    padding: 8px; /* Reduced padding */
    border: 1px solid #ccc;
    border-radius: 5px;
    margin-right: 5px; /* Reduced margin */
}

.sort-order-button {
    padding: 8px; /* Reduced padding */
    border: 1px solid #ccc;
    border-radius: 5px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px; /* Added margin to create space between filters and table */
}

th, td {
    text-align: left;
    padding: 8px;
    border-bottom: 1px solid #ddd;
}
</style>
