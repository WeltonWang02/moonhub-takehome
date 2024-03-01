<template>
  <div class="add-product">
    <h2 class="full-width">Add/Update Product</h2>
    <form @submit.prevent="submitProduct">
      <div class="form-group">
        <label for="productName">Product Name:</label>
        <input type="text" id="productName" v-model="product.name" required />
      </div>
      <div class="form-group">
        <label for="productInventory">Product Count:</label>
        <input type="number" id="productInventory" v-model="product.inventory" required />
      </div>
      <div class="form-group">
        <label for="productDescription">Product Description:</label>
        <textarea id="productDescription" v-model="product.description" required></textarea>
      </div>
      <button type="submit">Add/Update Product</button>
      <p v-if="response">{{ response.message }}</p>
      <p v-if="error">{{ error }}</p>
    </form>
  </div>
</template>

<script>
const backendUrl = import.meta.env.VITE_API_ENDPOINT
export default {
  data() {
    return {
      product: {
        name: '',
        inventory: 0,
        description: ''
      },
      response: null,
      error: null
    }
  },
  methods: {
    async submitProduct() {
      this.error = null // Reset error message
      try {
        const response = await fetch(`${backendUrl}/api/products`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.product)
        })
        if (response.status === 201) {
          this.response = await response.json()
          console.log('Response:', this.response)
          this.resetForm()
        } else {
          this.error = 'Failed to submit product. Please try again.'
          console.error('Failed to submit product')
        }
      } catch (error) {
        this.error = 'Error submitting product. Please check your connection.'
        console.error('Error submitting product:', error)
      }
    },
    resetForm() {
      this.product.name = ''
      this.product.inventory = 0
      this.product.description = ''
    }
  }
}
</script>

<style scoped>
.add-product {
  max-width: 500px;
  padding: 20px;
  flex-wrap: wrap;
}

.full-width {
  width: 100%;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

p {
  color: green;
}

p.error {
  color: red;
}
</style>
