def list_product_details_into_dict(product_details: list):
    cleaned_details = [detail.strip() for detail in product_details if detail.strip()]
    if len(cleaned_details) % 2 != 0:
        cleaned_details.remove(cleaned_details[-1])
    cleaned_details = [detail for detail in cleaned_details if detail != '\\n']
    return {cleaned_details[i]: cleaned_details[i + 1] for i in range(0, len(cleaned_details), 2)}
data = ['Material type', 'Lycra Cotton', 'Fit type', 'Regular', 'Style', 'Casual', 'Closure type', 'Pull On', 'Care instructions', 'Hand Wash Only', 'Age range description', 'Adult', 'Country of Origin', 'India', 'Manufacturer', 'Leriya Fashion, Leriya Fashion-India', 'Packer', 'Leriya Fashion-India', 'Importer', 'Leriya Fashion-India', 'Item Weight', '300 g', 'Item Dimensions LxWxH', '30 x 10 x 3 Centimeters', 'Included Components', 'Shirt, Pants', 'Generic Name', 'Kurta Set', '4.1 out of 5', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n', '\n\n\n\n\n\n\n\n  \n  \n    ', '\n  \n']

print(list_product_details_into_dict(data))