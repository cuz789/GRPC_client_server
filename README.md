# gRPC Client-Server Project with Redis and GCP Deployment

## **Overview**

This project implements a client-server architecture using gRPC protocol for high-performance remote procedure calls. The server, deployed on Google Cloud Platform (GCP), handles Redis-based data indexing and querying. The client runs locally and communicates with the server via gRPC for data operations and measurements.

## **Architecture**

gRPC Protocol: Enables communication between client and server with Protocol Buffers (.proto) for message serialization.

Redis: In-memory data store used for vector indexing and querying.

Python: Used for implementation of both client and server components.

Docker: Used to containerize and deploy the server application on GCP.

## **Features**
Data loading and indexing in Redis

Querying using vector-based similarity

Measuring performance of query responses

gRPC APIs defined using protobuf

Modular components for loading, indexing, querying, and testing

## **Project Structure**


![image](https://github.com/user-attachments/assets/1e2ad9ff-48eb-4273-be6e-7b368cbca088)

