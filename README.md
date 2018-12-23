# Sync_IoT


This project is aimed at intelligent routing of data from IoT devices to cloud, via an edge platform acting as a middle layer between them. Our main objective was to provide continuous delivery of data to the cloud with high availability and consistency. To scope down the problem at hand, we looked at scenarios where data is not necessarily required to be streamed live but could tolerate some delay at the cost of being filtered out. This type of framework is generally suitable for sensor devices like carbon monoxide detector, temperature & humidity measuring devices where real time data availability is not the primary concern but providing the high availability of data is very critical because during data analysis, false positive should be very low otherwise inferred results can be hazardous.


## System Architecture

<img src="https://github.com/Mahendra-Maiti/Sync_IoT/blob/master/System_Architecture.png">
<h4 align=center><b>Figure:</b> System Architecture</h4>

There are 4 main components in the proposed system. They are described below:

1.	**Client**:
Here IoT device will act as a client and to mimic the behavior of an IoT device, we run a process without any persistent data store and limited bandwidth (to limit this we run this process on LTE network). Client will send the data to the specific (most optimized node in terms of distance, compute capacity, memory and storage capacity) edge node in regular interval using TCP socket connection. To simulate mobile behavior of clients, the experiments are setup in a way that the clients change their location after regular interval of time. This movement is incorporated in the device module of the program.

2.	**Controller**:
Controller acts as an intelligent middleware layer to route the data to the most feasible and optimized edge node based on the current location of the IoT device and the available resources in the edge node. All edge nodes are connected to controller to share the timely resource statistics which in turn will determine the most optimal edge node for any client request. 
After controller boot up, we provide a list of edge node addresses to be registered to it. On every subsequent 10 second interval, the controller pings each of these edge nodes through exposed API endpoints to collect edge resource statistics. This is called as a health check. Based on what response is received if at all, the controller decides on the most optimal edge node for a requesting IoT device. In case of no response, the controller removes the corresponding edge repository from its active list. This is used to mimic the scenario where an edge repository might be down.

3.	**Edge Node**:
This acts as a persistent data store for client data which will get synchronized to the cloud in a timely manner. Every edge node has their own in-memory cache which will store the data for limited time. Every edge node has a worker running which will pull the data from the cache and synchronize with the cloud. Thus each node has relevant processes running to take care of three things: receiving data from the client, sending API response to the controller to share resource statistics, and regular transfer of the persisted data from cache to cloud.

4.	**Cloud**:
We use AWS’s FaaS (Function as a Service) framework to synchronize the data from edge node to the cloud. At the cloud side, we employ S3 buckets as the final data persistent store where every bucket corresponds to a unique IoT (client) device. Using AWS API gateway, we exposed a Lambda function which will accept the edge node request with the data in JSON format and create a file based on the device ID and timestamp. The lambda function then uploads this uniquely named temporary file to the specific S3 bucket of that device.


The workflow of our designed system can be understood through the following figure:


<img src="https://github.com/Mahendra-Maiti/Sync_IoT/blob/master/workflow.png">
<h4 align=center><b>Figure:</b> Workflow of implemented system</h4>




## Fitness Function
The fitness function for selecting most optimal edge repository for a particular requesting IoT device is:

<img src="https://github.com/Mahendra-Maiti/Sync_IoT/blob/master/Fitness_function.png">

This function is aimed to intelligently distribute the workload among active edge repositories such that the overall system performance is maximized.





## Results

- Employing a suitable filter function at the edge repository can greatly reduce the consumed network bandwidth while meeting requirements.

<img src="https://github.com/Mahendra-Maiti/Sync_IoT/blob/master/result_curve_bandwidth.png">
<h4 align=center><b>Figure:</b> Number of synchronized points after applying filter_1 (send_on_change), and filter_2 (12_hour_ average) </h4>



- Intelligent distribution of workload among edge repositories using fitness functions lead to reduction in synchronization times.

<img src="https://github.com/Mahendra-Maiti/Sync_IoT/blob/master/result_curve_time.png">
<h4 align=center><b>Figure:</b> Sychronization rate performance </h4>

<img src="https://github.com/Mahendra-Maiti/Sync_IoT/blob/master/Workload_distribution.png">
<h4 align=center><b>Figure:</b> Performance comparison with fitness function </h4>







