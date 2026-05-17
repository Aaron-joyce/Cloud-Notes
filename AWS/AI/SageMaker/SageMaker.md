# Amazon SageMaker

Amazon SageMaker is a fully managed service that provides every developer and data scientist with the ability to build, train, and deploy machine learning (ML) models quickly.

## End-to-End ML Lifecycle

### SageMaker Notebooks & Studio
- **SageMaker Notebooks**: Managed Jupyter notebook instances that provide a development environment for data exploration and model building.
- **SageMaker Studio**: A single, fully managed visual interface (IDE) for ML that allows you to perform all ML development steps in one place, enabling collaborative ML experimentation.

### SageMaker Data Wrangler & Feature Store
- **Data Wrangler**: Reduces the time it takes to aggregate and prepare data for machine learning from weeks to minutes via no-code data transformation pipelines.
- **Feature Store**: A centralized, secure, and highly available repository for managing, sharing, and discovering ML features across teams.

### SageMaker Training Jobs
Provides highly scalable distributed model training. 
- **Managed Spot Training**: Can lower training costs by up to 90% by utilizing spare AWS compute capacity.
- **Training Compiler**: Automatically optimizes ML models to run more efficiently on AWS hardware, reducing training time.

### SageMaker Inference Endpoints
SageMaker supports multiple model hosting options to match your workload's latency and throughput requirements:
- **Real-Time Inference**: For workloads needing sub-millisecond latency.
- **Serverless Inference**: Automatically provisions and scales compute capacity based on the volume of inference requests (ideal for intermittent traffic).
- **Asynchronous Inference**: Queues incoming requests and processes them asynchronously (ideal for large payload sizes or long processing times).
- **Batch Transform**: For offline predictions on large datasets where you don't need a persistent endpoint.

### SageMaker Model Monitor & Clarify
- **Model Monitor**: Continuously monitors the quality of ML models in production, detecting data drift and concept drift over time.
- **Clarify**: Provides insights into ML models and data to detect potential bias during data preparation and model training, and offers model explainability metrics to understand how models make predictions.
