# Product Catalogue Service

The Product Catalogue Service is a component of an online store project, designed to manage products and their variants efficiently. Built using `FastAPI` and `Beanie ODM` (`MongoDB`), this service follows the Hexagonal Architecture pattern to ensure modularity, testability, and maintainability. It provides a robust set of **CRUD** endpoints for managing **_products_**, **_variants_**, **_categories_**, **_media objects_**, and **_product-types_**.

---

## Features

- Product Management: Create, read, update, and delete products.
- Variant Management: Manage product variants with granular control.
- Category Management: Organize products into categories for better navigation.
- Media Object Management: Attach media objects (e.g., images, videos) to products and variants.
- Product types: Define and manage available options for product types and their variants.
- Hexagonal Architecture: Ensures separation of concerns, making the service modular and easy to test.
- FastAPI: High-performance framework for building APIs with automatic documentation (Swagger UI).
- Beanie ODM: MongoDB object-document mapper for seamless database interactions.

---

## Getting Started

### Prerequisites

- Python 3.11.6 or higher
- MongoDB (local or cloud instance)
- Poetry (for dependency management)

### Installation

1- **Clone the repository:**

```bash
git clone https://github.com/imirghania/product_catalogue_service.git
cd product_catalogue_service
```

2- **Set up a virtual environment and install dependencies:**

```bash
poetry install --with test
```

3- **Configure Environment Variables:**

Create a .env file in the root directory and add the following variables:

```env
MONGODB_URI=<mongodb-uri>
DATABASE_NAME=<db-name-for-example-product_catalogue_db>
```

4- **Activate the virtual environment:**

```bash
poetry shell
```

5- **Run the application:**

```bash
uvicorn product_catalouge.web.api.api:app --reload
```

You can access the API documentation via the following [Link](http://127.0.0.1:8000/api/docs)

6- **[Optional] Run the tests:**
The API endpoints are tested using PyTest. To run the tests, run the following command

```bash
pytest
```
