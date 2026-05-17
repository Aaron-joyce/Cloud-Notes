# Amazon Textract

Amazon Textract is a machine learning service that automatically extracts text, handwriting, and data from scanned documents. It goes beyond simple Optical Character Recognition (OCR) to identify, understand, and extract data from forms and tables.

## Intelligent Document Processing

### OCR for Typed and Handwritten Text
Textract accurately extracts text from both digitally created documents and physical scanned documents, seamlessly handling variations in printed text and human handwriting.

### Form and Table Extraction
Unlike traditional OCR that outputs a flat text file, Textract understands the layout of documents.
- **Form Data**: It identifies key-value pairs (e.g., "First Name: John"), preserving the relationship between the field label and its value without requiring manual mapping or templates.
- **Table Data**: It preserves the tabular structure of data, understanding rows, columns, and cell boundaries, allowing you to easily export the data to a database or spreadsheet.

### Queries API
Allows you to use natural language questions to extract targeted pieces of data from complex, unstructured documents. For example, instead of parsing a whole mortgage document, you can pass a Query like "What is the applicant's gross annual income?" and Textract will return the specific value found in the text.
