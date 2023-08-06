# README

## Code Description

This codeblock contains a Python script that performs data migration between two Couchbase clusters using the XDCR (Cross Datacenter Replication) feature. The script checks the cluster versions, verifies the existence of XDCR references, filters migratable buckets, starts the migration process, and prints the results.

## Prerequisites

To run this code, you need to have the following dependencies installed:

- `requests`: You can install it by running `pip install requests`.
- `time`: It is a built-in Python module and does not require separate installation.
- `tabulate`: You can install it by running `pip install tabulate`.

Make sure you have the necessary access rights and credentials to interact with the Couchbase clusters.

## Running the Code

To use this code, you need to create an instance of the `transportcb` class, providing the required parameters:
- `sourceip`: IP address of the source cluster.
- `destip`: IP address of the destination cluster.
- `user`: Username for authentication.
- `password`: Password for authentication.

After creating the instance, the script will automatically execute the necessary steps for data migration, including checking cluster versions, XDCR reference existence, filtering migratable buckets, starting the migration, and printing the results.


```
[INFO] : Checking cluster versions.
[INFO] : No XDCR reference found. Program will create one.
[INFO] : All conditions are met. Program will create XDCR reference and create replication for each bucket.
[INFO] : Created XDCR Reference.
[INFO]: beer-sample Created.
[INFO] : Added reference for bucket beer-sample
+------------------------------------------------------+----------+----------------------------------------------------------------------------+
| Issue                                                | Result   | Recommendation                                                             |
+======================================================+==========+============================================================================+
| Version Control Check Between Source and Destination | ✓        | Destination cluster version can not be smaller than source cluster version |
+------------------------------------------------------+----------+----------------------------------------------------------------------------+
| XDCR Reference Check                                 | ✓        | Program is assuming there is no XDCR reference for the new destination.    |
+------------------------------------------------------+----------+----------------------------------------------------------------------------+
| Create XDCR Reference                                | ✓        | Reference for XDCR created.                                                |
+------------------------------------------------------+----------+----------------------------------------------------------------------------+
```
## Output

The script will print the following information:

- Cluster version check result: Indicates whether the destination cluster's version is equal to or greater than the source cluster's version.
- XDCR reference check result: Indicates whether an existing XDCR reference is assumed for the new destination cluster.
- XDCR reference creation result: Indicates whether the script created a new XDCR reference.
- Recommendation: Provides recommendations based on the results of the checks.

The results will be displayed in a tabulated format.

Note: The codeblock assumes that the necessary imports and dependencies are already installed or available in the Python environment.