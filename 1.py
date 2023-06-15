import matplotlib.pyplot as plt
import random

# Hypothetical customer names and surnames
customers = ['Alice Smith', 'Bob Johnson', 'Carol Williams', 'David Brown', 'Eve Davis', 'Frank Miller', 'Grace Wilson', 'Helen Moore', 'Ivan Taylor', 'Jack Anderson', 'Karen Thomas', 'Leo Jackson', 'Mia White', 'Nina Harris', 'Oscar Martin']
# Random purchase amounts between 5 and 30
purchase_amounts = [random.randint(5, 30) for _ in range(len(customers))]

# Sort customers and purchase amounts by purchase amounts in ascending order
sorted_data = sorted(zip(customers, purchase_amounts), key=lambda x: x[1])
sorted_customers, sorted_amounts = zip(*sorted_data)

# Create a figure with desired dimensions
plt.figure(figsize=(10, 7))

# Create a horizontal bar chart
plt.barh(sorted_customers, sorted_amounts)

# Set chart title and labels
plt.title('Purchase Amounts by Customer (Sorted)')
plt.xlabel('Purchase Amount')
plt.ylabel('Customers')

# Show the chart
plt.show()
